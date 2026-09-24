"""Command-line interface for the OpenPCB prototype."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="openpcb",
        description="OpenPCB command-line prototype",
    )
    parser.add_argument("--echo", help="print a message and exit")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""
    args = build_parser().parse_args(argv)
    if args.echo:
        print(args.echo)
    else:
        print("OpenPCB CLI is an early-development scaffold. See docs/SPEC-1-OpenPCB.md.")
    return 0
