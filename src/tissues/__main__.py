"""Main module for the tissues package."""

import typer

import tissues


def cli():
    """Main entry point for the tissues package."""
    typer.run(tissues.main)
