# MCP Multi-User To Do List

This project is a **Multi-user To-Do List backend** built using the **Model Context Protocol (MCP)** and Python
Each user (client) has their own task list and stats, and you can interact with it from an MCP-compatible AI client like Claude Desktop.

---

#  Features

## Core Task Features

| Feature | Description |
|--------|-------------|
Add Task | Create a new task for a specific user |
List Tasks | Display tasks in a clean table format |
Edit Task | Modify an existing task’s title |
Delete Task | Remove a task permanently |
Filter Tasks | View tasks by status (completed / pending) |
Complete Task | Mark a task as done |

---

## Data & Architecture

| Feature | Description |
|--------|-------------|
Persistent Storage | Tasks are saved in `data.json` and persist between sessions |
Multi-User Support | Each `client_id` has an isolated task list |
Completion Analytics | Track totals, completed tasks, and completion rate |

---

## AI Integration

| Feature | Description |
|--------|-------------|
Claude MCP Integration | Claude can control the task manager through MCP tools |

---

