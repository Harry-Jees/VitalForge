# Vital Forge

Vital Forge is a desktop fitness-tracking application built with Python and Tkinter. It helps users track daily nutrition, workouts, hydration, sleep, step goals, and long-term progress while keeping the experience focused and lightweight.

## Features

- Daily activity and health logging
- Workout and nutrition tracking
- Goals for water intake, sleep, and steps
- Progress charts using Matplotlib
- Local credential file for MySQL access outside the source code
- Desktop packaging for Windows via PyInstaller

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
├── .secrets.example.ini
├── .env.example
├── database/
│   ├── connection.py
│   ├── schema.sql
│   ├── setup.py
│   └── queries.py
├── tests/
│   └── test_database_config.py
├── assets/
│   └── logo.png
└── dist/
    └── VitalForge.exe   # generated package output
```

## Credential storage

Keep all runtime database credentials in a local file named `.secrets.ini`.

Where to store it:
- Local development: `<repo>/.secrets.ini`
- Packaged app: place `.secrets.ini` next to the generated executable (`dist/VitalForge.exe`)

Use `.secrets.example.ini` as the template:

```ini
[mysql]
host = your-aiven-host.example.com
port = 10380
user = avnadmin
password = replace-with-your-rotated-aiven-password
```

Important:
- Do not commit `.secrets.ini`.
- Do not hard-code credentials into the source code.
- Do not bundle the secret file into the executable.
- These secret files are not excluded by a `.gitignore`; keep them local and
  do not stage or commit them.

The Supabase function settings are loaded from `.env` using `python-dotenv`.
Copy `.env.example` to `.env` and add the private `VITALFORGE_APP_API_KEY`
locally. The function URL is configurable with `VITALFORGE_FUNCTION_URL`.
Do not distribute `.env` or bundle its key with the desktop application; secrets
shipped to client machines can be extracted.

The backend calls the function with `GET`, sends the key in the `x-api-key`
header, and sends no request body. It expects a successful JSON response with
a non-empty string `credential` field. That credential is used only for
server-side MySQL connections. When `VITALFORGE_APP_API_KEY` is configured,
the function credential takes precedence over local password settings. Without
the function key, the app uses `MYSQL_PASSWORD` or the local `.secrets.ini`
password. At app startup the database connection is checked before the login
screen appears; a safe warning is shown if it is unavailable.

The function source supplied for this setup checks `x-api-key` itself, but the
deployed Supabase gateway also has JWT verification enabled. With no valid
Supabase JWT configured in this desktop app, the gateway can reject the GET
before it reaches the function. To use only the private app key, the function
must have platform JWT verification disabled (for example,
`[functions.get-vitalforge-key] verify_jwt = false` in `supabase/config.toml`)
while keeping the function's constant-time `x-api-key` check and required
function secrets. No deployed configuration was changed; approval and the
appropriate Supabase-side change are still required.

## Setup

1. Clone the repository.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Create your local secret file:

```bash
copy .secrets.example.ini .secrets.ini
```

Then update the file with your real MySQL credentials.

4. Create `.env` from `.env.example` and add the private function API key.

5. Run the database bootstrap if needed:

```bash
python database/setup.py
```

6. Launch the app:

```bash
python main.py
```

## Build for Windows EXE

From the project root:

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed --name VitalForge --add-data "assets;assets" main.py
```

The packaged executable is created in `dist/VitalForge.exe`.

## Production notes

- The app uses a fixed MySQL database name: `defaultdb`.
- It does not create or rename the database during setup.
- Local credentials are loaded from `.secrets.ini` or environment variables (`MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`).
- If the password is missing, the app fails fast with a clear error instead of failing later during a database call.

## Testing

```bash
python -m pytest -q
```
