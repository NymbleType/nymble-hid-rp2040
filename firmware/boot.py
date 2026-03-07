"""
boot.py — Runs before code.py on CircuitPython startup.

Configures USB HID device descriptors. This file should be
copied to the CIRCUITPY drive as boot.py.
"""

import usb_hid

# Enable only keyboard HID device (no mouse/consumer control)
# This keeps the descriptor simple and avoids conflicts.
usb_hid.enable((usb_hid.Device.KEYBOARD,))
