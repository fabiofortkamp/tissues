"""tissues - A tool to check if the number of issues has increased."""

import subprocess
import sys
from typing import Annotated, List, TextIO

import typer

DEFAULT_COMMAND_ARGS = ["ruff", "check", "--fix", "--quiet", "--exit-zero"]


def assemble_command(command: str, arguments: List[str]) -> List[str]:
    """Assemble the command to be run by the process management.

    Args:
        command (str): The command to run. May be composed of multiple words.
        arguments (List[str]): Extra arguments to pass to the command.

    Returns:
        List[str]: The command to be run by the process management.
    """
    return command.split() + arguments


def check_for_errors(process: subprocess.CompletedProcess, output: TextIO) -> None:
    """Check for errors in the process and raise an exception if found.

    Args:
        process (subprocess.CompletedProcess): The process to check for errors.
        output (TextIO): The output stream to write the error message to.
    """
    if process.stderr:
        print("Error running command:", file=output)
        print(process.stderr, file=output)
        raise typer.Exit(1)


def main(
    path: Annotated[List[str], typer.Argument(help="Path to the file(s) to check")],
    command: Annotated[str, typer.Option(help="The command to run")] = " ".join(
        DEFAULT_COMMAND_ARGS
    ),
):
    """Run given command and check if the number of issues has increased."""
    command_to_run = assemble_command(command, path)
    command_process = subprocess.run(command_to_run, capture_output=True, text=True)

    check_for_errors(command_process, sys.stderr)

    ## count the number of lines in the output buffer
    command_output = command_process.stdout
    lines = command_output.split("\n")
    # remove empty strings from the list
    lines = [line for line in lines if line]

    n_issues_new = len(lines)
    if command_output:
        print(command_output, file=sys.stdout)
    if n_issues_new == 0:
        print("No issues found.", file=sys.stderr)
        raise typer.Exit(0)

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
        print(
            "Number of issues did not decrease from "
            f"{n_issues_old} to {n_issues_new}.",
            file=sys.stderr,
        )
        raise typer.Exit(1)
