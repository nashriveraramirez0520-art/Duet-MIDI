# BOM draft: quantities extracted, sourcing still pending

`BOM.csv` now contains the components required for one assembled Duet-MIDI, plus its enclosure and connection hardware. Prices, suppliers and purchase links are blank where no exact part/order has been selected. This is **not a priced, submission-ready BOM**. Do not treat blank amounts as zero.

The inventory was extracted from the routed PCB, rather than estimated from the reference tutorial:

| References | Quantity | Requirement |
| --- | ---: | --- |
| U1 | 1 | Waveshare ESP32-S3-Zero; fixed male-header mounting |
| U2 | 1 | MCP23008, DIP-18, 7.62 mm row spacing |
| U3 | 1 | 74AHCT125, SOIC-14 narrow 3.9 mm body, 1.27 mm pitch |
| D1-D8 | 8 | SK6812MINI-E RGB, reverse mount, 3.2 x 2.8 mm |
| SW1, SW3-SW5 | 4 | 6 x 6 mm through-hole pushbuttons, 4.3 mm model height |
| SW2 | 1 | Switched vertical EC11-type encoder matching the Alps EC11E-Switch footprint |
| RV1 | 1 | 10 kOhm linear Bourns PTA3043-compatible slide pot, 30 mm travel |
| C1-C10 | 10 | 100 nF ceramic, 0805; choose voltage rating suitable for 5 V rails |
| R1, R2, R3, R7 | 4 | 10 kOhm, 0805 |
| R4, R5 | 2 | 4.7 kOhm, 0805 |
| R6 | 1 | 330 Ohm, 0805 |

The eight touch pads (J1) are copper features on the PCB, not eight purchased sensors or a pin header. H1-H4 are mounting holes, not purchased electrical components. The PCB file labels the fourth hole `REFH4`; it still represents the fourth M2 mounting position.

## Decisions before purchasing

- **Encoder:** the imported generic 3D model has a slight mounting-pin mismatch with the assigned footprint. Select an exact part using its datasheet and compare pin spacing, body, shaft D-flat, thread and push travel. The knob is not proof that every EC11 part fits.
- **Slider:** confirm the complete orderable part number, pin locations, travel, resistance/taper and actuator dimensions. Do not order solely from the label "10K". Its 3D transform was corrected locally after the originally uploaded KiCad sources; preserve the user's latest KiCad file.
- **Pushbuttons:** the enclosure extensions assume the 4.3 mm-height model. A taller button changes the fit.
- **Headers:** two 1x9 strips, 2.54 mm pitch, male only. The user has a header kit; no extra purchase is budgeted for those strips. Confirm actual mounting height.
- **Screws/nuts:** four M2 through screws and four nuts. Screw length, head dimensions and any required washers still need selection against the actual stack. Mounting positions are shared by the PCB, case and lid.
- **PCB:** CSV quantity is one assembled board. Use the fabrication supplier's actual minimum order quantity and shipping when pricing; do not calculate an order for one if the supplier requires five.
- **Printing:** eight pieces total: bottom, lid, four buttons, knob and slider cap. Printing charges depend on the actual service/material, supports and revised lid geometry; obtain the real quote.
- **Acrylic:** separate 1 mm bottom window, nominal 85.6 x 65.6 mm with R3.8 corners. Include cutting/adhesive costs if they are not already available.
- **LED update:** LED apertures and downward hollow tubes were added in Onshape after the repository's enclosure V1 export. Obtain the revised Top Cover STEP before final manufacturing exports. Transparent light-pipe inserts remain optional/unselected and are not counted as already purchased.
- **USB:** one data-capable cable with USB-C at the board end; choose the other end to suit the computer.

For budget submission, include actual pack quantities, shipping, taxes if required by the program, and links to the exact variants. Spare components can be bought in larger packs, but label pack pricing separately from per-board quantities.
