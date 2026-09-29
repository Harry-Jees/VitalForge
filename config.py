# config.py
# Vital Forge
# Material 3 Earthy Tone Palette + 8-Point Spacing.

import os
from configparser import ConfigParser
from pathlib import Path

# =========================================================
# Application
# =========================================================

APP_NAME = "Vital Forge"


WINDOW_WIDTH  = 1200
WINDOW_HEIGHT = 750


# =========================================================
# Material 3 — Earthy Green / Brown Palette
# =========================================================

# ── Primary (Forest Green) ────────────────────────────────
GREEN        = "#3E6B47"   # M3 Primary
DARK_GREEN   = "#2A4E31"   # M3 On-Primary-Container (dark)
LIGHT_GREEN  = "#B8E8C0"   # M3 Primary Container

# ── Secondary (Warm Brown / Earth) ───────────────────────
BROWN        = "#8B6343"   # M3 Secondary
DARK_BROWN   = "#4E3523"   # M3 On-Secondary-Container (dark)
LIGHT_BROWN  = "#F6DEC9"   # M3 Secondary Container

# ── Tertiary accent (Warm Amber) ─────────────────────────
AMBER        = "#A07834"
LIGHT_AMBER  = "#FFF0C7"

# ── Surface / Background ─────────────────────────────────
BG_COLOR     = "#F4EFE8"   # M3 Background  (warm parchment)
CARD_COLOR   = "#FFFDF8"   # M3 Surface     (near-white warm)
INPUT_COLOR  = "#F5F0EA"   # M3 Surface Variant (input bg)

# ── Text / On-Surface ─────────────────────────────────────
TEXT_COLOR   = "#1C1B16"   # M3 On-Surface
MUTED_TEXT   = "#6B6356"   # M3 On-Surface-Variant

# ── Outline / Borders ────────────────────────────────────
BORDER_COLOR = "#C8BFB4"   # M3 Outline Variant

# ── Status Colors ─────────────────────────────────────────
SUCCESS_COLOR = "#3B6E46"  # Earthy green
WARNING_COLOR = "#A07834"  # Amber
ERROR_COLOR   = "#B3261E"  # M3 Error


# =========================================================
# Fonts  (Segoe UI — Material 3 type scale)
# =========================================================

FONT_FAMILY = "Segoe UI"

FONT_SMALL      = (FONT_FAMILY, 9)
FONT_BODY       = (FONT_FAMILY, 10)
FONT_BODY_BOLD  = (FONT_FAMILY, 10, "bold")
FONT_BUTTON     = (FONT_FAMILY, 10, "bold")
FONT_SECTION    = (FONT_FAMILY, 13, "bold")
FONT_HEADING    = (FONT_FAMILY, 16, "bold")
FONT_PAGE_TITLE = (FONT_FAMILY, 20, "bold")
FONT_TITLE      = (FONT_FAMILY, 24, "bold")


# =========================================================
# Spacing  —  8-Point System
# =========================================================

SPACING_4  = 4
SPACING_8  = 8
SPACING_16 = 16
SPACING_24 = 24
SPACING_32 = 32
SPACING_40 = 40
SPACING_48 = 48
SPACING_64 = 64

# Named aliases
PAGE_PAD    = SPACING_32
CARD_PAD    = SPACING_24
SECTION_GAP = SPACING_32
FIELD_GAP   = SPACING_16
LABEL_GAP   = SPACING_8

# Corner radius (used everywhere for consistency)
RADIUS = 16


# =========================================================
# MySQL Configuration
# =========================================================

_LOCAL_SECRETS = ConfigParser(interpolation=None)
_LOCAL_SECRETS.read(Path(__file__).with_name(".secrets.ini"), encoding="utf-8")

MYSQL_HOST     = os.environ.get(
	"MYSQL_HOST",
	"vital-forge-bro-app.b.aivencloud.com"
)
MYSQL_PORT     = int(os.environ.get("MYSQL_PORT", "10380"))
MYSQL_USER     = os.environ.get("MYSQL_USER", "avnadmin")
MYSQL_PASSWORD = (
	_LOCAL_SECRETS.get("mysql", "password", fallback="")
	or os.environ.get("MYSQL_PASSWORD", "")
)
MYSQL_DATABASE = "defaultdb"


# =========================================================
# Demo Account
# =========================================================

DEMO_EMAIL    = "demo@vitalforge.local"
DEMO_PASSWORD = "password"


# =========================================================
# Application Data Requirements
# =========================================================

MIN_FOOD_ITEMS = 300
WORKOUT_COUNT  = 25
QUOTE_COUNT    = 100
WEEK_DAYS      = 7
