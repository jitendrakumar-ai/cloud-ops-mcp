FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY cloud_ops_mcp.py .

RUN pip install --no-cache-dir -e . || true

ENTRYPOINT ["python3", "cloud_ops_mcp.py"]
