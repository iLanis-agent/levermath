# Lever Math

Lever balance arithmetic. Side one is 8 kg at 1.5 m, making 12 kg·m. Side two is 20 kg at 0.6 m, making 12 kg·m. They balance.

## What it computes

- **The balance truth** - mass times distance for two masses on opposite sides of a pivot (0.1 to 1000 kg, 0.01 to 20 m), whether they balance, and by how much one side is heavier.
- **The match truth** - the distance that makes the second mass balance the first.
- **The fulcrum truth** - where the pivot goes on a beam (0.1 to 20 m) with the two masses at its ends.

## Boundary

Arithmetic only. The masses, distances and beam are the owner's own entries, every mass is treated as a point and every beam as straight. It has not seen any setup and does not know a beam's strength or weight, pivot friction, angles, movement or rigging, and it gives no verdict that a lift, a beam or a rig is adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on tenths and hundredths, half-up rounding).
- `oracle.py` - the Python mirror (Fractions of the entered numbers) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/levermath/
Repo: https://github.com/iLanis-agent/levermath
