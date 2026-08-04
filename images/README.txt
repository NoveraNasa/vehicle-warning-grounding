Synthetic dashboard warning evaluation images
================================================

Files used by src/evaluate_classifier.py:

- oil_pressure.jpg         red oil-can warning
- engine_temperature.jpg   red coolant-temperature warning
- battery.jpg              red charging-system warning
- brake_system.jpg         red brake-system warning
- tire_pressure.jpg        amber tire-pressure (TPMS) warning
- unknown.jpg              blue high-beam symbol, intentionally outside the five classes

Instructions
------------

1. Copy the six JPG files into vehicle-warning-grounding/images/.
2. Replace the old files when Finder asks.
3. Do not copy preview.jpg into the images folder; it is only a contact sheet.
4. Run: python src/evaluate_classifier.py

These are synthetic, vector-style evaluation fixtures created without external
image assets. They may be used and modified for this demonstration project.

Important limitation
--------------------

This is a small functional test set, not evidence of real-world model accuracy.
A research-quality evaluation should include many real dashboard photographs,
different vehicles, lighting conditions, viewing angles, and ambiguous cases.
