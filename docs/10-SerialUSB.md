# Serial/USB Setup Guide

## Discovery & Speeds
COM* (Windows), /dev/tty.* (macOS), /dev/ttyUSB* & /dev/ttyACM* (Linux). Typical 115200; Marlin variant 250000.

## Windows
Drivers: FTDI, CP210x, CH340. Troubleshoot via Device Manager; disable USB power saving.

## macOS
Built-in drivers for common adapters; prefer notarized app; avoid unsigned kexts.

## Linux
Add user to `dialout`; udev rules samples included in DEPLOYMENT.md.

## Controller Notes
GRBL 1.1 (`?`, `!`, `~`), Marlin, Smoothie, LinuxCNC (TCP if possible), Mach3/4 (via plugin/TCP/serial), FANUC DNC drip-feed, HPGL.
