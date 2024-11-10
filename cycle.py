import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import time

# File path for saving project data
PROJECTS_FILE = "projects.json"

# Load projects from JSON or initialize
def load_projects():
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    else:
        return {
            1: {"name": "Project A", "priority": "Low", "assigned_to": None, "last_worked": None, "assigned_count": 0},
            2: {"name": "Project B", "priority": "Low", "assigned_to": None, "last_worked": (datetime.now() - timedelta(days=30)).isoformat(), "assigned_count": 1},
            3: {"name": "Project C", "priority": "Low", "assigned_to": "John Doe", "last_worked": datetime.now().isoformat(), "assigned_count": 2},
            # ... more projects
        }

def save_projects(projects):
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=4, default=str)

# Load projects
projects = load_projects()

# Sample team member data
team_members = ["John Doe", "Jane Smith", "Peter Jones"]

# Function to sort low-priority projects
def sort_low_priority_projects(projects):
    low_priority = [p for p in projects.values() if p["priority"] == "Low"]
    return sorted(low_priority, key=lambda x: (x["assigned_count"], x.get("last_worked", datetime.min)))


# Streamlit app
st.title("Low Priority Project Management")

# Display sorted low-priority projects
sorted_projects = sort_low_priority_projects(projects)
st.header("Low Priority Queue")

for project in sorted_projects:
    last_worked = project.get("last_worked")
    if last_worked:
        last_worked = datetime.fromisoformat(last_worked).strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"{project['name']} - Assigned: {project['assigned_to']} - Last Worked: {last_worked or 'Never'}")


# Manual assignment
st.header("Manual Assignment")
selected_project = st.selectbox("Select Project:", [p["name"] for p in sorted_projects if p['priority'] == 'Low'])
selected_member = st.selectbox("Assign To:", team_members)

if st.button("Assign"):
    project_id = next((k for k, v in projects.items() if v["name"] == selected_project), None)
    if project_id:
        updated_project = projects[project_id].copy()
        updated_project["assigned_to"] = selected_member
        updated_project["last_worked"] = datetime.now().isoformat()
        updated_project["assigned_count"] += 1
        projects[project_id] = updated_project
        save_projects(projects)
        st.success(f"Assigned {selected_project} to {selected_member}")
        time.sleep(2)
        st.rerun()

# Reset button
if st.button("Reset"):
    try:
        os.remove(PROJECTS_FILE)
        projects = load_projects() # Reload initial data after file deletion
        st.success("Project data reset successfully!")
        time.sleep(2)
        st.rerun()
    except FileNotFoundError:
        st.warning("No project data file found to reset.")
    except Exception as e:
        st.error(f"An error occurred during reset: {e}")
