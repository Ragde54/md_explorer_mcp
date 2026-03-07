from pathlib import Path


class SecurityError(Exception):
    pass


def gatekeeper(root_directory: Path, filename: str) -> Path:
    """
    Validate and resolve a filename against a root directory.
    Raises SecurityError if the file is outside the root,
    not a .md file, or does not exist.
    """
    root = root_directory.resolve()
    file = (root / filename).resolve()

    if not file.is_relative_to(root):
        raise SecurityError(f"Access denied: {filename}")
    if file.suffix != ".md":
        raise SecurityError(f"Access denied: {filename}")
    if not file.is_file():
        raise SecurityError(f"Access denied: {filename}")
    return file
