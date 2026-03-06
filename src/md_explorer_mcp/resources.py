from md_explorer_mcp.server import mcp
from md_explorer_mcp.security import gatekeeper, SecurityError
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

notes_dir = Path(os.getenv("NOTES_DIR"))
if not notes_dir:
    raise ValueError("NOTES_DIR environment variable is not set")
notes_path = Path(notes_dir).expanduser().resolve()

@mcp.resource("notes:///{filename}")
def get_note(filename: str) -> str:
    """Get the content of a markdown file."""
    try:
        file_path = gatekeeper(notes_path, filename)
        return file_path.read_text()
    except SecurityError as e:
        return str(e)
