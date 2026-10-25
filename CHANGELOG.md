# Changelog

All notable changes to **Cloud Ops MCP** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.2.0] - 2026-10-25

### Added
- **3-Layer Workflow Engine**: Structured Snapshot, Filter, and Deep Audit workflows for ultra-fast cloud operations analysis.
- **Multi-IDE Compatibility**: Full protocol compliance for Claude Code, Cursor, OpenAI Codex CLI, Google Antigravity, OpenCode, and Windsurf/Cline.
- **Production CI Workflow**: Automated tests and self-test verification pipeline via GitHub Actions.
- **Docker Support**: Containerized deployment with Python 3.12-slim base image.

### Improved
- Memory footprint optimization during large resource snapshot evaluations.
- Security boundary enforcement with zero-telemetry disclosure compliance.

## [v1.1.0] - 2026-08-15

### Added
- Enhanced resource metrics inspection tools for Kubernetes and AWS EC2 workloads.
- Dynamic filtering capabilities based on resource tags and severity levels.

### Fixed
- Resolved edge case in tool response JSON serialization under Python 3.12.

## [v1.0.0] - 2026-05-10

### Added
- Initial public release of Cloud Ops Model Context Protocol (MCP) server.
- Basic cloud infrastructure snapshot and health status checking tools.
