import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_notes_dir = os.getenv("NOTES_DIR")
if not _notes_dir:
    raise ValueError("NOTES_DIR environment variable is not set")

NOTES_PATH = Path(_notes_dir).expanduser().resolve()

if not NOTES_PATH.exists():
    raise ValueError(f"NOTES_DIR path does not exist: {NOTES_PATH}")
if not NOTES_PATH.is_dir():
    raise ValueError(f"NOTES_DIR is not a directory: {NOTES_PATH}")
