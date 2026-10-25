"""Debounced active-low buttons on the MCP23008."""
import time
import busio
import digitalio
from adafruit_mcp230xx.mcp23008 import MCP23008
import config

BUTTONS = (
    ("mode", config.BUTTON_MODE),
    ("octave_down", config.BUTTON_OCTAVE_DOWN),
    ("octave_up", config.BUTTON_OCTAVE_UP),
    ("function", config.BUTTON_FUNCTION),
    ("encoder", config.BUTTON_ENCODER),
)


class ButtonControls:
    def __init__(self):
        self.i2c = busio.I2C(scl=config.I2C_SCL_PIN,
                             sda=config.I2C_SDA_PIN, frequency=100000)
        self.mcp = MCP23008(self.i2c, address=config.MCP23008_ADDRESS)
        for _, number in BUTTONS:
            self.mcp.get_pin(number).switch_to_input(pull=digitalio.Pull.UP)
        self.states = [False] * len(BUTTONS)
        self.candidates = [False] * len(BUTTONS)
        self.changed_at = [time.monotonic()] * len(BUTTONS)

    def pressed_events(self):
        now = time.monotonic()
        inputs = self.mcp.gpio
        events = []
        for i, (name, number) in enumerate(BUTTONS):
            detected = not bool(inputs & (1 << number))
            if detected != self.candidates[i]:
                self.candidates[i] = detected
                self.changed_at[i] = now
            if (self.candidates[i] != self.states[i]
                    and now - self.changed_at[i] >= config.BUTTON_DEBOUNCE_SECONDS):
                self.states[i] = self.candidates[i]
                if self.states[i]:
                    events.append(name)
        return events

    def deinit(self):
        self.i2c.deinit()
