# Vital Forge

Vital Forge is a desktop fitness-tracking application built with Python and Tkinter. It helps users track daily nutrition, workouts, hydration, sleep, step goals, and long-term progress while keeping the experience focused and lightweight.

## Features

- Daily activity and health logging
- Workout and nutrition tracking
- Goals for water intake, sleep, and steps
- Progress charts using Matplotlib
- Local credential file for MySQL access outside the source code
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

## Configuration and credentials

The app reads runtime configuration from a local `.env` file, environment
variables, or (for direct database access) a `.secrets.ini` file. Supply your
own configuration locally; do not put credentials in source control or public
documentation. The package build expects `.env` to be present locally and
includes it in the application package. It is not encrypted; anyone receiving
a package can extract its contents. Do not distribute packages containing
private credentials.

At startup, the app checks database connectivity and displays a warning if the
database is unavailable.

## Setup

1. Clone the repository.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Create and configure `.env` locally. Do not share a built package containing
   private credentials.

4. Run the database bootstrap if needed:

```bash
python database/setup.py
```

5. Launch the app:

```bash
python main.py
```

## Build desktop packages

Build on the platform you are targeting. PyInstaller does not cross-compile
between operating systems, so Windows, macOS, and Linux packages must each be
built on that operating system. The build uses the platform's bundled logo and
includes the local `.env` in the package. It is not encrypted.

The GitHub Actions workflow builds the macOS `.app`, Debian `.deb`, and Linux
`.AppImage` on GitHub-hosted runners. It uploads the packages for pushes and
pull requests targeting `main`; after a push to `main`, it also adds the
generated outputs under `dist/` to a follow-up commit. GitHub no longer offers
the requested `macos-13` hosted label, so the workflow uses the supported
`macos-15-intel` runner. It uses an empty `.env` placeholder, not repository
configuration, for these builds.

### Windows

The Windows build was rebuilt and verified in this workspace. To rebuild on
Windows, install Python dependencies and run:

```powershell
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean VitalForge.spec
```

The single-file executable is created at `dist/VitalForge.exe`.

### macOS

The GitHub Actions workflow builds the macOS application on GitHub's
`macos-15-intel` runner. To build it manually on macOS after installing the
Python dependencies:

```bash
python3 -m pip install -r requirements.txt
python3 -m PyInstaller --noconfirm --clean VitalForge.spec
```

The expected output is `dist/VitalForge.app`. Build and verify separately on
each Mac architecture you intend to support.

### Debian-based and other Linux distributions

Linux packaging configuration is present but has not been built or verified
on Linux. On a Linux host, install Python, Tkinter, project dependencies, and
PyInstaller. To build a Debian package, `dpkg-deb` is also required. To build
an AppImage, install `linuxdeploy` and `appimagetool` to bundle shared-library
dependencies. Then run:

```bash
python3 -m pip install -r requirements.txt
sh packaging/linux/build.sh all
```

The outputs are written to `dist/packages/`. Use `deb` to build only the
Debian package or `appimage` to build only the AppImage. AppImages are built
for the host architecture (`x86_64` or `aarch64`); build on each target
architecture and test on each Linux distribution you intend to support.

## Production notes

- The app uses a fixed MySQL database name: `defaultdb`.
- It does not create or rename the database during setup.
- Local database settings may be supplied in `.secrets.ini` or through environment variables.
- If configuration is missing, the app reports the database connection problem at startup.

## Testing

```bash
python -m pytest -q
```
