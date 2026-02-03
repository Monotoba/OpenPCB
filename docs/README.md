# OpenPCB Documentation

This directory contains all documentation for the OpenPCB project, organized by phase and topic.

## Quick Links

- **[Documentation Index](INDEX.md)** - Master index of all documentation
- **[Current Phase: Phase 1 Progress](PHASE1-PROGRESS.md)** - Implementation status tracker
- **[Phase 1 Architecture](PHASE1-ARCHITECTURE-CONFIG.md)** - Configuration system design

## Documentation Structure

### Core Documentation
Numbered documents (01-11) covering project fundamentals:
- Background, requirements, architecture
- Implementation plans and milestones
- Risk register and compliance
- Deployment guides

### Phase Documentation
Each development phase has dedicated documentation:

#### Phase 1: GUI Foundation (✅ Complete)
- **[PHASE1-PROGRESS.md](PHASE1-PROGRESS.md)** - Implementation tracker
- **[PHASE1-ARCHITECTURE-CONFIG.md](PHASE1-ARCHITECTURE-CONFIG.md)** - Configuration system

#### Phase 2: Viewer & Importers (Planned)
- PHASE2-PROGRESS.md (to be created)
- PHASE2-ARCHITECTURE-VIEWER.md (to be created)
- PHASE2-ARCHITECTURE-IMPORTERS.md (to be created)

#### Phase 3: Device Communication (Planned)
- PHASE3-PROGRESS.md (to be created)
- PHASE3-ARCHITECTURE-SENDER.md (to be created)

### Templates
Use these templates when starting a new phase:
- **[PHASE-TEMPLATE.md](PHASE-TEMPLATE.md)** - Progress tracker template
- **[PHASE-ARCHITECTURE-TEMPLATE.md](PHASE-ARCHITECTURE-TEMPLATE.md)** - Architecture doc template

## File Naming Convention

Follow these conventions for consistency:

### Phase Documentation
```
PHASE[N]-[TYPE].md

Where:
  N    = Phase number (1, 2, 3, etc.)
  TYPE = PROGRESS, ARCHITECTURE-[component], TESTING, etc.

Examples:
  PHASE1-PROGRESS.md
  PHASE1-ARCHITECTURE-CONFIG.md
  PHASE2-ARCHITECTURE-VIEWER.md
  PHASE3-TESTING-INTEGRATION.md
```

### Core Documentation
```
##-Name.md

Where:
  ## = Two-digit number (01-99)

Examples:
  01-Background.md
  02-Requirements.md
  11-PostProcessors.md
```

### Advanced Topics
```
A#-Name.md    (Appendix - deep dives)
B#-Name.md    (Bonus - supplementary topics)

Examples:
  A1-AutoLeveling.md
  B1-CLI.md
```

## Documentation Standards

### Required Metadata Header

Every phase document must include:

```markdown
**Phase**: [N] - [Phase Name]
**Status**: 🔴 NOT STARTED | 🟡 IN PROGRESS | ✅ COMPLETE
**Started**: [YYYY-MM-DD]
**Completed**: [YYYY-MM-DD or N/A]
**Related Docs**: [links to related documents]
```

### Status Indicators

Use consistent emoji indicators:
- 🔴 **Not Started** - Work hasn't begun
- 🟡 **In Progress** - Currently being worked on
- ✅ **Complete** - Finished and verified

### Version Control

Each document should include:
- **Created**: Date of initial creation
- **Last Updated**: Date of most recent modification
- **Phase Status**: Current state of the phase

## Creating New Phase Documentation

When starting a new phase:

1. **Copy the templates**:
   ```bash
   cp docs/PHASE-TEMPLATE.md docs/PHASE[N]-PROGRESS.md
   cp docs/PHASE-ARCHITECTURE-TEMPLATE.md docs/PHASE[N]-ARCHITECTURE-[component].md
   ```

2. **Fill in the metadata**:
   - Update phase number and name
   - Set initial status to 🔴 NOT STARTED
   - Add creation date
   - Link to related documents

3. **Update INDEX.md**:
   - Add new phase section
   - List all phase documents
   - Update "Current Phase" indicator

4. **Commit the templates**:
   ```bash
   git add docs/PHASE[N]-*.md docs/INDEX.md
   git commit -m "doc: add Phase [N] documentation templates"
   ```

5. **Update as you implement**:
   - Change status to 🟡 IN PROGRESS when starting
   - Check off completed tasks
   - Add verification results
   - Update "Last Updated" date

6. **Mark complete**:
   - Change status to ✅ COMPLETE
   - Add completion date
   - Verify all criteria met
   - Final commit with phase summary

## Maintenance Guidelines

### Do's
✅ Keep documentation up to date as implementation progresses
✅ Add "Last Updated" date when making changes
✅ Cross-reference related documents
✅ Include code examples and verification commands
✅ Document design decisions and trade-offs
✅ Maintain phase documentation permanently

### Don'ts
❌ Don't delete phase documentation (archive if needed)
❌ Don't skip the metadata headers
❌ Don't forget to update INDEX.md
❌ Don't mix phase numbers in file names
❌ Don't use inconsistent status indicators

## Phase Lifecycle

```
1. Phase Planned
   └─> Create PHASE[N]-PROGRESS.md (🔴 NOT STARTED)
   └─> Create PHASE[N]-ARCHITECTURE-*.md templates
   └─> Update INDEX.md

2. Phase Started
   └─> Update status to 🟡 IN PROGRESS
   └─> Add start date
   └─> Begin checking off tasks

3. Implementation
   └─> Update progress regularly
   └─> Add verification results
   └─> Document decisions

4. Phase Complete
   └─> Update status to ✅ COMPLETE
   └─> Add completion date
   └─> Verify all criteria met
   └─> Update INDEX.md with summary

5. Archived (if needed)
   └─> Move to archive/ subdirectory
   └─> Keep links in INDEX.md
   └─> Update README.md
```

## Current Project Status

- **Phase 1**: ✅ Complete (GUI Foundation)
- **Phase 2**: 🔴 Not Started (Viewer & Importers)
- **Phase 3**: 🔴 Not Started (Device Communication)

See [INDEX.md](INDEX.md) for complete documentation index.

---

**Last Updated**: 2026-02-02
**Maintained By**: OpenPCB Development Team
