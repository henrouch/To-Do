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

@mcp.tool(title="Filter Tasks")
def filter_tasks(
    client_id: str = DEFAULT_CLIENT,
    deadline: str = "",
    category: str = "",
    completed: str = ""   # "", "true", "false"
):
    """
    Filter by:
      - deadline (exact match string)
      - category (case-insensitive)
      - completed: "true" or "false" (optional)
    """
    data = load_data()
    if "clients" not in data:
        data["clients"] = {}
    ensure_client(data, client_id)

    tasks = data["clients"][client_id]["tasks"]

    # Apply filters
    result = tasks

    if deadline.strip():
        d = deadline.strip()
        result = [t for t in result if matches_deadline(t, d)]

    if category.strip():
        c = category.strip().lower()
        result = [t for t in result if str(t.get("category", "")).lower() == c]

    if completed.strip().lower() in ("true", "false"):
        want = completed.strip().lower() == "true"
        result = [t for t in result if bool(t.get("completed", False)) == want]

    return ok(tasks=result, count=len(result))







@mcp.tool(title="Get Stats")
def get_stats(client_id: str = DEFAULT_CLIENT):
    data = load_data()
    if "clients" not in data:
        data["clients"] = {}
    ensure_client(data, client_id)
    return ok(stats=data["clients"][client_id]["stats"])


if __name__ == "__main__":
    mcp.run()
