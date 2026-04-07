"""
boot.py — Runs before code.py on CircuitPython startup.

Configures USB identification, HID device descriptors, and disables
the CIRCUITPY USB drive so the device appears only as a keyboard.

To re-enable the CIRCUITPY drive for firmware updates, hold the
BOOTSEL button (or connect GP15 to GND) while plugging in the board.

This file should be copied to the CIRCUITPY drive as boot.py.
"""

import board
import digitalio
import storage
import supervisor
import usb_cdc
import usb_hid

FIRMWARE_VERSION = "0.2.0"

# --- Safe mode escape hatch ---
# Hold BOOTSEL (or ground GP15) during plug-in to keep CIRCUITPY
# drive and USB serial console enabled for debugging/updates.
safe_mode_pin = digitalio.DigitalInOut(board.GP15)
safe_mode_pin.direction = digitalio.Direction.INPUT
safe_mode_pin.pull = digitalio.Pull.UP

safe_mode = not safe_mode_pin.value  # Low = held/grounded = safe mode
safe_mode_pin.deinit()

# Set custom USB identification so the host detects "Nymble" in the
# device description instead of the default board name.
supervisor.set_usb_identification(
    manufacturer="Nymble",
    product=f"Nymble HID v{FIRMWARE_VERSION}",
)

# Enable only keyboard HID device (no mouse/consumer control)
usb_hid.enable((usb_hid.Device.KEYBOARD,))

if not safe_mode:
    # Disable CIRCUITPY USB mass storage — device appears only as a keyboard
    storage.disable_usb_drive()
    # Disable USB serial console (the data serial for code.py still works)
    usb_cdc.disable()
