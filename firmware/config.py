"""Duet-MIDI PCB wiring and initial, uncalibrated hardware settings."""
import board

TOUCH_PINS = (board.IO1, board.IO2, board.IO4, board.IO5,
              board.IO6, board.IO7, board.IO8, board.IO9)
SLIDER_PIN = board.IO10
ENCODER_A_PIN = board.IO11
ENCODER_B_PIN = board.IO12
I2C_SDA_PIN = board.IO13
I2C_SCL_PIN = board.IO44
MCP23008_ADDRESS = 0x20
BUTTON_MODE = 0
BUTTON_OCTAVE_DOWN = 1
BUTTON_OCTAVE_UP = 2
BUTTON_FUNCTION = 3
BUTTON_ENCODER = 4

LED_PIN = board.IO43  # External chain, not board.NEOPIXEL (GPIO21).
LED_COUNT = 8
# Pad 1..8 -> chain positions 0..7. Confirm the desired association on hardware.
# Electrical chain: D4 -> D3 -> D2 -> D1 -> D5 -> D6 -> D7 -> D8.
PAD_LED_INDICES = (0, 1, 2, 3, 4, 5, 6, 7)
LED_BRIGHTNESS = 0.08
LED_PIXEL_ORDER = "GRB"  # Verify with a red/green/blue test.
LED_UPDATE_INTERVAL = 0.033

MELODY_NOTES = (60, 62, 64, 65, 67, 69, 71, 72)
DRUM_NOTES = (36, 38, 42, 46, 41, 43, 49, 51)
MELODY_CHANNEL = 0  # MIDI channel 1, zero based.
DRUM_CHANNEL = 9    # MIDI channel 10, zero based.
NOTE_VELOCITY = 100
MIN_OCTAVE_SHIFT = -2
MAX_OCTAVE_SHIFT = 2

CALIBRATION_SAMPLES = 40
CALIBRATION_INTERVAL = 0.025
TOUCH_PRESS_RATIO = 1.20
TOUCH_RELEASE_RATIO = 1.10
TOUCH_DEBOUNCE_SECONDS = 0.020
BUTTON_DEBOUNCE_SECONDS = 0.030

SLIDER_CC = 1  # Modulation; software instrument must listen to this CC.
SLIDER_ADC_MIN = 0
SLIDER_ADC_MAX = 65535
SLIDER_INVERT = False
SLIDER_FILTER_ALPHA = 0.20
SLIDER_CC_STEP = 2
CONTROL_UPDATE_INTERVAL = 0.020

ENCODER_CC = 7  # Channel volume; host mapping may need configuration.
ENCODER_INITIAL_VALUE = 64
ENCODER_DIRECTION = 1  # Change to -1 if clockwise decreases.
ENCODER_DIVISOR = 4    # Confirm counts per detent on the purchased encoder.
