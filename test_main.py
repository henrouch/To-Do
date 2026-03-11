import json
import os
import sys
import types
import importlib
import pytest


# --------- import helper (stubs FastMCP if MCP isn't installed) ---------

def import_todo_module(module_name: str):
    """
    Imports your todo module. If mcp.server.fastmcp isn't installed,
    we stub it so the module imports cleanly.
    """
    try:
        import mcp.server.fastmcp  # noqa: F401
    except Exception:
        fastmcp_mod = types.ModuleType("mcp.server.fastmcp")

        class FastMCPStub:
            def __init__(self, name: str):
                self.name = name

            def tool(self, title=None):
                def deco(fn):
                    return fn
                return deco

            def run(self):
                return None

        fastmcp_mod.FastMCP = FastMCPStub
        sys.modules.setdefault("mcp", types.ModuleType("mcp"))
        sys.modules.setdefault("mcp.server", types.ModuleType("mcp.server"))
        sys.modules["mcp.server.fastmcp"] = fastmcp_mod

    return importlib.import_module(module_name)


# --------- fixtures ---------

@pytest.fixture
def todo(tmp_path, monkeypatch):
    """
    Imports main.py and redirects storage FILE to a temp path.
    """
    mod = import_todo_module("main")
    test_file = tmp_path / "tasks.json"
    monkeypatch.setattr(mod, "FILE", str(test_file), raising=False)
    monkeypatch.setattr(mod, "DATA_DIR", str(tmp_path), raising=False)
    return mod


def read_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


# ---------------- add_task (3 tests) ----------------

def test_add_task_success_and_persists(todo):
    res = todo.add_task("Buy milk")
    assert res["ok"] is True
    assert res["task"]["id"] == 1

    data = read_json(todo.FILE)
    tasks = data["clients"][todo.DEFAULT_CLIENT]["tasks"]
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Buy milk"


def test_add_task_rejects_blank_title(todo):
    res = todo.add_task("   ")
    assert res["ok"] is False
    assert "title is required" in res["error"]
    assert os.path.exists(todo.FILE) is False


def test_add_task_normalizes_fields(todo):
    res = todo.add_task("  Read  ", description="  ch1  ", deadline=" 2026-03-10 ", category="  HoMeWoRk ")
    t = res["task"]
    assert t["title"] == "Read"
    assert t["description"] == "ch1"
    assert t["deadline"] == "2026-03-10"
    assert t["category"] == "homework"


# ---------------- edit_task (3 tests) ----------------

def test_edit_task_updates_fields(todo):
    todo.add_task("Old", description="a", deadline="2026-01-01", category="work")
    res = todo.edit_task(1, new_title="New", new_description="b", new_deadline="2026-02-02", new_category="HOME")
    assert res["ok"] is True
    assert res["task"]["title"] == "New"
    assert res["task"]["category"] == "home"


def test_edit_task_rejects_non_int_id(todo):
    todo.add_task("X")
    res = todo.edit_task("abc", new_title="Y")
    assert res["ok"] is False
    assert "task_id must be an integer" in res["error"]


def test_edit_task_not_found(todo):
    todo.add_task("X")
    res = todo.edit_task(999, new_title="Y")
    assert res["ok"] is False
    assert "Task not found" in res["error"]


# ---------------- complete_task (3 tests) ----------------

def test_complete_task_sets_done(todo):
    todo.add_task("X")
    res = todo.complete_task(1, completed=True)
    assert res["ok"] is True
    assert res["task"]["completed"] is True


def test_complete_task_can_uncomplete(todo):
    todo.add_task("X")
    todo.complete_task(1, completed=True)
    res = todo.complete_task(1, completed=False)
    assert res["ok"] is True
    assert res["task"]["completed"] is False


def test_complete_task_not_found(todo):
    res = todo.complete_task(12345, completed=True)
    assert res["ok"] is False
    assert "Task not found" in res["error"]


# ---------------- delete_task (3 tests) ----------------

def test_delete_task_removes_task(todo):
    todo.add_task("A")
    todo.add_task("B")
    res = todo.delete_task(1, was_completed=False)
    assert res["ok"] is True
    assert res["deleted"]["title"] == "A"

    data = read_json(todo.FILE)
    tasks = data["clients"][todo.DEFAULT_CLIENT]["tasks"]
    assert [t["title"] for t in tasks] == ["B"]


def test_delete_task_updates_stats_completed(todo):
    todo.add_task("A")
    res = todo.delete_task(1, was_completed=True)
    assert res["ok"] is True
    assert res["stats"]["completed"] == 1
    assert res["stats"]["failed"] == 0


def test_delete_task_not_found(todo):
    todo.add_task("A")
    res = todo.delete_task(999, was_completed=True)
    assert res["ok"] is False
    assert "Task not found" in res["error"]


# ---------------- list_tasks (3 tests) ----------------

def test_list_tasks_empty_message(todo):
    out = todo.list_tasks()
    assert isinstance(out, str)
    assert "No tasks found" in out


def test_list_tasks_includes_rows(todo):
    todo.add_task("Task 1", deadline="2026-03-05", category="work")
    out = todo.list_tasks()
    assert "ID | Title | Deadline | Category | Status" in out
    assert "1 | Task 1 | 2026-03-05 | work | pending" in out


def test_list_tasks_marks_done(todo):
    todo.add_task("X")
    todo.complete_task(1, completed=True)
    out = todo.list_tasks()
    assert "1 | X | None | None | done" in out


# ---------------- filter_tasks (3 tests) ----------------

def test_filter_tasks_by_deadline(todo):
    todo.add_task("A", deadline="2026-03-01")
    todo.add_task("B", deadline="2026-03-02")
    res = todo.filter_tasks(deadline="2026-03-01")
    assert res["ok"] is True
    assert res["count"] == 1
    assert res["tasks"][0]["title"] == "A"


def test_filter_tasks_by_category(todo):
    todo.add_task("A", category="Work")
    todo.add_task("B", category="home")
    res = todo.filter_tasks(category="work")
    assert res["ok"] is True
    assert res["count"] == 1
    assert res["tasks"][0]["title"] == "A"


def test_filter_tasks_by_completed(todo):
    todo.add_task("A")
    todo.add_task("B")
    todo.complete_task(2, completed=True)

    res = todo.filter_tasks(completed="true")
    assert res["ok"] is True
    assert res["count"] == 1
    assert res["tasks"][0]["title"] == "B"


# ---------------- get_stats (3 tests) ----------------

def test_get_stats_starts_zero(todo):
    res = todo.get_stats()
    assert res["ok"] is True
    assert res["stats"] == {"completed": 0, "failed": 0}


def test_get_stats_reflects_deletes(todo):
    todo.add_task("A")
    todo.add_task("B")
    todo.delete_task(1, was_completed=True)
    todo.delete_task(2, was_completed=False)

    res = todo.get_stats()
    assert res["stats"]["completed"] == 1
    assert res["stats"]["failed"] == 1


def test_get_stats_other_client(todo):
    res = todo.get_stats(client_id="other_client")
    assert res["ok"] is True
    assert res["stats"] == {"completed": 0, "failed": 0}
