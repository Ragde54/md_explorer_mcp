# MCP Example Usage

This document outlines how an AI client (like Claude) can utilize the `md_explorer_mcp` server to read and interact with your markdown notes.

## 1. Listing Available Markdown Files

The client will automatically call the `resources/list` endpoint to discover files.

**Client Request (Internal MCP):**
```json
{
  "method": "resources/list",
  "params": {}
}
```

**Server Response:**
```json
{
  "resources": [
    {
      "uri": "file:///path/to/notes/architecture.md",
      "name": "architecture.md",
      "mimeType": "text/markdown"
    },
    {
      "uri": "file:///path/to/notes/daily/2026-03-05.md",
      "name": "2026-03-05.md",
      "mimeType": "text/markdown"
    }
  ]
}
```

## 2. Reading a File

When you ask Claude, "Can you summarize the architecture document?", it will use the `resources/read` endpoint.

**Client Request:**
```json
{
  "method": "resources/read",
  "params": {
    "uri": "file:///path/to/notes/architecture.md"
  }
}
```

**Server Response:**
```json
{
  "contents": [
    {
      "uri": "file:///path/to/notes/architecture.md",
      "mimeType": "text/markdown",
      "text": "# Architecture of Markdown Explorer MCP\n\nThis document..."
    }
  ]
}
```

## 3. Using Tools

If the server implements the optional search tool, the LLM can use it to find specific notes.

**Client asks:** "Find all notes mentioning 'FastAPI'."
**Tool Call:** `search_markdown(query="FastAPI")`
