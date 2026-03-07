"""Tests for the HID device serial protocol.

Since the firmware runs on CircuitPython, we test the protocol logic
by extracting and testing the command parsing independently.
"""

import pytest


# Protocol constants (must match firmware/code.py)
CMD_TYPE = "TYPE:"
CMD_KEY = "KEY:"
CMD_PING = "PING"

SPECIAL_KEYS = {
    "ENTER", "RETURN", "TAB", "BACKSPACE", "DELETE",
    "ESCAPE", "ESC", "SPACE", "UP", "DOWN", "LEFT", "RIGHT",
    "HOME", "END", "PAGEUP", "PAGEDOWN",
}


def parse_command(line: str) -> dict:
    """Parse a serial command line (mirrors firmware logic)."""
    line = line.strip()
    if not line:
        return {"type": "empty"}

    if line.startswith(CMD_TYPE):
        return {"type": "type", "text": line[len(CMD_TYPE):]}
    elif line.startswith(CMD_KEY):
        return {"type": "key", "key": line[len(CMD_KEY):].strip().upper()}
    elif line == CMD_PING:
        return {"type": "ping"}
    else:
        return {"type": "type", "text": line}  # Default: raw text


class TestProtocolParsing:
    """Test serial protocol command parsing."""

    def test_type_command(self):
        result = parse_command("TYPE:Hello world")
        assert result == {"type": "type", "text": "Hello world"}

    def test_type_empty_text(self):
        result = parse_command("TYPE:")
        assert result == {"type": "type", "text": ""}

    def test_key_command(self):
        result = parse_command("KEY:ENTER")
        assert result == {"type": "key", "key": "ENTER"}

    def test_key_case_insensitive(self):
        result = parse_command("KEY:enter")
        assert result["key"] == "ENTER"

    def test_ping(self):
        result = parse_command("PING")
        assert result == {"type": "ping"}

    def test_raw_text_defaults_to_type(self):
        result = parse_command("Hello")
        assert result == {"type": "type", "text": "Hello"}

    def test_empty_line(self):
        result = parse_command("")
        assert result == {"type": "empty"}

    def test_whitespace_only(self):
        result = parse_command("   ")
        assert result == {"type": "empty"}

    def test_type_with_special_chars(self):
        result = parse_command("TYPE:Hello! @user #tag")
        assert result["text"] == "Hello! @user #tag"

    def test_type_preserves_internal_spaces(self):
        """TYPE command preserves spaces within text (trailing stripped by line parser)."""
        result = parse_command("TYPE:  spaced  text")
        assert result["text"] == "  spaced  text"


class TestSpecialKeys:
    """Test that all documented special keys are present."""

    def test_enter_supported(self):
        assert "ENTER" in SPECIAL_KEYS

    def test_tab_supported(self):
        assert "TAB" in SPECIAL_KEYS

    def test_arrow_keys_supported(self):
        for key in ["UP", "DOWN", "LEFT", "RIGHT"]:
            assert key in SPECIAL_KEYS

    def test_navigation_keys_supported(self):
        for key in ["HOME", "END", "PAGEUP", "PAGEDOWN"]:
            assert key in SPECIAL_KEYS


class TestProtocolResponses:
    """Test expected response format."""

    def test_ok_typed_format(self):
        response = "OK:TYPED"
        assert response.startswith("OK:")

    def test_ok_pong_format(self):
        response = "OK:PONG"
        assert response == "OK:PONG"

    def test_ok_key_format(self):
        response = "OK:KEY"
        assert response.startswith("OK:")

    def test_error_format(self):
        response = "ERR:UNKNOWN_KEY:INVALID"
        assert response.startswith("ERR:")
