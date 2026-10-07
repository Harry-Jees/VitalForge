# -*- mode: python ; coding: utf-8 -*-


from pathlib import Path
import sys

import mysql.connector

project_dir = Path(SPECPATH)
env_file = project_dir / ".env"
if not env_file.is_file():
    raise FileNotFoundError(f"Required environment file not found: {env_file}")

mysql_connector_path = Path(mysql.connector.__file__).parent
assets_dir = project_dir / "assets"
app_icon = {
    "win32": assets_dir / "logo.ico",
    "darwin": assets_dir / "logo.icns",
}.get(sys.platform)

a = Analysis(
    [str(project_dir / "main.py")],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[
        (str(assets_dir), "assets"),
        (str(env_file), "."),
        (str(mysql_connector_path / "locales"), "mysql/connector/locales"),
    ],
    hiddenimports=["mysql.connector.locales.eng"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

if sys.platform == "win32":
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name="VitalForge",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        icon=str(app_icon),
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name="VitalForge",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name="VitalForge",
    )

    if sys.platform == "darwin":
        app = BUNDLE(
            coll,
            name="VitalForge.app",
            icon=str(app_icon),
            bundle_identifier="com.vitalforge.desktop",
            codesign_identity=None,
            entitlements_file=None,
        )
