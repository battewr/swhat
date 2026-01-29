# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.2] - 2026-01-28

### Refactored

- Extracted template content from `templates.py` into `src/swhat/templates/` package
  - `spec_template.py`, `checklist_template.py`, `plan_template.py`
- Renamed `templates.py` → `template_cli.py` (registry and lookup only)
- Renamed `init.py` → `init_cli.py` (avoid potential conflicts with `__init__.py`)

## [0.3.1] - 2026-01-28

### Added

- **Step 0 confirmation**: Feature workflow skills now ask "Would you like to proceed with a detailed specification attempt?" before starting
- If user declines, workflow proceeds with original request without specification

## [0.3.0] - 2026-01-28

### Added

- **Plan command**: New `/swhat.plan` (Claude) and `/swhat-plan` (Roo) commands to create implementation plans from specifications
- **Plan workflow**: Multi-phase planning with prerequisite spec check, context loading, research, and design phases

### Changed

- **Option 2 now functional**: "Help me map out how to accomplish this" now invokes the plan command instead of showing "Coming Soon"
- **Refactored command storage**: Extracted all command/skill strings from `init.py` into separate files under `src/swhat/commands/` for better maintainability

### Refactored

- Created `src/swhat/commands/` package with individual files:
  - `claude_specify_command.py`, `roo_specify_command.py`
  - `claude_plan_command.py`, `roo_plan_command.py`
  - `claude_feature_skill.py`, `roo_feature_skill.py`
- Reduced `init.py` from ~1450 lines to ~115 lines

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
