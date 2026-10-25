# Included CircuitPython dependencies

This folder includes unmodified upstream Python sources for `adafruit_mcp230xx`, `adafruit_bus_device`, `adafruit_register`, and `neopixel.py`. Copy the folder to `CIRCUITPY/lib/`. Desktop Python cannot run these hardware drivers.

Exact upstream commits and licenses are recorded in `../third_party/`. These libraries are third-party work, not original Duet-MIDI code. They have not been hardware-tested with this project.

Alternatively, use matching modules from the official bundle: https://circuitpython.org/libraries . Use the bundle for the installed CircuitPython major version, and avoid duplicate `.py`/`.mpy` versions of the same module. `adafruit_pixelbuf` and `neopixel_write` are native modules required by NeoPixel on this board.
