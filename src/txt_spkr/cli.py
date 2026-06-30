"""Command-line interface for the application."""

from __future__ import annotations

import sys

from txt_spkr.crew import run_crew


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    _configure_output()
    message = _get_message(argv)
    if not message:
        example = "Thank you. I'll see you later."
        raise SystemExit(f'Usage: python -m txt_spkr "{example}"')
    result = run_crew(message)
    if result:
        print(result)
    else:
        print("No result returned from crew.")
    return 0


def _get_message(argv: list[str] | None = None) -> str:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return ""

    return args[0]


def _configure_output() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")
