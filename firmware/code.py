"""CircuitPython entry point. Copy to CIRCUITPY, not desktop Python."""
import time
import analogio
import neopixel
import rotaryio
import supervisor
import touchio
import usb_midi

import config
from controls import ButtonControls
from midi_logic import Controller, TouchFilter

if len(usb_midi.ports) < 2:
    raise RuntimeError("USB MIDI is unavailable. Install boot.py and reset the board.")
if len(config.TOUCH_PINS) != len(config.MELODY_NOTES):
    raise ValueError("Touch pin count does not match note map")
if (len(config.PAD_LED_INDICES) != len(config.TOUCH_PINS)
        or len(set(config.PAD_LED_INDICES)) != len(config.PAD_LED_INDICES)
        or any(i < 0 or i >= config.LED_COUNT for i in config.PAD_LED_INDICES)):
    raise ValueError("LED mapping must have a unique valid index per pad")

midi_out = usb_midi.ports[1]


def send(message):
    # MIDI ports accept MIDI bytes; do not add USB event-packet headers.
    if midi_out.write(message) != len(message):
        raise OSError("USB MIDI message was not fully written; check the USB connection")


pixels = buttons = slider = encoder = None
pads = []
controller = None
try:
    pixels = neopixel.NeoPixel(
        config.LED_PIN, config.LED_COUNT,
        brightness=config.LED_BRIGHTNESS, auto_write=False,
        pixel_order=config.LED_PIXEL_ORDER,
    )
    pixels.fill((0, 0, 0))
    pixels.show()
    buttons = ButtonControls()
    slider = analogio.AnalogIn(config.SLIDER_PIN)
    encoder = rotaryio.IncrementalEncoder(
        config.ENCODER_A_PIN, config.ENCODER_B_PIN,
        divisor=config.ENCODER_DIVISOR,
    )
    pads = [touchio.TouchIn(pin) for pin in config.TOUCH_PINS]
    controller = Controller(config, send)
    print("Waiting for a USB host")
    while not supervisor.runtime.usb_connected:
        time.sleep(0.05)
    controller.panic()

    print("Duet-MIDI: keep all pads untouched during calibration")
    totals = [0] * len(pads)
    for _ in range(config.CALIBRATION_SAMPLES):
        for i, pad in enumerate(pads):
            totals[i] += pad.raw_value
        time.sleep(config.CALIBRATION_INTERVAL)
    baselines = [v / config.CALIBRATION_SAMPLES for v in totals]
    touches = TouchFilter(baselines, config.TOUCH_PRESS_RATIO,
                          config.TOUCH_RELEASE_RATIO, config.TOUCH_DEBOUNCE_SECONDS)
    print("Touch baselines:", baselines)
    print("Ready. MODE: melody/drums; FUNC: all notes off")

    previous_position = encoder.position
    previous_colors = None
    next_control = next_led = time.monotonic()
    controller.slider(slider.value)
    controller.sync_controls()

    while True:
        now = time.monotonic()
        for event in buttons.pressed_events():
            controller.button(event)
            print("Button:", event, "mode:", controller.mode,
                  "octave:", controller.octave_shift)

        for i, down in touches.update([pad.raw_value for pad in pads], now):
            controller.pad(i, down)

        if now >= next_control:
            position = encoder.position
            controller.encoder((position - previous_position) * config.ENCODER_DIRECTION)
            previous_position = position
            controller.slider(slider.value)
            next_control = now + config.CONTROL_UPDATE_INTERVAL

        if now >= next_led:
            colors = controller.colors()
            if colors != previous_colors:
                for i, color in enumerate(colors):
                    pixels[config.PAD_LED_INDICES[i]] = color
                pixels.show()
                previous_colors = colors
            next_led = now + config.LED_UPDATE_INTERVAL
        time.sleep(0.005)
finally:
    # Best effort on errors/interrupts. A disconnected cable cannot receive Note Off.
    if controller is not None:
        try:
            controller.panic()
        except (OSError, RuntimeError):
            pass
    if pixels is not None:
        pixels.deinit()
    for pad in pads:
        pad.deinit()
    for device in (encoder, slider, buttons):
        if device is not None:
            device.deinit()
