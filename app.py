import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# -------------------------------------------------------------------
# Session state: persist Owner, Pet, and Task objects across reruns
# -------------------------------------------------------------------
# Check if objects already exist before creating new ones.
# This prevents data from being wiped on every Streamlit rerun.

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=60)

if "pets" not in st.session_state:
    st.session_state.pets = []  # list of Pet objects

if "plan" not in st.session_state:
    st.session_state.plan = None  # will hold a DailyPlan after generation

# Convenience references (read from the vault each rerun)
owner = st.session_state.owner

# -------------------------------------------------------------------
# 1. Owner setup
# -------------------------------------------------------------------
st.subheader("Owner Profile")

owner_name = st.text_input("Owner name", value=owner.name)
available = st.number_input(
    "Available minutes for pet care today",
    min_value=1, max_value=480, value=owner.available_minutes,
)
# Keep the session object in sync with the UI widgets
owner.name = owner_name
owner.set_availability(int(available))

# -------------------------------------------------------------------
# 2. Add a pet
# -------------------------------------------------------------------
st.divider()
st.subheader("Pets")

col_pn, col_sp = st.columns(2)
with col_pn:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col_sp:
    new_species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])

if st.button("Add pet"):
    pet = Pet(name=new_pet_name, species=new_species)
    st.session_state.pets.append(pet)
    # Also register the pet on the Owner so the Scheduler can find it
    owner.add_pet(pet)

if st.session_state.pets:
    for pet in st.session_state.pets:
        st.write(f"**{pet.name}** ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

# -------------------------------------------------------------------
# 3. Add tasks to a pet
# -------------------------------------------------------------------
st.divider()
st.subheader("Tasks")

if st.session_state.pets:
    pet_names = [p.name for p in st.session_state.pets]
    selected_pet_name = st.selectbox("Assign task to pet", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20,
        )
    with col3:
        priority = st.selectbox(
            "Priority", ["high", "medium", "low"], index=0,
        )

    if st.button("Add task"):
        # Find the selected pet and attach the task
        target_pet = next(
            p for p in st.session_state.pets
            if p.name == selected_pet_name
        )
        target_pet.add_task(
            Task(
                name=task_title,
                category="general",
                duration_minutes=int(duration),
                priority=priority,
            )
        )

    # Show all tasks grouped by pet
    for pet in st.session_state.pets:
        if pet.tasks:
            st.write(f"**{pet.name}'s tasks:**")
            st.table([
                {
                    "Task": t.name,
                    "Duration": f"{t.duration_minutes} min",
                    "Priority": t.priority,
                }
                for t in pet.tasks
            ])
else:
    st.info("Add a pet first, then you can assign tasks.")

# -------------------------------------------------------------------
# 4. Generate schedule
# -------------------------------------------------------------------
st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add at least one pet with tasks first.")
    else:
        scheduler = Scheduler(owner)
        st.session_state.plan = scheduler.generate_plan()

if st.session_state.plan:
    plan = st.session_state.plan
    st.success(
        f"Scheduled {len(plan.scheduled_tasks)} task(s) "
        f"in {plan.total_minutes} minutes"
    )
    st.text(plan.display())
