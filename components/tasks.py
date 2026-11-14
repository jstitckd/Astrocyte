import hashlib

import streamlit as st

from models.areas import AREAS, Task


def tasks_for(context, area_id):
    tasks = list(AREAS[area_id].tasks)
    if area_id == "eva":
        tasks += [Task(context.store.eva_task_id(label), label) for label in context.store.eva_tasks(context.crew_id)]
    return tasks


def completion(context, day):
    tasks = [(area_id, task) for area_id in AREAS for task in tasks_for(context, area_id)]
    done = sum(context.store.task_done(context.dataset_id, context.crew_id, day, area_id, task.id) for area_id, task in tasks)
    return done, len(tasks)


def render_tasks(context, area_id, day):
    st.markdown("### Your checklist")
    st.caption(f"{day:%d %b %Y} · Manual completion, separate from your readings.")
    for task in tasks_for(context, area_id):
        scope = f"{context.dataset_id}/{context.crew_id}/{day}/{area_id}/{task.id}"
        key = "task_" + hashlib.sha256(scope.encode()).hexdigest()[:20]
        done = context.store.task_done(context.dataset_id, context.crew_id, day, area_id, task.id)
        st.checkbox(task.label, value=done, key=key, on_change=_save_task,
                    args=(context.store, context.dataset_id, context.crew_id, day, area_id, task.id, key))
    if area_id == "eva":
        st.caption("Illustrative planning checklist. Follow your mission's approved procedures; this app does not certify EVA readiness.")
        with st.expander("Edit pre-EVA checklist"):
            with st.form("configure_eva_" + context.crew_id):
                text = st.text_area("One item per line · 1–12 items", value="\n".join(context.store.eva_tasks(context.crew_id)), max_chars=1932)
                if st.form_submit_button("Save checklist"):
                    try:
                        context.store.configure_eva(context.crew_id, text)
                        st.session_state.flash = "Pre-EVA checklist updated for this crew member, in this session."
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))


def _save_task(store, dataset, crew, day, area, task_id, key):
    store.set_task(dataset, crew, day, area, task_id, st.session_state[key])
