#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
MODE="${1:-all}"

if [ "$(uname -s)" != "Linux" ]; then
    echo "Linux packages must be built on a Linux host." >&2
    exit 1
fi

case "$MODE" in
    all|deb|appimage) ;;
    *)
        printf 'Usage: %s [all|deb|appimage]\n' "$0" >&2
        exit 2
        ;;
esac

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required to build VitalForge." >&2
    exit 1
fi

if [ ! -f "$ROOT/.env" ]; then
    echo "Required environment file not found: $ROOT/.env" >&2
    exit 1
fi

python3 -m PyInstaller --noconfirm --clean "$ROOT/VitalForge.spec"
APP_SOURCE="$ROOT/dist/VitalForge"
if [ ! -x "$APP_SOURCE/VitalForge" ]; then
    echo "PyInstaller did not produce the expected Linux application directory." >&2
    exit 1
fi

mkdir -p "$ROOT/dist/packages"
APP_ARCH="$(uname -m)"
case "$APP_ARCH" in
    x86_64) APPIMAGE_ARCH=x86_64 ;;
    aarch64|arm64) APPIMAGE_ARCH=aarch64 ;;
    *)
        echo "Unsupported Linux architecture for packaging: $APP_ARCH" >&2
        exit 1
        ;;
esac

make_appdir() {
    appdir="$1"
    layout="$2"
    mkdir -p \
        "$appdir/usr/bin" \
        "$appdir/usr/share/applications" \
        "$appdir/usr/share/icons/hicolor/512x512/apps"
    if [ "$layout" = "appimage" ]; then
        cp -a "$APP_SOURCE/." "$appdir/usr/bin/"
    else
        mkdir -p "$appdir/usr/lib/vitalforge"
        cp -a "$APP_SOURCE/." "$appdir/usr/lib/vitalforge/"
        ln -s ../lib/vitalforge/VitalForge "$appdir/usr/bin/VitalForge"
    fi
    cp "$ROOT/packaging/linux/VitalForge.desktop" \
        "$appdir/usr/share/applications/VitalForge.desktop"
    python3 -c 'import sys; from PIL import Image; Image.open(sys.argv[1]).convert("RGBA").resize((512, 512), Image.Resampling.LANCZOS).save(sys.argv[2])' \
        "$ROOT/assets/logo-rounded.png" \
        "$appdir/usr/share/icons/hicolor/512x512/apps/VitalForge.png"
}

if [ "$MODE" = "all" ] || [ "$MODE" = "deb" ]; then
    if ! command -v dpkg-deb >/dev/null 2>&1; then
        echo "dpkg-deb is required for .deb packages; install dpkg or build appimage only." >&2
        exit 1
    fi

    VERSION="$(sed -n 's/^version = "\(.*\)"/\1/p' "$ROOT/pyproject.toml" | head -n 1)"
    if [ -z "$VERSION" ]; then
        echo "Could not read project version from pyproject.toml." >&2
        exit 1
    fi

    DEB_ROOT="$(mktemp -d)"
    trap 'rm -rf "$DEB_ROOT"' EXIT HUP INT TERM
    make_appdir "$DEB_ROOT" deb
    mkdir -p "$DEB_ROOT/DEBIAN"
    cat > "$DEB_ROOT/DEBIAN/control" <<EOF
Package: vitalforge
Version: $VERSION
Section: utils
Priority: optional
Architecture: $(dpkg-deb --print-architecture)
Maintainer: Vital Forge Team
Description: Desktop fitness tracking application
EOF
    dpkg-deb --root-owner-group --build \
        "$DEB_ROOT" "$ROOT/dist/packages/vitalforge_${VERSION}_$(dpkg-deb --print-architecture).deb"
    rm -rf "$DEB_ROOT"
    trap - EXIT HUP INT TERM
fi

if [ "$MODE" = "all" ] || [ "$MODE" = "appimage" ]; then
    if ! command -v linuxdeploy >/dev/null 2>&1; then
        echo "linuxdeploy is required to bundle shared-library dependencies for AppImage." >&2
        exit 1
    fi
    if ! command -v appimagetool >/dev/null 2>&1; then
        echo "appimagetool is required to build an AppImage." >&2
        exit 1
    fi

    APPDIR="$(mktemp -d)"
    trap 'rm -rf "$APPDIR"' EXIT HUP INT TERM
    make_appdir "$APPDIR" appimage
    cp "$ROOT/packaging/linux/AppRun" "$APPDIR/AppRun"
    chmod +x "$APPDIR/AppRun"
    cp "$ROOT/packaging/linux/VitalForge.desktop" "$APPDIR/VitalForge.desktop"
    cp "$APPDIR/usr/share/icons/hicolor/512x512/apps/VitalForge.png" \
        "$APPDIR/VitalForge.png"
    linuxdeploy --appdir "$APPDIR" \
        --executable "$APPDIR/usr/bin/VitalForge" \
        --desktop-file "$APPDIR/VitalForge.desktop" \
        --icon-file "$APPDIR/VitalForge.png"
    ARCH="$APPIMAGE_ARCH" appimagetool "$APPDIR" \
        "$ROOT/dist/packages/VitalForge-$APPIMAGE_ARCH.AppImage"
    rm -rf "$APPDIR"
    trap - EXIT HUP INT TERM
fi

echo "Linux packages are available in $ROOT/dist/packages"
