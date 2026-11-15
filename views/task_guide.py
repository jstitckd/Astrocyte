"""Learning page opened by a habitat task notification."""
import streamlit as st

from models.task_guides import TASK_GUIDES
from services.dashboard import SAMPLE_TASKS, complete_task


def _go(page):
    st.session_state.page = page


def _finish(task_id):
    complete_task(task_id)
    st.session_state.page = "home"


def render():
    st.button("← Dashboard", key="task_back", on_click=_go, args=("home",))
    task_id = st.session_state.get("selected_habitat_task")
    task = next((task for task in SAMPLE_TASKS if task["id"] == task_id), None)
    guide = TASK_GUIDES.get(task["id"]) if task else None
    if not task or not guide:
        st.title("Task guide")
        st.info("Choose a task notification on the dashboard map to open its guide.")
        return

    st.title(task["title"])
    with st.container(border=True, key="taskguide_preparation"):
        st.markdown("**Before you begin**")
        st.write(guide["equipment"])
    with st.container(border=True, key="taskguide_steps"):
        for number, (title, instructions) in enumerate(guide["steps"], 1):
            st.markdown(f"**{number}. {title}**")
            st.write(instructions)
    if guide.get("source"):
        label, url = guide["source"]
        st.markdown(f"Reference: [{label}]({url})")
    st.button(f"Open {task['crew']}'s health", key="task_crew_health", on_click=_go, args=(task["crew"],))
    if task_id in st.session_state.get("completed_habitat_tasks", []):
        st.success("This task is complete.")
    else:
        st.button("Mark task complete & return to Dashboard", type="primary", key="finish_task_guide", on_click=_finish, args=(task_id,))
