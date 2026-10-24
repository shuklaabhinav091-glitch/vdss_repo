# VDSS — Vanguard Dust Suppression System

**Sensor-driven, closed-loop mist suppression for jaw-crusher discharge points.**
Edge-computed control that tracks the dust plume using wind direction and particulate readings, and aims a rotating mist ring at it, instead of spraying a fixed zone all the time.

> **Status: BENCH-STAGE PROTOTYPE.** Not field-tested.
> Every performance figure in this repo is a **design target / engineering estimate** until Test Protocol v1 is complete. Nothing here is a field-measured or validated result.

Built at RIIDL, Somaiya Vidyavihar University, Mumbai. Vishwakarma Awards 2026–27 entry.

---

## How it works (functional architecture)

```
 ┌───────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
 │ Laser-scattering  │   │ Orthogonal pitot     │   │ Water flow sensor    │
 │ PM sensor         │   │ pair (wind vector)   │   │                      │
 └─────────┬─────────┘   └──────────┬───────────┘   └──────────┬───────────┘
           └────────────────┬───────┴──────────────────────────┘
                            ▼
              ┌───────────────────────────┐
              │ Edge controller (10 Hz)   │
              │ sense → fuse → decide     │
              └─────────────┬─────────────┘
                            ▼
              ┌───────────────────────────┐
              │ Servo-driven 8-nozzle     │
              │ mist ring (~270° arc)     │
              └───────────────────────────┘
```

1. **Sense** — particulate concentration, wind vector, water flow.
2. **Fuse** — estimate where the plume is heading.
3. **Decide** — spray only when dust is present, only where it is going.
4. **Act** — rotate the mist ring to the plume bearing; log everything.

## Design targets (NOT measured)

| Metric | Target | Status |
|---|---|---|
| PM10 reduction at discharge point | 88–93% | Design target — to be tested under Test Protocol v1 |
| Water saving vs. continuous spray | ~36% | Design target |
| Sense-to-actuate response | ~0.3 s | Design target |

## Repo layout

| Path | What lives here |
|---|---|
| `firmware/` | PlatformIO project for the edge controller |
| `analysis/` | Test Protocol v1 analysis (Python / pandas) |
| `cad/` | Renders and neutral exports (STEP/STL) — no native SolidWorks files |
| `hardware/` | Public-safe block diagrams only |
| `docs/` | Test protocol, roadmap, media for the competition |

## Build (firmware)

```bash
cd firmware
cp include/config.example.h include/config.h   # fill real values locally — never commit
pio run                                         # build
pio run -t upload                               # flash
pio device monitor -b 115200
```

## Run analysis

```bash
cd analysis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python protocol_v1_analysis.py data/sample/sample_run.csv
```

## Roadmap

- [ ] Bench POC complete + 60 s smoke/fan/servo tracking video
- [ ] Test Protocol v1 runs (baseline vs. VDSS, repeated trials)
- [ ] Vishwakarma Stage 3 prototype submission
- [ ] Quarry pilot

## Disclosure note

Calibration constants, control thresholds, wiring/pin maps, BOM and the sensor-fusion math are **not in this repository**. See `docs/IP_POLICY.md`.

© 2026 Vanguard DSS. All rights reserved. No license is granted to use, copy or modify this code.
