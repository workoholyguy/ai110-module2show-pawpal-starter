# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
