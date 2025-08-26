#!/usr/bin/env python3
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def generate_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def add_task(description):
    tasks = load_tasks()
    task = {
        "id": generate_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added (ID: {task['id']})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"✏️ Task {task_id} updated")
            return
    print(f"⚠️ Task {task_id} not found")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"⚠️ Task {task_id} not found")
        return
    save_tasks(new_tasks)
    print(f"🗑️ Task {task_id} deleted")

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"🔖 Task {task_id} marked as {status}")
            return
    print(f"⚠️ Task {task_id} not found")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    if not tasks:
        print("📭 No tasks found")
        return
    for task in tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']}")

def run_interactive():
    print("=== Task Tracker App ===")
    print("Type 'help' for commands, 'exit' to quit.\n")
    while True:
        command = input("task-cli> ").strip()
        if command == "exit":
            print("👋 Goodbye.")
            break
        elif command == "help":
            print("""
Commands:
  add <description>          - Add a new task
  update <id> <description>  - Update a task
  delete <id>                - Delete a task
  mark-in-progress <id>      - Mark task as in progress
  mark-done <id>             - Mark task as done
  list                       - List all tasks
  list todo                  - List tasks not done
  list in-progress           - List tasks in progress
  list done                  - List completed tasks
  exit                       - Exit the app
""")
        elif command.startswith("add "):
            add_task(command[4:])
        elif command.startswith("update "):
            parts = command.split(" ", 2)
            if len(parts) < 3:
                print("⚠️ Usage: update <id> <description>")
            else:
                update_task(int(parts[1]), parts[2])
        elif command.startswith("delete "):
            parts = command.split(" ")
            if len(parts) != 2:
                print("⚠️ Usage: delete <id>")
            else:
                delete_task(int(parts[1]))
        elif command.startswith("mark-in-progress "):
            parts = command.split(" ")
            if len(parts) != 2:
                print("⚠️ Usage: mark-in-progress <id>")
            else:
                mark_task(int(parts[1]), "in-progress")
        elif command.startswith("mark-done "):
            parts = command.split(" ")
            if len(parts) != 2:
                print("⚠️ Usage: mark-done <id>")
            else:
                mark_task(int(parts[1]), "done")
        elif command.startswith("list"):
            parts = command.split(" ")
            if len(parts) == 1:
                list_tasks()
            elif parts[1] in ["todo", "done", "in-progress"]:
                list_tasks(parts[1])
            else:
                print("⚠️ Invalid list option. Use: todo, in-progress, done")
        else:
            print("⚠️ Unknown command. Type 'help'.")

if __name__ == "__main__":
    run_interactive()

