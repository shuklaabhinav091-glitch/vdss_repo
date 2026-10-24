// config.example.h — PLACEHOLDER values only.
//
// Copy to config.h and fill real values locally:
//     cp include/config.example.h include/config.h
//
// config.h is gitignored. Real thresholds, pin maps and timings are
// NDA-gated and must never be committed or shown publicly.
#pragma once

// ---- Loop timing ----
#define VDSS_LOOP_HZ          10      // control loop rate (public: 10 Hz)

// ---- I/O (PLACEHOLDERS — set in config.h) ----
#define PIN_PM_RX             0
#define PIN_PM_TX             0
#define PIN_PITOT_A           0
#define PIN_PITOT_B           0
#define PIN_FLOW              0
#define PIN_PUMP              0
#define SERVO_CHANNEL         0

// ---- Control thresholds (PLACEHOLDERS) ----
#define PM_ON_THRESHOLD       0.0f    // start spraying above this
#define PM_OFF_THRESHOLD      0.0f    // stop spraying below this (hysteresis)

// ---- Mist ring geometry ----
#define RING_ARC_DEG          270.0f  // usable sweep (public)
#define SERVO_MIN_PULSE       0
#define SERVO_MAX_PULSE       0
