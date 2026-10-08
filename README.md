# Vital Forge

Vital Forge is a desktop fitness-tracking application built with Python and Tkinter. It helps users track daily nutrition, workouts, hydration, sleep, step goals, and long-term progress while keeping the experience focused and lightweight.

## Features

- Daily activity and health logging
- Workout and nutrition tracking
- Goals for water intake, sleep, and steps
- Progress charts using Matplotlib
- Native desktop packages for Windows, macOS, Debian-based Linux, and other Linux distributions

## Tech stack

- Python 3.10+
- Tkinter for the desktop UI
- MySQL for persistent user and tracking data
- Matplotlib for charts
- PyInstaller for executable builds

## Repository structure

```text
VitalForge/
├── main.py
├── config.py
├── screens.py
├── ui_components.py
├── data.py
├── charts.py
├── utils.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── VitalForge.spec
├── database/
│   ├── connection.py
│   ├── schema.sql
│   ├── setup.py
│   └── queries.py
├── assets/
│   ├── logo.png
│   ├── logo-rounded.png
│   ├── logo.ico
│   └── logo.icns
├── packaging/
│   └── linux/            # Debian and AppImage packaging files
└── dist/                 # generated build output
```

## Setup

1. Clone the repository.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Run the database bootstrap if needed:

```bash
python database/setup.py
```

4. Launch the app:

```bash
python main.py
```

## Desktop distributions

The GitHub Actions workflow builds the macOS and Linux distributions on
GitHub-hosted runners. It runs on pushes and pull requests targeting `main`,
and can also be started manually from the
[Actions page](https://github.com/Harry-Jees/VitalForge/actions/workflows/build-distributions.yml).
Every successful run uploads downloadable workflow artifacts. For a successful
push to `main`, a follow-up Actions job also commits the generated distributions
to `dist/`.

The [latest completed build](https://github.com/Harry-Jees/VitalForge/actions/runs/37737546539)
succeeded, and these outputs are available in the repository:

| Platform | Distribution | Repository path |
| --- | --- | --- |
| macOS (Intel) | Application bundle | `dist/VitalForge.app` |
| Linux (x86_64) | Debian package | `dist/packages/vitalforge_1.0.0_amd64.deb` |
| Linux (x86_64) | AppImage | `dist/packages/VitalForge-x86_64.AppImage` |
| Windows | Executable | `dist/VitalForge.exe` |

The automated workflow currently builds macOS and Linux distributions.
The Windows executable is present in `dist/`; Windows builds are not part of
that workflow.

## Testing

```bash
python -m pytest -q
```
