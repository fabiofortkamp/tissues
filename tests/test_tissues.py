"""Tests for the tissues module."""

from io import StringIO

import pytest
import tissues
import typer


def test_assemble_command_multiple_words_and_arguments():
    """Test assemble_command with multiple words and arguments."""
    command = "ruff check"
    arguments = ["--fix", "--quiet", "--exit-zero"]
    expected = ["ruff", "check", "--fix", "--quiet", "--exit-zero"]
    assert tissues.assemble_command(command, arguments) == expected


def test_assemble_command_single_word_and_arguments():
    """Test assemble_command with a single word and arguments."""
    command = "ruff"
    arguments = ["--fix", "--quiet", "--exit-zero"]
    expected = ["ruff", "--fix", "--quiet", "--exit-zero"]
    assert tissues.assemble_command(command, arguments) == expected


def test_assemble_command_no_arguments():
    """Test assemble_command with no arguments."""
    command = "ruff"
    arguments = []
    expected = ["ruff"]
    assert tissues.assemble_command(command, arguments) == expected


def test_check_for_errors_no_errors(capsys):
    """Test that an error in a process is recognized."""
    process = tissues.subprocess.CompletedProcess(
        args=["ruff", "check", "--fix", "--quiet", "--exit-zero"],
        returncode=0,
        stdout="",
        stderr="error",
    )

    # create a in-memory text buffer
    buffer = StringIO()
    with pytest.raises(typer.Exit):
        tissues.check_for_errors(process, buffer)

    assert buffer.getvalue() == "Error running command:\nerror\n"
