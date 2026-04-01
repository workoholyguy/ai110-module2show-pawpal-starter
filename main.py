"""Temporary testing ground — verify pawpal_system logic in the terminal."""

from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup (intentional conflict: two tasks at 07:00) ---
owner = Owner(name="Jordan", available_minutes=90)

mochi = Pet(name="Mochi", species="dog")
mochi.add_task(Task("Morning walk", "walk", 30, "high", "daily",
                     scheduled_time="07:00", due_date=date.today()))
mochi.add_task(Task("Breakfast", "feeding", 10, "high", "daily",
                     scheduled_time="07:00", due_date=date.today()))
mochi.add_task(Task("Flea medication", "medication", 5, "medium", "weekly",
                     scheduled_time="12:00", due_date=date.today()))

whiskers = Pet(name="Whiskers", species="cat")
whiskers.add_task(Task("Litter box cleanup", "grooming", 10, "high", "daily",
                        scheduled_time="06:30", due_date=date.today()))
whiskers.add_task(Task("Feeder puzzle", "enrichment", 20, "low", "daily",
                        scheduled_time="12:00", due_date=date.today()))
whiskers.add_task(Task("Evening brushing", "grooming", 15, "medium", "daily",
                        scheduled_time="18:00", due_date=date.today()))

owner.add_pet(mochi)
owner.add_pet(whiskers)

# --- 1. Generate schedule ---
scheduler = Scheduler(owner)
plan = scheduler.generate_plan()
print(plan.display())

# --- 2. Conflict detection ---
print("\n== Conflict Detection ==")
warnings = scheduler.detect_conflicts(plan.scheduled_tasks)
if warnings:
    for w in warnings:
        print(f"  WARNING: {w}")
else:
    print("  No conflicts found.")

# --- 3. Sort by time ---
print("\n== Schedule Sorted by Time ==")
by_time = Scheduler.sort_by_time(plan.scheduled_tasks)
for t in by_time:
    print(f"  {t.scheduled_time}  {t.name} ({t.priority})")

# --- 4. Recurring task demo ---
print("\n== Recurring Task Demo ==")
walk = mochi.tasks[0]
print(f"Completing: {walk.name} (due {walk.due_date}, daily)")
next_walk = mochi.complete_task(walk)
print(f"  Next occurrence: {next_walk.name} due {next_walk.due_date}")

flea = mochi.tasks[2]
print(f"Completing: {flea.name} (due {flea.due_date}, weekly)")
next_flea = mochi.complete_task(flea)
print(f"  Next occurrence: {next_flea.name} due {next_flea.due_date}")

# --- 5. Filtering ---
print("\n== Filter: incomplete grooming tasks ==")
grooming = owner.filter_tasks(completed=False, category="grooming")
for t in grooming:
    print(f"  {t.name} ({t.duration_minutes} min)")
