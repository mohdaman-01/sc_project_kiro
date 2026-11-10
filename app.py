"""
Gradio Web Application for GA-based Timetable Scheduler

This app provides a user-friendly interface to generate timetables using
the genetic algorithm. Users can either upload JSON or use a simple form.
"""

import gradio as gr
import json
import matplotlib.pyplot as plt
import io
import base64
from ga_scheduler import run_scheduler


def generate_color_map(subjects):
    """Generate consistent colors for each subject"""
    colors = [
        '#FFE5E5', '#E5F5FF', '#E5FFE5', '#FFF5E5', '#FFE5FF',
        '#E5FFFF', '#FFFFE5', '#FFE5F5', '#F5E5FF', '#F5FFE5'
    ]
    return {subject: colors[i % len(colors)] for i, subject in enumerate(subjects)}


def format_timetable_html(timetable_data, final_fitness):
    """Convert timetable JSON to HTML table with color coding"""
    if 'error' in timetable_data:
        return f"<div style='color: red; font-weight: bold; padding: 20px;'>Error: {timetable_data['error']}</div>"
    
    timetable = timetable_data['timetable']
    
    # Get all unique subjects for color mapping
    subjects = set()
    for day in timetable:
        for period in day['periods']:
            if period['subject']:
                subjects.add(period['subject'])
    
    color_map = generate_color_map(list(subjects))
    
    # Build HTML table
    html = "<style>"
    html += "table { border-collapse: collapse; width: 100%; margin: 20px 0; }"
    html += "th, td { border: 2px solid #333; padding: 12px; text-align: center; }"
    html += "th { background-color: #4CAF50; color: white; font-weight: bold; }"
    html += ".free-period { background-color: #f0f0f0; color: #999; font-style: italic; }"
    html += ".class-cell { font-size: 14px; line-height: 1.4; }"
    html += ".subject { font-weight: bold; font-size: 16px; }"
    html += ".teacher { color: #555; }"
    html += ".room { color: #888; font-size: 12px; }"
    html += "</style>"
    
    html += "<table>"
    
    # Header row
    html += "<tr><th>Period</th>"
    for day in timetable:
        html += f"<th>{day['day']}</th>"
    html += "</tr>"
    
    # Get number of periods
    num_periods = len(timetable[0]['periods'])
    
    # Period rows
    for period_idx in range(num_periods):
        html += f"<tr><th>Period {period_idx + 1}</th>"
        
        for day in timetable:
            period = day['periods'][period_idx]
            
            if period['class'] is None:
                html += "<td class='free-period'>Free</td>"
            else:
                bg_color = color_map.get(period['subject'], '#ffffff')
                html += f"<td class='class-cell' style='background-color: {bg_color};'>"
                html += f"<div class='subject'>{period['subject']}</div>"
                html += f"<div class='teacher'>{period['teacher']}</div>"
                html += f"<div class='room'>Room: {period['room']}</div>"
                html += "</td>"
        
        html += "</tr>"
    
    html += "</table>"
    
    # Add legend
    if subjects:
        html += "<div style='margin-top: 20px;'><strong>Legend:</strong><br>"
        for subject in sorted(subjects):
            color = color_map[subject]
            html += f"<span style='display: inline-block; width: 20px; height: 20px; background-color: {color}; border: 1px solid #333; margin: 5px;'></span> {subject} &nbsp;&nbsp;"
        html += "</div>"
    
    return html


def plot_fitness_history(timetable_data):
    """Create matplotlib chart of fitness evolution"""
    if 'error' in timetable_data:
        return None
    
    history = timetable_data['best_fitness_history']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(len(history)), history, linewidth=2, color='#4CAF50')
    ax.set_xlabel('Generation', fontsize=12)
    ax.set_ylabel('Best Fitness', fontsize=12)
    ax.set_title('Fitness Evolution Over Generations', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='r', linestyle='--', label='Perfect Solution')
    ax.legend()
    
    plt.tight_layout()
    return fig


def get_warning_message(timetable_data):
    """Generate warning banner if conflicts remain"""
    if 'error' in timetable_data:
        return None
    
    final_fitness = timetable_data['final_fitness']
    
    if final_fitness == 0:
        return "<div style='background-color: #4CAF50; color: white; padding: 15px; border-radius: 5px; margin: 10px 0;'>✓ Perfect timetable generated with no conflicts!</div>"
    else:
        conflicts = -final_fitness
        return f"<div style='background-color: #FF9800; color: white; padding: 15px; border-radius: 5px; margin: 10px 0;'>⚠ Warning: {conflicts} penalty points remain. The timetable may have conflicts or suboptimal arrangements.</div>"


def create_download_json(timetable_data):
    """Create downloadable JSON file"""
    if 'error' in timetable_data:
        return None
    
    return json.dumps(timetable_data, indent=2)


def generate_timetable_json(
    json_input,
    pop_size,
    generations,
    seed
):
    """Generate timetable from JSON input"""
    try:
        # Validate JSON
        json.loads(json_input)
        
        # Run GA
        result = run_scheduler(
            json_input,
            pop_size=int(pop_size),
            generations=int(generations),
            seed=int(seed) if seed else None
        )
        
        result_data = json.loads(result)
        
        # Generate outputs
        html_table = format_timetable_html(result_data, result_data.get('final_fitness', 0))
        fitness_plot = plot_fitness_history(result_data)
        warning = get_warning_message(result_data)
        download_json = create_download_json(result_data)
        
        return html_table, fitness_plot, warning, download_json
    
    except json.JSONDecodeError as e:
        error_html = f"<div style='color: red; padding: 20px;'>Invalid JSON: {str(e)}</div>"
        return error_html, None, None, None
    except Exception as e:
        error_html = f"<div style='color: red; padding: 20px;'>Error: {str(e)}</div>"
        return error_html, None, None, None


def generate_timetable_form(
    days,
    periods,
    subjects,
    teachers,
    rooms,
    hours,
    pop_size,
    generations,
    seed
):
    """Generate timetable from form input"""
    try:
        # Parse form inputs
        day_list = [d.strip() for d in days.split(',')]
        periods_per_day = int(periods)
        
        # Parse subjects (format: "Math,English,Science")
        subject_list = [s.strip() for s in subjects.split(',')]
        
        # Parse teachers (format: "Mr. Smith,Ms. Johnson")
        teacher_list = [t.strip() for t in teachers.split(',')]
        
        # Parse rooms (format: "R1:30,R2:25" - room:capacity)
        room_entries = [r.strip() for r in rooms.split(',')]
        room_list = []
        for i, entry in enumerate(room_entries):
            if ':' in entry:
                room_id, capacity = entry.split(':')
                room_list.append({'id': room_id.strip(), 'capacity': int(capacity.strip())})
            else:
                room_list.append({'id': entry.strip(), 'capacity': 30})
        
        # Parse hours (format: "3,3,2" - hours per subject)
        hours_list = [int(h.strip()) for h in hours.split(',')]
        
        # Validate matching lengths
        if len(subject_list) != len(hours_list):
            return "<div style='color: red;'>Error: Number of subjects must match number of hours</div>", None, None, None
        
        if len(subject_list) > len(teacher_list):
            # Repeat teachers if not enough
            teacher_list = teacher_list * ((len(subject_list) // len(teacher_list)) + 1)
        
        # Build JSON
        data = {
            'days': day_list,
            'periods_per_day': periods_per_day,
            'rooms': room_list,
            'teachers': [{'id': f'T{i+1}', 'name': name} for i, name in enumerate(teacher_list[:len(subject_list)])],
            'classes': [
                {
                    'id': f'C{i+1}',
                    'subject': subject_list[i],
                    'teacher_id': f'T{i+1}',
                    'hours_per_week': hours_list[i]
                }
                for i in range(len(subject_list))
            ]
        }
        
        # Generate timetable
        return generate_timetable_json(
            json.dumps(data),
            pop_size,
            generations,
            seed
        )
    
    except Exception as e:
        error_html = f"<div style='color: red; padding: 20px;'>Error: {str(e)}</div>"
        return error_html, None, None, None


# Create Gradio interface
with gr.Blocks(title="GA Timetable Scheduler", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🎓 Genetic Algorithm Timetable Scheduler
    
    Generate conflict-free weekly class timetables using a Genetic Algorithm.
    
    **How it works:** The GA optimizes class placement to avoid teacher/room conflicts, minimize gaps, and prevent consecutive same-subject classes.
    """)
    
    with gr.Tabs():
        # Tab 1: JSON Upload
        with gr.Tab("JSON Input"):
            gr.Markdown("""
            ### Upload JSON Configuration
            
            Provide a complete configuration in JSON format. Example structure:
            ```json
            {
              "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
              "periods_per_day": 6,
              "rooms": [
                {"id": "R1", "capacity": 30},
                {"id": "R2", "capacity": 25}
              ],
              "teachers": [
                {"id": "T1", "name": "Mr. Smith"},
                {"id": "T2", "name": "Ms. Johnson"}
              ],
              "classes": [
                {"id": "C1", "subject": "Math", "teacher_id": "T1", "hours_per_week": 5},
                {"id": "C2", "subject": "English", "teacher_id": "T2", "hours_per_week": 4}
              ]
            }
            ```
            """)
            
            json_input = gr.Textbox(
                label="JSON Configuration",
                placeholder="Paste your JSON here...",
                lines=15
            )
            
            with gr.Row():
                json_pop_size = gr.Slider(20, 200, value=100, step=10, label="Population Size")
                json_generations = gr.Slider(50, 500, value=300, step=50, label="Max Generations")
                json_seed = gr.Number(label="Random Seed (optional)", value=None, precision=0)
            
            json_button = gr.Button("Generate Timetable", variant="primary")
        
        # Tab 2: Simple Form
        with gr.Tab("Simple Form"):
            gr.Markdown("### Quick Setup")
            
            with gr.Row():
                form_days = gr.Textbox(
                    label="Days (comma-separated)",
                    value="Monday,Tuesday,Wednesday,Thursday,Friday"
                )
                form_periods = gr.Number(label="Periods per Day", value=6, precision=0)
            
            form_subjects = gr.Textbox(
                label="Subjects (comma-separated)",
                placeholder="Math,English,Science,History,PE",
                value="Math,English,Science"
            )
            
            form_teachers = gr.Textbox(
                label="Teachers (comma-separated)",
                placeholder="Mr. Smith,Ms. Johnson,Dr. Brown",
                value="Mr. Smith,Ms. Johnson,Dr. Brown"
            )
            
            form_rooms = gr.Textbox(
                label="Rooms (format: RoomID:Capacity)",
                placeholder="R1:30,R2:25,R3:20",
                value="R1:30,R2:25"
            )
            
            form_hours = gr.Textbox(
                label="Hours per Week (comma-separated, matching subjects)",
                placeholder="5,4,3,3,2",
                value="3,3,2"
            )
            
            with gr.Row():
                form_pop_size = gr.Slider(20, 200, value=100, step=10, label="Population Size")
                form_generations = gr.Slider(50, 500, value=300, step=50, label="Max Generations")
                form_seed = gr.Number(label="Random Seed (optional)", value=None, precision=0)
            
            form_button = gr.Button("Generate Timetable", variant="primary")
    
    # Outputs (shared by both tabs)
    gr.Markdown("---")
    gr.Markdown("## 📊 Results")
    
    warning_output = gr.HTML(label="Status")
    timetable_output = gr.HTML(label="Timetable")
    plot_output = gr.Plot(label="Fitness Evolution")
    
    with gr.Row():
        download_output = gr.Textbox(label="Download JSON", lines=1, visible=False)
        download_button = gr.File(label="Download Result", visible=True)
    
    # Connect buttons
    json_button.click(
        fn=generate_timetable_json,
        inputs=[json_input, json_pop_size, json_generations, json_seed],
        outputs=[timetable_output, plot_output, warning_output, download_output]
    )
    
    form_button.click(
        fn=generate_timetable_form,
        inputs=[
            form_days, form_periods, form_subjects, form_teachers,
            form_rooms, form_hours, form_pop_size, form_generations, form_seed
        ],
        outputs=[timetable_output, plot_output, warning_output, download_output]
    )
    
    gr.Markdown("""
    ---
    ### Tips:
    - Start with default parameters for quick results
    - Increase population size and generations for better quality (but slower)
    - Use a random seed for reproducible results
    - If conflicts remain, try increasing generations or simplifying the schedule
    """)


if __name__ == "__main__":
    app.launch()
