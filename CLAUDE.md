# CLAUDE.md - Cloud Ops MCP Guidelines

## Overview
`cloud-ops-mcp` is an ultra-professional Model Context Protocol (MCP) server designed for cloud infrastructure auditing, resource filtering, and snapshot management.

## Development Commands
- **Run Server:** `python3 cloud_ops_mcp.py`
- **Self Test:** `python3 cloud_ops_mcp.py --self-test`
- **Docker Build:** `docker build -t cloud-ops-mcp .`
- **Docker Run:** `docker run -it --rm cloud-ops-mcp`

## Code Style & Architecture
- **Python Version:** 3.10+ (Tested on Python 3.12-slim)
- **Architecture:** 3-Layer Workflow Architecture:
  1. **Snapshot Layer:** Fast initial infrastructure state capture.
  2. **Filter Layer:** Target resource scoping by severity, tags, or status.
  3. **Deep Audit Layer:** Detailed diagnostic analysis of specific resources.
- **Zero Telemetry:** Strict local-only processing. No outbound telemetry or external data collection.
