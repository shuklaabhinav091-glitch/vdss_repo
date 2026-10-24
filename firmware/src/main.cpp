// VDSS edge controller — main loop (10 Hz)
//
// sense -> fuse -> decide -> act -> log
//
// Real config lives in include/config.h (gitignored). If it is missing,
// the build falls back to placeholder values so CI / reviewers can compile.
#if __has_include("config.h")
  #include "config.h"
#else
  #warning "config.h not found - using config.example.h placeholders (not for hardware)"
  #include "config.example.h"
#endif

#include <Arduino.h>
#include "vdss.h"

namespace vdss {

// ---------------------------------------------------------------------------
// Weak default stubs. Real implementations in src/*_private.cpp override these.
// ---------------------------------------------------------------------------
__attribute__((weak)) void halBegin() {}

__attribute__((weak)) bool halRead(Reading& r) {
  r = Reading{0, 0, 0, 0, 0, false};
  return false;
}

__attribute__((weak)) void halSetPump(bool) {}
__attribute__((weak)) void halAim(float) {}

__attribute__((weak)) Estimate fuse(const Reading&) {
  return Estimate{RING_ARC_DEG / 2.0f, 0.0f, false};  // hold centre
}

// ---------------------------------------------------------------------------
// Decision: spray only when dust is present, aim at the estimated plume.
// Hysteresis prevents pump chatter around the threshold.
// ---------------------------------------------------------------------------
Command decide(const Reading& r, const Estimate& e, bool spraying) {
  Command c{spraying, e.valid ? e.bearingDeg : RING_ARC_DEG / 2.0f};
  if (!r.pmValid) {
    c.spray = false;  // fail-safe: no valid PM reading -> no spray
    return c;
  }
  if (!spraying && r.pm10 > PM_ON_THRESHOLD)  c.spray = true;
  if (spraying  && r.pm10 < PM_OFF_THRESHOLD) c.spray = false;
  c.aimDeg = constrain(c.aimDeg, 0.0f, RING_ARC_DEG);
  return c;
}

}  // namespace vdss

// ---------------------------------------------------------------------------
static const unsigned long kPeriodMs = 1000UL / VDSS_LOOP_HZ;
static unsigned long lastTick = 0;
static bool spraying = false;

static void logCsv(unsigned long t, const vdss::Reading& r,
                   const vdss::Estimate& e, const vdss::Command& c) {
  // t_ms,pm10,pm25,flow_lpm,bearing_deg,est_valid,spray,aim_deg
  Serial.print(t);            Serial.print(',');
  Serial.print(r.pm10, 1);    Serial.print(',');
  Serial.print(r.pm25, 1);    Serial.print(',');
  Serial.print(r.flowLpm, 2); Serial.print(',');
  Serial.print(e.bearingDeg, 1); Serial.print(',');
  Serial.print(e.valid);      Serial.print(',');
  Serial.print(c.spray);      Serial.print(',');
  Serial.println(c.aimDeg, 1);
}

void setup() {
  Serial.begin(115200);
  vdss::halBegin();
  Serial.println(F("t_ms,pm10,pm25,flow_lpm,bearing_deg,est_valid,spray,aim_deg"));
}

void loop() {
  const unsigned long now = millis();
  if (now - lastTick < kPeriodMs) return;
  lastTick = now;

  vdss::Reading r;
  vdss::halRead(r);
  const vdss::Estimate e = vdss::fuse(r);
  const vdss::Command  c = vdss::decide(r, e, spraying);

  vdss::halAim(c.aimDeg);
  vdss::halSetPump(c.spray);
  spraying = c.spray;

  logCsv(now, r, e, c);
}
