from pathlib import Path

import pytest
from mcp.shared.exceptions import McpError
from md_explorer_mcp.resources import get_note
from pytest import MonkeyPatch


def test_get_note(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    # Happy path
    monkeypatch.setattr("md_explorer_mcp.resources.NOTES_PATH", tmp_path)
    note_file = tmp_path / "test_note.md"
    note_file.write_text("# Test Note")
    result = get_note(note_file.name)
    assert result == "# Test Note"


def test_get_note_nonexistent(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    # Non-existent file
    monkeypatch.setattr("md_explorer_mcp.resources.NOTES_PATH", tmp_path)
    with pytest.raises(McpError):
        get_note("non_existent_note.md")


def test_get_note_outside_root(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    # Path traversal attack
    monkeypatch.setattr("md_explorer_mcp.resources.NOTES_PATH", tmp_path)
    with pytest.raises(McpError):
        get_note("../../etc/passwd")


def test_get_note_blocks_non_markdown(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    # No md extension
    monkeypatch.setattr("md_explorer_mcp.resources.NOTES_PATH", tmp_path)
    with pytest.raises(McpError):
        get_note("test_note.txt")
