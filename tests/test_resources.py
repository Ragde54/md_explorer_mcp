import pytest
from mcp.shared.exceptions import McpError
from md_explorer_mcp.resources import get_note

def test_get_note(tmp_path, monkeypatch):
    # Happy path
    monkeypatch.setattr("md_explorer_mcp.resources.notes_path", tmp_path)
    note_file = tmp_path / "test_note.md"
    note_file.write_text("# Test Note")
    result = get_note(note_file.name)
    assert result == "# Test Note"

def test_get_note_nonexistent(tmp_path, monkeypatch):
    # Non-existent file
    monkeypatch.setattr("md_explorer_mcp.resources.notes_path", tmp_path)
    with pytest.raises(McpError):
        get_note("non_existent_note.md")

def test_get_note_outside_root(tmp_path, monkeypatch):
    # Path traversal attack
    monkeypatch.setattr("md_explorer_mcp.resources.notes_path", tmp_path)
    with pytest.raises(McpError):
        get_note("../../etc/passwd")

def test_get_note_blocks_non_markdown(tmp_path, monkeypatch):
    # No md extension
    monkeypatch.setattr("md_explorer_mcp.resources.notes_path", tmp_path)
    with pytest.raises(McpError):
        get_note("test_note.txt")