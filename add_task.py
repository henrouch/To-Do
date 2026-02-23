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
