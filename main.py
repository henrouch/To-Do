from mcp.server.fastmcp import FastMCP
import json
import os

mcp = FastMCP("todo")

# Persistent storage
DATA_DIR = os.path.join(os.path.expanduser("~"), "todo_data")
os.makedirs(DATA_DIR, exist_ok=True)
FILE = os.path.join(DATA_DIR, "tasks.json")

DEFAULT_CLIENT = "default"


# ---------- Storage helpers ----------

def load_data():
    if not os.path.exists(FILE):
        return {"clients": {}}
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
        if "clients" not in data or not isinstance(data["clients"], dict):
            return {"clients": {}}
        return data
    except Exception:
        return {"clients": {}}


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def ensure_client(data, client_id):
    if client_id not in data["clients"]:
        data["clients"][client_id] = {
            "tasks": [],
            "next_id": 1,
            "stats": {"completed": 0, "failed": 0}
        }
    if "stats" not in data["clients"][client_id]:
        data["clients"][client_id]["stats"] = {"completed": 0, "failed": 0}


def next_task_id(data, client_id):
    nid = data["clients"][client_id].get("next_id", 1)
    try:
        nid = int(nid)
    except Exception:
        nid = 1
    data["clients"][client_id]["next_id"] = nid + 1
    return nid


def ok(**kwargs):
    return {"ok": True, **kwargs}


def err(message, **kwargs):
    return {"ok": False, "error": message, **kwargs}


def matches_deadline(task, deadline):
    # simple exact-match deadline filter (ex: "2026-02-21")
    return str(task.get("deadline", "")) == str(deadline)

@mcp.tool(title="Add Task")
def add_task(
    title: str,
    description: str = "",
    deadline: str = "",
    category: str = "",
    client_id: str = DEFAULT_CLIENT
):
    title = (title or "").strip()
    if not title:
        return err("title is required")

    data = load_data()
    if "clients" not in data:
        data["clients"] = {}
    ensure_client(data, client_id)

    task = {
        "id": next_task_id(data, client_id),
        "title": title,
        "description": description.strip(),
        "deadline": deadline.strip(),     # optional (empty string means none)
        "category": category.strip().lower(),  # ex: "homework", "work"
        "completed": False
    }

    data["clients"][client_id]["tasks"].append(task)
    save_data(data)
    return ok(task=task)

@mcp.tool(title="Delete Task")
def delete_task(
    task_id: int,
    client_id: str = DEFAULT_CLIENT,
    was_completed: bool = False
):
    """
    Deletes a task and updates stats:
      - was_completed=True => completed counter +1
      - was_completed=False => failed counter +1
    """
    data = load_data()
    if "clients" not in data:
        data["clients"] = {}
    ensure_client(data, client_id)

    try:
        task_id = int(task_id)
    except Exception:
        return err("task_id must be an integer", task_id=task_id)

    tasks = data["clients"][client_id]["tasks"]
    for i, task in enumerate(tasks):
        if int(task["id"]) == task_id:
            deleted = tasks.pop(i)

            if bool(was_completed):
                data["clients"][client_id]["stats"]["completed"] += 1
            else:
                data["clients"][client_id]["stats"]["failed"] += 1

            save_data(data)
            return ok(deleted=deleted, stats=data["clients"][client_id]["stats"])

    return err("Task not found", task_id=task_id)



@mcp.tool(title="List Tasks")
def list_tasks(client_id: str = DEFAULT_CLIENT):
    data = load_data()
    ensure_client(data, client_id)

    tasks = data["clients"][client_id]["tasks"]
    stats = data["clients"][client_id]["stats"]

    if not tasks:
        return f"No tasks found for client '{client_id}'."

    output = []
    output.append(f"Client: {client_id}\n")
    output.append("ID | Title | Deadline | Category | Status")
    output.append("---|-------|----------|-----------|--------")

    for task in tasks:
        status = "done" if task.get("completed") else "pending"
        deadline = task.get("deadline") or "None"
        category = task.get("category") or "None"

        output.append(
            f"{task['id']} | {task['title']} | {deadline} | {category} | {status}"
        )

    output.append("\nCompleted: " + str(stats["completed"]))
    output.append("Failed: " + str(stats["failed"]))
    return "\n".join(output)

@mcp.tool(title="Edit Task")
def edit_task(
    task_id: int,
    client_id: str = DEFAULT_CLIENT,
    new_title: str = None,
    new_description: str = None,
    new_deadline: str = None,
    new_category: str = None
):
    data = load_data()
    if "clients" not in data:
        data["clients"] = {}
    ensure_client(data, client_id)

    try:
        task_id = int(task_id)
    except Exception:
        return err("task_id must be an integer", task_id=task_id)

    for task in data["clients"][client_id]["tasks"]:
        if int(task["id"]) == task_id:
            if new_title is not None:
                nt = str(new_title).strip()
                if not nt:
                    return err("new_title cannot be empty")
                task["title"] = nt
            if new_description is not None:
                task["description"] = str(new_description).strip()
            if new_deadline is not None:
                task["deadline"] = str(new_deadline).strip()
            if new_category is not None:
                task["category"] = str(new_category).strip().lower()

            save_data(data)
            return ok(task=task)

    return err("Task not found", task_id=task_id)



@mcp.tool(title="Get Stats")
def get_stats(client_id: str = DEFAULT_CLIENT):
    data = load_data()
    if "clients" not in data:
        data["clients"] = {}
    ensure_client(data, client_id)
    return ok(stats=data["clients"][client_id]["stats"])


if __name__ == "__main__":
    mcp.run()
