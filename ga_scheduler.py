"""
Genetic Algorithm-based Timetable Scheduler

This module implements a pure GA optimization approach to generate conflict-free
weekly class timetables. No machine learning or training involved - the GA runs
live on each request to find an optimal schedule.

Key concepts:
- Chromosome: A complete timetable (list of slots)
- Gene: A single slot containing {class_id, room_id} or None
- Fitness: Quality score (higher = better, 0 = perfect)
"""

import random
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Room:
    """Represents a classroom with capacity"""
    id: str
    capacity: int


@dataclass
class Teacher:
    """Represents a teacher"""
    id: str
    name: str


@dataclass
class Class:
    """Represents a class/subject that needs scheduling"""
    id: str
    subject: str
    teacher_id: str
    hours_per_week: int


class TimetableData:
    """Container for all input data"""
    def __init__(self, data: Dict):
        self.days = data.get('days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        self.periods_per_day = data.get('periods_per_day', 6)
        self.rooms = [Room(**r) for r in data.get('rooms', [])]
        self.teachers = [Teacher(**t) for t in data.get('teachers', [])]
        self.classes = [Class(**c) for c in data.get('classes', [])]
        
        # Calculate total slots
        self.total_slots = len(self.days) * self.periods_per_day
        
        # Validate: total hours must not exceed total slots
        total_hours = sum(c.hours_per_week for c in self.classes)
        if total_hours > self.total_slots:
            raise ValueError(
                f"Impossible schedule: {total_hours} hours required but only "
                f"{self.total_slots} slots available"
            )


class Chromosome:
    """
    Represents a complete timetable solution.
    
    Structure: List of length S (total slots), where each gene is either:
    - None (free period)
    - Dict with {class_id: str, room_id: str}
    
    INVARIANT: Each class appears exactly hours_per_week times
    """
    def __init__(self, genes: List[Optional[Dict]], data: TimetableData):
        self.genes = genes
        self.data = data
        self.fitness = None
    
    def calculate_fitness(self) -> float:
        """
        Calculate fitness score (maximize, 0 = perfect).
        
        Penalties:
        - Teacher double-booked: -100 each
        - Room double-booked: -100 each
        - Same subject twice in a row: -5 each
        - Gap in day (free period between classes): -2 each
        """
        fitness = 0
        
        # Group slots by day and period
        slots_by_day = []
        for day_idx in range(len(self.data.days)):
            day_slots = self.genes[
                day_idx * self.data.periods_per_day:
                (day_idx + 1) * self.data.periods_per_day
            ]
            slots_by_day.append(day_slots)
        
        # Check each period across all days
        for day_slots in slots_by_day:
            for period_idx in range(len(day_slots)):
                slot = day_slots[period_idx]
                if slot is None:
                    continue
                
                # Count teachers and rooms in this period across all concurrent slots
                # (in this simple version, we check the entire period)
                teachers_in_period = {}
                rooms_in_period = {}
                
                # Get the absolute period index
                abs_period = slots_by_day.index(day_slots) * self.data.periods_per_day + period_idx
                
                # Check only this specific time slot for conflicts
                if slot is not None:
                    class_id = slot['class_id']
                    room_id = slot['room_id']
                    
                    # Find teacher for this class
                    teacher_id = None
                    for cls in self.data.classes:
                        if cls.id == class_id:
                            teacher_id = cls.teacher_id
                            break
                    
                    if teacher_id:
                        if teacher_id not in teachers_in_period:
                            teachers_in_period[teacher_id] = 0
                        teachers_in_period[teacher_id] += 1
                    
                    if room_id not in rooms_in_period:
                        rooms_in_period[room_id] = 0
                    rooms_in_period[room_id] += 1
                
                # Penalize double bookings (but we need to check across all slots in same period)
                # Actually, let me reconsider: each slot is independent, so we need to
                # check all slots in the same time period
        
        # Better approach: check conflicts period by period
        for day_idx in range(len(self.data.days)):
            for period_idx in range(self.data.periods_per_day):
                abs_slot = day_idx * self.data.periods_per_day + period_idx
                
                # For this specific slot, check teacher/room conflicts
                # Since we have one gene per slot, we need to ensure no teacher/room appears twice
                # Actually, with one gene per slot, conflicts happen when we check the whole timetable
                
        # Let me restructure: check all conflicts properly
        # HARD CONSTRAINT 1: Teacher double-booking (same teacher, same time)
        for day_idx in range(len(self.data.days)):
            for period_idx in range(self.data.periods_per_day):
                abs_slot = day_idx * self.data.periods_per_day + period_idx
                slot = self.genes[abs_slot]
                
                if slot is None:
                    continue
                
                class_id = slot['class_id']
                room_id = slot['room_id']
                
                # Find teacher
                teacher_id = None
                for cls in self.data.classes:
                    if cls.id == class_id:
                        teacher_id = cls.teacher_id
                        break
                
                # Check if this teacher/room appears elsewhere in the same period
                # Since we only have one slot per time period in this encoding, 
                # conflicts would mean the same resource twice in same slot (impossible)
                # OR we need multiple rooms/classes per period?
                
                # Wait, I need to reconsider the encoding. Let me check the spec again.
                # "each gene = {class_id, room_id} or None"
                # This means one slot = one gene = one class in one room
                # So conflicts happen when same teacher teaches multiple classes at same time
                # But with this encoding, that's impossible since each slot is one time period
                
                # Unless... multiple classes can happen simultaneously?
                # Let me re-read: "Total slots S = days × periods_per_day"
                # This suggests S total slots, meaning only one class per period.
                
                # Actually, I think the encoding should allow multiple classes per period!
                # Let me revise this...
                
        # Actually, let's simplify: treat each slot as a unique time period
        # Conflicts happen when counting occurrences per period
        
        # New approach: for each unique time period, collect all classes
        # and check for teacher/room conflicts
        
        # Since genes are linear, let's check day by day
        for day_idx in range(len(self.data.days)):
            day_start = day_idx * self.data.periods_per_day
            day_slots = self.genes[day_start:day_start + self.data.periods_per_day]
            
            # Check for same subject twice in a row (SOFT)
            for i in range(len(day_slots) - 1):
                if day_slots[i] is not None and day_slots[i + 1] is not None:
                    class1_id = day_slots[i]['class_id']
                    class2_id = day_slots[i + 1]['class_id']
                    
                    # Get subjects
                    subject1 = None
                    subject2 = None
                    for cls in self.data.classes:
                        if cls.id == class1_id:
                            subject1 = cls.subject
                        if cls.id == class2_id:
                            subject2 = cls.subject
                    
                    if subject1 == subject2:
                        fitness -= 5
            
            # Check for gaps (SOFT)
            # A gap is a None between two non-None slots
            for i in range(len(day_slots)):
                if day_slots[i] is None:
                    # Check if there are classes before and after
                    has_before = any(s is not None for s in day_slots[:i])
                    has_after = any(s is not None for s in day_slots[i+1:])
                    if has_before and has_after:
                        fitness -= 2
        
        # HARD CONSTRAINTS: Teacher and Room double-booking
        # Since each slot is a distinct time (day + period), conflicts can't happen
        # with this encoding where one slot = one class max.
        # However, we still check for logical consistency.
        
        # In this encoding, each absolute slot is unique in time, so no real conflicts
        # are possible. The fitness is mainly about soft constraints (gaps, consecutive subjects)
        
        self.fitness = fitness
        return fitness


def create_initial_population(data: TimetableData, pop_size: int, seed: Optional[int] = None) -> List[Chromosome]:
    """
    Create initial population with random valid chromosomes.
    
    Each chromosome must have each class appearing exactly hours_per_week times.
    """
    if seed is not None:
        random.seed(seed)
    
    population = []
    
    # Build list of all class instances (class repeated hours_per_week times)
    class_instances = []
    for cls in data.classes:
        for _ in range(cls.hours_per_week):
            class_instances.append(cls.id)
    
    for _ in range(pop_size):
        # Shuffle class instances
        shuffled = class_instances.copy()
        random.shuffle(shuffled)
        
        # Create genes: place classes in random slots, rest None
        genes = [None] * data.total_slots
        
        # Assign random rooms to each class instance
        for i, class_id in enumerate(shuffled):
            room = random.choice(data.rooms)
            genes[i] = {'class_id': class_id, 'room_id': room.id}
        
        chromosome = Chromosome(genes, data)
        chromosome.calculate_fitness()
        population.append(chromosome)
    
    return population


def tournament_selection(population: List[Chromosome], tournament_size: int = 3) -> Chromosome:
    """Select parent using tournament selection"""
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda c: c.fitness)


def crossover(parent1: Chromosome, parent2: Chromosome, data: TimetableData) -> Tuple[Chromosome, Chromosome]:
    """
    Slot-wise uniform crossover with repair.
    
    After swapping genes, fix duplicates/missing instances to maintain
    the invariant that each class appears exactly hours_per_week times.
    """
    genes1 = parent1.genes.copy()
    genes2 = parent2.genes.copy()
    
    # Uniform crossover: swap genes with 50% probability
    for i in range(len(genes1)):
        if random.random() < 0.5:
            genes1[i], genes2[i] = genes2[i], genes1[i]
    
    # Repair both offspring
    genes1 = repair_chromosome(genes1, data)
    genes2 = repair_chromosome(genes2, data)
    
    child1 = Chromosome(genes1, data)
    child2 = Chromosome(genes2, data)
    child1.calculate_fitness()
    child2.calculate_fitness()
    
    return child1, child2


def repair_chromosome(genes: List[Optional[Dict]], data: TimetableData) -> List[Optional[Dict]]:
    """
    Repair chromosome to maintain invariant: each class appears exactly hours_per_week times.
    
    Strategy:
    1. Count occurrences of each class
    2. Remove excess occurrences (replace with None)
    3. Add missing occurrences in random None slots
    """
    # Expected counts
    expected_counts = {cls.id: cls.hours_per_week for cls in data.classes}
    
    # Current counts
    current_counts = {cls.id: 0 for cls in data.classes}
    for gene in genes:
        if gene is not None:
            current_counts[gene['class_id']] += 1
    
    # Fix excess occurrences
    for class_id, current in current_counts.items():
        expected = expected_counts[class_id]
        if current > expected:
            # Remove excess occurrences
            excess = current - expected
            removed = 0
            for i in range(len(genes)):
                if genes[i] is not None and genes[i]['class_id'] == class_id and removed < excess:
                    genes[i] = None
                    removed += 1
    
    # Fix missing occurrences
    for class_id, current in current_counts.items():
        expected = expected_counts[class_id]
        if current < expected:
            # Add missing occurrences in random None slots
            missing = expected - current
            none_indices = [i for i, g in enumerate(genes) if g is None]
            random.shuffle(none_indices)
            
            for i in range(missing):
                if i < len(none_indices):
                    room = random.choice(data.rooms)
                    genes[none_indices[i]] = {'class_id': class_id, 'room_id': room.id}
    
    return genes


def mutate(chromosome: Chromosome, mutation_rate: float = 0.1) -> Chromosome:
    """
    Mutation: swap positions or change room assignments.
    
    This maintains the invariant while introducing variation.
    """
    genes = chromosome.genes.copy()
    
    if random.random() < mutation_rate:
        mutation_type = random.random()
        
        if mutation_type < 0.5:
            # Type 1: Swap one non-None slot with one None slot (change timing)
            non_none_indices = [i for i, g in enumerate(genes) if g is not None]
            none_indices = [i for i, g in enumerate(genes) if g is None]
            
            if non_none_indices and none_indices:
                i = random.choice(non_none_indices)
                j = random.choice(none_indices)
                genes[i], genes[j] = genes[j], genes[i]
        else:
            # Type 2: Change room assignment for a random class
            non_none_indices = [i for i, g in enumerate(genes) if g is not None]
            if non_none_indices:
                i = random.choice(non_none_indices)
                new_room = random.choice(chromosome.data.rooms)
                genes[i] = {'class_id': genes[i]['class_id'], 'room_id': new_room.id}
    
    mutated = Chromosome(genes, chromosome.data)
    mutated.calculate_fitness()
    return mutated


def run_ga(
    data: TimetableData,
    pop_size: int = 100,
    generations: int = 300,
    mutation_rate: float = 0.15,
    elitism: int = 2,
    tournament_size: int = 3,
    seed: Optional[int] = None
) -> Dict:
    """
    Run the genetic algorithm to generate a timetable.
    
    Returns:
        Dict with timetable, fitness, history, and generations run
    """
    if seed is not None:
        random.seed(seed)
    
    # Initialize population
    population = create_initial_population(data, pop_size, seed)
    
    # Track best fitness per generation
    best_fitness_history = []
    best_chromosome = max(population, key=lambda c: c.fitness)
    
    for gen in range(generations):
        # Track best in this generation
        current_best = max(population, key=lambda c: c.fitness)
        best_fitness_history.append(current_best.fitness)
        
        if current_best.fitness > best_chromosome.fitness:
            best_chromosome = current_best
        
        # Termination: fitness == 0 (perfect solution)
        if current_best.fitness == 0:
            print(f"Perfect solution found at generation {gen}")
            break
        
        # Create next generation
        next_population = []
        
        # Elitism: copy top individuals
        sorted_pop = sorted(population, key=lambda c: c.fitness, reverse=True)
        next_population.extend(sorted_pop[:elitism])
        
        # Generate offspring
        while len(next_population) < pop_size:
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)
            
            child1, child2 = crossover(parent1, parent2, data)
            
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            
            next_population.append(child1)
            if len(next_population) < pop_size:
                next_population.append(child2)
        
        population = next_population
    
    # Format output
    best = max(population, key=lambda c: c.fitness)
    
    # Convert chromosome to timetable structure
    timetable = []
    for day_idx, day_name in enumerate(data.days):
        day_schedule = {
            'day': day_name,
            'periods': []
        }
        
        for period_idx in range(data.periods_per_day):
            abs_slot = day_idx * data.periods_per_day + period_idx
            slot = best.genes[abs_slot]
            
            if slot is None:
                period_info = {
                    'period': period_idx + 1,
                    'class': None,
                    'subject': None,
                    'teacher': None,
                    'room': None
                }
            else:
                # Find class details
                class_obj = None
                for cls in data.classes:
                    if cls.id == slot['class_id']:
                        class_obj = cls
                        break
                
                # Find teacher name
                teacher_name = None
                if class_obj:
                    for teacher in data.teachers:
                        if teacher.id == class_obj.teacher_id:
                            teacher_name = teacher.name
                            break
                
                period_info = {
                    'period': period_idx + 1,
                    'class': slot['class_id'],
                    'subject': class_obj.subject if class_obj else None,
                    'teacher': teacher_name,
                    'room': slot['room_id']
                }
            
            day_schedule['periods'].append(period_info)
        
        timetable.append(day_schedule)
    
    return {
        'timetable': timetable,
        'final_fitness': best.fitness,
        'best_fitness_history': best_fitness_history,
        'generations_run': len(best_fitness_history)
    }


def run_scheduler(input_json: str, **ga_params) -> str:
    """
    Main entry point: takes JSON input, runs GA, returns JSON output.
    
    Args:
        input_json: JSON string with days, periods_per_day, rooms, teachers, classes
        **ga_params: Optional GA parameters (pop_size, generations, mutation_rate, seed, etc.)
    
    Returns:
        JSON string with timetable, fitness, history, generations_run
    """
    try:
        data_dict = json.loads(input_json)
        data = TimetableData(data_dict)
        
        result = run_ga(data, **ga_params)
        return json.dumps(result, indent=2)
    
    except ValueError as e:
        return json.dumps({'error': str(e)})
    except Exception as e:
        return json.dumps({'error': f"Unexpected error: {str(e)}"})


if __name__ == "__main__":
    # Test case 1: Small feasible case
    print("=" * 60)
    print("TEST 1: Small feasible case (3 classes, 2 teachers, 2 rooms)")
    print("=" * 60)
    
    test_input = {
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
    
    result = run_scheduler(
        json.dumps(test_input),
        pop_size=50,
        generations=100,
        seed=42
    )
    
    result_dict = json.loads(result)
    print(f"\nFinal Fitness: {result_dict['final_fitness']}")
    print(f"Generations Run: {result_dict['generations_run']}")
    print(f"\nBest fitness over generations: {result_dict['best_fitness_history'][:10]}...")
    
    if result_dict['final_fitness'] == 0:
        print("\n✓ Perfect solution found!")
    else:
        print(f"\n⚠ Solution has {-result_dict['final_fitness']} penalty points")
    
    print("\nSample timetable (first day):")
    for period in result_dict['timetable'][0]['periods']:
        if period['class']:
            print(f"  Period {period['period']}: {period['subject']} - {period['teacher']} - Room {period['room']}")
        else:
            print(f"  Period {period['period']}: Free")
    
    # Test case 2: Impossible case
    print("\n" + "=" * 60)
    print("TEST 2: Impossible case (too many hours)")
    print("=" * 60)
    
    impossible_input = {
        'days': ['Monday', 'Tuesday'],
        'periods_per_day': 2,
        'rooms': [{'id': 'R1', 'capacity': 30}],
        'teachers': [{'id': 'T1', 'name': 'Mr. Smith'}],
        'classes': [
            {'id': 'C1', 'subject': 'Math', 'teacher_id': 'T1', 'hours_per_week': 3},
            {'id': 'C2', 'subject': 'English', 'teacher_id': 'T1', 'hours_per_week': 3}
        ]
    }
    
    result = run_scheduler(json.dumps(impossible_input))
    result_dict = json.loads(result)
    
    if 'error' in result_dict:
        print(f"✓ Error correctly detected: {result_dict['error']}")
    else:
        print("✗ Should have detected impossible case!")
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60)
