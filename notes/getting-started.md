# Getting Started with md_explorer_mcp

This guide helps you set up the `md_explorer_mcp` server to expose your local Markdown files to an MCP-compatible client like Claude Desktop.

## Prerequisites
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management) or standard `pip`
- Claude Desktop App (or any other MCP client)

## Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/md_explorer_mcp.git
   cd md_explorer_mcp
   ```

2. **Install the package:**
   Using standard pip:
   ```bash
   pip install -e .
   ```
   Or using `uv`:
   ```bash
   uv pip install -e .
   ```

3. **Verify installation:**
   ```bash
   python -m md_explorer_mcp --help
   ```

## Configuring Claude Desktop

To connect Claude Desktop to your local Markdown files, you need to update its configuration file.

1. Open your Claude Desktop configuration file:
   - **macOS/Linux:** `~/.claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the `md_explorer_mcp` server to the `mcpServers` object, specifying the path to the directory containing your markdown files:

   ```json
   {
     "mcpServers": {
       "md-explorer": {
         "command": "python",
         "args": [
           "-m",
           "md_explorer_mcp",
           "--dir",
           "/path/to/your/markdown/notes"
         ]
       }
     }
   }
   ```

3. **Restart Claude Desktop**. It should now automatically discover and be able to read all `.md` files in the specified directory!
