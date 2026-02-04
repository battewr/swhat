"""Project initialization for swhat.

This module handles the `swhat init` command which sets up a project
for specification-driven development by creating directories and
installing AI agent command files.
"""

from pathlib import Path

import click

from swhat.commands import (
    CLAUDE_SPECIFY_COMMAND,
    ROO_SPECIFY_COMMAND,
    CLAUDE_PLAN_COMMAND,
    ROO_PLAN_COMMAND,
    CLAUDE_FEATURE_SKILL,
    ROO_FEATURE_SKILL,
)


def _write_file(path: Path, content: str, display_path: str) -> None:
    """Write a file and report status."""
    action = "Updated" if path.exists() else "Created"
    path.write_text(content, encoding="utf-8")
    click.echo(f"  {action} {display_path}")


def initialize_project() -> bool:
    """Initialize the current directory for swhat specification workflow.

    Creates:
        - .swhat/ directory for user workspace
        - .claude/commands/swhat.specify.md for Claude Code
        - .claude/commands/swhat.plan.md for Claude Code
        - .claude/skills/swhat-feature-workflow/SKILL.md for Claude Code
        - .roo/commands/swhat-specify.md for Roo
        - .roo/commands/swhat-plan.md for Roo
        - .roo/skills/swhat-feature-workflow/SKILL.md for Roo

    Returns:
        True if initialization succeeded, False otherwise.
    """
    cwd = Path.cwd()

    click.echo("Initializing swhat in current directory...")

    # Create .swhat/ directory
    swhat_dir = cwd / ".swhat"
    if swhat_dir.exists():
        click.echo("  .swhat/ already exists")
    else:
        swhat_dir.mkdir(parents=True, exist_ok=True)
        click.echo("  Created .swhat/")

    # Claude Code: commands
    claude_commands_dir = cwd / ".claude" / "commands"
    claude_commands_dir.mkdir(parents=True, exist_ok=True)
    _write_file(
        claude_commands_dir / "swhat.specify.md",
        CLAUDE_SPECIFY_COMMAND,
        ".claude/commands/swhat.specify.md",
    )
    _write_file(
        claude_commands_dir / "swhat.plan.md",
        CLAUDE_PLAN_COMMAND,
        ".claude/commands/swhat.plan.md",
    )

    # Claude Code: skills
    claude_skill_dir = cwd / ".claude" / "skills" / "swhat-feature-workflow"
    claude_skill_dir.mkdir(parents=True, exist_ok=True)
    _write_file(
        claude_skill_dir / "SKILL.md",
        CLAUDE_FEATURE_SKILL,
        ".claude/skills/swhat-feature-workflow/SKILL.md",
    )

    # Roo: commands (uses dashes, not dots)
    roo_commands_dir = cwd / ".roo" / "commands"
    roo_commands_dir.mkdir(parents=True, exist_ok=True)
    _write_file(
        roo_commands_dir / "swhat-specify.md",
        ROO_SPECIFY_COMMAND,
        ".roo/commands/swhat-specify.md",
    )
    _write_file(
        roo_commands_dir / "swhat-plan.md",
        ROO_PLAN_COMMAND,
        ".roo/commands/swhat-plan.md",
    )

    # Roo: skills
    roo_skill_dir = cwd / ".roo" / "skills" / "swhat-feature-workflow"
    roo_skill_dir.mkdir(parents=True, exist_ok=True)
    _write_file(
        roo_skill_dir / "SKILL.md",
        ROO_FEATURE_SKILL,
        ".roo/skills/swhat-feature-workflow/SKILL.md",
    )

    click.echo("")
    click.echo("Initialization complete!")
    click.echo("")
    click.echo("Commands installed:")
    click.echo("  Claude Code: /swhat.specify <feature description>")
    click.echo("               /swhat.plan")
    click.echo("  Roo:         /swhat-specify <feature description>")
    click.echo("               /swhat-plan")
    click.echo("")
    click.echo("Skills installed (auto-activate on feature requests):")
    click.echo("  swhat-feature-workflow - clarifies requirements before coding")
    return True
