"""CLI entry point for swhat."""

import click


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


if __name__ == "__main__":
    main()
