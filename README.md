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

# Model Context Protocol Setup Guide

## Installation

- Install the MCP Python package with pip:
  ```bash
  pip install "mcp[cli]"
  ```

- Install the `requests` package:
  ```bash
  pip install requests
  ```

- Download the Claude Desktop client.

---

## Python Setup

- In your Python code, import the MCP library:
  ```python
  from mcp.server.fastmcp import FastMCP
  ```
  Read the documentation on how to use this class.

- Define a tool for the service:
  ```python
  @mcp.tool(title="My Task")
  ```

---

# MCP Todo Server — Complete Setup Guide (Mac & Windows)

This guide walks you through creating a local **Todo MCP server**, connecting it to **Claude Desktop**, and verifying that it works. Follow every step in order.
## 📁 Step 1 — Create a New Project Folder
### Mac / Linux
```bash
cd ~
mkdir todo_project
cd todo_project
````

### Windows (PowerShell)

```powershell
cd $HOME
mkdir todo_project
cd todo_project
```

## Step 2 — Create and Activate a Virtual Environment

### Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

You must see:

```text
(.venv)
```

If you see it → the virtual environment is active 

## Step 3 — Install MCP

Install MCP inside the virtual environment:

```bash
pip install "mcp[cli]"
```

Verify installation:

```bash
mcp --help
```

If help text appears → MCP installed correctly 

## Step 4 — Add `server.py` to the Project Folder

Put your `server.py` file inside:

```
todo_project/
```

Make sure the filename is exactly:

```
server.py
```

## Step 5 — Test the Server Manually (One Time)

```bash
python server.py
```

If there are **no red errors**, press:

```
CTRL + C
```

Server works 

## Step 6 — Connect the Server to Claude Desktop

### Open the Claude Config Folder

#### Mac

```bash
open ~/Library/Application\ Support/Claude/
```

#### Windows (File Explorer)

Navigate to:

```
C:\Users\YOUR_USERNAME\AppData\Roaming\Claude\
```

Create or open:

```
claude_desktop_config.json
```

Paste the following and replace `YOUR_USERNAME` with your actual username.

### Mac Config

```json
{
  "mcpServers": {
    "todo": {
      "command": "/Users/YOUR_USERNAME/todo_project/.venv/bin/python",
      "args": ["-u", "/Users/YOUR_USERNAME/todo_project/server.py"]
    }
  }
}
```

### Windows Config

```json
{
  "mcpServers": {
    "todo": {
      "command": "C:\\Users\\YOUR_USERNAME\\todo_project\\.venv\\Scripts\\python.exe",
      "args": ["-u", "C:\\Users\\YOUR_USERNAME\\todo_project\\server.py"]
    }
  }
}
```

To find your username:

### Mac / Linux

```bash
whoami
```

### Windows

```powershell
whoami
```

Save the file.

## Step 7 — Restart Claude Desktop

1. Close Claude Desktop completely
2. Reopen it
3. Wait about 10 seconds

## Step 8 — Enable the MCP Connector

1. Start a **new chat**
2. Click ➕
3. Click **Connectors**
4. Click **todo**
5. Choose **Always allow**

## Step 9 — Final Test

In Claude, type exactly:

```
Add a task called My first task for client {randomname}
```

Then:

```
List tasks
```

You should see your task 





## Verify

Prompt Claude Desktop to list the available actions it has.

---

## Resources

- Python SDK GitHub:  
  https://github.com/modelcontextprotocol/python-sdk

- MCP Documentation:  
  https://modelcontextprotocol.io/docs/getting-started/intro

