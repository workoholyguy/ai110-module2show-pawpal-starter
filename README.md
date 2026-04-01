# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Beyond basic task listing, PawPal+ includes four algorithmic features:

- **Multi-key sorting** — tasks are sorted by priority (high first), then by shortest duration within the same priority. This "shortest-job-first" strategy fits more tasks into limited time.
- **Filtering** — `Owner.filter_tasks()` lets you query tasks by pet name, completion status, or category (e.g., "show me all of Mochi's incomplete walks").
- **Recurring tasks** — when a daily or weekly task is marked complete, a new instance is automatically created with the next due date (`today + 1 day` or `today + 7 days`) using Python's `timedelta`.
- **Conflict detection** — `Scheduler.detect_conflicts()` scans scheduled tasks for time-slot collisions (two tasks at the same "HH:MM") and returns warning messages instead of crashing.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Test | What it verifies |
|------|-----------------|
| `test_mark_complete_changes_status` | Calling `mark_complete()` on a Task flips `completed` from `False` to `True` |
| `test_add_task_increases_pet_task_count` | Each call to `Pet.add_task()` increases the pet's task list by exactly one |

### Confidence level: 3/5 stars

The core data operations (task completion and task addition) are verified and passing. However, the test suite does not yet cover the scheduler's priority sorting, the greedy packing algorithm, recurring task generation, conflict detection, or edge cases like zero available minutes or an empty task list. With additional tests for those behaviors, confidence would rise to 4-5 stars.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
