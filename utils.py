# utils.py
# Vital Forge - General Utilities

import base64
import hashlib
import math
import re
import secrets
from datetime import date, datetime, timedelta


# =========================================================
# PASSWORD SECURITY
# =========================================================

def hash_password(password):
    """Hash a password using PBKDF2-HMAC-SHA256 with a random salt."""
    if password is None:
        raise ValueError("Password cannot be empty.")

    password = str(password)
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000,
    )
    encoded_salt = base64.b64encode(salt).decode("ascii")
    encoded_hash = base64.b64encode(derived).decode("ascii")
    return f"pbkdf2_sha256$200000${encoded_salt}${encoded_hash}"


def verify_password(password, password_hash):
    """Check whether a password matches a stored hash, including older SHA-256 entries."""
    if not password or not password_hash:
        return False

    if password_hash.startswith("pbkdf2_sha256$"):
        try:
            algorithm, iterations_text, salt_b64, digest_b64 = password_hash.split("$")
            iterations = int(iterations_text)
            salt = base64.b64decode(salt_b64.encode("ascii"))
            expected = base64.b64decode(digest_b64.encode("ascii"))
            calculated = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                iterations,
            )
            return secrets.compare_digest(calculated, expected)
        except (TypeError, ValueError):
            return False

    return hashlib.sha256(password.encode("utf-8")).hexdigest() == password_hash


# =========================================================
# VALIDATION
# =========================================================

def is_valid_email(email):
    """Check whether an email has a valid basic format."""

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pattern, email.strip()) is not None


def is_valid_password(password):
    """Require a minimally strong password for account creation."""
    if not isinstance(password, str):
        return False

    if len(password) < 8:
        return False

    if not re.search(r"[A-Za-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True


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


def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI from kilograms and centimeters, returning None for invalid input."""
    try:
        weight = float(weight_kg)
        height_m = float(height_cm) / 100
    except (TypeError, ValueError):
        return None

    if not math.isfinite(weight) or not math.isfinite(height_m) or weight <= 0 or height_m <= 0:
        return None

    return weight / (height_m * height_m)


def get_bmi_category(bmi):
    """Classify BMI using standard adult screening cutoffs."""
    if bmi is None:
        return "Enter valid height and weight"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal Weight"
    if bmi < 30:
        return "Overweight"
    return "Obese"


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

def get_rounded_image(image_path, size=(64, 64), radius=None):
    """
    Load an image from image_path, crop/fit to size, apply a rounded or circular mask
    with anti-aliasing, and return a Tkinter ImageTk.PhotoImage object.
    """
    import os
    from PIL import Image, ImageDraw, ImageTk

    if not os.path.exists(image_path):
        return None

    try:
        img = Image.open(image_path).convert("RGBA")
        scale = 4
        w, h = size[0] * scale, size[1] * scale
        img = img.resize((w, h), Image.Resampling.LANCZOS)
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)

        if radius is None:
            draw.ellipse((0, 0, w, h), fill=255)
        else:
            draw.rounded_rectangle((0, 0, w, h), radius=radius * scale, fill=255)

        output = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        output.paste(img, (0, 0), mask)
        output = output.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(output)
    except Exception as e:
        print(f"Error creating rounded image from {image_path}: {e}")
        return None


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