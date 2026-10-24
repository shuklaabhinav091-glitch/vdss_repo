// vdss.h — public interfaces for the VDSS control loop.
//
// The loop is: sense() -> fuse() -> decide() -> act() -> log().
// Hardware drivers and sensor-fusion math are implemented in
// src/*_private.cpp (gitignored). This repo ships weak default
// stubs so it always compiles, even without the private files.
#pragma once
#include <Arduino.h>

namespace vdss {

struct Reading {
  float pm10;          // particulate concentration (ug/m3)
  float pm25;
  float dpA;           // differential pressure, pitot A (raw/scaled)
  float dpB;           // differential pressure, pitot B
  float flowLpm;       // water flow (L/min)
  bool  pmValid;
};

struct Estimate {
  float bearingDeg;    // estimated plume bearing, 0..RING_ARC_DEG
  float windSpeed;     // m/s (estimate)
  bool  valid;
};

struct Command {
  bool  spray;
  float aimDeg;
};

// --- Hardware abstraction (override in hal_private.cpp) ---
void halBegin();
bool halRead(Reading& r);
void halSetPump(bool on);
void halAim(float deg);

// --- Fusion (override in fusion_private.cpp) ---
Estimate fuse(const Reading& r);

// --- Decision logic (public) ---
Command decide(const Reading& r, const Estimate& e, bool spraying);

}  // namespace vdss
