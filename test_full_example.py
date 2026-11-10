"""
Test the full example timetable with realistic data
"""

import json
from ga_scheduler import run_scheduler

print("=" * 70)
print("FULL EXAMPLE TEST: Realistic School Timetable")
print("=" * 70)

# Load example
with open('example_timetable.json', 'r') as f:
    example_data = f.read()

print("\nInput:")
print("-" * 70)
data = json.loads(example_data)
print(f"Days: {', '.join(data['days'])}")
print(f"Periods per day: {data['periods_per_day']}")
print(f"Total slots: {len(data['days']) * data['periods_per_day']}")
print(f"Rooms: {len(data['rooms'])}")
print(f"Teachers: {len(data['teachers'])}")
print(f"Classes: {len(data['classes'])}")

total_hours = sum(c['hours_per_week'] for c in data['classes'])
print(f"Total hours needed: {total_hours}")
print(f"Utilization: {total_hours}/{len(data['days']) * data['periods_per_day']} = {total_hours / (len(data['days']) * data['periods_per_day']) * 100:.1f}%")

print("\n" + "-" * 70)
print("Running Genetic Algorithm...")
print("-" * 70)

result_json = run_scheduler(
    example_data,
    pop_size=100,
    generations=300,
    seed=42
)

result = json.loads(result_json)

print(f"\nResult:")
print(f"  Final Fitness: {result['final_fitness']}")
print(f"  Generations Run: {result['generations_run']}")

if result['final_fitness'] == 0:
    print(f"  Status: ✅ PERFECT SOLUTION!")
else:
    print(f"  Status: ⚠️  Suboptimal ({-result['final_fitness']} penalty points)")

print(f"\nFitness Evolution (first 20 generations):")
for i, fitness in enumerate(result['best_fitness_history'][:20]):
    print(f"  Gen {i:3d}: {fitness:5.0f}")

if len(result['best_fitness_history']) > 20:
    print(f"  ... ({len(result['best_fitness_history']) - 20} more generations)")
    print(f"  Gen {len(result['best_fitness_history'])-1:3d}: {result['best_fitness_history'][-1]:5.0f}")

print("\n" + "-" * 70)
print("Sample Timetable - Monday")
print("-" * 70)

monday = result['timetable'][0]
print(f"\n{monday['day']}:")
for period in monday['periods']:
    period_num = period['period']
    if period['class']:
        print(f"  Period {period_num}: {period['subject']:20s} | {period['teacher']:15s} | Room {period['room']}")
    else:
        print(f"  Period {period_num}: {'FREE':20s} |")

print("\n" + "=" * 70)
print("TEST COMPLETE ✅")
print("=" * 70)

# Save result for inspection
with open('test_output.json', 'w') as f:
    json.dump(result, f, indent=2)
print("\nFull result saved to: test_output.json")
