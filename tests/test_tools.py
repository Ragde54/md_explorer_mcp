from pathlib import Path

import pytest
from mcp.shared.exceptions import McpError
from md_explorer_mcp.tools import list_files, search_files
from pytest import MonkeyPatch

# === List Files tool ===


def test_list_files(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("md_explorer_mcp.tools.NOTES_PATH", tmp_path)
    (tmp_path / "test.md").write_text("test")  # 4 bytes
    assert list_files() == [{"filename": "test.md", "size_bytes": 4}]


def test_list_files_empty_dir(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("md_explorer_mcp.tools.NOTES_PATH", tmp_path)
    assert list_files() == []


def test_list_files_non_md_files(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("md_explorer_mcp.tools.NOTES_PATH", tmp_path)
    (tmp_path / "test.txt").write_text("test")
    (tmp_path / "test2.md").write_text("test")
    assert list_files() == [{"filename": "test2.md", "size_bytes": 4}]


def test_list_files_alpha_sort(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("md_explorer_mcp.tools.NOTES_PATH", tmp_path)
    (tmp_path / "c_note.md").write_text("test")
    (tmp_path / "a_note.md").write_text("test")
    (tmp_path / "b_note.md").write_text("test")
    assert list_files() == [
        {"filename": "a_note.md", "size_bytes": 4},
        {"filename": "b_note.md", "size_bytes": 4},
        {"filename": "c_note.md", "size_bytes": 4},
    ]


# === Search Files tool ===


def test_search_files_valid_pattern(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("md_explorer_mcp.tools.NOTES_PATH", tmp_path)
    (tmp_path / "test.md").write_text("# Heading\nsome content\nanother line")
    (tmp_path / "test2.md").write_text("# Heading\nnew content\nanother line")
    assert search_files("content") == [
        {"filename": "test.md", "matches": ["some content"]},
        {"filename": "test2.md", "matches": ["new content"]},
    ]  # sorted by filename


def test_search_files_no_results(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("md_explorer_mcp.tools.NOTES_PATH", tmp_path)
    (tmp_path / "test.md").write_text("# Heading\nsome content\nanother line")
    assert search_files("non_existent") == []


def test_search_files_invalid_pattern(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    with pytest.raises(McpError):
        search_files("[invalid regex")


def test_search_files_non_md_files(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("md_explorer_mcp.tools.NOTES_PATH", tmp_path)
    (tmp_path / "test.txt").write_text("test txt")
    (tmp_path / "test2.md").write_text("test md")
    assert search_files("test") == [{"filename": "test2.md", "matches": ["test md"]}]
