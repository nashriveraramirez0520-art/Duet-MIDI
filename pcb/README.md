# PCB files

The schematic, routed PCB, project rules, custom libraries, and manufacturing exports are here. Open `Duet-MIDI.kicad_pro` in KiCad 10 with the folder structure intact.

## Libraries

`Duet.pretty` contains the eight-pad touch footprint. The project-local `fp-lib-table` also registers `libraries/Hackclub.pretty` under its original name, **Hackclub Footprints**. `sym-lib-table` registers the supplied **Hackclub Symbols** library. Standard components use KiCad's installed libraries.

The Waveshare 3D model is optional and is not bundled here. To display it, download the upstream Hackclub KiCad Libraries and set `HACKCLUB_3DMODEL_DIR` to its `3D models` folder. Missing 3D models do not remove the component footprints from the PCB.

## Board and exports

- Board outline: 100 × 91.75 mm; two copper layers; nominal thickness 1.6 mm.
- Four 2.2 mm non-plated mounting holes for M2 hardware.
- Eight routed openings for the reverse-mount LEDs.
- Seven Gerber layers, separate plated/non-plated drill files, and a Gerber job file are in `gerbers/`.
- `Duet-MIDI-Gerbers.zip` contains the manufacturing export reviewed in Gerber Viewer.

The PCB, schematic, project, and custom rule files are the uploaded design files, unchanged. Only the library registration tables were adjusted for portability. The exports are from the earlier fabrication export in the same design session; regenerate them after any further board edits.

## Checks and remaining work

The supplied routing screenshot shows zero DRC violations and zero unconnected items, with schematic parity disabled. Five checks were ignored: missing courtyard, track endpoint not centered on via, tuning profile track geometries, footprint filter mismatch, and component type versus footprint-pad mismatch. A later parity check identified four PCB-only mounting footprints.

The older `.rpt` files in the uploaded archive predate the final routing fixes and are not included as a final passing report. Generate a fresh report from this project before placing an order.

The global copper-to-edge minimum is 0.50 mm. The custom rule in `Duet-MIDI.kicad_dru` allows 0.20 mm around LED footprint cutouts; the chosen manufacturer must accept that clearance. Exact purchased LED, slider, encoder, and switch variants still need to be matched to their footprints. Use an AHCT125 variant with the intended input thresholds rather than substituting an HC/AHC part without checking compatibility.

Hardware operation has not been tested. Touch calibration, MIDI behavior, RGB brightness/current limits, and the USB power budget remain part of firmware and prototype validation. Some 3D models are absent in the screenshots.
