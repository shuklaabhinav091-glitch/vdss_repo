"""Capture the VDSS controller's serial CSV into a Test Protocol v1 data file.

The firmware prints:
    t_ms,pm10,pm25,flow_lpm,bearing_deg,est_valid,spray,aim_deg
This script prepends trial_id and condition to every row so the file can go
straight into analysis/protocol_v1_analysis.py.

Usage:
    pip install pyserial
    python tools/serial_logger.py --port /dev/cu.usbmodem1101 \
        --trial b1 --condition baseline --seconds 60

Find your port: `pio device list` (Mac ports look like /dev/cu.usbmodem*).
Ctrl+C stops early; whatever was captured is kept.
"""
from __future__ import annotations

import argparse
import time
from datetime import datetime
from pathlib import Path

import serial  # pyserial

HEADER = "t_ms,pm10,pm25,flow_lpm,bearing_deg,est_valid,spray,aim_deg"
RAW_DIR = Path(__file__).resolve().parents[1] / "analysis" / "data" / "raw"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", required=True)
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--trial", required=True, help="e.g. b1, v2")
    ap.add_argument("--condition", required=True, choices=["baseline", "vdss"])
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = args.out or RAW_DIR / f"{stamp}_{args.condition}_{args.trial}.csv"

    rows = 0
    with serial.Serial(args.port, args.baud, timeout=1) as ser, out.open("w") as f:
        time.sleep(2)              # UNO resets when the port opens
        ser.reset_input_buffer()
        f.write(f"trial_id,condition,{HEADER}\n")
        end = time.monotonic() + args.seconds
        print(f"Logging {args.condition}/{args.trial} for {args.seconds:.0f}s -> {out}")
        try:
            while time.monotonic() < end:
                line = ser.readline().decode("ascii", errors="ignore").strip()
                if not line or line.startswith("t_ms") or line.count(",") != 7:
                    continue       # skip header, boot noise, partial lines
                f.write(f"{args.trial},{args.condition},{line}\n")
                rows += 1
                if rows % 50 == 0:
                    print(f"  {rows} rows", end="\r")
        except KeyboardInterrupt:
            print("\nStopped early.")
    print(f"\nSaved {rows} rows to {out}")


if __name__ == "__main__":
    main()
