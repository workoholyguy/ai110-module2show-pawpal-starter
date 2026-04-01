# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The initial UML design splits the system into five classes, each with a single clear responsibility:

- **Owner** — Holds the pet owner's name and how many minutes they have available for pet care today. Its only behavior is `set_availability()`, which updates that time budget. This class exists so the scheduler has a constraint to plan against.
- **Pet** — Stores the pet's name, species, and any special needs (e.g., allergies, medications). `update_info()` lets the user edit these details. Keeping pet data separate from the owner means the system could support multiple pets in the future.
- **Task** — Represents one care activity (walk, feeding, medication, grooming, or enrichment) with a duration in minutes and an integer priority (1 = highest, 3 = lowest). `edit()` allows updating any field. This is the core unit the scheduler works with.
- **Scheduler** — The central engine. It holds references to an Owner, a Pet, and a list of Tasks. `add_task()` / `remove_task()` manage the list. `generate_plan()` is where the real logic lives: it sorts tasks by priority, fits as many as possible into the owner's available minutes, and returns a DailyPlan. `explain_plan()` produces a reasoning string for a given plan.
- **DailyPlan** — The output object. It separates tasks into `scheduled_tasks` (what fits) and `skipped_tasks` (what didn't), tracks `total_minutes`, and carries a `reasoning` string. `display()` formats everything for the UI.

I used Python `@dataclass` for Owner, Pet, Task, and DailyPlan because they are primarily data holders — dataclasses give clean `__init__`, `__repr__`, and `__eq__` for free. Scheduler is a regular class because it manages mutable state and contains the core algorithm.

**Core user actions identified from the scenario:**

1. **Add a pet and owner profile** — The user enters basic information about themselves (name, time available for pet care) and their pet (name, species, any special needs). This establishes the context and constraints the scheduler will work with.

2. **Add and edit care tasks** — The user creates pet care tasks such as walks, feeding, medication, grooming, or enrichment activities. Each task has at least a duration and a priority level. The user can update these tasks as needs change (e.g., a vet prescribes new medication or a walk schedule shifts).

3. **Generate and view a daily care plan** — The user requests a daily schedule that fits their available time. The system prioritizes tasks by urgency and importance, produces an ordered plan, and explains why it arranged tasks that way (e.g., "Medication is scheduled first because it is high priority and time-sensitive").

**Building blocks (classes, attributes, and methods):**

### 1. Owner
Represents the pet owner and their constraints.
- **Attributes:**
  - `name` (str) — the owner's name
  - `available_minutes` (int) — total minutes the owner has for pet care today
- **Methods:**
  - `set_availability(minutes)` — update how much time the owner has available

### 2. Pet
Represents the pet being cared for.
- **Attributes:**
  - `name` (str) — the pet's name
  - `species` (str) — e.g., dog, cat, rabbit
  - `special_needs` (str) — any notes like allergies or medical conditions
- **Methods:**
  - `update_info(name, species, special_needs)` — edit the pet's profile details

### 3. Task
Represents a single care activity to be scheduled.
- **Attributes:**
  - `name` (str) — description of the task (e.g., "Morning walk")
  - `category` (str) — type of task: walk, feeding, medication, grooming, enrichment
  - `duration_minutes` (int) — how long the task takes
  - `priority` (int) — urgency level (1 = highest, 3 = lowest)
- **Methods:**
  - `edit(name, category, duration_minutes, priority)` — update task details

### 4. Scheduler
The engine that produces a daily plan from the owner's constraints and task list.
- **Attributes:**
  - `owner` (Owner) — the owner whose schedule is being built
  - `pet` (Pet) — the pet being cared for
  - `tasks` (list of Task) — all available tasks to consider
- **Methods:**
  - `add_task(task)` — add a new task to the list
  - `remove_task(task)` — remove a task from the list
  - `generate_plan()` — sort tasks by priority, fit them into the owner's available time, and return a DailyPlan
  - `explain_plan(plan)` — produce a human-readable explanation of why tasks were ordered/included

### 5. DailyPlan
The output of the scheduler — an ordered list of tasks that fit the day's constraints.
- **Attributes:**
  - `scheduled_tasks` (list of Task) — tasks included in the plan, in order
  - `skipped_tasks` (list of Task) — tasks that didn't fit the available time
  - `total_minutes` (int) — total duration of the scheduled tasks
  - `reasoning` (str) — explanation of why the plan looks the way it does
- **Methods:**
  - `display()` — format the plan for presentation in the UI

**b. Design changes**

Yes — reviewing the skeleton against the starter `app.py` revealed two mismatches that need to be addressed during implementation:

1. **Priority type mismatch.** The UML and skeleton use an integer priority (1, 2, 3), but `app.py` already uses string priorities ("high", "medium", "low") in its selectbox. During implementation I will need to either convert between the two or standardize on one. Standardizing on strings in the Task class (and sorting by a known order) is likely simpler because it avoids asking the user to think in numbers.

2. **`explain_plan()` is redundant with `DailyPlan.reasoning`.** The original UML puts `explain_plan(plan)` on the Scheduler *and* a `reasoning` attribute on DailyPlan. In practice the reasoning should be generated *inside* `generate_plan()` and stored directly on the DailyPlan it returns. That way `DailyPlan.display()` can present everything in one place without needing to call back into the Scheduler. I plan to fold the explanation logic into `generate_plan()` and may remove or simplify `explain_plan()` as a standalone method.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
