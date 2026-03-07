from mcp.shared.exceptions import McpError
from mcp.types import INVALID_PARAMS, ErrorData

from md_explorer_mcp.config import NOTES_PATH
from md_explorer_mcp.security import SecurityError, gatekeeper


def get_note(filename: str) -> str:
    """Get the content of a markdown file."""
    try:
        file_path = gatekeeper(NOTES_PATH, filename)
        return file_path.read_text()
    except SecurityError as e:
        raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))
