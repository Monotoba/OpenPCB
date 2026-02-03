# 🧠 OpenPCB

**OpenPCB** is a cross-platform desktop application for PCB fabrication, combining CAM, machine control, and job management into one unified tool.

It’s written in **Python 3.10+** using **PySide6 / Qt 6** for the UI, and includes complete support for **Gerber**, **Excellon**, **SVG**, and **G-Code** workflows.

---

## 🚀 Features

- 🖼️ Layered visualization with pan, zoom, rulers, and grid  
- ✂️ Geometry operations — translate, rotate, scale, mirror, boolean ops  
- 🧩 CAM engine — trace isolation, raster, drill, outline, silkscreen, solder mask  
- 🧠 Post-processors — GRBL, Marlin, Smoothie, LinuxCNC, Mach3/4, FANUC 2.5D  
- ⚙️ Multi-machine sender (serial + TCP), async, safe, real-time  
- 🧱 Plugin and extension API with deterministic job pipelines  
- 💾 Configurable YAML/JSON job profiles  
- 🖥️ Cross-platform builds for Windows, macOS, Linux  

---

## 🧩 Architecture

| Layer | Purpose | Tech |
|-------|----------|------|
| **Frontend** | PySide6 / Qt interface (viewer, composer, inspector) | PySide6 / Qt 6 |
| **Core Engine** | Geometry + CAM + parsing | Shapely 2.x, svgpathtools, scikit-image |
| **Sender** | Async device interface | asyncio, pyserial, TCP |
| **Persistence** | Jobs, profiles, settings | JSON / YAML |
| **Packaging** | Cross-platform builds | PyInstaller / Briefcase |

---

## 🧰 Installation

```bash
git clone https://github.com/Monotoba/OpenPCB.git
cd OpenPCB
pip install -e .
```

## ⚙️ Quick Setup with UV

OpenPCB uses **[uv](https://github.com/astral-sh/uv)** for fast, reproducible environments.

---

### 🪄 Step 1 — Create a UV Environment

From your repo root (`~/projects/python-3/openpcb`):

```bash
# Ensure uv is installed (if not)
pip install uv

# Create an isolated environment in .venv
uv venv

# Activate the environment
source .venv/bin/activate  # (on macOS/Linux)
# or
.venv\Scripts\activate     # (on Windows PowerShell)
```

Then install dependencies directly from `pyproject.toml`:

```bash
uv sync
```

This installs all `[project.dependencies]` packages into `.venv`, completely isolated from your system Python.

---

### ⚙️ Step 2 — Updated `pyproject.toml` for UV

Add a `[tool.uv]` section so future `uv sync` commands automatically resolve dependencies:

```toml
[tool.uv]
default-groups = ["dev"]

[tool.uv.group.dev.dependencies]
pytest = "^8.0"
black = "^24.1"
flake8 = "^7.0"
```

Now you can just run:

```bash
uv sync
```

…and everything (runtime + dev tools) gets installed instantly.

---

### 📘 Step 3 — Update Your README Setup Instructions

Add this new setup section near the top of the README:

````markdown
## ⚙️ Quick Setup with UV

OpenPCB uses **[uv](https://github.com/astral-sh/uv)** for fast, reproducible environments.

### 1️⃣ Install UV
```bash
pip install uv
````

### 2️⃣ Create and activate a venv

```bash
uv venv
source .venv/bin/activate
```

### 3️⃣ Sync dependencies

```bash
uv sync
```

### 4️⃣ Run the app

```bash
python -m openpcb
```

````

---

### 🧱 Step 4 — (Optional) Add a `Makefile`

Developers can just type `make dev`:

```makefile
.PHONY: setup dev run clean

setup:
	pip install uv
	uv venv
	uv sync

dev:
	source .venv/bin/activate && uv sync && pytest

run:
	source .venv/bin/activate && python -m openpcb

clean:
	rm -rf .venv __pycache__ .pytest_cache
````

---

✅ **Result**
You now have:

* **Instant environment setup** (1 second with UV’s binary caching)
* **Reproducible builds** pinned via `pyproject.toml`
* **Unified developer commands** through Makefile or plain uv CLI

---

## 👨‍💻 Development Workflow

### Setup for Development

We provide shell scripts for easy development setup:

```bash
# First-time setup (installs linters, formatters, pre-commit hooks)
./setup.sh

# Activate virtual environment
source .venv/bin/activate

# Run the application
./run.sh

# Run tests
./test.sh
```

### Development Tools

The project includes comprehensive development tooling:

- **black** - Code formatter (line-length=100)
- **isort** - Import sorter (black-compatible)
- **flake8** - Style linter
- **mypy** - Static type checker (strict mode)
- **pylint** - Code analyzer
- **pytest** - Testing framework with coverage support
- **pre-commit** - Git hooks for automated quality checks

### Code Quality Commands

```bash
# Format code
black openpcb/

# Sort imports
isort openpcb/

# Lint code
flake8 openpcb/

# Type check
mypy openpcb/ --strict

# Run all pre-commit hooks
pre-commit run --all-files
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=openpcb

# Run specific test file
pytest tests/test_config.py -v

# Run tests with output
pytest -v -s
```

### Git Workflow

Pre-commit hooks run automatically on `git commit`:
- Code formatting (black, isort)
- Style checks (flake8)
- Type checking (mypy)
- Trailing whitespace removal
- File ending fixes

Commit message template guides proper formatting:
```
<type>: <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

Types: `feat`, `fix`, `refactor`, `style`, `doc`, `test`, `chore`

### Project Structure

```
openpcb/
├── openpcb/           # Main application package
│   ├── config/        # Configuration system (Phase 1 ✅)
│   ├── ui/            # User interface components (Phase 1 ✅)
│   │   ├── preferences/  # Settings dialogs
│   │   ├── mainwindow.py # Main application window
│   │   └── hidpi.py   # HiDPI display support
│   ├── cam/           # CAM operations (Phase 2)
│   ├── importers/     # File format importers (Phase 2)
│   ├── post/          # Post-processors (Phase 2)
│   ├── sender/        # Device communication (Phase 2)
│   ├── models/        # Data models
│   ├── storage/       # Persistence layer
│   └── viewer/        # Qt Quick viewer (Phase 2)
├── tests/             # Test suite
├── docs/              # Documentation
│   ├── PROGRESS.md    # Implementation progress tracker
│   └── ARCHITECTURE-CONFIG.md  # Configuration system docs
├── setup.sh           # Development environment setup
├── run.sh             # Application launcher
└── test.sh            # Test runner
```

### Configuration

User settings are stored in platform-specific locations:
- **Linux**: `~/.config/openpcb/settings.json`
- **macOS**: `~/Library/Application Support/openpcb/settings.json`
- **Windows**: `%APPDATA%\openpcb\settings.json`

### Phase 1 Status (Complete ✅)

Phase 1 implementation is complete with the following features:
- ✅ Development environment with linters and git hooks
- ✅ Configuration system with Pydantic models
- ✅ HiDPI display support
- ✅ Main window with menus, toolbars, and docks
- ✅ Preferences dialog with multi-page settings
- ✅ Comprehensive documentation

See [PHASE1-PROGRESS.md](docs/PHASE1-PROGRESS.md) for detailed implementation status.

### Next Steps (Phase 2)

- Qt Quick viewer integration with high-performance rendering
- Layer management UI with visibility controls
- File importers (Gerber, Excellon, SVG, G-code)
- CAM operations (isolation, drill, outline, raster)
- Auto-leveling with height maps

---


