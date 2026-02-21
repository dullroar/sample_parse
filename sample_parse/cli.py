"""Command-line interface for the sample parsing utility."""

import json
import re

import click

from .common import parse_string_to_typed


@click.group()
@click.version_option()
def cli():
    """Sample: A utility for parsing strings to their intended Python types."""


@cli.command()
@click.argument("value")
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output the result as JSON (if possible).",
)
def parse(value: str, output_json: bool):
    """Parse a string value to its intended type.

    Examples:
        sample parse "123"
        sample parse '{"key": "value"}'
        sample parse "[1, 2, 3]"
        sample parse "3.14"
        sample parse "/[a-z]+/"
        sample parse "hello"
    """
    result = parse_string_to_typed(value)

    if output_json:
        try:
            # Try to convert to JSON-serializable format
            if isinstance(result, re.Pattern):
                output = {"type": "regex", "pattern": result.pattern}
            else:
                output = result
            click.echo(json.dumps(output, indent=2))
        except TypeError as e:
            click.echo(f"Error: Cannot serialize result to JSON: {e}", err=True)
    else:
        # Display the result with type info
        type_name = type(result).__name__
        if isinstance(result, re.Pattern):
            click.echo(f"Pattern: /{result.pattern}/")
        else:
            click.echo(f"{type_name}: {repr(result)}")


@cli.command()
@click.argument("values", nargs=-1, required=True)
@click.option("--json", "output_json", is_flag=True, help="Output results as JSON.")
def parse_batch(values, output_json: bool):
    """Parse multiple values at once.

    Example:
        sample parse-batch "123" "3.14" '{"key": "value"}'
    """
    results = []
    for value in values:
        parsed = parse_string_to_typed(value)
        if isinstance(parsed, re.Pattern):
            output_value = f"/{parsed.pattern}/"
        else:
            output_value = parsed
        results.append({
            "input": value,
            "output": output_value,
            "type": type(parsed).__name__
        })

    if output_json:
        click.echo(json.dumps(results, indent=2))
    else:
        for item in results:
            click.echo(f"Input: {item['input']}")
            click.echo(f"  Type: {item['type']}")
            click.echo(f"  Value: {item['output']}")


if __name__ == "__main__":
    cli()
