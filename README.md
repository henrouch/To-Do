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
  pip install mcp[cli]
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

## Claude Desktop Configuration

Edit the Claude Desktop configuration in one of the following ways:

- Go to:  
  **Settings → Developer → Edit Config**

**OR**

- Locate the configuration file on your system:

  - **macOS:**  
    `~/Library/Application Support/Claude/claude_desktop_config.json`

  - **Windows:**  
    `%APPDATA%\Claude\claude_desktop_config.json`

---

## Add MCP Server Entry

- Create an entry for `"mcpServers"` in the config file.
- Enter your server configuration information.
- Start your Python program.
- Once configured, Claude Desktop should recognize that the server is running.

---

## Verify

Prompt Claude Desktop to list the available actions it has.

---

## Resources

- Python SDK GitHub:  
  https://github.com/modelcontextprotocol/python-sdk

- MCP Documentation:  
  https://modelcontextprotocol.io/docs/getting-started/intro

