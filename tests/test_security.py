from pathlib import Path

import pytest

from md_explorer_mcp.security import SecurityError, gatekeeper


def test_happy_path(tmp_path: Path) -> None:
    # Happy path
    root = tmp_path
    filename = "notes.md"
    test_file = root / filename
    test_file.write_text("# Hello")  # This makes .exists() and .is_file() True
    result = gatekeeper(root, filename)

    assert result == test_file.resolve()


def test_blocked_outside_root(tmp_path: Path) -> None:
    # Directory traversal attack
    root = tmp_path / "app_data"
    root.mkdir()
    bad_filename = "../../etc/passwd"

    with pytest.raises(SecurityError, match="Access denied"):
        gatekeeper(root, bad_filename)


def test_blocked_wrong_extension(tmp_path: Path) -> None:
    # Wrong file extension
    root = tmp_path
    secret_file = root / "script.py"
    secret_file.write_text("print('virus')")

    with pytest.raises(SecurityError, match="Access denied"):
        gatekeeper(root, "script.py")


def test_blocked_non_existent(tmp_path: Path) -> None:
    # Non-existent file
    with pytest.raises(SecurityError, match="Access denied"):
        gatekeeper(tmp_path, "ghost.md")


def test_blocked_directory(tmp_path: Path) -> None:
    # Directory instead of file
    root = tmp_path
    dir_path = tmp_path / "app_data"
    dir_path.mkdir()

    with pytest.raises(SecurityError, match="Access denied"):
        gatekeeper(root, "app_data")
