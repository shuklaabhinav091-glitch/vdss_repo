# Test Protocol v1 (bench) — outline

> Fill in with the final protocol. Results from this protocol are the ONLY numbers that may later be called "measured (bench)".

## Objective
Compare closed-loop VDSS against a baseline on the bench, for:
1. Mean PM10 at the measurement point
2. Water used per trial
3. Sense-to-actuate response time

## Conditions
| Condition | Description |
|---|---|
| `baseline` | _define: no suppression / continuous spray_ |
| `vdss` | closed-loop tracking enabled |

## Setup
- Dust/smoke source: _TBD_
- Wind source: fan at _TBD_ settings, plus direction changes during the run
- Measurement point: _TBD distance/position_
- Trial length: _TBD_ s; minimum trials per condition: _TBD_ (≥ 3, more is better)

## Logging
Controller logs CSV over serial at 10 Hz:
`t_ms,pm10,pm25,flow_lpm,bearing_deg,est_valid,spray,aim_deg`
Add `trial_id` and `condition` columns when saving to `analysis/data/raw/`.

## Analysis
`python analysis/protocol_v1_analysis.py data/raw/<file>.csv`
Reports per-condition mean ± SD, 95% CI (t-distribution), % reduction and Welch t-test.

## Reporting rule
Always state: bench conditions, number of trials, mean ± SD, 95% CI. Never extrapolate bench results to field performance.
