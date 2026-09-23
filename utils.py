# utils.py
# Vital Forge - General Utilities

import hashlib
import re
from datetime import date, datetime, timedelta


# =========================================================
# PASSWORD SECURITY
# =========================================================

def hash_password(password):
    """Convert a password into a secure SHA-256 hash."""

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def verify_password(password, password_hash):
    """Check whether a password matches its stored hash."""

    return hash_password(password) == password_hash


# =========================================================
# VALIDATION
# =========================================================

def is_valid_email(email):
    """Check whether an email has a valid basic format."""

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pattern, email.strip()) is not None


def is_valid_password(password):
    """Check the minimum password requirement."""

    return len(password) >= 6


def is_valid_name(name):
    """Check that a name is not empty."""

    return bool(name.strip())


def is_positive_number(value):
    """Check whether a value is a positive number."""

    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False


def is_non_negative_number(value):
    """Check whether a value is zero or greater."""

    try:
        return float(value) >= 0
    except (ValueError, TypeError):
        return False


# =========================================================
# DATE FUNCTIONS
# =========================================================

def today():
    """Return today's date."""

    return date.today()


def today_string():
    """Return today's date as YYYY-MM-DD."""

    return date.today().strftime("%Y-%m-%d")


def format_date(value):
    """Convert a date into a readable format."""

    if isinstance(value, datetime):
        value = value.date()

    if isinstance(value, date):
        return value.strftime("%d %b %Y")

    return str(value)


def get_previous_dates(days=7):
    """Return a list of dates including today."""

    current_date = date.today()

    dates = []

    for i in range(days):
        dates.append(
            current_date - timedelta(days=i)
        )

    return dates


# =========================================================
# NUMBER HELPERS
# =========================================================

def safe_float(value, default=0):
    """Convert a value to float safely."""

    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value, default=0):
    """Convert a value to integer safely."""

    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def clamp(value, minimum, maximum):
    """Keep a number inside a specified range."""

    return max(minimum, min(value, maximum))


def percentage(current, target):
    """Calculate progress percentage."""

    if target <= 0:
        return 0

    return clamp(
        (current / target) * 100,
        0,
        100
    )


# =========================================================
# TEXT HELPERS
# =========================================================

def clean_text(text):
    """Remove unnecessary spaces from text."""

    return " ".join(
        str(text).strip().split()
    )


def capitalize_name(name):
    """Format a person's name neatly."""

    return " ".join(
        word.capitalize()
        for word in clean_text(name).split()
    )


# =========================================================
# GOAL HELPERS
# =========================================================

def get_goal_description(goal):
    """Return a short description for a selected goal."""

    descriptions = {
        "Weight loss":
            "Focus on regular activity and healthy daily habits.",

        "Weight gain":
            "Focus on consistent activity, recovery, and balanced nutrition.",

        "Muscular build":
            "Focus on strength-building activity and good recovery.",

        "General fitness":
            "Focus on maintaining an active and balanced routine.",

        "Endurance":
            "Focus on gradually improving stamina and activity levels."
    }

    return descriptions.get(
        goal,
        "Focus on building healthy and consistent habits."
    )


# =========================================================
# UI HELPERS
# =========================================================

def clear_frame(frame):
    """Remove all widgets from a Tkinter frame."""

    for widget in frame.winfo_children():
        widget.destroy()


def center_toplevel(window, width, height):
    """Center a Tkinter Toplevel window."""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


# =========================================================
# ERROR HANDLING
# =========================================================

def get_error_message(error):
    """Return a readable error message."""

    if error is None:
        return "An unknown error occurred."

    return str(error)