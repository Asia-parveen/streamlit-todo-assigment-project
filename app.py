


import streamlit as st
import json
from pathlib import Path

# File to store tasks
task_file = Path("tasks.json")

# Load tasks from file
def load_tasks():
    if task_file.exists():
        with open(task_file, "r") as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(task_file, "w") as f:
        json.dump(tasks, f, indent=4)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "task_input" not in st.session_state:
    st.session_state.task_input = ""

# Streamlit UI
st.set_page_config(page_title="To-Do List", page_icon="📝", layout="centered")
st.title("📝 To-Do List App")
st.markdown("### Organize your tasks efficiently!")

# Input field for new task
new_task = st.text_input("Add a new task:", value=st.session_state.get("task_input", ""), key="task_input_input")

if st.button("➕ Add Task", use_container_width=True):
    if new_task.strip():
        st.session_state.tasks.append({"task": new_task, "completed": False})
        save_tasks(st.session_state.tasks)

        # Reset input field safely
        st.session_state.task_input = ""  # Update before UI renders
        st.rerun()  # ✅ Use this instead of experimental_rerun()
    else:
        st.warning("Task cannot be empty!")

# Display tasks
st.subheader("Your Tasks")
if not st.session_state.tasks:
    st.info("No tasks added yet. Start by adding a new task above!")
else:
    for index, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        with col1:
            task_text = f"✔️ {task['task']}" if task["completed"] else task["task"]
            st.markdown(f"**{task_text}**" if not task["completed"] else f"~~{task_text}~~")
        with col2:
            if st.button("✅ Done", key=f"done_{index}", use_container_width=True):
                st.session_state.tasks[index]["completed"] = True
                save_tasks(st.session_state.tasks)
                st.rerun()  # ✅ Use st.rerun()
        with col3:
            if st.button("🗑️ Delete", key=f"delete_{index}", use_container_width=True):
                del st.session_state.tasks[index]
                save_tasks(st.session_state.tasks)
                st.rerun()  # ✅ Use st.rerun()

# Apply CSS for better UI
def add_css():
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] input {
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
            border: 2px solid #ff6a00;
        }
        div[data-testid="stButton"] button {
            font-size: 16px;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
            transition: 0.3s;
        }
        div[data-testid="stButton"] button:first-of-type {
            background: linear-gradient(135deg, #ff5733, #ff8c00);
            color: white;
            border: none;
        }
        div[data-testid="stButton"] button:first-of-type:hover {
            background: linear-gradient(135deg, #ff2e00, #ff6a00);
        }
        div[data-testid="stButton"] button:nth-of-type(2) {
            background: #28a745;
            color: white;
        }
        div[data-testid="stButton"] button:nth-of-type(2):hover {
            background: #218838;
        }
        div[data-testid="stButton"] button:nth-of-type(3) {
            background: #dc3545;
            color: white;
        }
        div[data-testid="stButton"] button:nth-of-type(3):hover {
            background: #c82333;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_css()



