# Architecture of Markdown Explorer MCP

The `md_explorer_mcp` is designed to provide secure, structured access to a local directory containing Markdown files for LLM clients via the Model Context Protocol (MCP).

## Core Components

1. **MCP Server Core (`src/md_explorer_mcp/server.py`)**
   - Implements the base MCP protocol handling.
   - Manages communication over stdio with the connected MCP client (e.g., Claude Desktop).

2. **Resource Manager (`src/md_explorer_mcp/resources.py`)**
   - Discovers and exposes `.md` files as MCP resources.
   - Handles file path resolution and URI formatting (`file://...`).
   - Caches file metadata to improve listing performance.

3. **Markdown Handler (`src/md_explorer_mcp/markdown.py`)**
   - Responsible for reading and basic parsing of markdown files.
   - Can extract frontmatter and split large markdown documents into manageable chunks if requested.

4. **Security Module (`src/md_explorer_mcp/security.py`)**
   - Enforces path traversal protections.
   - Ensures the server only exposes files within the configured root directory.
   - Prevents access to hidden files (`.env`, `.git`, etc.) even if they end in `.md`.

## Request Flow
1. **List Resources**: The client requests available resources. The `Resource Manager` scans the allowed directory and returns a list of URIs for all discovered markdown files.
2. **Read Resource**: The client requests the content of a specific URI.
3. The `Security Module` validates the URI against the allowed root path.
4. If valid, the `Markdown Handler` reads the file and returns the text content to the client over the MCP session.
