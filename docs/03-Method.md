# Method

## Architecture
- Frontend (PySide6/Qt Quick viewer, inspectors, job composer)
- Core Engine (Shapely 2.x, svgpathtools, scikit-image, potracer; importers; CAM; panelization; post-processors; optimizers)
- Sender (asyncio, pyserial/TCP; 4 devices; parsers; flow control)
- Persistence (JSON project; SQLite height maps/history; YAML/JSON profiles)

## Component Diagram (PlantUML)
```plantuml
@startuml
skinparam componentStyle rectangle
component "UI (PySide6)" as UI
component "Viewer (QtQuick)" as VIEW
component "Importers" as IMP
component "Geometry Kernel\n(Shapely, svgpathtools)" as GEO
component "CAM Engine" as CAM
component "Post-Processor" as POST
component "Sender/IO" as IO
component "Profiles (YAML/JSON)" as PROF
component "Storage (SQLite/JSON)" as DB
UI --> VIEW
UI --> CAM
VIEW --> GEO
UI --> IMP
IMP --> GEO
CAM --> GEO
CAM --> POST
POST --> IO
UI --> IO
UI --> DB
CAM --> DB
IO --> DB
IO --> PROF
CAM --> PROF
IMP --> PROF
@enduml
```

## Data Model
- Project JSON with layers, panel (`gap.x/y`), CAM ops, autolevel config, machines, post, jobs.
- Machine Profile YAML (controller, envelope, mapping).
- Controller dialect table (GRBL/Marlin/Smoothie/LinuxCNC/Mach3/4/FANUC subset/HPGL).

## Algorithms
- Isolation routing (multi-offset), raster/hatch, drilling/peck, outline & tabs, panelization, toolpath optimization, auto-leveling (bilinear/IDW/RBF), sender concurrency (asyncio).
