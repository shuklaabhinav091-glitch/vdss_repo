# What goes in this repo (and what never does)

Read this before your first commit. If in doubt, ask in #firmware or #operations before pushing.

## OK to commit
- Functional architecture, block diagrams, control-loop structure
- Outcome **targets** (always labelled "design target")
- Applications, roadmap, fabrication materials
- Analysis code and *reviewed* results from Test Protocol v1

## NEVER commit (NDA-gated)
| Category | Where it lives instead |
|---|---|
| Firmware thresholds, timings, calibration constants | `firmware/include/config.h` (gitignored) |
| Sensor-fusion / pressure-to-angle math | `firmware/src/fusion_private.cpp` (gitignored) |
| Hardware drivers naming specific parts | `firmware/src/hal_private.cpp` (gitignored) |
| Wiring diagrams, pin maps | private drive / private repo |
| BOM, part numbers, pricing | private drive |
| Native SolidWorks files | private drive (renders go in the deck) |

In public text use functional terms: "laser-scattering PM sensor", "differential-pressure pitot pair", "servo-driven mist ring".

## Data honesty
- No performance number goes in README, docs or slides as "measured" until it comes out of Test Protocol v1 analysis and is reviewed.
- `analysis/data/sample/synthetic_*` is random test data for checking the pipeline. **Never cite it.**

## If you leaked something
Don't just delete it in a new commit — it stays in git history. Tell the founder immediately; the history has to be rewritten and any exposed value treated as public.
