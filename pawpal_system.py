"""
PawPal+ Logic Layer
====================
Backend classes for the PawPal+ pet care planning assistant.
Mirrors the UML class diagram in uml.mmd.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


# ---------------------------------------------------------------------------
# Data classes (pure data holders)
# ---------------------------------------------------------------------------

@dataclass
class Owner:
    """Represents the pet owner and their time constraints."""

    name: str
    available_minutes: int  # total minutes the owner can spend on pet care today

    def set_availability(self, minutes: int) -> None:
        """Update the owner's available time for pet care."""
        self.available_minutes = minutes


@dataclass
class Pet:
    """Represents the pet being cared for."""

    name: str
    species: str  # e.g. "dog", "cat", "rabbit"
    special_needs: str = ""  # optional notes (allergies, conditions, etc.)

    def update_info(self, name: str, species: str, special_needs: str) -> None:
        """Edit the pet's profile details."""
        self.name = name
        self.species = species
        self.special_needs = special_needs


@dataclass
class Task:
    """A single pet care activity that can be scheduled."""

    name: str  # e.g. "Morning walk"
    category: str  # walk, feeding, medication, grooming, enrichment
    duration_minutes: int  # how long the task takes
    priority: int  # 1 = highest, 3 = lowest

    def edit(
        self,
        name: str,
        category: str,
        duration_minutes: int,
        priority: int,
    ) -> None:
        """Update this task's details."""
        self.name = name
        self.category = category
        self.duration_minutes = duration_minutes
        self.priority = priority


# ---------------------------------------------------------------------------
# Plan output
# ---------------------------------------------------------------------------

@dataclass
class DailyPlan:
    """The output of the scheduler — an ordered schedule for the day."""

    scheduled_tasks: List[Task] = field(default_factory=list)
    skipped_tasks: List[Task] = field(default_factory=list)
    total_minutes: int = 0
    reasoning: str = ""

    def display(self) -> str:
        """Return a human-readable string of the daily plan."""
        # TODO: implement formatted output
        pass


# ---------------------------------------------------------------------------
# Scheduler (core engine)
# ---------------------------------------------------------------------------

class Scheduler:
    """Builds a daily care plan from owner constraints and a task list."""

    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner: Owner = owner
        self.pet: Pet = pet
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the scheduler's task list."""
        self.tasks.remove(task)

    def generate_plan(self) -> DailyPlan:
        """Sort tasks by priority, fit them into available time, and return a DailyPlan."""
        # TODO: implement scheduling logic
        pass

    def explain_plan(self, plan: DailyPlan) -> str:
        """Produce a human-readable explanation of why the plan is arranged as it is."""
        # TODO: implement reasoning output
        pass
