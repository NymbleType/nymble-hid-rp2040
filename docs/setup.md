# Setup — nymble-hid-rp2040

## Hardware

- Raspberry Pi Pico (RP2040) or compatible board
- USB cable (data-capable, not charge-only)

## Firmware Setup

### 1. Install CircuitPython

1. Download CircuitPython for your board from [circuitpython.org](https://circuitpython.org/downloads)
2. Hold BOOTSEL on the Pico and plug it in via USB
3. Drag the `.uf2` file to the `RPI-RP2` drive
4. The board will reboot and appear as `CIRCUITPY`

### 2. Install Libraries

Download the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries) and copy these to `CIRCUITPY/lib/`:

- `adafruit_hid/` (entire folder)

### 3. Deploy Firmware

Copy from this repo to the `CIRCUITPY` drive:

```
firmware/boot.py  →  CIRCUITPY/boot.py
firmware/code.py  →  CIRCUITPY/code.py
```

**Important:** After copying `boot.py`, you must **power-cycle** the board (unplug and replug USB) for it to take effect.

### 4. Verify

Open a serial terminal (e.g., `screen /dev/ttyACM0 115200` on Linux):

```
nymble-hid-rp2040 ready
```

Send `PING` — you should get `OK:PONG` back and see two quick LED blinks.

## Serial Protocol

The device reads newline-terminated commands over USB serial:

| Command | Example | Description |
|---------|---------|-------------|
| `TYPE:<text>` | `TYPE:Hello world` | Types the text as keystrokes |
| `KEY:<name>` | `KEY:ENTER` | Presses a special key |
| `PING` | `PING` | Health check (responds `OK:PONG`) |
| Raw text | `Hello` | Treated as `TYPE:Hello` |

### Supported Special Keys

`ENTER`, `TAB`, `BACKSPACE`, `DELETE`, `ESCAPE`, `SPACE`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `HOME`, `END`, `PAGEUP`, `PAGEDOWN`

## Troubleshooting

- **No serial port appears:** Ensure CircuitPython is installed (not MicroPython). Check `boot.py` is on the drive.
- **Keystrokes not appearing:** Some OS security settings block new HID devices. On macOS, check System Preferences → Security & Privacy → Input Monitoring.
- **Characters dropped:** Increase `CHAR_DELAY` in `code.py` (default: 20ms).
