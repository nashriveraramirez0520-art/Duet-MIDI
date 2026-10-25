# Duet-MIDI firmware V1

This is the first CircuitPython implementation for the Waveshare ESP32-S3-Zero. The code is prepared and the hardware-independent logic has desktop tests. It has **not** been run on the board: USB enumeration, pin operation, timing, sensitivity, encoder detents, LED order, and current consumption still need real tests.

## Controls

| Control | Initial behavior |
| --- | --- |
| Eight pads | C-major melody on MIDI channel 1; drum mapping on channel 10 |
| MODE | Switch melody/drums and release existing notes |
| OCT- / OCT+ | Shift melody by up to two octaves each way; ignored in drums |
| FUNC | Note Off for active notes and All Notes Off on both channels |
| Slider | MIDI CC1 (modulation), 0..127, filtered and rate limited |
| Encoder | MIDI CC7 (channel volume), 0..127 |
| Encoder push | Reset CC7 to 64 |
| RGB LEDs | Blue idle in melody, orange idle in drums, white for active notes |

MIDI channel constants are zero based in code. Pads use fixed velocity 100, not pressure/velocity sensing. The host instrument must support or map CC1/CC7; this is not a standalone synthesizer. Mode or octave changes release notes and require held pads to be released and touched again.

## Files

- `boot.py`: enable USB MIDI and disable unused keyboard/mouse USB interfaces. Changes require a reset/power cycle.
- `config.py`: PCB pins, note mappings, brightness and initial sensitivity settings.
- `controls.py`: MCP23008 button input and debounce.
- `midi_logic.py`: note lifecycle, touch filtering and MIDI control mappings.
- `code.py`: board initialization and hardware polling loop.
- `lib/README.md`: external libraries to install; pinned upstream Python sources are included, with licenses in `third_party/`.
- `tests/`: desktop logic checks; do not copy them onto the board.

## Install on the board

1. Install a stable CircuitPython build specifically for [Waveshare ESP32-S3-Zero](https://circuitpython.org/board/waveshare_esp32_s3_zero/). Use its board-specific installation instructions. Installation replaces the existing board firmware; do this when ready to program that board.
2. Connect a USB data cable. The board should expose a `CIRCUITPY` drive.
3. Copy the included `lib/` directory into `CIRCUITPY/lib/`. It includes pinned upstream Python sources for MCP230xx, BusDevice, Register and NeoPixel. Alternatively use the [official library bundle](https://circuitpython.org/libraries) matching the installed CircuitPython major version. Do not install both `neopixel.py` and a different `neopixel.mpy` together.
4. Copy the five top-level `.py` files listed above into the **root of CIRCUITPY**, not a nested `firmware/` directory. Copy `config.py` too. Reset after copying `boot.py`.
5. Keep hands away from all pads during the startup calibration (40 samples, with a configured 25 ms delay between sample sets). Open the serial console for baseline values or startup errors.
6. Select the board's MIDI input in a DAW or MIDI monitor. Its default USB product name may be the CircuitPython board name, not Duet-MIDI. Verify each pad's Note On and Note Off before trying the full instrument.

The firmware requires the MCP23008 to be connected and powered. A bare ESP32 board by itself will report an I2C device error with this complete build. Do not run `code.py` using desktop Python or install CircuitPython hardware modules with desktop pip.

## Hardware settings still to verify

- Touch values use a no-touch baseline, 20% press margin, 10% release margin and 20 ms debounce. These are starting settings, not measured thresholds. Reboot with pads untouched to recalibrate. There is no long-term automatic drift compensation yet.
- Slider: measure real ADC endpoints and adjust `SLIDER_ADC_MIN/MAX` if needed. Adjust inversion, filter and CC mapping in `config.py`.
- Encoder: confirm `ENCODER_DIVISOR=4` and direction for the purchased part. It uses GPIO11/12 and their external pull-ups.
- LEDs: external data is GPIO43 through the AHCT buffer, not the ESP board's GPIO21 LED. The chain is D4,D3,D2,D1,D5,D6,D7,D8. Test RGB channel order and the logical pad-to-LED mapping. Brightness starts at 0.08; that setting is not a measured USB power budget. There is no current sensor or automatic current limiter.
- I2C: SDA GPIO13, SCL GPIO44 (RX), MCP23008 address 0x20. GP0..4 are MODE, OCT-, OCT+, FUNC and encoder push, with internal pull-ups enabled.
- A failed/partial USB write raises an error instead of silently claiming delivery. On disconnection the host cannot receive cleanup messages; reconnect/reset and use the host's panic function if notes remain active. Reconnection recovery is not implemented yet.
- Reset/reload cleanup is best effort; a forced power loss cannot send Note Off. Close or silence the host instrument before unplugging.

## Desktop checks

From the repository root, using Python 3:

```sh
python -m unittest discover -s firmware/tests -v
python -m compileall -q firmware
```

The tests exercise note release across mode/octave changes, held-pad retrigger prevention, polyphony, panic, CC endpoints and suppression, encoder limits/reset, and touch debounce/hysteresis. They do not emulate CircuitPython USB, I2C, ADC, rotary input, or LED hardware.

References: [touchio](https://docs.circuitpython.org/en/stable/shared-bindings/touchio/), [usb_midi](https://docs.circuitpython.org/en/stable/shared-bindings/usb_midi/), [analogio](https://docs.circuitpython.org/en/stable/shared-bindings/analogio/), [rotaryio](https://docs.circuitpython.org/en/stable/shared-bindings/rotaryio/), [NeoPixel](https://docs.circuitpython.org/projects/neopixel/en/latest/api.html), [MCP230xx](https://docs.circuitpython.org/projects/mcp230xx/en/latest/api.html).
