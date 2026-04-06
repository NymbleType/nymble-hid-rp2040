"""
nymble-hid-rp2040 — Main CircuitPython entry point.

Receives text over USB serial and injects it as HID keystrokes.
This file should be copied to the CIRCUITPY drive as code.py.

Protocol:
    PING              → OK:PONG
    TYPE:text          → types "text" as keystrokes → OK:TYPED
    KEY:ENTER          → presses a special key → OK:KEY
    COMBO:CTRL+A       → presses key combination → OK:COMBO
    HOLD:SHIFT         → holds a key down → OK:HOLD
    RELEASE            → releases all held keys → OK:RELEASE
    SPEED:50           → sets inter-key delay to 50ms → OK:SPEED
    DELAY:1000         → pauses for 1000ms → OK:DELAY
    raw text           → types as keystrokes → OK:TYPED
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
CMD_COMBO = "COMBO:"
CMD_HOLD = "HOLD:"
CMD_RELEASE = "RELEASE"
CMD_SPEED = "SPEED:"
CMD_DELAY = "DELAY:"
CMD_PING = "PING"

# Typing delay between characters (seconds) — adjustable via SPEED command
char_delay = 0.02

# Key name mapping for special keys and modifiers
KEY_MAP = {
    # Special keys
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
    "INSERT": Keycode.INSERT,
    "CAPSLOCK": Keycode.CAPS_LOCK,
    "PRINTSCREEN": Keycode.PRINT_SCREEN,
    "SCROLLLOCK": Keycode.SCROLL_LOCK,
    "PAUSE": Keycode.PAUSE,
    # F-keys
    "F1": Keycode.F1, "F2": Keycode.F2, "F3": Keycode.F3,
    "F4": Keycode.F4, "F5": Keycode.F5, "F6": Keycode.F6,
    "F7": Keycode.F7, "F8": Keycode.F8, "F9": Keycode.F9,
    "F10": Keycode.F10, "F11": Keycode.F11, "F12": Keycode.F12,
    # Modifiers
    "CTRL": Keycode.CONTROL,
    "CONTROL": Keycode.CONTROL,
    "SHIFT": Keycode.SHIFT,
    "ALT": Keycode.ALT,
    "GUI": Keycode.GUI,
    "WIN": Keycode.GUI,
    "WINDOWS": Keycode.GUI,
    "CMD": Keycode.GUI,
    "COMMAND": Keycode.GUI,
    "SUPER": Keycode.GUI,
    # Single letter/number keys (for combos like CTRL+A)
    "A": Keycode.A, "B": Keycode.B, "C": Keycode.C, "D": Keycode.D,
    "E": Keycode.E, "F": Keycode.F, "G": Keycode.G, "H": Keycode.H,
    "I": Keycode.I, "J": Keycode.J, "K": Keycode.K, "L": Keycode.L,
    "M": Keycode.M, "N": Keycode.N, "O": Keycode.O, "P": Keycode.P,
    "Q": Keycode.Q, "R": Keycode.R, "S": Keycode.S, "T": Keycode.T,
    "U": Keycode.U, "V": Keycode.V, "W": Keycode.W, "X": Keycode.X,
    "Y": Keycode.Y, "Z": Keycode.Z,
    "0": Keycode.ZERO, "1": Keycode.ONE, "2": Keycode.TWO,
    "3": Keycode.THREE, "4": Keycode.FOUR, "5": Keycode.FIVE,
    "6": Keycode.SIX, "7": Keycode.SEVEN, "8": Keycode.EIGHT,
    "9": Keycode.NINE,
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
            pass  # Skip characters not in the layout
        time.sleep(char_delay)


def resolve_key(name):
    """Resolve a key name to a Keycode. Returns None if unknown."""
    return KEY_MAP.get(name.strip().upper())


def press_key(key_name):
    """Press and release a single special key by name."""
    keycode = resolve_key(key_name)
    if keycode:
        keyboard.press(keycode)
        keyboard.release_all()
        print("OK:KEY")
    else:
        print("ERR:UNKNOWN_KEY:" + key_name.strip())


def press_combo(combo_str):
    """Press a key combination like CTRL+A or CTRL+SHIFT+V."""
    parts = combo_str.strip().split("+")
    keycodes = []
    for part in parts:
        keycode = resolve_key(part)
        if keycode is None:
            print("ERR:UNKNOWN_KEY:" + part.strip())
            return
        keycodes.append(keycode)

    keyboard.press(*keycodes)
    keyboard.release_all()
    print("OK:COMBO")


def hold_key(key_name):
    """Press and hold a key (don't release until RELEASE command)."""
    keycode = resolve_key(key_name)
    if keycode:
        keyboard.press(keycode)
        print("OK:HOLD")
    else:
        print("ERR:UNKNOWN_KEY:" + key_name.strip())


def release_keys():
    """Release all held keys."""
    keyboard.release_all()
    print("OK:RELEASE")


def set_speed(ms_str):
    """Set the inter-key typing delay in milliseconds."""
    global char_delay
    try:
        ms = int(ms_str.strip())
        if ms < 0:
            ms = 0
        char_delay = ms / 1000.0
        print("OK:SPEED")
    except ValueError:
        print("ERR:INVALID_SPEED:" + ms_str.strip())


def do_delay(ms_str):
    """Pause for the specified number of milliseconds."""
    try:
        ms = int(ms_str.strip())
        if ms < 0:
            ms = 0
        if ms > 30000:
            ms = 30000  # Cap at 30 seconds for safety
        time.sleep(ms / 1000.0)
        print("OK:DELAY")
    except ValueError:
        print("ERR:INVALID_DELAY:" + ms_str.strip())


def handle_line(line):
    """Process a single line of input."""
    line = line.strip()
    if not line:
        return

    if line == CMD_PING:
        print("OK:PONG")
        blink(2, 0.05)

    elif line == CMD_RELEASE:
        release_keys()

    elif line.startswith(CMD_TYPE):
        type_text(line[len(CMD_TYPE):])
        blink(1)
        print("OK:TYPED")

    elif line.startswith(CMD_KEY):
        press_key(line[len(CMD_KEY):])

    elif line.startswith(CMD_COMBO):
        press_combo(line[len(CMD_COMBO):])

    elif line.startswith(CMD_HOLD):
        hold_key(line[len(CMD_HOLD):])

    elif line.startswith(CMD_SPEED):
        set_speed(line[len(CMD_SPEED):])

    elif line.startswith(CMD_DELAY):
        do_delay(line[len(CMD_DELAY):])

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
        char = sys.stdin.read(1)
        if char == "\n" or char == "\r":
            if buf:
                handle_line(buf)
                buf = ""
        elif char:
            buf += char
    else:
        time.sleep(0.01)
