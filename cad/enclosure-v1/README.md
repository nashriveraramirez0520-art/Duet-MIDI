# Duet-MIDI enclosure V1

This is the first enclosure version for Duet-MIDI. The CAD and printable files are prepared, but I still need to print the small controls and check their fit on the actual hardware before printing the whole case.

## Files

- `step/`: eight individual solid parts in their assembly positions.
- `stl/`: the same eight parts, individually centered in XY and placed on Z=0, in millimeters. The top cover is flipped so its outer face faces the build plate and its posts point upward. These are starting orientations; review supports and first-layer contact in the slicer.
- `enclosure-v1-assembly.step.gz` (decompress with gzip or 7-Zip to obtain the STEP): reference assembly combining the latest electronics, the eight individual parts, and the corrected encoder knob. The encoder solid was retained from the previous full export because it was hidden in the last one. It preserves solid positions, but does not contain the Onshape feature history, materials, or original part labels.
- `validation.json`: mesh checks and approximate bounding dimensions. Tiny deviations in mesh bounds do not represent a design dimension change.

Print one of each of the eight STL files. Buttons 1 through 4 are separate files; they are four physical buttons, not four alternative designs.

## Design

The footprint is 105 x 96.75 mm. The main enclosure is 18.5 mm high, plus 2 mm feet; the knob and slider grip extend above the lid. There is a common opening over the touch area, a slot for the slider, four button extensions, a USB opening, and a separate encoder knob.

The case and lid share the four M2 PCB mounting positions at X=+/-46 mm and Y=+/-41.875 mm. Printed clearance holes are 2.4 mm. The underside of each lid post ends at Z=8.6 mm, based on a nominal 1.6 mm PCB resting at Z=7 mm; the imported substrate is 1.51 mm thick. Confirm the actual stack before tightening. The screws go in from below and nuts sit above the lid; there are no nuts between the PCB and the lid posts. Screw length and head fit still need checking against the chosen hardware.

The encoder knob has a nominal 6.3 mm circular diameter in its D-shaped socket and an 8 mm lower relief. The slider cap has a 2.1 x 5.3 mm rectangular socket, 4.5 mm deep. Both controls start at Z=20 mm, giving 1.5 mm above the lid.

The ESP32 mounting choice is fixed male headers, without female sockets, targeting about 2.5 mm between the main PCB top and the module underside. Check the actual assembled height.

## Separate bottom window

The bottom window was designed for 1 mm acrylic: 85.6 x 65.6 mm with 3.8 mm corner radii. The pocket is 86 x 66 mm and 1.2 mm deep; the through-opening is 80 x 60 mm. Confirm the pocket against the actual cut acrylic and adhesive. The window is not included among the eight printed parts.

## Checks and next steps

Each individual STEP imports as one valid solid. Each STL has two incident triangles per mesh edge after welding coincident coordinates, with no degenerate triangles in that check. These mesh checks do not establish physical fit or electrical operation.

The earlier assembled CAD check found no case/electronics solid intersections and no slider/cap collisions with the case, knob, or button extensions at Y offsets -15, 0, and +15 mm. This checks those three positions, not a continuous motion simulation. The corrected knob was checked against the imported encoder. The model of the encoder is generic, so check the actual purchased shaft before relying on its socket dimensions.

Print one button, the encoder knob, and the slider cap first. Check button travel and retention, knob rotation and push travel, and slider grip retention. Then check the complete slider travel, USB cable overmold, real PCB thickness, acrylic fit, and screw stack. The bottom case has integral feet, so inspect the underside in the slicer and add supports as needed; it is not a verified support-free print.

No physical prototype, fit test, slicing validation, or electronics test has been completed for this enclosure version.

Source: [Onshape document](https://cad.onshape.com/documents/5af46204eeb29ad0fa03019d/w/52b0aef6fb09ac80a2bff0bc/e/92c0bc1531caa20fbf243b4c).
