from fastapi import FastAPI
from fastmcp import FastMCP

app = FastAPI(title="My Existing API")
mcp_server = FastMCP.from_fastapi(app)
