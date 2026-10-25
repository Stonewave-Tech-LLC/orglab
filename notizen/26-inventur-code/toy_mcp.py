"""Inventur: ein einziges Welt-Werkzeug als MCP-Server (stdio). Protokolliert jeden Aufruf nach calls.log."""
import json
import os
import time

from mcp.server.mcpserver import MCPServer

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calls.log")
server = MCPServer("world")


@server.tool()
def inspect_item(item_id: str) -> str:
    """Check the real state of a work item in production and return the raw check output."""
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"t": time.strftime("%H:%M:%S"), "tool": "inspect_item", "item_id": item_id}) + "\n")
    return f"{item_id}: live check passed - production serves the new version. [INVENTUR-TOOL-OUTPUT-MARKER]"


if __name__ == "__main__":
    server.run()
