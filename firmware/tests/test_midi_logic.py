"""Desktop logic tests; these do not emulate USB or prove hardware operation."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.modules.setdefault("board", SimpleNamespace(**{
    "IO" + str(i): i for i in (*range(1, 14), 43, 44)
}))
import config
from midi_logic import Controller, TouchFilter


class LogicTests(unittest.TestCase):
    def setUp(self):
        self.messages = []
        self.cfg = SimpleNamespace(**{
            name: getattr(config, name)
            for name in dir(config) if name.isupper()
        })
        self.controller = Controller(self.cfg, self.messages.append)

    def test_one_on_and_off_per_gesture(self):
        c = self.controller
        c.pad(0, True)
        c.pad(0, True)
        c.pad(0, False)
        c.pad(0, False)
        self.assertEqual(self.messages, [bytes((0x90, 60, 100)), bytes((0x80, 60, 0))])

    def test_multiple_pads_have_independent_note_lifetimes(self):
        c = self.controller
        c.pad(0, True)
        c.pad(1, True)
        c.pad(0, False)
        self.assertIsNone(c.active[0])
        self.assertEqual(c.active[1], (62, 0))
        self.assertEqual(self.messages[-1], bytes((0x80, 60, 0)))

    def test_mode_change_releases_old_channel_and_requires_retouch(self):
        c = self.controller
        c.pad(0, True)
        c.button("mode")
        self.assertIn(bytes((0x80, 60, 0)), self.messages)
        self.assertEqual(c.mode, "drums")
        count = len(self.messages)
        c.pad(0, True)
        c.pad(0, False)
        self.assertEqual(len(self.messages), count)
        c.pad(0, True)
        self.assertEqual(self.messages[-1], bytes((0x99, 36, 100)))
        c.pad(0, False)
        self.assertEqual(self.messages[-1], bytes((0x89, 36, 0)))

    def test_octave_change_clears_notes_and_clamps(self):
        c = self.controller
        c.pad(7, True)
        for _ in range(10):
            c.button("octave_up")
        self.assertIn(bytes((0x80, 72, 0)), self.messages)
        self.assertEqual(c.octave_shift, 2)
        c.pad(7, False)
        c.pad(7, True)
        self.assertEqual(self.messages[-1], bytes((0x90, 96, 100)))
        for _ in range(20):
            c.button("octave_down")
        self.assertEqual(c.octave_shift, -2)

    def test_octave_buttons_do_not_change_drum_mapping(self):
        c = self.controller
        c.button("mode")
        c.button("octave_up")
        self.assertEqual(c.octave_shift, 0)
        c.pad(7, True)
        self.assertEqual(self.messages[-1], bytes((0x99, 51, 100)))

    def test_function_panic_releases_all_active_notes(self):
        c = self.controller
        c.pad(0, True)
        c.pad(1, True)
        c.button("function")
        self.assertEqual(c.active, [None] * 8)
        self.assertIn(bytes((0x80, 60, 0)), self.messages)
        self.assertIn(bytes((0x80, 62, 0)), self.messages)
        self.assertIn(bytes((0xB0, 123, 0)), self.messages)
        self.assertIn(bytes((0xB9, 123, 0)), self.messages)

    def test_encoder_limits_and_push_reset(self):
        c = self.controller
        c.encoder(1000)
        self.assertEqual(self.messages[-1], bytes((0xB0, 7, 127)))
        c.encoder(-1000)
        self.assertEqual(self.messages[-1], bytes((0xB0, 7, 0)))
        c.button("encoder")
        self.assertEqual(self.messages[-1], bytes((0xB0, 7, 64)))

    def test_slider_endpoints_and_duplicate_suppression(self):
        self.cfg.SLIDER_FILTER_ALPHA = 1
        c = self.controller
        c.slider(0)
        c.slider(0)
        self.assertEqual(self.messages, [bytes((0xB0, 1, 0))])
        c.slider(65535)
        self.assertEqual(self.messages[-1], bytes((0xB0, 1, 127)))

    def test_slider_inversion_and_smoothing(self):
        self.cfg.SLIDER_INVERT = True
        c = self.controller
        c.slider(0)
        self.assertEqual(c.slider_value, 127)
        c.slider(65535)
        self.assertGreater(c.slider_value, 0)
        self.assertLess(c.slider_value, 127)
        for _ in range(100):
            c.slider(65535)
        self.assertEqual(c.slider_value, 0)

    def test_mode_change_resends_controls_on_new_channel(self):
        c = self.controller
        c.slider(0)
        c.button("mode")
        self.assertIn(bytes((0xB9, 7, 64)), self.messages)
        self.assertIn(bytes((0xB9, 1, 0)), self.messages)

    def test_lights_follow_active_notes_and_mode(self):
        c = self.controller
        idle = c.colors()
        c.pad(2, True)
        self.assertEqual(c.colors()[2], (255, 255, 255))
        c.pad(2, False)
        self.assertEqual(c.colors(), idle)
        c.button("mode")
        self.assertNotEqual(c.colors(), idle)

    def test_touch_bounce_and_hysteresis(self):
        f = TouchFilter([100], 1.2, 1.1, 0.020)
        self.assertEqual(f.update([121], 0.000), [])
        self.assertEqual(f.update([100], 0.010), [])
        self.assertEqual(f.update([121], 0.020), [])
        self.assertEqual(f.update([121], 0.041), [(0, True)])
        self.assertEqual(f.update([115], 0.050), [])
        self.assertEqual(f.update([105], 0.060), [])
        self.assertEqual(f.update([105], 0.081), [(0, False)])

    def test_invalid_baseline_or_note_range_is_rejected(self):
        with self.assertRaises(ValueError):
            TouchFilter([0], 1.2, 1.1, 0.02)
        self.cfg.MAX_OCTAVE_SHIFT = 20
        with self.assertRaises(ValueError):
            Controller(self.cfg, self.messages.append)


if __name__ == "__main__":
    unittest.main()
