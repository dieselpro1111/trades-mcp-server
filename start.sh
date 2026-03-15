#!/bin/bash
# Railway sets PORT dynamically; default to 8000 for local dev
PORT="${PORT:-8000}"
exec fastmcp run server.py:mcp --transport http --port "$PORT" --host 0.0.0.0
