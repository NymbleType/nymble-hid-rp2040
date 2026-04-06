# nymble-hid-rp2040

RP2040-based USB HID device for keystroke injection.

## Overview

CircuitPython firmware for a Raspberry Pi Pico (RP2040) that acts as a USB HID keyboard. Receives commands over USB serial and types text, presses keys, executes combos, and controls timing — all as real keystrokes on the host machine.

**Pipeline position:** `text source → relay (nymble-relay) → typing (this repo)`

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

| Command | Example | Response | Description |
|---------|---------|----------|-------------|
| `TYPE:<text>` | `TYPE:Hello world` | `OK:TYPED` | Types text as keystrokes |
| `KEY:<name>` | `KEY:ENTER` | `OK:KEY` | Presses a special key |
| `COMBO:<keys>` | `COMBO:CTRL+A` | `OK:COMBO` | Presses a key combination |
| `HOLD:<key>` | `HOLD:SHIFT` | `OK:HOLD` | Holds a key down |
| `RELEASE` | `RELEASE` | `OK:RELEASE` | Releases all held keys |
| `SPEED:<ms>` | `SPEED:50` | `OK:SPEED` | Sets inter-key delay in ms |
| `DELAY:<ms>` | `DELAY:1000` | `OK:DELAY` | Pauses for N milliseconds |
| `PING` | `PING` | `OK:PONG` | Health check |
| Raw text | `Hello` | `OK:TYPED` | Treated as TYPE |

### Supported Keys

**Special keys:** `ENTER`, `TAB`, `BACKSPACE`, `DELETE`, `ESCAPE`, `SPACE`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `HOME`, `END`, `PAGEUP`, `PAGEDOWN`, `INSERT`, `CAPSLOCK`, `PRINTSCREEN`, `SCROLLLOCK`, `PAUSE`, `F1`–`F12`

**Modifiers:** `CTRL`, `SHIFT`, `ALT`, `GUI`/`WIN`/`CMD`/`SUPER`

**Letters/numbers:** `A`–`Z`, `0`–`9` (for use in combos)

### Examples

```
TYPE:Hello world          → types "Hello world"
KEY:ENTER                 → presses Enter
COMBO:CTRL+C              → copies selection
COMBO:CTRL+SHIFT+V        → pastes as plain text
SPEED:80                  → human-like typing speed
TYPE:slow and steady      → types at 80ms per character
SPEED:0                   → back to full speed
DELAY:2000                → waits 2 seconds
HOLD:SHIFT                → holds Shift
TYPE:hello                → types "HELLO" (Shift is held)
RELEASE                   → releases Shift
```

## Quick Start

1. Flash CircuitPython onto the Pico
2. Copy `adafruit_hid` to `CIRCUITPY/lib/`
3. Copy `firmware/boot.py` and `firmware/code.py` to `CIRCUITPY/`
4. Power-cycle the board

See [docs/setup.md](docs/setup.md) for full instructions.

## Hardware

Any RP2040 or RP2350 board works. The Raspberry Pi Pico is the cheapest option at ~$4.

## License

MIT
