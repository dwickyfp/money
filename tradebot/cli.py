"""Command-line entry point for the tradebot package."""

from __future__ import annotations

from tradebot.engine import main as _engine_main


def main(argv: list[str] | None = None) -> None:
    """Function : main
    Descriptions : Run the tradebot command-line interface.
    Param :
        Param <argv> : Optional command-line arguments.
    """
    _engine_main(argv)
