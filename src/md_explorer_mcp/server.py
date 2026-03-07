from mcp.server.fastmcp import FastMCP

mcp = FastMCP("md-explorer-mcp")

from md_explorer_mcp.resources import get_note  # noqa: E402
from md_explorer_mcp.tools import list_files, search_files  # noqa: E402

mcp.tool()(list_files)
mcp.tool()(search_files)
mcp.resource("notes:///{filename}")(get_note)
