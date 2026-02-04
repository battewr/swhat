"""CLI entry point for swhat."""

import sys

import click

from swhat.init_cli import initialize_project
from swhat.template_cli import get_template, list_templates


@click.group(invoke_without_command=True)
@click.version_option(
    package_name="swhat", prog_name="swhat", message="%(prog)s, version %(version)s"
)
@click.option("-h", "--help", is_flag=True, help="Show this message and exit.")
@click.pass_context
def main(ctx: click.Context, help: bool) -> None:
    """swhat - Specification-driven development CLI

    Transform natural language feature descriptions into AI-implementable
    execution plans.
    """
    if help or ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.argument("name", required=False, default=None)
@click.option("--list", "-l", "list_flag", is_flag=True, help="List available templates.")
def template(name: str | None, list_flag: bool) -> None:
    """Output a specification template.

    If NAME is provided, outputs the template content to stdout.
    If no NAME is provided or --list is used, lists available templates.

    Examples:

        swhat template specification

        swhat template specification-checklist

        swhat template --list
    """
    # Show list if --list flag or no name provided
    if list_flag or name is None or name.strip() == "":
        click.echo("Available templates:")
        for template_name, description in list_templates():
            click.echo(f"  {template_name:<25} {description}")
        return

    # Look up template by name (case-insensitive)
    result = get_template(name)
    if result is None:
        click.echo(f"Error: Template '{name}' not found.", err=True)
        click.echo("", err=True)
        click.echo("Available templates:", err=True)
        for template_name, description in list_templates():
            click.echo(f"  {template_name:<25} {description}", err=True)
        sys.exit(1)

    # Output template content to stdout
    content, _ = result
    click.echo(content)


@main.command()
def init() -> None:
    """Initialize the current directory for swhat specification workflow.

    Creates the .swhat/ directory and installs AI agent command files
    to .claude/commands/ and .roo/commands/.

    Examples:

        swhat init

        cd /path/to/project && swhat init
    """
    success = initialize_project()
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
