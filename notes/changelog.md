# Changelog - Markdown Explorer MCP

All notable changes to the `md_explorer_mcp` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-02-28
### Added
- Added support for recursive directory scanning to find Markdown files in subfolders.
- New tool `search_markdown` to search for specific text within all exposed markdown files.
- Added YAML frontmatter parsing capabilities to extract metadata from files.

### Changed
- Improved error handling when a requested file is deleted while the server is running.
- Restructured internal modules to separate `security.py` from `resources.py`.

## [0.2.1] - 2026-01-15
### Fixed
- Fixed an issue where files with uppercase extensions (`.MD`) were ignored.
- Resolved a path traversal vulnerability in `read_resource` where `../` could be used to escape the root directory.

## [0.2.0] - 2025-12-10
### Added
- Implemented file watching. The server now notifies the client automatically when a markdown file changes on disk.
- Added support for `.mdx` files in addition to standard `.md`.

## [0.1.0] - 2025-11-01
### Added
- Initial proof-of-concept release.
- Basic MCP server implementation using stdio.
- Exposes all `.md` files in a flat directory as read-only text resources.
