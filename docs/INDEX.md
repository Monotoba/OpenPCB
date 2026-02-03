# OpenPCB — Documentation Index

## Core Documentation

- [Background](01-Background.md)
- [Requirements (MoSCoW)](02-Requirements.md)
- [Method (Architecture, Data, Algorithms)](03-Method.md)
- [Implementation Plan](04-Implementation.md)
- [Milestones](05-Milestones.md)
- [Gathering Results (Acceptance, KPIs)](06-GatheringResults.md)
- [Risk Register](07-RiskRegister.md)
- [Compliance Checklist (LGPL/Qt & Third-Party)](08-Compliance.md)
- [Qt Deployment Checklist](09-Deployment.md)
- [Serial/USB Setup Guide](10-SerialUSB.md)
- [Post-Processors — GRBL vs Mach3](11-PostProcessors.md)
- [Backlog (Epics & Stories)](BACKLOG.md)
- [SPEC (single-file combined)](SPEC-1-OpenPCB.md)
- [Third-Party Notices](THIRD_PARTY_NOTICES.md)
- [Deployment & Serial (condensed)](DEPLOYMENT.md)

## Phase 1: GUI Foundation (Complete ✅)

**Status**: Complete (2026-02-02)
**Focus**: Development environment, configuration system, HiDPI support, main window, preferences dialog

- [Phase 1 Progress Tracker](PHASE1-PROGRESS.md) - Implementation status, verification commands, completion criteria
- [Phase 1 Architecture: Configuration System](PHASE1-ARCHITECTURE-CONFIG.md) - Technical deep-dive into settings management
- [HiDPI Issues and Solutions](HIDPI-ISSUES.md) - Known HiDPI problems and fixes (menu positioning on GNOME)

**Deliverables**:
- ✅ Development environment with linters, formatters, git hooks
- ✅ Thread-safe configuration system with Pydantic models
- ✅ HiDPI display support for all platforms
- ✅ Main window with menus, toolbars, dock widgets
- ✅ Multi-page preferences dialog
- ✅ Comprehensive test suite (14 tests)
- ✅ 1,600+ lines of documentation

## Phase 2: Viewer & Importers (Planned)

**Status**: Not Started
**Focus**: Qt Quick viewer, layer management, file importers, CAM operations

**Planned Documentation**:
- PHASE2-PROGRESS.md - Implementation tracker
- PHASE2-ARCHITECTURE-VIEWER.md - Qt Quick rendering architecture
- PHASE2-ARCHITECTURE-IMPORTERS.md - File format parsers

**Planned Deliverables**:
- Qt Quick viewer with high-performance rendering (1M+ segments at ≥45 FPS)
- Layer management UI with visibility controls
- File importers (Gerber, Excellon, SVG, G-code)
- CAM operations (isolation, drill, outline, raster)
- Auto-leveling with height maps

## Phase 3: Device Communication (Planned)

**Status**: Not Started
**Focus**: Multi-machine sender, real-time control, job execution

**Planned Documentation**:
- PHASE3-PROGRESS.md - Implementation tracker
- PHASE3-ARCHITECTURE-SENDER.md - Device communication architecture

## Advanced Topics

- [Auto-Leveling Deep Dive](A1-AutoLeveling.md)
- [Laser Raster/Vector Engraving](A2-Laser.md)
- [Mouse-Bite Panelization](A3-MouseBites.md)
- [V-Groove & Panel Rails/Fiducials](A4-VGrooveRailsFids.md)
- [CLI Smoke Test](B1-CLI.md)

---

## Documentation Standards

### File Naming Convention

- **Core Docs**: `##-Name.md` (numbered sequentially)
- **Phase Docs**: `PHASE#-TYPE.md` where:
  - `#` = Phase number (1, 2, 3, etc.)
  - `TYPE` = PROGRESS, ARCHITECTURE-*, TESTING, etc.
- **Advanced Topics**: `A#-Name.md` (appendix)
- **Special Topics**: `B#-Name.md` (bonus/supplementary)

### Phase Documentation Requirements

Each phase must include:
1. **PHASE#-PROGRESS.md** - Implementation tracker with:
   - Task checklist
   - Status indicators (🔴 Not Started | 🟡 In Progress | 🟢 Complete)
   - Verification commands
   - Completion criteria
   - Git commits
   - Next steps

2. **PHASE#-ARCHITECTURE-*.md** - Technical documentation for major components:
   - Architecture diagrams
   - Component details
   - Design decisions and rationale
   - Code examples
   - Testing strategy
   - Performance characteristics
   - Best practices

3. **Version Control**:
   - Each phase doc includes creation date
   - Last updated date at bottom
   - Phase status at top (Not Started, In Progress, Complete)
   - Link to related commits

### Maintenance Guidelines

- Phase documentation is **permanent** - never delete
- Update status when phase completes
- Add "Last Updated" date on modifications
- Cross-reference between related docs
- Keep INDEX.md up to date with new docs
- Archive completed phase docs but keep accessible

---

**Last Updated**: 2026-02-02
**Current Phase**: Phase 1 (Complete) → Phase 2 (Next)
