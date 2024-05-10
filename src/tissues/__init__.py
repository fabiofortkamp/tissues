"""tissues - A tool to check if the number of issues has increased."""

import subprocess
import sys
from typing import Annotated, List

import typer

DEFAULT_COMMAND_ARGS = ["ruff", "check", "--fix", "--quiet", "--exit-zero"]


def main(
    path: Annotated[List[str], typer.Argument(help="Path to the file(s) to check")],
    command: Annotated[str, typer.Option(help="The command to run")] = " ".join(
        DEFAULT_COMMAND_ARGS
    ),
):
    """Run given command and check if the number of issues has increased."""
    command_to_run = command.split() + path
    command_process = subprocess.run(command_to_run, capture_output=True, text=True)

    if command_process.stderr != "":
        print("Could not run linter command:", file=sys.stderr)
        print(command_process.stderr, file=sys.stderr)
        raise typer.Exit(1)

    ## count the number of lines in the output buffer
    command_output = command_process.stdout
    lines = command_output.split("\n")
    # remove empty strings from the list
    lines = [line for line in lines if line]

    n_issues_new = len(lines)
    if command_output:
        print(command_output, file=sys.stdout)

    issues_filename = f".{command.split()[0]}-issues"
    # read the number of issues from the previous run
    try:
        with open(issues_filename) as f:
            n_issues_old = int(f.read())
    except Exception:
        n_issues_old = 0

    # write the number of issues from the current run
    with open(issues_filename, "w") as f:
        f.write(str(n_issues_new))

    # if the number of issues has increased, print the output and return 1
    if n_issues_new >= n_issues_old:
        return 1

    return 0
