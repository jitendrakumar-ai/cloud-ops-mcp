# cloud-# ⚡ cloud-ops-mcp

> **Production-ready Python Model Context Protocol (MCP) server for Cloud Telemetry, Port Diagnostics, Log Analysis & Secret Auditing — built for Claude Desktop, Cursor, Windsurf & AI Agents.**

---

## 🌟 Overview

`cloud-ops-mcp` is an open-source, light-weight, stdio-based MCP server built in Python. It provides autonomous AI agents with critical real-time cloud operations, system telemetry, security secret auditing, port checking, log analysis, and Docker container inspection capabilities.

---

## 🛠️ Tools Included

1. **`system_health_snapshot`**
   - Captures real-time CPU core count, disk usage (total, used, free GB), OS platform, and Python environment details.
2. **`check_port_status`**
   - Checks TCP connectivity and listening status for target host and ports (e.g., 80, 443, 22, 8080, 5432).
3. **`audit_env_secrets`**
   - Scans environment variables or custom `.env` string inputs for leaked credentials, API tokens (AWS, GitHub, OpenAI), and passwords.
4. **`analyze_log_file`**
   - Parses log files or text blobs to extract error counts, warning summaries, and stack trace samples.
5. **`inspect_docker_containers`**
   - Queries Docker engine daemon to list running container statuses, images, IDs, and exposed port mappings.

---

## ⚙️ MCP Installation & Setup Configs

### 1. Claude Desktop (`claude_desktop_config.json`)

Add the following block to your `claude_desktop_config.json` (located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "cloud-ops-mcp": {
      "command": "python3",
      "args": [
        "/path/to/cloud-ops-mcp/cloud_ops_mcp.py"
      ]
    }
  }
}
```

### 2. Cursor (`.cursor/mcp.json`)

Add the following to your workspace or global `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "cloud-ops-mcp": {
      "command": "python3",
      "args": [
        "${workspaceFolder}/cloud_ops_mcp.py"
      ]
    }
  }
}
```

---

## 🚀 Quickstart

Run the server manually over stdio:

```bash
python3 cloud_ops_mcp.py
```

---

## 📄 License

MIT License © jitendrakumarvoicex-art (Dhruv)
