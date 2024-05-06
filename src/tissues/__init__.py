"""Main module for the tissues package."""

import subprocess
import sys

ISSUES_FILENAME = ".ruff.issues"
RUFF_COMMAND_ARGS = ["ruff", "check", "--fix", "--quiet", "--exit-zero"]


def main() -> int:
    
    # run the ruff command, appending the first command line argument to it
    command = RUFF_COMMAND_ARGS + sys.argv[1:]
    ruff_process = subprocess.run(
        command, capture_output=True, text=True
    )

    if ruff_process.returncode != 0:
        print("Could not run ruff command", file=sys.stderr)
        return 1

    ## count the number of lines in the output buffer
    ruff_output = ruff_process.stdout
    lines = ruff_output.split("\n")
    # remove empty strings from the list
    lines = [line for line in lines if line]

    n_issues_new = len(lines)
    if ruff_output:
        print(ruff_output, file=sys.stdout)

    # read the number of issues from the previous run
    try:
        with open(ISSUES_FILENAME, "r") as f:
            n_issues_old = int(f.read())
    except Exception:
        n_issues_old = 0

    # write the number of issues from the current run
    with open(ISSUES_FILENAME, "w") as f:
        f.write(str(n_issues_new))

    # if the number of issues has increased, print the output and return 1
    if n_issues_new >= n_issues_old:
        return 1

    return 0
