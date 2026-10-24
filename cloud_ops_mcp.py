import sys
import json
import os
import socket
import platform
import subprocess
import re

def handle_request(request):
    method = request.get("method")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "cloud-ops-mcp",
                    "version": "1.0.0"
                }
            }
        }

    elif method == "notifications/initialized":
        return None

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "system_health_snapshot",
                        "description": "Capture system CPU, memory, disk usage, and host details.",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "check_port_status",
                        "description": "Check whether specific TCP ports are open or listening.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "host": {"type": "string", "default": "127.0.0.1"},
                                "ports": {"type": "array", "items": {"type": "integer"}, "default": [80, 443, 22, 8080, 5432]}
                            }
                        }
                    },
                    {
                        "name": "audit_env_secrets",
                        "description": "Audit environment variables and text for potential exposed secret keys or tokens.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "env_content": {"type": "string", "description": "Optional raw .env file string to analyze."}
                            }
                        }
                    },
                    {
                        "name": "analyze_log_file",
                        "description": "Parse log text or log files for errors, warnings, and stack traces.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "log_path": {"type": "string"},
                                "log_text": {"type": "string"}
                            }
                        }
                    },
                    {
                        "name": "inspect_docker_containers",
                        "description": "Inspect active Docker containers, statuses, ports, and image tags.",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        }

    elif method == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "system_health_snapshot":
            res = system_health_snapshot()
        elif tool_name == "check_port_status":
            res = check_port_status(args.get("host", "127.0.0.1"), args.get("ports", [80, 443, 22, 8080, 5432]))
        elif tool_name == "audit_env_secrets":
            res = audit_env_secrets(args.get("env_content"))
        elif tool_name == "analyze_log_file":
            res = analyze_log_file(args.get("log_path"), args.get("log_text"))
        elif tool_name == "inspect_docker_containers":
            res = inspect_docker_containers()
        else:
            res = {"error": f"Unknown tool: {tool_name}"}

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": "Method not found"}
    }

def system_health_snapshot():
    info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "os_name": os.name,
    }
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        info["disk_total_gb"] = round(total / (1024**3), 2)
        info["disk_used_gb"] = round(used / (1024**3), 2)
        info["disk_free_gb"] = round(free / (1024**3), 2)
    except Exception as e:
        info["disk_error"] = str(e)
    return info

def check_port_status(host="127.0.0.1", ports=[80, 443, 22, 8080, 5432]):
    results = {}
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        status = sock.connect_ex((host, int(port)))
        results[str(port)] = "OPEN" if status == 0 else "CLOSED"
        sock.close()
    return {"host": host, "port_statuses": results}

def audit_env_secrets(env_content=None):
    findings = []
    patterns = [
        (r'(?i)(api[_-]?key|secret|password|auth[_-]?token|private[_-]?key)\s*=\s*[\'"]?([^\s\'"]+)[\'"]?', "High Severity Secret"),
        (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token"),
        (r'sk-[a-zA-Z0-9]{32,}', "OpenAI API Key"),
        (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID")
    ]
    data_to_scan = env_content if env_content else "\n".join([f"{k}={v}" for k, v in os.environ.items()])
    for line in data_to_scan.splitlines():
        for pattern, desc in patterns:
            match = re.search(pattern, line)
            if match:
                masked = line[:10] + "..." if len(line) > 10 else line
                findings.append({"description": desc, "sample": masked})
    return {"findings_count": len(findings), "findings": findings}

def analyze_log_file(log_path=None, log_text=None):
    content = ""
    if log_path and os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    elif log_text:
        content = log_text
    else:
        return {"error": "No log source provided or file does not exist."}
    lines = content.splitlines()
    errors = [l for l in lines if "ERROR" in l or "CRITICAL" in l or "Exception" in l]
    warnings = [l for l in lines if "WARN" in l]
    return {
        "total_lines": len(lines),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "sample_errors": errors[:5],
        "sample_warnings": warnings[:5]
    }

def inspect_docker_containers():
    try:
        res = subprocess.run(["docker", "ps", "--format", "{{.ID}}|{{.Image}}|{{.Status}}|{{.Ports}}"], capture_output=True, text=True)
        if res.returncode != 0:
            return {"status": "Docker not available or not running", "details": res.stderr.strip()}
        containers = []
        for line in res.stdout.strip().splitlines():
            if line:
                cid, img, status, ports = line.split("|")
                containers.append({"container_id": cid, "image": img, "status": status, "ports": ports})
        return {"containers_count": len(containers), "containers": containers}
    except Exception as e:
        return {"error": str(e)}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            if res:
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
