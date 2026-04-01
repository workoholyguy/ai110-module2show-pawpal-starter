"""
PawPal+ Logic Layer
====================
Backend classes for the PawPal+ pet care planning assistant.
Mirrors the UML class diagram in uml.mmd (with design updates
noted in reflection.md section 1b).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List

# Priority ordering used by the scheduler (highest first).
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


# -------------------------------------------------------------------
# Task
# -------------------------------------------------------------------

@dataclass
class Task:
    """A single pet care activity that can be scheduled."""

    name: str               # e.g. "Morning walk"
    category: str           # walk, feeding, medication, grooming, enrichment
    duration_minutes: int   # how long the task takes
    priority: str = "medium"  # "high", "medium", or "low"
    frequency: str = "daily"  # "daily", "weekly", "as needed"
    completed: bool = False
    scheduled_time: str = ""  # "HH:MM" format, e.g. "07:30"
    due_date: date | None = None  # when this task is due

    # How far ahead each frequency pushes the next occurrence.
    FREQUENCY_DELTA = {
        "daily": timedelta(days=1),
        "weekly": timedelta(weeks=1),
    }

    def edit(
        self,
        name: str | None = None,
        category: str | None = None,
        duration_minutes: int | None = None,
        priority: str | None = None,
        frequency: str | None = None,
    ) -> None:
        """Update any subset of this task's details."""
        if name is not None:
            self.name = name
        if category is not None:
            self.category = category
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency

    def mark_complete(self) -> Task | None:
        """Mark this task as done and return the next occurrence if recurring."""
        self.completed = True
        delta = self.FREQUENCY_DELTA.get(self.frequency)
        if delta is None:
            # "as needed" — no automatic recurrence
            return None
        next_due = (self.due_date or date.today()) + delta
        return Task(
            name=self.name,
            category=self.category,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            scheduled_time=self.scheduled_time,
            due_date=next_due,
        )

    def mark_incomplete(self) -> None:
        """Reset this task to not-done."""
        self.completed = False


# -------------------------------------------------------------------
# Pet
# -------------------------------------------------------------------

@dataclass
class Pet:
    """A pet and its associated care tasks."""

    name: str
    species: str              # "dog", "cat", "rabbit", etc.
    special_needs: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        self.tasks.remove(task)

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task done; if recurring, add the next occurrence automatically."""
        next_task = task.mark_complete()
        if next_task is not None:
            self.tasks.append(next_task)
        return next_task

    def pending_tasks(self) -> List[Task]:
        """Return only tasks that haven't been completed yet."""
        return [t for t in self.tasks if not t.completed]

    def update_info(
        self,
        name: str | None = None,
        species: str | None = None,
        special_needs: str | None = None,
    ) -> None:
        """Edit the pet's profile details."""
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if special_needs is not None:
            self.special_needs = special_needs


# -------------------------------------------------------------------
# Owner
# -------------------------------------------------------------------

@dataclass
class Owner:
    """The pet owner — manages multiple pets and time constraints."""

    name: str
    available_minutes: int          # time budget for pet care today
    pets: List[Pet] = field(default_factory=list)

    def set_availability(self, minutes: int) -> None:
        """Update the owner's available time."""
        self.available_minutes = minutes

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        self.pets.remove(pet)

    def all_tasks(self) -> List[Task]:
        """Gather every task across all pets."""
        result: List[Task] = []
        for pet in self.pets:
            result.extend(pet.tasks)
        return result

    def all_pending_tasks(self) -> List[Task]:
        """Gather every incomplete task across all pets."""
        result: List[Task] = []
        for pet in self.pets:
            result.extend(pet.pending_tasks())
        return result

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
        category: str | None = None,
    ) -> List[Task]:
        """Filter tasks across all pets by pet name, status, or category."""
        # Start with tasks from a specific pet, or all pets
        if pet_name is not None:
            matching_pets = [p for p in self.pets if p.name == pet_name]
            tasks = []
            for pet in matching_pets:
                tasks.extend(pet.tasks)
        else:
            tasks = self.all_tasks()

        # Filter by completion status
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]

        # Filter by category
        if category is not None:
            tasks = [t for t in tasks if t.category == category]

        return tasks


# -------------------------------------------------------------------
# DailyPlan (output object)
# -------------------------------------------------------------------

@dataclass
class DailyPlan:
    """The scheduler's output — an ordered schedule for the day."""

    scheduled_tasks: List[Task] = field(default_factory=list)
    skipped_tasks: List[Task] = field(default_factory=list)
    total_minutes: int = 0
    reasoning: str = ""

    def display(self) -> str:
        """Return a human-readable summary of the plan."""
        lines: List[str] = []
        lines.append("== Daily Plan ==")
        lines.append(
            f"Scheduled: {len(self.scheduled_tasks)} task(s) "
            f"| {self.total_minutes} min total"
        )
        lines.append("")

        for i, task in enumerate(self.scheduled_tasks, start=1):
            lines.append(
                f"  {i}. {task.name} "
                f"({task.category}, {task.duration_minutes} min, "
                f"priority: {task.priority})"
            )

        if self.skipped_tasks:
            lines.append("")
            lines.append("Skipped (not enough time):")
            for task in self.skipped_tasks:
                lines.append(
                    f"  - {task.name} "
                    f"({task.duration_minutes} min, "
                    f"priority: {task.priority})"
                )

        if self.reasoning:
            lines.append("")
            lines.append("Reasoning:")
            lines.append(f"  {self.reasoning}")

        return "\n".join(lines)


# -------------------------------------------------------------------
# Scheduler (core engine)
# -------------------------------------------------------------------

class Scheduler:
    """Builds a daily care plan by querying the Owner for pet data."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    @staticmethod
    def sort_by_time(tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled_time in HH:MM format."""
        # Tasks without a scheduled_time sort to the end.
        # The lambda splits "HH:MM" into (hours, minutes) for
        # correct chronological ordering.
        return sorted(
            tasks,
            key=lambda t: (
                tuple(int(x) for x in t.scheduled_time.split(":"))
                if t.scheduled_time
                else (99, 99)
            ),
        )

    def generate_plan(self) -> DailyPlan:
        """
        Build a DailyPlan:
        1. Collect all pending tasks from the owner's pets.
        2. Sort by priority (high > medium > low), then shortest
           duration first within the same priority so more tasks fit.
        3. Greedily pack tasks into the owner's available time.
        4. Anything that doesn't fit goes into skipped_tasks.
        5. Attach reasoning explaining the decisions.
        """
        pending = self.owner.all_pending_tasks()

        # Multi-key sort: priority first, then shortest duration.
        # This "shortest-job-first" secondary sort helps fit more
        # tasks into limited time.
        sorted_tasks = sorted(
            pending,
            key=lambda t: (
                PRIORITY_ORDER.get(t.priority, 99),
                t.duration_minutes,
            ),
        )

        scheduled: List[Task] = []
        skipped: List[Task] = []
        time_left = self.owner.available_minutes

        for task in sorted_tasks:
            if task.duration_minutes <= time_left:
                scheduled.append(task)
                time_left -= task.duration_minutes
            else:
                skipped.append(task)

        total = self.owner.available_minutes - time_left

        reasoning = self._build_reasoning(scheduled, skipped)

        return DailyPlan(
            scheduled_tasks=scheduled,
            skipped_tasks=skipped,
            total_minutes=total,
            reasoning=reasoning,
        )

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warning messages for tasks that share the same scheduled_time."""
        # Group tasks by their scheduled_time slot.
        time_slots: dict[str, List[Task]] = {}
        for task in tasks:
            if not task.scheduled_time:
                continue
            time_slots.setdefault(task.scheduled_time, []).append(task)

        warnings: List[str] = []
        for time, group in time_slots.items():
            if len(group) > 1:
                names = ", ".join(t.name for t in group)
                warnings.append(
                    f"Conflict at {time}: {names} "
                    f"({len(group)} tasks overlap)"
                )
        return warnings

    def _build_reasoning(
        self,
        scheduled: List[Task],
        skipped: List[Task],
    ) -> str:
        """Generate a plain-English explanation of the plan."""
        parts: List[str] = []

        parts.append(
            f"The owner has {self.owner.available_minutes} minutes "
            f"available today."
        )

        if scheduled:
            parts.append(
                "Tasks are ordered by priority (high before medium "
                "before low) and packed greedily into the time budget."
            )
            high = [t for t in scheduled if t.priority == "high"]
            if high:
                names = ", ".join(t.name for t in high)
                parts.append(
                    f"High-priority tasks scheduled first: {names}."
                )

        if skipped:
            names = ", ".join(t.name for t in skipped)
            parts.append(
                f"Skipped due to insufficient time: {names}."
            )

        if not scheduled:
            parts.append(
                "No tasks could be scheduled — either none are "
                "pending or none fit the available time."
            )

        return " ".join(parts)
