"""USB settings apply only after a board reset/power cycle."""
import usb_hid
import usb_midi

# This controller uses MIDI, not USB keyboard/mouse interfaces.
usb_hid.disable()
usb_midi.enable()
