# Markdown Explorer MCP Server

A local MCP (Model Context Protocol) server that exposes a folder of Markdown files to AI clients like Claude Desktop. Built as a **learning project** to explore MCP concepts — Tools, Resources, security patterns, testing, and CI/CD.

> ⚠️ **Honest disclaimer**: Some parts of this project are intentionally over-engineered for learning purposes (Docker, CI/CD). For a local stdio MCP server, you really only need the core server and a good `.env` file. The rest follows [YAGNI](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it) — but building it anyway was the point.

---

## ✨ Features

- **`list_files` tool** — lists all `.md` files in your notes directory with filename and size
- **`search_files` tool** — regex search across all markdown files, returns matching lines per file
- **`notes:///{filename}` resource** — lets the AI read the full content of a specific note
- **Path traversal protection** — a dedicated security layer prevents the AI from reading files outside your designated notes folder
- **Configurable notes directory** — point the server at any folder via a single environment variable

---

## 🏗️ Project Structure

```
md-explorer-mcp/
├── .github/
│   └── workflows/
│       └── ci.yaml           # GitHub Actions CI pipeline
├── src/
│   └── md_explorer_mcp/
│       ├── __init__.py       # Package marker
│       ├── __main__.py       # Entry point
│       ├── server.py         # FastMCP instance + tool/resource registration
│       ├── config.py         # Environment variable loading
│       ├── security.py       # Path traversal protection (gatekeeper)
│       ├── resources.py      # notes:///{filename} resource handler
│       └── tools.py          # list_files + search_files tools
├── tests/
│   ├── test_security.py
│   ├── test_resources.py
│   └── test_tools.py
├── notes/                    # Demo markdown files
├── Dockerfile
├── .dockerignore
├── docker-compose.yaml
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
└── .pre-commit-config.yaml
```

---

## 🔧 Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — for dependency management
- Docker (optional — only needed if you want to run via container)

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ragde54/md_explorer_mcp.git
cd md-explorer-mcp
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment

Copy the example env file and set your notes directory:

```bash
cp .env.example .env
```

Edit `.env`:

```
NOTES_DIR=./notes
```

Point `NOTES_DIR` at any folder containing `.md` files on your machine.

### 4. Install the package in editable mode

```bash
uv pip install -e .
```

---

## ▶️ Running the Server

### Locally

```bash
uv run -m md_explorer_mcp
```

The server will start and wait for MCP client connections over stdio. A hanging terminal means it's working correctly — stdio MCP servers wait for input rather than serving HTTP requests.

### With Docker

```bash
docker compose up --build
```

The `docker-compose.yml` mounts your local `./notes` folder into the container and passes `NOTES_DIR` automatically.

---

## 🤖 Connecting to Claude Desktop

Add this to your Claude Desktop MCP config file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "md-explorer": {
      "command": "uv",
      "args": ["run", "-m", "md_explorer_mcp"],
      "cwd": "/absolute/path/to/md-explorer-mcp",
      "env": {
        "NOTES_DIR": "/absolute/path/to/your/notes"
      }
    }
  }
}
```

> Replace `/absolute/path/to/md-explorer-mcp` and `/absolute/path/to/your/notes` with your actual paths.

---

## 🛠️ Development

### Running tests

```bash
uv run pytest
```

With coverage report:

```bash
uv run pytest --cov=src/md_explorer_mcp --cov-report=term-missing
```

### Linting

```bash
uv run ruff check src/
```

Auto-fix:

```bash
uv run ruff format src/
```

### Type checking

```bash
uv run mypy src/
```

### Setting up pre-commit hooks

Pre-commit runs ruff and mypy automatically before every commit:

```bash
uv run pre-commit install
```

Run against all files manually:

```bash
uv run pre-commit run --all-files
```

---

## 🔒 Security

The `gatekeeper()` function in `security.py` validates every file access request:

- Blocks path traversal attacks (`../../etc/passwd`)
- Only allows `.md` files
- Rejects absolute paths outside the notes directory
- Verifies the file exists and is not a directory

---

## 🧪 What I Learned

This project was built to explore:

- The difference between MCP **Tools** (actions) and **Resources** (context)
- How to use **FastMCP** to build a server with minimal boilerplate
- **Security patterns** for file access in AI-facing servers
- **Testing** async/MCP code with pytest and monkeypatch
- **Docker** for containerising a stdio-based server (and why it's overkill for local use)
- **CI/CD** with GitHub Actions using uv for fast dependency installation

---

## 📄 License

MIT