"""Tests for PawPal+ core classes."""

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() should set completed to True."""
    task = Task("Morning walk", "walk", 30, "high")
    assert task.completed is False

    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its task list by one."""
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Breakfast", "feeding", 10, "high"))
    assert len(pet.tasks) == 1

    pet.add_task(Task("Evening walk", "walk", 25, "medium"))
    assert len(pet.tasks) == 2
