"""
boot.py — Runs before code.py on CircuitPython startup.

Configures USB identification and HID device descriptors.
This file should be copied to the CIRCUITPY drive as boot.py.

The custom USB product string lets the relay-tray detect any board
running Nymble firmware, regardless of chip (RP2040, RP2350, etc).
"""

import supervisor
import usb_hid

FIRMWARE_VERSION = "0.2.0"

# Set custom USB identification so the host detects "Nymble" in the
# device description instead of the default board name.
# This makes detection firmware-aware rather than hardware-aware.
supervisor.set_usb_identification(
    manufacturer="Nymble",
    product=f"Nymble HID v{FIRMWARE_VERSION}",
)

# Enable only keyboard HID device (no mouse/consumer control)
# This keeps the descriptor simple and avoids conflicts.
usb_hid.enable((usb_hid.Device.KEYBOARD,))
