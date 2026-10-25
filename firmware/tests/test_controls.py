"""MCP button polling checks with a mocked I2C device, not a hardware test."""
import importlib.util
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.modules.setdefault("board", SimpleNamespace(**{
    "IO" + str(i): i for i in (*range(1, 14), 43, 44)
}))


class ButtonTests(unittest.TestCase):
    def make_reader(self):
        bus = SimpleNamespace(deinit=lambda: None)
        pins = []
        def get_pin(n):
            pins.append(n)
            return SimpleNamespace(switch_to_input=lambda **kw: None)
        mcp = SimpleNamespace(gpio=0xFF, get_pin=get_pin)
        modules = {
            "busio": SimpleNamespace(I2C=lambda **kw: bus),
            "digitalio": SimpleNamespace(Pull=SimpleNamespace(UP="UP")),
            "adafruit_mcp230xx": SimpleNamespace(),
            "adafruit_mcp230xx.mcp23008": SimpleNamespace(MCP23008=lambda *a, **kw: mcp),
        }
        spec = importlib.util.spec_from_file_location(
            "controls_under_test", Path(__file__).resolve().parents[1] / "controls.py")
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(module)
        module.time = SimpleNamespace(monotonic=lambda: self.now)
        self.now = 0.0
        return module.ButtonControls(), mcp, pins

    def test_active_low_bounce_and_no_repeat_while_held(self):
        reader, mcp, pins = self.make_reader()
        self.assertEqual(pins, [0, 1, 2, 3, 4])
        mcp.gpio = 0xFE
        self.assertEqual(reader.pressed_events(), [])
        self.now = 0.010
        mcp.gpio = 0xFF
        self.assertEqual(reader.pressed_events(), [])
        self.now = 0.020
        mcp.gpio = 0xFE
        self.assertEqual(reader.pressed_events(), [])
        self.now = 0.051
        self.assertEqual(reader.pressed_events(), ["mode"])
        self.now = 1.0
        self.assertEqual(reader.pressed_events(), [])
        mcp.gpio = 0xFF
        reader.pressed_events()
        self.now = 1.031
        self.assertEqual(reader.pressed_events(), [])
        mcp.gpio = 0xFE
        reader.pressed_events()
        self.now = 1.062
        self.assertEqual(reader.pressed_events(), ["mode"])

    def test_encoder_push_is_gp4_not_an_esp32_gpio(self):
        reader, mcp, _ = self.make_reader()
        mcp.gpio = 0xEF
        reader.pressed_events()
        self.now = 0.031
        self.assertEqual(reader.pressed_events(), ["encoder"])
