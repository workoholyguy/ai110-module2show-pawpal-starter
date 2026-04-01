"""Temporary testing ground — verify pawpal_system logic in the terminal."""

from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", available_minutes=90)

# Pet 1: Mochi the dog
mochi = Pet(name="Mochi", species="dog")
mochi.add_task(Task("Morning walk", "walk", 30, "high", "daily"))
mochi.add_task(Task("Breakfast", "feeding", 10, "high", "daily"))
mochi.add_task(Task("Flea medication", "medication", 5, "medium", "weekly"))

# Pet 2: Whiskers the cat
whiskers = Pet(name="Whiskers", species="cat")
whiskers.add_task(Task("Litter box cleanup", "grooming", 10, "high", "daily"))
whiskers.add_task(Task("Feeder puzzle", "enrichment", 20, "low", "daily"))
whiskers.add_task(Task("Evening brushing", "grooming", 15, "medium", "daily"))

owner.add_pet(mochi)
owner.add_pet(whiskers)

# --- Generate and print the schedule ---
scheduler = Scheduler(owner)
plan = scheduler.generate_plan()

print(plan.display())
