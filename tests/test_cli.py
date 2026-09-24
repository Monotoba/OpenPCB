"""Tests for the OpenPCB command-line scaffold."""

from openpcb.cli import main


def test_echo(capsys):
    """The echo option should print the supplied message."""
    assert main(["--echo", "hello"]) == 0
    assert capsys.readouterr().out == "hello\n"


def test_scaffold_message(capsys):
    """The default CLI response should accurately describe its status."""
    assert main([]) == 0
    assert "early-development scaffold" in capsys.readouterr().out
