# Initial design plan

## Goal

Build one USB MIDI controller that can play melodies and trigger percussion using the same eight capacitive pads.

## First-version scope

Eight touch pads, four mechanical buttons, one encoder, one slide potentiometer, and RGB feedback. Select exact parts and LED quantity after checking the pin budget, power budget, cost, and physical layout.

## Proposed behavior

| Input | Melody mode | Drum mode |
| --- | --- | --- |
| Pads 1–8 | Eight notes from the selected scale | Eight configurable drum notes |
| Mode button | Switch to drum mode | Switch to melody mode |
| Octave buttons | Shift melody mapping within valid MIDI note range | No remapping in the first version |
| Fourth button | Function to be selected | Function to be selected |
| Encoder | Assignable MIDI CC | Assignable MIDI CC |
| Slider | Assignable MIDI CC | Assignable MIDI CC |

Initial melody mapping can be a C-major scale; exact defaults, channels, and drum note numbers remain to be confirmed against the target software. Notes should support simultaneous touches.

## Firmware requirements

- Send Note On when a pad becomes active and the corresponding Note Off when it is released.
- Track the original note and channel for every active pad.
- Release active notes before changing mode or octave so notes do not get stuck.
- Debounce mechanical buttons and decode the encoder.
- Calibrate touch input and use thresholds with hysteresis.
- Smooth and limit slider updates to avoid unnecessary MIDI traffic.
- Use fixed, adjustable velocity initially; do not claim pressure sensing.
- Define startup behavior for pads that are already being touched.
- Confirm MIDI output in a monitor and then in a software instrument.

## Hardware decisions still open

1. Controller board and USB MIDI firmware platform.
2. Eight exposed touch-capable pins, an ADC pin, digital control pins, and RGB data.
3. Whether the encoder push switch will be used; it is not included in the initial pin budget.
4. Exact switch, encoder, slider, and RGB part numbers.
5. RGB supply, current limit, decoupling, and any signal-level conversion.
6. Touch-pad shape, spacing, surface finish, and enclosure openings.
7. USB access, mounting points, and final board dimensions.

Do not assign schematic pins or order components until the relevant board documentation and part drawings have been checked.

## Validation plan

Review schematic rules, pin functions, footprint dimensions, PCB rules, USB and power requirements, enclosure clearances, and procurement files. Physical tests must then establish touch reliability, simultaneous notes, mode changes, MIDI recognition, slider behavior, and lighting stability.
