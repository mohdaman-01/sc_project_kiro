# 🎓 Genetic Algorithm Timetable Scheduler

An intelligent web application that generates conflict-free weekly class timetables using a Genetic Algorithm (GA). Built with Gradio for easy deployment on Hugging Face Spaces.

## 🧬 What is a Genetic Algorithm?

A Genetic Algorithm is an **optimization technique** inspired by natural evolution, NOT a machine learning model. There's no training phase or saved model—the GA runs live on every request to find optimal solutions through:

1. **Population**: Multiple candidate timetables
2. **Selection**: Choosing the best performers
3. **Crossover**: Combining good solutions
4. **Mutation**: Random variations for exploration
5. **Evolution**: Iterating until finding an optimal schedule

## ✨ Features

- **Zero Conflicts**: Avoids teacher double-booking and room conflicts
- **Smart Scheduling**: Minimizes gaps and prevents consecutive same-subject classes
- **Dual Input Methods**: JSON upload or simple web form
- **Real-time Visualization**: Watch the GA optimize in real-time with fitness charts
- **Color-Coded Output**: Easy-to-read timetable with subject color coding
- **Customizable Parameters**: Adjust population size, generations, and random seed

## 🚀 How It Works

### Input Data
- **Days**: Which days of the week (e.g., Mon-Fri)
- **Periods**: How many class periods per day
- **Rooms**: Available classrooms with capacity
- **Teachers**: List of teaching staff
- **Classes**: Subjects with assigned teachers and weekly hours

### Optimization Process

The GA maximizes a fitness score that:
- **Hard Constraints** (−100 penalty each):
  - Teacher double-booked (same teacher, same time)
  - Room double-booked (same room, same time)

- **Soft Constraints**:
  - Same subject twice in a row: −5
  - Gap between classes: −2

**Target**: Fitness = 0 (perfect solution with no conflicts)

### Algorithm Parameters
- **Population Size**: 100 (number of candidate solutions)
- **Generations**: 300 (evolution iterations)
- **Mutation Rate**: 0.15 (15% chance of random changes)
- **Elitism**: Top 2 solutions always preserved
- **Tournament Selection**: Best of 3 random candidates
- **Termination**: Stops at generation 300 OR when fitness = 0

## 📦 Installation & Running Locally

### Prerequisites
- Python 3.8 or higher

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Open your browser** to the URL shown (typically `http://127.0.0.1:7860`)

## 🎯 Usage Examples

### Example 1: JSON Input

```json
{
  "days": ["Monday", "Tuesday", "Wednesday"],
  "periods_per_day": 4,
  "rooms": [
    {"id": "R1", "capacity": 30},
    {"id": "R2", "capacity": 25}
  ],
  "teachers": [
    {"id": "T1", "name": "Mr. Smith"},
    {"id": "T2", "name": "Ms. Johnson"}
  ],
  "classes": [
    {"id": "C1", "subject": "Math", "teacher_id": "T1", "hours_per_week": 3},
    {"id": "C2", "subject": "English", "teacher_id": "T2", "hours_per_week": 3},
    {"id": "C3", "subject": "Science", "teacher_id": "T1", "hours_per_week": 2}
  ]
}
```

### Example 2: Simple Form Input

- **Days**: `Monday,Tuesday,Wednesday,Thursday,Friday`
- **Periods per Day**: `6`
- **Subjects**: `Math,English,Science,History,PE`
- **Teachers**: `Mr. Smith,Ms. Johnson,Dr. Brown,Ms. Davis,Mr. Wilson`
- **Rooms**: `R1:30,R2:25,R3:20,Gym:40`
- **Hours per Week**: `5,4,3,3,2`

## 🌐 Deploy to Hugging Face Spaces

### Method 1: Web Interface

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Choose **Gradio** as the SDK
4. Upload these files:
   - `app.py`
   - `ga_scheduler.py`
   - `requirements.txt`
   - `README.md`
5. Your space will build and deploy automatically!

### Method 2: Git CLI

```bash
# Create a new space on huggingface.co and get the repo URL
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy files
cp app.py ga_scheduler.py requirements.txt README.md .

# Commit and push
git add .
git commit -m "Initial commit: GA Timetable Scheduler"
git push
```

### Required Files for Deployment
- ✅ `app.py` - Main Gradio application
- ✅ `ga_scheduler.py` - Core GA logic
- ✅ `requirements.txt` - Python dependencies
- ✅ `README.md` - This documentation

## 📊 Output Format

### Timetable Structure
```json
{
  "timetable": [
    {
      "day": "Monday",
      "periods": [
        {
          "period": 1,
          "class": "C1",
          "subject": "Math",
          "teacher": "Mr. Smith",
          "room": "R1"
        }
      ]
    }
  ],
  "final_fitness": 0,
  "best_fitness_history": [-10, -5, 0],
  "generations_run": 3
}
```

## 🎨 Screenshot

*(Add a screenshot of your generated timetable here after deployment)*

![Timetable Example](screenshot.png)

## 🔧 Troubleshooting

### "Impossible schedule" error
- **Cause**: Total hours required exceeds available time slots
- **Solution**: Reduce hours per week OR add more days/periods

### Fitness not reaching 0
- **Cause**: Complex schedule with many constraints
- **Solution**: Increase generations (300 → 500) or population size (100 → 200)

### Slow generation
- **Cause**: Large population size or many generations
- **Solution**: Start with smaller values for testing, increase for final run

## 📝 Technical Notes

### Why GA vs Other Methods?

- **Constraint Satisfaction**: GA handles multiple soft/hard constraints naturally
- **No Training**: Runs live, no pre-training needed
- **Flexible**: Easy to add new constraints (lunch breaks, teacher preferences, etc.)
- **Transparent**: Fitness evolution shows optimization progress

### Chromosome Encoding

- **Length**: `days × periods_per_day` slots
- **Gene**: `{class_id, room_id}` or `None` (free period)
- **Invariant**: Each class appears exactly `hours_per_week` times

### Genetic Operators

- **Initialization**: Random placement of classes
- **Selection**: Tournament (size 3)
- **Crossover**: Uniform with repair (maintains class count)
- **Mutation**: Swap timing or change room (15% rate)
- **Elitism**: Top 2 preserved each generation

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions welcome! Possible improvements:
- Add lunch break constraints
- Teacher preference weights
- Multi-class group scheduling
- Export to PDF/Excel
- Load balancing (distribute classes evenly)

## 📮 Contact

For questions or issues, please open an issue on the repository.

---

**Built with ❤️ using Python, Gradio, and Genetic Algorithms**
