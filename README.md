# OpenPCB

[![CI](https://github.com/Monotoba/OpenPCB/actions/workflows/ci.yml/badge.svg)](https://github.com/Monotoba/OpenPCB/actions/workflows/ci.yml)
[![Python 3.11–3.12](https://img.shields.io/badge/python-3.11%E2%80%933.12-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52.svg)](https://doc.qt.io/qtforpython-6/)
[![License: BSD-2-Clause](https://img.shields.io/badge/license-BSD--2--Clause-blue.svg)](LICENSE)
[![Status: early development](https://img.shields.io/badge/status-early_development-orange.svg)](#project-status)

OpenPCB is an early-stage, cross-platform desktop workspace for PCB fabrication. The
project aims to bring board visualization, CAM preparation, job management, and machine
control into one application for hobbyists and small shops.

> [!IMPORTANT]
> OpenPCB is a project in progress and is **not ready for production use**. The application
> currently provides its GUI and configuration foundation; PCB import, CAM generation, and
> machine control remain planned work.

## Project status

The current prototype includes:

- A PySide6 main-window scaffold with menus, toolbars, and dockable panels
- Persistent, validated settings using Pydantic
- Display, HiDPI, and workspace preference pages
- Platform-specific settings storage and window-geometry persistence
- Automated tests for the configuration layer

The following major capabilities are not implemented yet:

- Gerber, Excellon, SVG, raster, and G-code import
- Interactive board and toolpath visualization
- Isolation, drilling, outline, raster, and panelization CAM operations
- Post-processing and machine communication
- Project persistence and distributable desktop builds

See the [development backlog](docs/BACKLOG.md) and
[Phase 1 report](docs/PHASE1-PROGRESS.md) for more detail.

## Try the prototype

OpenPCB requires Python 3.11 or 3.12. The simplest development setup uses
[uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/Monotoba/OpenPCB.git
cd OpenPCB
uv sync --extra dev
uv run openpcb
```

The window is currently a functional shell: it lets you explore the preferences and layout,
but it does not yet process PCB files.

You can also exercise the small command-line scaffold:

```bash
uv run openpcb --echo "OpenPCB is running"
```

## Development

Run the checks used by CI:

```bash
uv sync --extra dev
uv run pytest
uv build
```

The existing helper scripts remain available:

```bash
./setup.sh
./run.sh
./test.sh
```

The source layout reflects the intended architecture. Modules that are still empty are
placeholders for planned work, not completed features.

```text
openpcb/
├── config/       # Implemented settings models and persistence
├── ui/           # Implemented application shell and preferences
├── cam/          # Planned CAM operations
├── importers/    # Planned PCB and toolpath importers
├── post/         # Planned post-processors
├── sender/       # Planned device communication
├── storage/      # Planned project persistence
└── viewer/       # Planned interactive viewer
```

## Contributing

Contributions are welcome, especially focused changes that advance an item in the backlog.
Before starting a large feature, please open an issue to discuss scope and architecture.

When submitting a change:

1. Keep unfinished behavior clearly identified as experimental or planned.
2. Add or update tests for implemented behavior.
3. Run `uv run pytest` and `uv build` locally.
4. Describe what is working now and what remains outside the change.

## Documentation

- [Documentation index](docs/INDEX.md)
- [Project specification](docs/SPEC-1-OpenPCB.md)
- [Phase 1 architecture](docs/PHASE1-ARCHITECTURE-CONFIG.md)
- [Deployment notes](docs/DEPLOYMENT.md)
- [Risk register](docs/07-RiskRegister.md)

## License

OpenPCB is available under the [BSD 2-Clause License](LICENSE).
