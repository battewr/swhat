# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-01-28

### Added

- **Plan template**: New `swhat template plan` command to output implementation plan template
- **AGENTS.md**: Comprehensive AI agent instructions for working on the codebase
- **Next Steps workflow**: After successful specification, users are presented with options to iterate, map out implementation (coming soon), or attempt implementation
- **Clean build scripts documentation**: Added documentation for `clean_build.sh` and `clean_build.ps1` in README

### Changed

- Updated specify commands and skills with new "Next Steps" workflow offering three options after successful specification
- Skills now include Step 6 for handling user selection after specification completion

## [0.1.0] - 2026-01-28

### Added

- **CLI framework**: Initial `swhat` command-line tool using Click
- **Template command**: `swhat template` to output specification templates
  - `specification` - Feature specification template
  - `specification-checklist` - Spec quality validation checklist
- **Init command**: `swhat init` to initialize projects for swhat workflow
  - Creates `.swhat/` workspace directory
  - Installs Claude Code commands and skills
  - Installs Roo Code commands and skills
- **Feature workflow skill**: Auto-triggers on feature requests to clarify requirements before coding
- **Cross-platform support**: Windows PowerShell and Unix bash build scripts
- **CMake build system**: Cross-platform build targets for dev, build, lint, format, and clean

### Documentation

- README with installation and usage instructions
- Constitution defining project principles (CLI-first, UV standards, AI context engineering, YAGNI)
