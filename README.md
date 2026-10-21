# Duet-MIDI

A dual-mode USB MIDI controller for melodies and drum pads, designed for **Hack Club Half Life — Week 3: Music**.

**Status: concept and project setup.** Hardware selection, schematic, PCB layout, enclosure, and firmware are still in development. No hardware has been built or tested.

## The idea

Duet-MIDI will use the same eight capacitive touch pads in two modes:

- **Melody mode:** play a scale and shift the octave with dedicated buttons.
- **Drum mode:** trigger eight percussion sounds in a connected music application.

A mode button will switch the pad mapping, with RGB feedback indicating the active mode. An encoder and a slider will provide additional MIDI controls.

Duet-MIDI is a controller, not a standalone synthesizer. A computer running a software instrument or drum sampler will generate the sound.

## Planned controls

| Control | Quantity | Intended function |
| --- | --- | --- |
| Capacitive touch pad | 8 | Play notes or trigger drum sounds |
| Mechanical button | 4 | Mode, octave down, octave up, and one assignable function |
| Rotary encoder | 1 | Adjust an assignable MIDI control |
| Slide potentiometer | 1 | Send an assignable continuous MIDI control |
| RGB lighting | TBD | Indicate the active mode and pad activity |
| USB connection | 1 | MIDI data and power |

These are design targets, not a finalized parts list. Touch input will initially use fixed, adjustable note velocity; pressure-sensitive playing is outside the initial scope.

## Intended operation

1. Connect the controller to a computer using a USB data cable.
2. Select Duet-MIDI as a MIDI input in compatible music software.
3. Load a software instrument or drum sampler.
4. Choose melody or drum mode and play the pads.
5. Use the octave buttons, encoder, and slider to adjust the performance.

This workflow is planned and has not yet been verified on a device.

## Design approach

- Design the schematic and PCB in **KiCad**.
- Verify the microcontroller's native USB MIDI support, exposed touch-capable GPIOs, ADC inputs, and pin budget before wiring.
- Match component footprints to the exact parts selected for purchase.
- Keep touch sensing and RGB power requirements in mind during layout.
- Design a separate enclosure in **Onshape** after the PCB dimensions and control positions are established.
- Implement and test basic USB MIDI first, followed by touch calibration, both modes, controls, and lighting.

## Repository

| Location | Contents |
| --- | --- |
| [pcb/](pcb/) | KiCad source and future manufacturing exports |
| [firmware/](firmware/) | Firmware plan and future source code |
| [cad/](cad/) | Enclosure CAD and future printable exports |
| [docs/design-plan.md](docs/design-plan.md) | Scope, initial behavior, and decisions to resolve |
| [docs/images/](docs/images/) | Future progress screenshots and renders |
| [JOURNAL.md](JOURNAL.md) | Development journal |
| [BOM.csv](BOM.csv) | Parts-list template; sourcing is not complete |

## Milestones

- [x] Define the dual-mode concept.
- [x] Create the repository and documentation structure.
- [ ] Choose the controller board and verify a feasible pin assignment.
- [ ] Select exact controls and prepare the component budget.
- [ ] Complete the schematic and review electrical rule checks.
- [ ] Create the touch-pad footprints and complete PCB routing.
- [ ] Review design rule checks and manufacturing constraints.
- [ ] Prepare initial firmware and document the build environment.
- [ ] Design the enclosure and check component access.
- [ ] Export manufacturing files and finalize the BOM.
- [ ] Assemble the hardware and test with music software.

## Reference and attribution

The starting reference is [Kai Pereira's MIDI Keypad tutorial](https://github.com/KaiPereira/MIDI-Keypad). Duet-MIDI will develop its own layout, two-mode interaction, and enclosure. Any reused source files or libraries will retain their applicable attribution and license notices.

Project by **Nash Andrés Rivera Ramírez**.
