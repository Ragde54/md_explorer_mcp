import re

from mcp.shared.exceptions import McpError
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, ErrorData

from md_explorer_mcp.config import NOTES_PATH


def list_files() -> list[dict[str, str | int]]:
    """
    List all markdown files in the notes directory.
    Returns a list of files with their filename and size in bytes.
    Use this tool first to discover what notes are available before reading them.
    """
    try:
        return [
            {"filename": file.name, "size_bytes": file.stat().st_size}
            for file in sorted(NOTES_PATH.glob("*.md"), key=lambda x: x.name)
        ]
    except Exception as e:
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=str(e)))


def search_files(search_pattern: str) -> list[dict[str, str | list[str]]]:
    """
    Search all markdown files for lines matching a regex pattern.
    Returns a list of files with their matching lines.
    Pattern must be a valid Python regex string.
    Use this tool to find specific content across all notes without reading each file individually.
    Example patterns:
    - 'neural networks?' matches 'neural network' or 'neural networks'
    - 'TODO|FIXME' matches lines containing either word
    - '^#' matches all markdown headings
    """

    # Validate regex
    try:
        compiled_pattern = re.compile(search_pattern)
    except re.error:
        raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid regex: {search_pattern}"))

    search_result: list[dict[str, str | list[str]]] = []
    for file in sorted(NOTES_PATH.glob("*.md"), key=lambda x: x.name):
        try:
            matches: list[str] = []
            content = file.read_text()
            for line in content.splitlines():
                if compiled_pattern.search(line):
                    matches.append(line)
            if matches:
                search_result.append({"filename": file.name, "matches": matches})
        except OSError:
            continue  # skip unreadable files

    return search_result
