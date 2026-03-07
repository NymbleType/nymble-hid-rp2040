# nymble-hid-rp2040

RP2040-based USB HID device for keystroke injection.

## Overview

CircuitPython firmware for a Raspberry Pi Pico (RP2040) that acts as a USB HID keyboard. Receives text over USB serial and types it as keystrokes on the host machine.

**Pipeline position:** `mic → transcription (nymble-whisper-pi) → relay (nymble-relay-tray) → typing (this repo)`

## Stack

- **Language:** CircuitPython
- **HID Library:** adafruit_hid
- **Protocol:** Line-based serial commands over USB

## Structure

```
firmware/
  boot.py           # USB HID descriptor config (runs at boot)
  code.py           # Main firmware (serial → HID keystrokes)
docs/
  setup.md          # Setup & flashing guide
tools/              # Flash and debug utilities
```

## Serial Protocol

| Command | Example | Description |
|---------|---------|-------------|
| `TYPE:<text>` | `TYPE:Hello world` | Types text as keystrokes |
| `KEY:<name>` | `KEY:ENTER` | Presses a special key |
| `PING` | `PING` | Health check → `OK:PONG` |
| Raw text | `Hello` | Treated as TYPE |

## Quick Start

1. Flash CircuitPython onto the Pico
2. Copy `adafruit_hid` to `CIRCUITPY/lib/`
3. Copy `firmware/boot.py` and `firmware/code.py` to `CIRCUITPY/`
4. Power-cycle the board

See [docs/setup.md](docs/setup.md) for full instructions.

## License

TBD
