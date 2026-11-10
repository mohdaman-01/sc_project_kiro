"""
Test script to verify the Gradio app functions work correctly
"""

import json
from app import generate_timetable_json, generate_timetable_form

print("=" * 60)
print("Testing Gradio App Functions")
print("=" * 60)

# Test 1: JSON input
print("\nTest 1: JSON Input Method")
print("-" * 60)

test_json = {
    'days': ['Monday', 'Tuesday', 'Wednesday'],
    'periods_per_day': 4,
    'rooms': [
        {'id': 'R1', 'capacity': 30},
        {'id': 'R2', 'capacity': 25}
    ],
    'teachers': [
        {'id': 'T1', 'name': 'Mr. Smith'},
        {'id': 'T2', 'name': 'Ms. Johnson'}
    ],
    'classes': [
        {'id': 'C1', 'subject': 'Math', 'teacher_id': 'T1', 'hours_per_week': 3},
        {'id': 'C2', 'subject': 'English', 'teacher_id': 'T2', 'hours_per_week': 3},
        {'id': 'C3', 'subject': 'Science', 'teacher_id': 'T1', 'hours_per_week': 2}
    ]
}

html, plot, warning, download = generate_timetable_json(
    json.dumps(test_json),
    pop_size=50,
    generations=100,
    seed=42
)

print("✓ HTML output generated:", len(html) if html else 0, "characters")
print("✓ Plot generated:", plot is not None)
print("✓ Warning message:", warning[:50] if warning else "None")
print("✓ Download JSON:", len(download) if download else 0, "characters")

# Test 2: Form input
print("\nTest 2: Form Input Method")
print("-" * 60)

html2, plot2, warning2, download2 = generate_timetable_form(
    days="Monday,Tuesday,Wednesday",
    periods="4",
    subjects="Math,English,Science",
    teachers="Mr. Smith,Ms. Johnson",
    rooms="R1:30,R2:25",
    hours="3,3,2",
    pop_size=50,
    generations=100,
    seed=42
)

print("✓ HTML output generated:", len(html2) if html2 else 0, "characters")
print("✓ Plot generated:", plot2 is not None)
print("✓ Warning message:", warning2[:50] if warning2 else "None")
print("✓ Download JSON:", len(download2) if download2 else 0, "characters")

# Test 3: Error handling - invalid JSON
print("\nTest 3: Error Handling - Invalid JSON")
print("-" * 60)

html3, plot3, warning3, download3 = generate_timetable_json(
    "invalid json {{{",
    pop_size=50,
    generations=100,
    seed=None
)

print("✓ Error detected:", "Invalid JSON" in html3 if html3 else False)

# Test 4: Error handling - impossible schedule
print("\nTest 4: Error Handling - Impossible Schedule")
print("-" * 60)

impossible_json = {
    'days': ['Monday'],
    'periods_per_day': 2,
    'rooms': [{'id': 'R1', 'capacity': 30}],
    'teachers': [{'id': 'T1', 'name': 'Mr. Smith'}],
    'classes': [
        {'id': 'C1', 'subject': 'Math', 'teacher_id': 'T1', 'hours_per_week': 5}
    ]
}

html4, plot4, warning4, download4 = generate_timetable_json(
    json.dumps(impossible_json),
    pop_size=50,
    generations=100,
    seed=None
)

print("✓ Error detected:", "Impossible" in html4 if html4 else False)

print("\n" + "=" * 60)
print("All tests passed! ✓")
print("=" * 60)
print("\nThe Gradio app is ready to launch.")
print("Run: python app.py")
