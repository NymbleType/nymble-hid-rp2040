"""
nymble-hid-rp2040 — Main CircuitPython entry point.

Receives text over USB serial and injects it as HID keystrokes.
This file should be copied to the CIRCUITPY drive as code.py.

Protocol:
    PING         → OK:PONG
    TYPE:text     → types "text" as keystrokes → OK:TYPED
    KEY:ENTER     → presses Enter key → OK:KEY
    raw text      → types as keystrokes → OK:TYPED
"""

import sys
import time
import board
import digitalio
import supervisor
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Status LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# HID keyboard setup
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Protocol constants
CMD_TYPE = "TYPE:"
CMD_KEY = "KEY:"
CMD_PING = "PING"

# Typing delay between characters (seconds) — prevents dropped keystrokes
CHAR_DELAY = 0.02

# Key name mapping for special keys
SPECIAL_KEYS = {
    "ENTER": Keycode.ENTER,
    "RETURN": Keycode.ENTER,
    "TAB": Keycode.TAB,
    "BACKSPACE": Keycode.BACKSPACE,
    "DELETE": Keycode.DELETE,
    "ESCAPE": Keycode.ESCAPE,
    "ESC": Keycode.ESCAPE,
    "SPACE": Keycode.SPACE,
    "UP": Keycode.UP_ARROW,
    "DOWN": Keycode.DOWN_ARROW,
    "LEFT": Keycode.LEFT_ARROW,
    "RIGHT": Keycode.RIGHT_ARROW,
    "HOME": Keycode.HOME,
    "END": Keycode.END,
    "PAGEUP": Keycode.PAGE_UP,
    "PAGEDOWN": Keycode.PAGE_DOWN,
}


def blink(count=1, duration=0.1):
    """Blink the onboard LED."""
    for _ in range(count):
        led.value = True
        time.sleep(duration)
        led.value = False
        time.sleep(duration)


def type_text(text):
    """Type text as HID keystrokes with per-character delay."""
    for char in text:
        try:
            layout.write(char)
        except ValueError:
            # Skip characters not in the layout
            pass
        time.sleep(CHAR_DELAY)


def press_key(key_name):
    """Press a special key by name."""
    key_name = key_name.strip().upper()
    keycode = SPECIAL_KEYS.get(key_name)
    if keycode:
        keyboard.press(keycode)
        keyboard.release_all()
        print("OK:KEY")
    else:
        print("ERR:UNKNOWN_KEY:" + key_name)


def handle_line(line):
    """Process a single line of input."""
    line = line.strip()
    if not line:
        return

    if line == CMD_PING:
        print("OK:PONG")
        blink(2, 0.05)

    elif line.startswith(CMD_TYPE):
        text = line[len(CMD_TYPE):]
        type_text(text)
        blink(1)
        print("OK:TYPED")

    elif line.startswith(CMD_KEY):
        key_name = line[len(CMD_KEY):]
        press_key(key_name)

    else:
        # Default: treat as raw text to type
        type_text(line)
        blink(1)
        print("OK:TYPED")


# --- Main loop ---
print("nymble-hid-rp2040 ready")
blink(3, 0.1)

buf = ""
while True:
    if supervisor.runtime.serial_bytes_available:
        # Read from USB serial console via sys.stdin
        # (supervisor.runtime.serial_bytes_available checks the console)
        char = sys.stdin.read(1)
        if char == "\n" or char == "\r":
            if buf:
                handle_line(buf)
                buf = ""
        elif char:
            buf += char
    else:
        time.sleep(0.01)
