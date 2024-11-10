import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sample project data (replace with database or other persistent storage)
projects = {
    1: {"name": "Project A", "priority": "Low", "assigned_to": None, "last_worked": None, "assigned_count": 0},
    2: {"name": "Project B", "priority": "Low", "assigned_to": None, "last_worked": datetime.now() - timedelta(days=30), "assigned_count": 1},
    3: {"name": "Project C", "priority": "High", "assigned_to": "John Doe", "last_worked": datetime.now(), "assigned_count": 2},
    # ... more projects
}

team_members = ["John Doe", "Jane Smith", "Peter Jones"]  # Replace with team member data

# Function to sort low-priority projects
def sort_low_priority_projects(projects):
    low_priority = [p for p in projects.values() if p["priority"] == "Low"]
    return sorted(low_priority, key=lambda x: (x["assigned_count"], x.get("last_worked", datetime.min)))  # Sort by assigned count, then last worked date

# Streamlit app
st.title("Low Priority Project Management")

# Display sorted low-priority projects
sorted_projects = sort_low_priority_projects(projects)
st.header("Low Priority Queue")
for project in sorted_projects:
    st.write(f"{project['name']} - Assigned: {project['assigned_to']} - Last Worked: {project.get('last_worked', 'Never')}")

# Manual assignment
st.header("Manual Assignment")
selected_project = st.selectbox("Select Project:", [p["name"] for p in sorted_projects])
selected_member = st.selectbox("Assign To:", team_members)

if st.button("Assign"):
    project_id = next((k for k, v in projects.items() if v["name"] == selected_project), None)
    if project_id:
        projects[project_id]["assigned_to"] = selected_member
        projects[project_id]["last_worked"] = datetime.now()
        projects[project_id]["assigned_count"] += 1
        st.success(f"Assigned {selected_project} to {selected_member}")
        # Rerun the app to update the display
        st.rerun()


# ... (More features like activity logging, reporting, etc. would go here)
