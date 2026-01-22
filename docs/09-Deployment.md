# Deployment & Serial/USB Setup

## Qt Deployment Checklist (PyInstaller / PySide6)
- Use virtualenv, pin versions, test with QT_DEBUG_PLUGINS=1.
- Include platform/style/imageformats/printsupport plugins.
- Windows: MSVC toolset, code-sign installer, VC++ redist.
- macOS: app bundle with @rpath frameworks, codesign + notarize, Gatekeeper check.
- Linux: AppImage packaging, test on clean VM.
- Runtime: qt.conf to force plugin paths, include license notices.

## Serial/USB Setup Guide
### Windows
- Drivers: FTDI (0403:6001), CP210x (10c4:ea60), CH340 (1a86:7523).
- Troubleshoot: Device Manager, USB power saving.

### macOS
- Built-in drivers for common adapters; avoid unsigned kexts; notarized app.

### Linux
- Add user to `dialout`; udev rules sample:
```
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666", GROUP="dialout"
```

## Safety & Preflight
- Verify work envelope vs job bbox, set origin/units, dry-run with spindle/laser disabled, test hold/resume/reset.
