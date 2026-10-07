# screens.py
# Vital Forge — Application screens and navigation.

import datetime
import random
import tkinter as tk
from tkinter import messagebox, ttk

from config import (
    APP_NAME,
    FONT_FAMILY,
    BG_COLOR, CARD_COLOR, INPUT_COLOR,
    GREEN, DARK_GREEN, LIGHT_GREEN,
    BROWN, DARK_BROWN, LIGHT_BROWN,
    TEXT_COLOR, MUTED_TEXT, BORDER_COLOR,
    SUCCESS_COLOR, WARNING_COLOR, ERROR_COLOR,
    FONT_SMALL, FONT_BODY, FONT_BODY_BOLD,
    FONT_BUTTON, FONT_SECTION, FONT_HEADING,
    FONT_PAGE_TITLE, FONT_TITLE,
    SPACING_4, SPACING_8, SPACING_16, SPACING_24, SPACING_32, SPACING_40,
    PAGE_PAD, CARD_PAD, FIELD_GAP, LABEL_GAP, SECTION_GAP,
    DEMO_EMAIL, DEMO_PASSWORD, resource_path,
)

from data import (
    FOODS, WORKOUTS, QUOTES, WEEKLY_WORKOUT_SCHEDULE,
    GENDER_OPTIONS, ACTIVITY_LEVELS, LONG_TERM_GOALS,
    DEFAULT_WATER_GOAL, DEFAULT_SLEEP_GOAL, DEFAULT_STEPS_GOAL,
)

from utils import (
    hash_password, verify_password,
    is_valid_email, is_valid_password, is_valid_name,
    get_goal_description, clear_frame,
    get_rounded_image, center_toplevel, calculate_bmi, get_bmi_category,
)

from ui_components import (
    configure_styles,
    Card, VFButton,
    create_title, create_page_title, create_heading,
    create_section_label, create_label, create_muted_label,
    create_entry, create_combobox, create_progress_bar,
    create_spinbox, create_checkbox, create_separator,
    StatCard, ScrollableFrame,
    build_field,
)

from database import queries
from database.connection import test_connection

from charts import (
    create_workout_completion_chart,
    create_weight_chart,
    create_daily_metrics_chart,
    create_goal_progress_chart,
    create_goal_pie_chart,
)


# =========================================================
# MAIN APP CLASS
# =========================================================

class VitalForgeApp:
    """Root application controller."""

    def __init__(self, root):
        self.root = root

        self.user      = None
        self.user_id   = None
        self.profile   = None
        self.demo_mode = False

        self.main_container = None
        self.content_frame  = None
        self.nav_frame      = None

        self._image_cache = {}
        self.selected_workout_date = datetime.date.today()

        self.quote = random.choice(QUOTES)

        # Demo in-memory stores
        self.demo_tracking      = {}
        self.demo_food_logs     = []
        self.demo_workout_history = {}
        self.demo_exercise_logs = {}

        configure_styles()
        self.root.configure(bg=BG_COLOR)
        self.show_login()

    # ─────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────

    def _get_logo(self, size=(64, 64), radius=None):
        """Retrieve or cache a rounded Tkinter photo logo."""
        key = (size, radius)
        if key not in self._image_cache:
            logo_path = resource_path("assets/logo.png")
            self._image_cache[key] = get_rounded_image(logo_path, size=size, radius=radius)
        return self._image_cache[key]

    def set_title(self, page=""):
        self.root.title(f"{APP_NAME}  —  {page}" if page else APP_NAME)

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _make_root_frame(self):
        self.clear_root()
        f = tk.Frame(self.root, bg=BG_COLOR)
        f.pack(fill="both", expand=True)
        self.main_container = f
        return f

    def show_error(self, title, msg):
        messagebox.showerror(title, msg)

    def show_info(self, title, msg):
        messagebox.showinfo(title, msg)

    def logout(self):
        self.user = self.user_id = self.profile = None
        self.demo_mode = False
        self.demo_tracking = {}
        self.demo_food_logs = []
        self.demo_workout_history = {}
        self.demo_exercise_logs = {}
        self.selected_workout_date = datetime.date.today()
        self.show_login()

    # ─────────────────────────────────────────────────────
    # AUTH SCREENS
    # ─────────────────────────────────────────────────────

    def show_login(self):
        self.set_title("Login")
        outer = self._make_root_frame()

        # Centering container
        card = Card(outer, padding=SPACING_40)
        card.place(relx=0.5, rely=0.5, anchor="center", width=440)

        inner = card.content

        # Rounded Logo
        logo_img = self._get_logo((80, 80))
        if logo_img:
            tk.Label(inner, image=logo_img, bg=CARD_COLOR).pack(pady=(0, SPACING_8))
        else:
            tk.Label(
                inner, text="🌿", bg=CARD_COLOR, fg=GREEN,
                font=(FONT_FAMILY, 28),
            ).pack(pady=(0, SPACING_4))

        create_title(inner, APP_NAME, bg=CARD_COLOR).pack(anchor="center")

        create_muted_label(
            inner, "Build healthier habits, one day at a time.", bg=CARD_COLOR,
        ).pack(anchor="center", pady=(SPACING_4, SPACING_24))

        create_separator(inner).pack(fill="x", pady=(0, SPACING_24))

        # Fields
        create_label(inner, "Email", bg=CARD_COLOR).pack(anchor="w")
        email_e = create_entry(inner)
        email_e.pack(fill="x", pady=(LABEL_GAP, FIELD_GAP))

        create_label(inner, "Password", bg=CARD_COLOR).pack(anchor="w")
        pass_e = create_entry(inner, show="*")
        pass_e.pack(fill="x", pady=(LABEL_GAP, SPACING_24))

        def do_login():
            email = email_e.get().strip().lower()
            pw    = pass_e.get()
            if not email or not pw:
                self.show_error("Login", "Please enter your email and password.")
                return
            if email == DEMO_EMAIL and pw == DEMO_PASSWORD:
                self.start_demo_mode()
                return
            if not test_connection():
                self.show_error(
                    "Database",
                    "Cannot connect to MySQL.\n\nPlease ensure MySQL is running and the "
                    "database is set up as described in README.md."
                )
                return
            try:
                user = queries.get_user_by_email(email)
                if not user:
                    self.show_error("Login", "No account found with that email.")
                    return
                if not verify_password(pw, user["password_hash"]):
                    self.show_error("Login", "Incorrect password.")
                    return
                self.user     = user
                self.user_id  = user["user_id"]
                self.demo_mode = False
                self.profile   = queries.get_profile(self.user_id)
                if self.profile:
                    self.show_dashboard()
                else:
                    self.show_survey()
            except Exception as e:
                self.show_error("Login Error", str(e))

        VFButton(inner, "Login", command=do_login).pack(fill="x", pady=(0, SPACING_8))
        VFButton(
            inner, "Create an account", command=self.show_register,
            style="secondary",
        ).pack(fill="x")

        create_muted_label(
            inner,
            f"Demo:  {DEMO_EMAIL}  /  {DEMO_PASSWORD}",
            bg=CARD_COLOR,
        ).pack(anchor="center", pady=(SPACING_16, 0))

        pass_e.bind("<Return>", lambda e: do_login())

    # ─────────────────────────────────────────────────────

    def show_register(self):
        self.set_title("Create Account")
        outer = self._make_root_frame()

        card = Card(outer, padding=SPACING_40)
        card.place(relx=0.5, rely=0.5, anchor="center", width=460)
        inner = card.content

        # Rounded Logo
        logo_img = self._get_logo((64, 64))
        if logo_img:
            tk.Label(inner, image=logo_img, bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_8))

        create_page_title(inner, "Create your account", bg=CARD_COLOR).pack(anchor="w")
        create_muted_label(
            inner, "Only Name, Email and Password are needed here.", bg=CARD_COLOR,
        ).pack(anchor="w", pady=(SPACING_4, SPACING_24))

        create_label(inner, "Name", bg=CARD_COLOR).pack(anchor="w")
        name_e = create_entry(inner)
        name_e.pack(fill="x", pady=(LABEL_GAP, FIELD_GAP))

        create_label(inner, "Email", bg=CARD_COLOR).pack(anchor="w")
        email_e = create_entry(inner)
        email_e.pack(fill="x", pady=(LABEL_GAP, FIELD_GAP))

        create_label(inner, "Password", bg=CARD_COLOR).pack(anchor="w")
        pass_e = create_entry(inner, show="*")
        pass_e.pack(fill="x", pady=(LABEL_GAP, SPACING_24))

        def do_register():
            name  = name_e.get().strip()
            email = email_e.get().strip().lower()
            pw    = pass_e.get()
            if not is_valid_name(name):
                self.show_error("Registration", "Please enter a valid name.")
                return
            if not is_valid_email(email):
                self.show_error("Registration", "Please enter a valid email address.")
                return
            if not is_valid_password(pw):
                self.show_error(
                    "Registration",
                    "Password must be at least 8 characters and include letters and numbers.",
                )
                return
            if email == DEMO_EMAIL:
                self.show_error("Registration", "That email is reserved for the demo account.")
                return
            if not test_connection():
                self.show_error("Database", "MySQL could not be reached. Real accounts require MySQL.")
                return
            try:
                if queries.get_user_by_email(email):
                    if messagebox.askyesno(
                        "Account Exists",
                        "An account with that email address already exists.\n\n"
                        "Would you like to go to the Login screen to log in?"
                    ):
                        self.show_login()
                    return
                uid = queries.create_user(name, email, hash_password(pw), False)
                self.user      = queries.get_user_by_id(uid)
                self.user_id   = uid
                self.demo_mode = False
                self.show_survey()
            except Exception as e:
                self.show_error("Registration Error", str(e))

        VFButton(inner, "Create Account", command=do_register).pack(fill="x", pady=(0, SPACING_8))
        VFButton(inner, "Back to Login", command=self.show_login, style="secondary").pack(fill="x")

    # ─────────────────────────────────────────────────────
    # SURVEY
    # ─────────────────────────────────────────────────────

    def show_survey(self):
        self.set_title("Fitness Survey")
        outer = self._make_root_frame()

        scroll = ScrollableFrame(outer)
        scroll.pack(fill="both", expand=True)

        page = scroll.scrollable_frame

        header = tk.Frame(page, bg=BG_COLOR)
        header.pack(fill="x", padx=PAGE_PAD, pady=(SPACING_32, SPACING_16))

        create_page_title(header, "Tell us about yourself").pack(anchor="w")
        create_muted_label(
            header,
            "This helps Vital Forge personalise your dashboard and workout suggestions.",
        ).pack(anchor="w", pady=(SPACING_4, 0))

        card = Card(page, padding=SPACING_32)
        card.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_32))
        inner = card.content

        # ── fields ───────────────────────────────────────────────────────────
        def row(parent):
            f = tk.Frame(parent, bg=CARD_COLOR)
            f.pack(fill="x", pady=(0, FIELD_GAP))
            return f

        # Age
        create_label(inner, "Age", bg=CARD_COLOR).pack(anchor="w")
        age_e = create_entry(inner)
        age_e.pack(fill="x", pady=(LABEL_GAP, FIELD_GAP))

        # Gender
        create_label(inner, "Gender", bg=CARD_COLOR).pack(anchor="w")
        gender_box = create_combobox(inner, GENDER_OPTIONS)
        gender_box.pack(fill="x", pady=(LABEL_GAP, FIELD_GAP))

        # Height / Weight on same row
        hw = tk.Frame(inner, bg=CARD_COLOR)
        hw.pack(fill="x", pady=(0, FIELD_GAP))
        hw.columnconfigure(0, weight=1)
        hw.columnconfigure(1, weight=1)

        lh = tk.Frame(hw, bg=CARD_COLOR)
        lh.grid(row=0, column=0, sticky="ew", padx=(0, SPACING_8))
        create_label(lh, "Height (cm)", bg=CARD_COLOR).pack(anchor="w")
        height_e = create_entry(lh)
        height_e.pack(fill="x", pady=(LABEL_GAP, 0))

        lw = tk.Frame(hw, bg=CARD_COLOR)
        lw.grid(row=0, column=1, sticky="ew", padx=(SPACING_8, 0))
        create_label(lw, "Weight (kg)", bg=CARD_COLOR).pack(anchor="w")
        weight_e = create_entry(lw)
        weight_e.pack(fill="x", pady=(LABEL_GAP, 0))

        create_separator(inner).pack(fill="x", pady=SPACING_16)

        # Activity
        create_label(inner, "Activity Level", bg=CARD_COLOR).pack(anchor="w")
        activity_box = create_combobox(inner, ACTIVITY_LEVELS)
        activity_box.pack(fill="x", pady=(LABEL_GAP, FIELD_GAP))

        # Goals row
        go = tk.Frame(inner, bg=CARD_COLOR)
        go.pack(fill="x", pady=(0, FIELD_GAP))
        go.columnconfigure(0, weight=1)
        go.columnconfigure(1, weight=1)
        go.columnconfigure(2, weight=1)

        def goal_col(parent, col, label, default):
            f = tk.Frame(parent, bg=CARD_COLOR)
            px_l = 0 if col == 0 else SPACING_8
            px_r = 0 if col == 2 else SPACING_8
            f.grid(row=0, column=col, sticky="ew", padx=(px_l, px_r))
            create_label(f, label, bg=CARD_COLOR).pack(anchor="w")
            e = create_entry(f)
            e.insert(0, str(default))
            e.pack(fill="x", pady=(LABEL_GAP, 0))
            return e

        water_e = goal_col(go, 0, "Water Goal (ml)", DEFAULT_WATER_GOAL)
        sleep_e = goal_col(go, 1, "Sleep Goal (hrs)", DEFAULT_SLEEP_GOAL)
        steps_e = goal_col(go, 2, "Steps Goal",       DEFAULT_STEPS_GOAL)

        create_separator(inner).pack(fill="x", pady=SPACING_16)

        # Long-term goal
        create_label(inner, "Long-Term Goal", bg=CARD_COLOR).pack(anchor="w")
        goal_box = create_combobox(inner, LONG_TERM_GOALS)
        goal_box.pack(fill="x", pady=(LABEL_GAP, SPACING_4))

        desc_label = create_muted_label(inner, get_goal_description(LONG_TERM_GOALS[0]), bg=CARD_COLOR)
        desc_label.pack(anchor="w", pady=(0, SPACING_24))

        # Pre-fill profile if existing
        p = self.profile or {}
        if p.get("age"):
            age_e.insert(0, str(p["age"]))
        if p.get("gender") and p["gender"] in GENDER_OPTIONS:
            gender_box.set(p["gender"])
        if p.get("height_cm"):
            height_e.insert(0, str(p["height_cm"]))
        if p.get("weight_kg"):
            weight_e.insert(0, str(p["weight_kg"]))
        if p.get("activity_level") and p["activity_level"] in ACTIVITY_LEVELS:
            activity_box.set(p["activity_level"])
        if p.get("water_goal_ml"):
            water_e.delete(0, tk.END)
            water_e.insert(0, str(p["water_goal_ml"]))
        if p.get("sleep_goal_hours"):
            sleep_e.delete(0, tk.END)
            sleep_e.insert(0, str(p["sleep_goal_hours"]))
        if p.get("steps_goal"):
            steps_e.delete(0, tk.END)
            steps_e.insert(0, str(p["steps_goal"]))
        if p.get("long_term_goal") and p["long_term_goal"] in LONG_TERM_GOALS:
            goal_box.set(p["long_term_goal"])
            desc_label.config(text=get_goal_description(p["long_term_goal"]))

        def _update_desc(e=None):
            g = goal_box.get()
            desc_label.config(text=get_goal_description(g) if g else "")
        goal_box.bind("<<ComboboxSelected>>", _update_desc)

        # ── save ─────────────────────────────────────────────────────────────
        def do_save():
            try:
                age    = int(age_e.get())
                height = float(height_e.get())
                weight = float(weight_e.get())
                water  = int(water_e.get())
                sleep  = float(sleep_e.get())
                steps  = int(steps_e.get())
            except ValueError:
                self.show_error("Survey", "Please enter valid numbers in all numeric fields.")
                return

            gender   = gender_box.get().strip()
            activity = activity_box.get().strip()
            goal     = goal_box.get().strip()

            if not (1 <= age <= 120):
                self.show_error("Survey", "Please enter a valid age (1–120).")
                return
            if height <= 0 or weight <= 0:
                self.show_error("Survey", "Height and weight must be positive numbers.")
                return
            if water <= 0 or sleep <= 0 or steps <= 0:
                self.show_error("Survey", "Daily goals must be greater than zero.")
                return
            if not gender or not activity or not goal:
                self.show_error("Survey", "Please complete every field.")
                return

            profile_data = {
                "age":              age,
                "gender":           gender,
                "height_cm":        height,
                "weight_kg":        weight,
                "activity_level":   activity,
                "water_goal_ml":    water,
                "sleep_goal_hours": sleep,
                "steps_goal":       steps,
                "long_term_goal":   goal,
            }

            try:
                if self.demo_mode:
                    self.profile = {"user_id": self.user_id, **profile_data}
                else:
                    queries.save_profile(self.user_id, profile_data)
                    self.profile = queries.get_profile(self.user_id)
                self.show_dashboard()
            except Exception as e:
                self.show_error("Survey Error", str(e))

        VFButton(inner, "Save & Continue", command=do_save).pack(anchor="e")

    # ─────────────────────────────────────────────────────
    # DEMO MODE
    # ─────────────────────────────────────────────────────

    def _build_personalized_workout_plan(self, target_date=None):
        """Create a workout recommendation from the user's profile and goals."""
        if target_date is None:
            target_date = getattr(self, "selected_workout_date", datetime.date.today())

        schedule = WEEKLY_WORKOUT_SCHEDULE[target_date.weekday()]
        if not schedule.get("exercises"):
            return {
                "name": "Recovery Day",
                "description": "Light movement, mobility, and recovery-focused recovery work.",
                "difficulty": "Beginner",
                "completed": True,
                "day": schedule["day"],
                "focus": "Recovery and mobility",
                "exercises": ["Mobility flow", "Easy walk", "Stretch and reset"],
                "target_date": target_date,
            }

        goal = str((self.profile or {}).get("long_term_goal", "General fitness")).strip() or "General fitness"
        activity = str((self.profile or {}).get("activity_level", "Moderately active")).strip() or "Moderately active"

        goal_map = {
            "Weight loss": {
                "name": "Fat-Burning Circuit",
                "focus": "Low-impact cardio and calorie burn",
                "exercises": ["Brisk walking intervals", "Bodyweight squats", "Incline push-ups", "Plank holds"],
            },
            "Weight gain": {
                "name": "Lean Mass Builder",
                "focus": "Controlled strength and recovery",
                "exercises": ["Goblet squats", "Incline push-ups", "Bent-over rows", "Rested lunges"],
            },
            "Muscular build": {
                "name": "Strength Builder",
                "focus": "Progressive strength and muscular control",
                "exercises": ["Air squats", "Push-ups", "Rows", "Reverse lunges", "Core holds"],
            },
            "Endurance": {
                "name": "Endurance Session",
                "focus": "Steady aerobic work and stamina",
                "exercises": ["Brisk march", "Step-ups", "Jumping jacks", "Wall sits", "Rowing motion"],
            },
            "General fitness": {
                "name": "Balanced Fitness",
                "focus": "Steady strength, movement quality, and conditioning",
                "exercises": ["Dynamic warm-up", "Bodyweight squats", "Push-ups", "Core activation", "Easy cardio"],
            },
        }

        recommendation = goal_map.get(goal, goal_map["General fitness"])
        difficulty = "Beginner"
        if activity in {"Very active", "Extremely active"}:
            difficulty = "Intermediate"

        exercises = list(recommendation["exercises"])
        if activity in {"Sedentary", "Lightly active"}:
            exercises = exercises[:3]

        return {
            "name": recommendation["name"],
            "description": (
                f"{schedule['day']} plan tailored for {goal.lower()} and a {activity.lower()} lifestyle. "
                f"Focus on controlled effort and consistency."
            ),
            "difficulty": difficulty,
            "completed": False,
            "day": schedule["day"],
            "focus": recommendation["focus"],
            "exercises": exercises,
            "target_date": target_date,
        }

    def start_demo_mode(self):
        self.demo_mode = True
        self.user = {
            "user_id": 0, "name": "Demo User",
            "email": DEMO_EMAIL, "is_demo": True,
        }
        self.user_id = 0
        self.profile = {
            "user_id": 0,
            "age": 25, "gender": "Prefer not to say",
            "height_cm": 170.0, "weight_kg": 70.0,
            "activity_level": "Moderately active",
            "water_goal_ml":    DEFAULT_WATER_GOAL,
            "sleep_goal_hours": DEFAULT_SLEEP_GOAL,
            "steps_goal":       DEFAULT_STEPS_GOAL,
            "long_term_goal":   "General fitness",
        }
        self.demo_tracking = {}
        self.demo_food_logs = []
        self.demo_workout_history = {}
        self.demo_exercise_logs = {}
        self.show_dashboard()

    # ─────────────────────────────────────────────────────
    # APP SHELL (nav + content area)
    # ─────────────────────────────────────────────────────

    def build_app_shell(self, active_tab="Dashboard"):
        self.clear_root()

        shell = tk.Frame(self.root, bg=BG_COLOR)
        shell.pack(fill="both", expand=True)

        # ── Top bar ───────────────────────────────────────────
        topbar = tk.Frame(shell, bg=CARD_COLOR, height=56)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        # Brand header with rounded logo
        brand_frame = tk.Frame(topbar, bg=CARD_COLOR)
        brand_frame.pack(side="left", padx=SPACING_24)

        logo_img = self._get_logo((34, 34))
        if logo_img:
            tk.Label(brand_frame, image=logo_img, bg=CARD_COLOR).pack(side="left", padx=(0, SPACING_8))

        tk.Label(
            brand_frame, text=APP_NAME,
            font=FONT_SECTION, bg=CARD_COLOR, fg=DARK_GREEN,
        ).pack(side="left")

        # Quote (truncated so it never overflows)
        quote_text = (self.quote[:80] + "…") if len(self.quote) > 80 else self.quote
        tk.Label(
            topbar, text=f"« {quote_text} »",
            font=FONT_SMALL, bg=CARD_COLOR, fg=MUTED_TEXT,
        ).pack(side="left", padx=SPACING_16, fill="x", expand=True)

        VFButton(
            topbar, "Logout", command=self.logout, style="ghost",
        ).pack(side="right", padx=SPACING_16)

        # Thin divider
        create_separator(shell).pack(fill="x")

        # ── Sidebar nav ───────────────────────────────────────
        sidebar = tk.Frame(shell, bg=CARD_COLOR, width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Spacer at top
        tk.Frame(sidebar, bg=CARD_COLOR, height=SPACING_16).pack(fill="x")

        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Workout",   self.show_workout),
            ("Food",      self.show_food),
            ("Progress",  self.show_progress),
            ("Profile",   self.show_profile),
        ]

        for name, command in nav_items:
            is_active = (name == active_tab)

            btn_frame = tk.Frame(
                sidebar,
                bg=LIGHT_GREEN if is_active else CARD_COLOR,
            )
            btn_frame.pack(fill="x", padx=SPACING_16, pady=SPACING_4)

            # Active indicator bar
            if is_active:
                tk.Frame(btn_frame, bg=GREEN, width=4).pack(side="left", fill="y")

            tk.Label(
                btn_frame,
                text=name,
                bg=LIGHT_GREEN if is_active else CARD_COLOR,
                fg=DARK_GREEN  if is_active else TEXT_COLOR,
                font=FONT_BODY_BOLD if is_active else FONT_BODY,
                anchor="w",
                cursor="hand2",
                padx=SPACING_16,
                pady=SPACING_8,
            ).pack(side="left", fill="x", expand=True)

            btn_frame.bind("<Button-1>", lambda e, cmd=command: cmd())
            for child in btn_frame.winfo_children():
                child.bind("<Button-1>", lambda e, cmd=command: cmd())

        # Right-side thin divider
        create_separator(sidebar).pack(side="right", fill="y")

        # ── Content area ──────────────────────────────────────
        self.content_frame = tk.Frame(shell, bg=BG_COLOR)
        self.content_frame.pack(side="left", fill="both", expand=True)

    # ─────────────────────────────────────────────────────
    # DASHBOARD
    # ─────────────────────────────────────────────────────

    def show_dashboard(self):
        self.set_title("Dashboard")
        self.build_app_shell("Dashboard")

        scroll = ScrollableFrame(self.content_frame)
        scroll.pack(fill="both", expand=True)
        page = scroll.scrollable_frame

        # ── Header ───────────────────────────────────────────
        hdr = tk.Frame(page, bg=BG_COLOR)
        hdr.pack(fill="x", padx=PAGE_PAD, pady=(SPACING_32, SPACING_8))

        name = self.user.get("name", "there")
        create_page_title(hdr, f"Good day, {name}").pack(anchor="w")
        create_muted_label(hdr, "Here's your daily fitness overview.").pack(anchor="w", pady=(SPACING_4, 0))

        # ── Stat cards ────────────────────────────────────────
        today_data = self._get_today_tracking()

        water = today_data.get("water_ml", 0) or 0
        steps = today_data.get("steps",    0) or 0
        sleep = today_data.get("sleep_hours", 0) or 0
        tracked_weight = today_data.get("weight_kg") or self.profile.get("weight_kg")
        bmi_weight = self.profile.get("weight_kg") or tracked_weight
        h_cm = self.profile.get("height_cm")
        bmi = calculate_bmi(bmi_weight, h_cm)
        bmi_cat = get_bmi_category(bmi)
        bmi_color = (
            WARNING_COLOR if bmi_cat == "Underweight"
            else SUCCESS_COLOR if bmi_cat == "Normal Weight"
            else BROWN if bmi_cat == "Overweight"
            else ERROR_COLOR if bmi_cat == "Obese"
            else MUTED_TEXT
        )
        bmi_status = bmi_cat

        wg = self.profile.get("water_goal_ml", DEFAULT_WATER_GOAL)
        sg = self.profile.get("steps_goal", DEFAULT_STEPS_GOAL)
        lg = self.profile.get("sleep_goal_hours", DEFAULT_SLEEP_GOAL)

        stat_row = tk.Frame(page, bg=BG_COLOR)
        stat_row.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
        stat_row.columnconfigure((0, 1, 2, 3), weight=1)

        StatCard(
            stat_row, "Water",
            f"{water:,.0f} ml",
            f"Goal: {wg:,} ml",
            progress=water / wg if wg else 0,
            accent=GREEN,
        ).grid(row=0, column=0, sticky="nsew", padx=(0, SPACING_4))

        StatCard(
            stat_row, "Steps",
            f"{steps:,}",
            f"Goal: {sg:,}",
            progress=steps / sg if sg else 0,
            accent=BROWN,
        ).grid(row=0, column=1, sticky="nsew", padx=SPACING_4)

        StatCard(
            stat_row, "Sleep",
            f"{sleep:.1f} hrs",
            f"Goal: {lg:.1f} hrs",
            progress=sleep / lg if lg else 0,
            accent=DARK_GREEN,
        ).grid(row=0, column=2, sticky="nsew", padx=SPACING_4)

        StatCard(
            stat_row, "BMI",
            f"{bmi:.1f} kg/m²" if bmi is not None else "—",
            f"Status: {bmi_status}",
            accent=bmi_color,
        ).grid(row=0, column=3, sticky="nsew", padx=(SPACING_4, 0))

        # ── Daily tracking form ───────────────────────────────
        tc = Card(page, padding=SPACING_24)
        tc.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
        ti = tc.content

        create_section_label(ti, "Daily Tracking", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_16))

        water_var  = tk.StringVar(value=str(int(water)))
        steps_var  = tk.StringVar(value=str(int(steps)))
        sleep_var  = tk.StringVar(value=str(sleep))
        weight_var = tk.StringVar(value=str(tracked_weight))

        def _track_row(parent, label, var, unit=""):
            row = tk.Frame(parent, bg=CARD_COLOR)
            row.pack(fill="x", pady=SPACING_4)
            lbl_txt = f"{label}  {unit}" if unit else label
            tk.Label(
                row, text=lbl_txt,
                bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_BODY,
                width=22, anchor="w",
            ).pack(side="left")
            e = create_entry(row)
            e.insert(0, var.get())
            e.pack(side="left", fill="x", expand=True)
            e.bind("<KeyRelease>", lambda ev: var.set(e.get()))
            return e

        _track_row(ti, "Water", water_var, "(ml)")
        _track_row(ti, "Steps", steps_var)
        _track_row(ti, "Sleep", sleep_var, "(hours)")
        _track_row(ti, "Weight", weight_var, "(kg)")

        def do_save_tracking():
            try:
                new_water  = max(0, float(water_var.get() or 0))
                new_steps  = max(0, int(float(steps_var.get() or 0)))
                new_sleep  = max(0, float(sleep_var.get() or 0))
                new_weight = max(0, float(weight_var.get() or 0))
            except ValueError:
                self.show_error("Tracking", "Please enter valid numbers.")
                return

            data = {
                "water_ml":    new_water,
                "steps":       new_steps,
                "sleep_hours": new_sleep,
                "weight_kg":   new_weight if new_weight > 0 else today_data.get("weight_kg"),
                "notes":       today_data.get("notes", ""),
            }

            try:
                if self.demo_mode:
                    self.demo_tracking[str(datetime.date.today())] = data
                    if new_weight > 0:
                        self.profile["weight_kg"] = new_weight
                else:
                    queries.save_daily_tracking(self.user_id, data)
                    if new_weight > 0:
                        self.profile["weight_kg"] = new_weight
                        queries.save_profile(self.user_id, self.profile)
                self.show_dashboard()
            except Exception as e:
                self.show_error("Tracking Error", str(e))

        VFButton(ti, "Save Today's Tracking", command=do_save_tracking).pack(anchor="e", pady=(SPACING_16, 0))

        # ── Today's workout preview ───────────────────────────
        wc = Card(page, padding=SPACING_24)
        wc.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
        wi = wc.content

        create_section_label(wi, "Today's Workout", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_8))

        workout = self._get_or_assign_workout()

        if workout:
            tk.Label(
                wi, text=workout["name"],
                bg=CARD_COLOR, fg=DARK_GREEN, font=FONT_BODY_BOLD,
            ).pack(anchor="w")

            tk.Label(
                wi, text=workout.get("description", ""),
                bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_BODY,
                wraplength=800, justify="left",
            ).pack(anchor="w", pady=(SPACING_4, SPACING_8))

            done = bool(workout.get("completed"))
            tk.Label(
                wi,
                text="✔  Completed" if done else "○  Not yet completed",
                bg=CARD_COLOR,
                fg=SUCCESS_COLOR if done else MUTED_TEXT,
                font=FONT_BODY_BOLD,
            ).pack(anchor="w")

            VFButton(
                wi, "Open Workout", command=self.show_workout, style="accent",
            ).pack(anchor="e", pady=(SPACING_8, 0))
        else:
            create_muted_label(wi, "No workout assigned yet.", bg=CARD_COLOR).pack(anchor="w")

        # ── Long-term goal with Pie Chart & Interactive Logger ──
        gc = Card(page, padding=SPACING_24)
        gc.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_32))
        gi = gc.content

        goal = self.profile.get("long_term_goal", "General fitness")

        goal_split = tk.Frame(gi, bg=CARD_COLOR)
        goal_split.pack(fill="x")
        goal_split.columnconfigure(0, weight=3)
        goal_split.columnconfigure(1, weight=2)

        left_info = tk.Frame(goal_split, bg=CARD_COLOR)
        left_info.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING_16))

        create_section_label(left_info, "Long-Term Goal Progress", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_8))
        tk.Label(left_info, text=goal, bg=CARD_COLOR, fg=DARK_GREEN, font=FONT_BODY_BOLD).pack(anchor="w")
        tk.Label(
            left_info, text=get_goal_description(goal),
            bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_BODY,
            wraplength=450, justify="left",
        ).pack(anchor="w", pady=(SPACING_4, SPACING_16))

        # Retrieve current goal progress %
        if self.demo_mode:
            demo_prog = self._demo_goal_progress()
            current_pct = float(demo_prog[-1]["progress_value"]) if demo_prog else 0.0
        else:
            try:
                prog_recs = queries.get_goal_progress(self.user_id, 30)
                if prog_recs:
                    r0 = prog_recs[-1]
                    current_pct = float(r0.get("progress_percentage") or r0.get("progress_value") or 0.0)
                else:
                    current_pct = 0.0
            except Exception:
                current_pct = 0.0

        # Progress entry form
        prog_form = tk.Frame(left_info, bg=CARD_COLOR)
        prog_form.pack(anchor="w", pady=(SPACING_8, 0))

        tk.Label(prog_form, text="Update Goal Progress (%): ", bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_SMALL).pack(side="left")
        prog_e = create_spinbox(prog_form, from_=0, to=100, increment=5, width=6)
        prog_e.delete(0, tk.END)
        prog_e.insert(0, f"{current_pct:.0f}")
        prog_e.pack(side="left", padx=(SPACING_4, SPACING_16))

        def do_update_goal_progress():
            try:
                val = max(0.0, min(100.0, float(prog_e.get() or 0)))
            except ValueError:
                self.show_error("Goal Progress", "Please enter a valid number (0–100).")
                return

            try:
                if self.demo_mode:
                    today_d = datetime.date.today()
                    # Update demo goal progress
                    if hasattr(self, "_custom_demo_goal_pct"):
                        self._custom_demo_goal_pct = val
                    else:
                        self._custom_demo_goal_pct = val
                else:
                    queries.save_goal_progress(self.user_id, val, datetime.date.today())
                self.show_info("Goal Progress Updated", f"Goal progress updated to {val:.0f}%. Graph updated!")
                self.show_dashboard()
            except Exception as ex:
                self.show_error("Goal Progress Error", str(ex))

        VFButton(prog_form, "Update Graph", command=do_update_goal_progress, style="accent").pack(side="left")

        right_pie = tk.Frame(goal_split, bg=CARD_COLOR)
        right_pie.grid(row=0, column=1, sticky="nsew")

        try:
            effective_pct = getattr(self, "_custom_demo_goal_pct", current_pct) if self.demo_mode else current_pct
            create_goal_pie_chart(right_pie, goal, effective_pct)
        except Exception as ex:
            create_muted_label(right_pie, f"Pie chart unavailable: {ex}", bg=CARD_COLOR).pack()

    # ─────────────────────────────────────────────────────
    # TRACKING HELPERS
    # ─────────────────────────────────────────────────────

    def _get_today_tracking(self):
        today_str = str(datetime.date.today())
        empty = {
            "water_ml": 0, "steps": 0, "sleep_hours": 0,
            "weight_kg": self.profile.get("weight_kg"), "notes": "",
        }
        if self.demo_mode:
            return self.demo_tracking.get(today_str, empty)
        result = queries.get_daily_tracking(self.user_id)
        return result if result else empty

    def _get_or_assign_workout(self, target_date=None):
        if target_date is None:
            target_date = getattr(self, "selected_workout_date", datetime.date.today())

        if self.demo_mode:
            key = str(target_date)
            if key in self.demo_workout_history:
                return self.demo_workout_history[key]

            workout = self._build_personalized_workout_plan(target_date)
            self.demo_workout_history[key] = workout
            return workout

        existing = queries.get_today_workout(self.user_id, target_date)
        if not existing:
            goal = (self.profile or {}).get("long_term_goal") or "General fitness"
            suitable = queries.get_workouts_for_goal(goal)
            if not suitable:
                suitable = queries.get_all_workouts()
            if not suitable:
                return None
            queries.assign_workout(self.user_id, suitable[0]["workout_id"], target_date)
            existing = queries.get_today_workout(self.user_id, target_date)

        if not existing:
            return None

        scheduled = WEEKLY_WORKOUT_SCHEDULE[target_date.weekday()]
        workout = dict(existing)
        workout.update({
            "name": existing.get("name") or scheduled["focus"],
            "description": existing.get("description") or f"{scheduled['day']}: complete the assigned workout plan.",
            "difficulty": existing.get("difficulty") or "Scheduled",
            "day": scheduled["day"],
            "focus": scheduled["focus"],
            "exercises": list(scheduled.get("exercises", [])),
            "target_date": target_date,
        })
        return workout

    # ─────────────────────────────────────────────────────
    # WORKOUT
    # ─────────────────────────────────────────────────────

    def show_workout(self):
        self.set_title("Workout")
        self.build_app_shell("Workout")

        scroll = ScrollableFrame(self.content_frame)
        scroll.pack(fill="both", expand=True)
        page = scroll.scrollable_frame

        hdr = tk.Frame(page, bg=BG_COLOR)
        hdr.pack(fill="x", padx=PAGE_PAD, pady=(SPACING_32, SPACING_8))
        
        target_date = getattr(self, "selected_workout_date", datetime.date.today())
        schedule = WEEKLY_WORKOUT_SCHEDULE[target_date.weekday()]
        
        create_page_title(hdr, f"{schedule['day']} Workout").pack(anchor="w")
        create_muted_label(
            hdr, target_date.strftime("%B %d, %Y") + " | Weekly workout plan",
        ).pack(anchor="w", pady=(SPACING_4, 0))

        # ── Day Selector (Monday to Sunday) ───────────────────
        date_nav = tk.Frame(page, bg=BG_COLOR)
        date_nav.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))

        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())

        for i in range(7):
            d = start_of_week + datetime.timedelta(days=i)
            is_selected = (d == target_date)
            is_today = (d == today)

            day_name = WEEKLY_WORKOUT_SCHEDULE[i]["day"][:3]
            lbl_txt = f"{day_name}\n{d.strftime('%b %d')}"
            if is_today:
                lbl_txt += "\n(Today)"

            btn_bg = LIGHT_GREEN if is_selected else CARD_COLOR
            fg_col = DARK_GREEN if is_selected else TEXT_COLOR

            f = tk.Frame(
                date_nav,
                bg=btn_bg,
                highlightbackground=GREEN if is_selected else BORDER_COLOR,
                highlightthickness=2 if is_selected else 1,
                cursor="hand2",
                padx=SPACING_4,
                pady=SPACING_8,
            )
            f.pack(side="left", fill="both", expand=True, padx=SPACING_4)

            lbl = tk.Label(
                f, text=lbl_txt, bg=btn_bg, fg=fg_col,
                font=FONT_BODY_BOLD if is_selected else FONT_SMALL,
                justify="center", cursor="hand2",
            )
            lbl.pack(expand=True)

            def _select_day(ev, day_val=d):
                self.selected_workout_date = day_val
                self.show_workout()

            f.bind("<Button-1>", _select_day)
            lbl.bind("<Button-1>", _select_day)

        workout = self._get_or_assign_workout(target_date)

        if not workout:
            card = Card(page, padding=SPACING_24)
            card.pack(fill="x", padx=PAGE_PAD)
            create_muted_label(card.content, "No workout could be assigned.", bg=CARD_COLOR).pack()
            return

        card = Card(page, padding=SPACING_32)
        card.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_32))
        inner = card.content

        tk.Label(
            inner, text=workout["focus"],
            bg=CARD_COLOR, fg=DARK_GREEN, font=FONT_HEADING,
        ).pack(anchor="w")

        diff_badge = tk.Frame(inner, bg=LIGHT_GREEN)
        diff_badge.pack(anchor="w", pady=(SPACING_4, SPACING_16))
        tk.Label(
            diff_badge,
            text=f"  {workout.get('difficulty', '')}  ",
            bg=LIGHT_GREEN, fg=DARK_GREEN, font=FONT_SMALL,
        ).pack()

        tk.Label(
            inner, text=workout.get("description", ""),
            bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_BODY,
            wraplength=750, justify="left",
        ).pack(anchor="w")

        create_separator(inner).pack(fill="x", pady=SPACING_24)

        if not workout["exercises"]:
            tk.Label(
                inner, text="Rest and recover today.",
                bg=CARD_COLOR, fg=SUCCESS_COLOR, font=FONT_BODY_BOLD,
            ).pack(anchor="w")
            return

        try:
            if self.demo_mode:
                checked = self.demo_exercise_logs.get(str(target_date), {})
            else:
                checked = {
                    row["exercise_index"]: bool(row["completed"])
                    for row in queries.get_exercise_logs(self.user_id, target_date)
                }
        except Exception as e:
            self.show_error("Workout Error", f"Could not load exercise checklist: {e}")
            return

        exercise_vars = []

        def save_exercise(index, exercise_name, variable):
            try:
                if self.demo_mode:
                    key = str(target_date)
                    self.demo_exercise_logs.setdefault(key, {})[index] = variable.get()
                else:
                    queries.save_exercise_log(
                        self.user_id, target_date, index, exercise_name, variable.get(),
                    )

                done = all(var.get() for var in exercise_vars)
                if self.demo_mode:
                    self.demo_workout_history[str(target_date)]["completed"] = done
                else:
                    queries.complete_workout(self.user_id, target_date, completed=done)
            except Exception as e:
                self.show_error("Workout Error", str(e))

        for index, exercise_name in enumerate(workout["exercises"], start=1):
            variable = tk.BooleanVar(value=checked.get(index, False))
            exercise_vars.append(variable)
            create_checkbox(
                inner,
                f"{index}. {exercise_name}",
                variable,
                command=lambda i=index, name=exercise_name, var=variable: save_exercise(i, name, var),
            ).pack(anchor="w", pady=(0, SPACING_8))

        if all(variable.get() for variable in exercise_vars):
            tk.Label(
                inner, text="✔  Great job — workout completed!",
                bg=CARD_COLOR, fg=SUCCESS_COLOR, font=FONT_BODY_BOLD,
            ).pack(anchor="w", pady=(SPACING_8, 0))

    # ─────────────────────────────────────────────────────
    # FOOD
    # ─────────────────────────────────────────────────────

    def show_food(self):
        self.set_title("Food")
        self.build_app_shell("Food")

        scroll = ScrollableFrame(self.content_frame)
        scroll.pack(fill="both", expand=True)
        page = scroll.scrollable_frame

        # Header
        hdr = tk.Frame(page, bg=BG_COLOR)
        hdr.pack(fill="x", padx=PAGE_PAD, pady=(SPACING_32, SPACING_8))
        
        title_box = tk.Frame(hdr, bg=BG_COLOR)
        title_box.pack(side="left", fill="x", expand=True)
        create_page_title(title_box, "Food & Nutrition").pack(anchor="w")
        create_muted_label(title_box, "Search, log foods, track net nutrients, and add custom entries.").pack(anchor="w", pady=(SPACING_4, 0))

        # Add Custom Food Button
        def open_add_custom_food_dialog():
            dlg = tk.Toplevel(self.root)
            dlg.title("Add Custom Food")
            center_toplevel(dlg, 440, 560)
            dlg.configure(bg=CARD_COLOR)
            dlg.grab_set()

            card = Card(dlg, padding=SPACING_24)
            card.pack(fill="both", expand=True, padx=SPACING_16, pady=SPACING_16)
            ci = card.content

            create_heading(ci, "New Custom Food", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_16))

            def _field(parent, label, default=""):
                create_label(parent, label, bg=CARD_COLOR).pack(anchor="w")
                e = create_entry(parent)
                if default:
                    e.insert(0, str(default))
                e.pack(fill="x", pady=(LABEL_GAP, SPACING_8))
                return e

            name_e    = _field(ci, "Food Name", "Protein Smoothie")
            serving_e = _field(ci, "Serving Size", "1 glass / 300ml")
            cal_e     = _field(ci, "Calories (kcal)", "250")
            prot_e    = _field(ci, "Protein (g)", "20")
            carbs_e   = _field(ci, "Carbohydrates (g)", "30")
            fat_e     = _field(ci, "Fat (g)", "5")
            fiber_e   = _field(ci, "Fiber (g)", "3")

            create_label(ci, "Category", bg=CARD_COLOR).pack(anchor="w")
            cat_box = create_combobox(ci, ["Custom", "Protein", "Dairy", "Grains & Cereals", "Indian", "Fruits", "Vegetables", "Other"])
            cat_box.set("Custom")
            cat_box.pack(fill="x", pady=(LABEL_GAP, SPACING_16))

            def do_save_custom():
                n = name_e.get().strip()
                s = serving_e.get().strip()
                if not n or not s:
                    messagebox.showerror("Error", "Name and serving size are required.", parent=dlg)
                    return
                try:
                    c = float(cal_e.get() or 0)
                    p = float(prot_e.get() or 0)
                    cb = float(carbs_e.get() or 0)
                    f = float(fat_e.get() or 0)
                    fb = float(fiber_e.get() or 0)
                except ValueError:
                    messagebox.showerror("Error", "Nutrient values must be numbers.", parent=dlg)
                    return

                category = cat_box.get() or "Custom"

                try:
                    if self.demo_mode:
                        FOODS.insert(0, {
                            "name": n, "serving_size": s, "calories": c,
                            "protein_g": p, "carbohydrates_g": cb,
                            "fat_g": f, "fiber_g": fb, "category": category
                        })
                    else:
                        queries.create_custom_food(n, s, c, p, cb, f, fb, category)

                    dlg.destroy()
                    self.show_info("Custom Food Added", f"'{n}' has been added to the database.")
                    do_search()
                except Exception as ex:
                    messagebox.showerror("Database Error", str(ex), parent=dlg)

            VFButton(ci, "Save Custom Food", command=do_save_custom, style="accent").pack(fill="x", pady=(SPACING_8, 0))

        VFButton(hdr, "+ Add Custom Food", command=open_add_custom_food_dialog, style="secondary").pack(side="right")

        # ── Net Nutrients Card ────────────────────────────────
        net_card = Card(page, padding=SPACING_16)
        net_card.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
        net_inner = net_card.content

        create_section_label(net_inner, "Daily Net Nutrients Consumed Today", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_8))
        nutrients_row = tk.Frame(net_inner, bg=CARD_COLOR)
        nutrients_row.pack(fill="x")

        def render_net_nutrients():
            for w in nutrients_row.winfo_children():
                w.destroy()

            if self.demo_mode:
                logged = list(self.demo_food_logs)
            else:
                try:
                    logged = queries.get_food_logs(self.user_id, datetime.date.today())
                except Exception:
                    logged = []

            tot_cal = tot_prot = tot_carbs = tot_fat = tot_fiber = 0.0

            for item in logged:
                s = float(item.get("servings") or 1)
                tot_cal += float(item.get("calories") or 0) * s
                tot_prot += float(item.get("protein_g") or 0) * s
                tot_carbs += float(item.get("carbohydrates_g") or 0) * s
                tot_fat += float(item.get("fat_g") or 0) * s
                tot_fiber += float(item.get("fiber_g") or 0) * s

            items = [
                ("Calories", f"{tot_cal:,.0f}", "kcal", GREEN),
                ("Protein", f"{tot_prot:.1f}", "g", DARK_GREEN),
                ("Carbs", f"{tot_carbs:.1f}", "g", BROWN),
                ("Fat", f"{tot_fat:.1f}", "g", DARK_BROWN),
                ("Fiber", f"{tot_fiber:.1f}", "g", SUCCESS_COLOR),
            ]

            nutrients_row.columnconfigure((0, 1, 2, 3, 4), weight=1)
            for idx, (label, val, unit, color) in enumerate(items):
                box = tk.Frame(
                    nutrients_row, bg=BG_COLOR,
                    highlightbackground=BORDER_COLOR, highlightthickness=1,
                    padx=SPACING_8, pady=SPACING_8,
                )
                box.grid(row=0, column=idx, sticky="nsew", padx=SPACING_4)
                tk.Label(box, text=label, bg=BG_COLOR, fg=MUTED_TEXT, font=FONT_SMALL).pack()
                tk.Label(box, text=val, bg=BG_COLOR, fg=color, font=FONT_HEADING).pack()
                tk.Label(box, text=unit, bg=BG_COLOR, fg=MUTED_TEXT, font=FONT_SMALL).pack()

        # Layout for Search and Log
        layout = tk.Frame(page, bg=BG_COLOR)
        layout.pack(fill="both", expand=True, padx=PAGE_PAD, pady=(0, SPACING_16))
        layout.grid_columnconfigure(0, weight=3)
        layout.grid_columnconfigure(1, weight=2)

        search_card = Card(layout, padding=SPACING_16)
        search_card.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING_8))
        search_inner = search_card.content

        search_row = tk.Frame(search_inner, bg=CARD_COLOR)
        search_row.pack(fill="x")

        search_e = create_entry(search_row)
        search_e.pack(side="left", fill="x", expand=True)

        results_scroll = ScrollableFrame(search_inner, background=CARD_COLOR, height=450)
        results_scroll.pack(fill="both", expand=True, pady=(SPACING_8, 0))
        results_wrap = results_scroll.scrollable_frame

        def do_search():
            for w in results_wrap.winfo_children():
                w.destroy()

            term = search_e.get().strip()

            if self.demo_mode:
                foods = [f for f in FOODS if (not term or term.lower() in f["name"].lower())][:60]
            else:
                try:
                    foods = queries.search_foods(term, 60)
                except Exception as e:
                    create_muted_label(results_wrap, f"Search error: {e}").pack(pady=SPACING_16)
                    return

            if not foods:
                create_muted_label(results_wrap, "No foods found.").pack(pady=SPACING_32)
                return

            for food in foods:
                self._food_row(results_wrap, food, refresh_all=refresh_food_view)

        VFButton(search_row, "Search", command=do_search, style="primary").pack(side="right", padx=(SPACING_8, 0))
        search_e.bind("<Return>", lambda e: do_search())

        log_card = Card(layout, padding=SPACING_16)
        log_card.grid(row=0, column=1, sticky="nsew", padx=(SPACING_8, 0))
        log_inner = log_card.content

        create_section_label(log_inner, "Today's Food Log", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_8))
        
        logged_scroll = ScrollableFrame(log_inner, background=CARD_COLOR, height=450)
        logged_scroll.pack(fill="both", expand=True)
        logged_wrap = logged_scroll.scrollable_frame

        def render_logged_foods():
            for w in logged_wrap.winfo_children():
                w.destroy()

            if self.demo_mode:
                foods = list(self.demo_food_logs)
            else:
                try:
                    foods = queries.get_food_logs(self.user_id, datetime.date.today())
                except Exception as e:
                    create_muted_label(logged_wrap, f"Log error: {e}", bg=CARD_COLOR).pack(pady=SPACING_16)
                    return

            if not foods:
                create_muted_label(logged_wrap, "No foods logged today yet.", bg=CARD_COLOR).pack(pady=SPACING_16)
                return

            for idx, item in enumerate(foods):
                row = tk.Frame(logged_wrap, bg=CARD_COLOR)
                row.pack(fill="x", pady=SPACING_4)

                name = item.get("name", "Unknown food")
                servings = item.get("servings", 1)
                if servings in (None, ""):
                    servings = 1

                info_txt = f"{name} ({servings}x)"
                tk.Label(
                    row, text=info_txt,
                    bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_BODY_BOLD,
                    anchor="w",
                ).pack(side="left", fill="x", expand=True)

                def _delete_item(item_data=item, index_val=idx):
                    try:
                        if self.demo_mode:
                            if index_val < len(self.demo_food_logs):
                                self.demo_food_logs.pop(index_val)
                        else:
                            queries.delete_food_log(item_data["food_log_id"], self.user_id)
                        refresh_food_view()
                    except Exception as e:
                        self.show_error("Delete Error", str(e))

                del_btn = tk.Button(
                    row, text="🗑", bg=CARD_COLOR, fg=ERROR_COLOR,
                    font=(FONT_FAMILY, 10), bd=0, cursor="hand2",
                    command=_delete_item,
                )
                del_btn.pack(side="right", padx=(SPACING_4, 0))

        def refresh_food_view():
            render_logged_foods()
            render_net_nutrients()

        refresh_food_view()
        do_search()

    def _food_row(self, parent, food, refresh_all=None):
        card = Card(parent, padding=SPACING_16)
        card.pack(fill="x", pady=(0, SPACING_8))
        inner = card.content

        top = tk.Frame(inner, bg=CARD_COLOR)
        top.pack(fill="x")

        tk.Label(
            top, text=food["name"],
            bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_BODY_BOLD,
        ).pack(side="left")

        tk.Label(
            top, text=f"  ({food.get('category', '')})",
            bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_SMALL,
        ).pack(side="left")

        serving = food.get("serving_size", "—")
        cal     = food.get("calories", 0)
        prot    = food.get("protein_g", 0)
        carbs   = food.get("carbohydrates_g", 0)
        fat     = food.get("fat_g", 0)
        fiber   = food.get("fiber_g", 0)

        info = f"Serving: {serving}   ·   {cal} kcal   ·   P {prot}g   ·   C {carbs}g   ·   F {fat}g   ·   Fb {fiber}g"
        tk.Label(
            inner, text=info,
            bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_SMALL,
            anchor="w",
        ).pack(fill="x", pady=(SPACING_4, SPACING_4))

        bottom_row = tk.Frame(inner, bg=CARD_COLOR)
        bottom_row.pack(fill="x", pady=(SPACING_4, 0))

        tk.Label(bottom_row, text="Servings:", bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_SMALL).pack(side="left")
        servings_e = create_spinbox(bottom_row, from_=0.5, to=10.0, increment=0.5, width=5)
        servings_e.delete(0, tk.END)
        servings_e.insert(0, "1.0")
        servings_e.pack(side="left", padx=(SPACING_4, SPACING_16))

        def do_log():
            try:
                try:
                    servings_val = max(0.1, float(servings_e.get() or 1.0))
                except ValueError:
                    servings_val = 1.0

                if self.demo_mode:
                    self.demo_food_logs.append({
                        "name": food["name"],
                        "servings": servings_val,
                        "calories": food.get("calories", 0),
                        "protein_g": food.get("protein_g", 0),
                        "carbohydrates_g": food.get("carbohydrates_g", 0),
                        "fat_g": food.get("fat_g", 0),
                        "fiber_g": food.get("fiber_g", 0),
                        "serving_size": food.get("serving_size", "1 serving"),
                        "category": food.get("category", "Other"),
                    })
                else:
                    queries.add_food_log(self.user_id, food["food_id"], servings=servings_val)
                self.show_info("Food Logged", f"{servings_val} serving(s) of {food['name']} added to today's log.")
                if refresh_all is not None:
                    refresh_all()
            except Exception as e:
                self.show_error("Food Log Error", str(e))

        VFButton(bottom_row, "➕ Log Food", command=do_log, style="accent").pack(side="right")

    # ─────────────────────────────────────────────────────
    # PROGRESS
    # ─────────────────────────────────────────────────────

    def show_progress(self):
        self.set_title("Progress")
        self.build_app_shell("Progress")

        scroll = ScrollableFrame(self.content_frame)
        scroll.pack(fill="both", expand=True)
        page = scroll.scrollable_frame

        hdr = tk.Frame(page, bg=BG_COLOR)
        hdr.pack(fill="x", padx=PAGE_PAD, pady=(SPACING_32, SPACING_8))
        heading = tk.Frame(hdr, bg=BG_COLOR)
        heading.pack(side="left", fill="x", expand=True)
        create_page_title(heading, "Progress").pack(anchor="w")
        create_muted_label(
            heading,
            f"Live data · Updated {datetime.datetime.now():%I:%M:%S %p}",
        ).pack(anchor="w", pady=(SPACING_4, 0))
        VFButton(
            hdr,
            "Refresh",
            command=self.show_progress,
            style="secondary",
        ).pack(side="right")

        if self.demo_mode:
            tracking = self._demo_tracking_history()
            workouts = self._demo_workout_history()
            progress_records = self._demo_goal_progress()
            progress_error = None
        else:
            try:
                tracking = queries.get_tracking_history(self.user_id, 30)
                workouts = queries.get_workout_history(self.user_id, 30)
            except Exception as e:
                create_muted_label(page, f"Error loading progress data: {e}").pack(padx=PAGE_PAD)
                return
            try:
                progress_records = queries.get_goal_progress(self.user_id, 30)
                progress_error = None
            except Exception as e:
                progress_records = []
                progress_error = e

        def chart_card(title):
            c = Card(page, padding=SPACING_24)
            c.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
            ci = c.content
            create_section_label(ci, title, bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_8))
            return ci

        # Workout chart
        wc = chart_card("Workout Completion")
        try:
            create_workout_completion_chart(wc, workouts)
        except Exception as e:
            create_muted_label(wc, f"Chart unavailable: {e}", bg=CARD_COLOR).pack()

        # Weight chart
        wgc = chart_card("Weight Tracking")
        try:
            create_weight_chart(wgc, tracking)
        except Exception as e:
            create_muted_label(wgc, f"Chart unavailable: {e}", bg=CARD_COLOR).pack()

        # Daily metrics chart
        mc = chart_card("Daily Activity")
        try:
            create_daily_metrics_chart(mc, tracking)
        except Exception as e:
            create_muted_label(mc, f"Chart unavailable: {e}", bg=CARD_COLOR).pack()

        # Goal breakdown donut pie chart
        pie_card = Card(page, padding=SPACING_24)
        pie_card.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
        pie_inner = pie_card.content

        create_section_label(pie_inner, "Goal Completion Overview", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_8))
        
        goal_name = self.profile.get("long_term_goal", "General fitness")
        
        try:
            if progress_error is not None:
                raise progress_error
            if self.demo_mode:
                cur_pct = getattr(
                    self,
                    "_custom_demo_goal_pct",
                    float(progress_records[-1]["progress_value"]) if progress_records else 0.0,
                )
            else:
                cur_pct = (
                    float(
                        progress_records[-1].get("progress_percentage")
                        if progress_records[-1].get("progress_percentage") is not None
                        else progress_records[-1].get("progress_value") or 0.0
                    )
                    if progress_records
                    else 0.0
                )

            create_goal_pie_chart(pie_inner, goal_name, cur_pct)
        except Exception as e:
            create_muted_label(pie_inner, f"Chart unavailable: {e}", bg=CARD_COLOR).pack()

        # Goal progress chart
        gpc = chart_card("Long-Term Goal Progress Trend")
        try:
            if progress_error is not None:
                raise progress_error
            create_goal_progress_chart(gpc, progress_records)
        except Exception as e:
            create_muted_label(gpc, f"Chart unavailable: {e}", bg=CARD_COLOR).pack()

        # Bottom padding
        tk.Frame(page, bg=BG_COLOR, height=SPACING_32).pack()

    # Demo data helpers
    def _demo_tracking_history(self):
        today = datetime.date.today()
        rows = []
        for i in range(7):
            day = today - datetime.timedelta(days=6 - i)
            key = str(day)
            if key in self.demo_tracking:
                data = self.demo_tracking[key].copy()
            else:
                data = {
                    "water_ml":    1600 + i * 120,
                    "steps":       4000 + i * 600,
                    "sleep_hours": 6.0  + i * 0.3,
                    "weight_kg":   self.profile.get("weight_kg"),
                }
            data["tracking_date"] = day
            rows.append(data)
        return rows

    def _demo_workout_history(self):
        today = datetime.date.today()
        return [
            {
                "assignment_date": today - datetime.timedelta(days=6 - i),
                "completed":       (i % 3 != 0),
                "workout_name":    "Demo Workout",
            }
            for i in range(7)
        ]

    def _demo_goal_progress(self):
        today = datetime.date.today()
        records = [
            {
                "progress_date":  today - datetime.timedelta(days=6 - i),
                "progress_value": 15 + i * 12,
            }
            for i in range(7)
        ]
        if hasattr(self, "_custom_demo_goal_pct"):
            records[-1]["progress_value"] = self._custom_demo_goal_pct
        return records

    # ─────────────────────────────────────────────────────
    # PROFILE
    # ─────────────────────────────────────────────────────

    def show_profile(self):
        self.set_title("Profile")
        self.build_app_shell("Profile")

        scroll = ScrollableFrame(self.content_frame)
        scroll.pack(fill="both", expand=True)
        page = scroll.scrollable_frame

        hdr = tk.Frame(page, bg=BG_COLOR)
        hdr.pack(fill="x", padx=PAGE_PAD, pady=(SPACING_32, SPACING_8))
        create_page_title(hdr, "Profile").pack(anchor="w")
        create_muted_label(hdr, "Your Vital Forge account and fitness information.").pack(anchor="w", pady=(SPACING_4, 0))

        # Account card
        ac = Card(page, padding=SPACING_24)
        ac.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
        ai = ac.content

        create_section_label(ai, "Account", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_16))
        self._profile_row(ai, "Name",  self.user.get("name", ""))
        self._profile_row(ai, "Email", self.user.get("email", ""))

        # Fitness profile card
        pc = Card(page, padding=SPACING_24)
        pc.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
        pi = pc.content

        create_section_label(pi, "Fitness Profile", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_16))

        fields = [
            ("Age",           self.profile.get("age")),
            ("Gender",        self.profile.get("gender")),
            ("Height",        f"{self.profile.get('height_cm')} cm"),
            ("Weight",        f"{self.profile.get('weight_kg')} kg"),
            ("Activity",      self.profile.get("activity_level")),
            ("Water Goal",    f"{self.profile.get('water_goal_ml')} ml / day"),
            ("Sleep Goal",    f"{self.profile.get('sleep_goal_hours')} hrs / night"),
            ("Steps Goal",    f"{self.profile.get('steps_goal'):,} steps / day"),
            ("Long-Term Goal",self.profile.get("long_term_goal")),
        ]

        for label, val in fields:
            self._profile_row(pi, label, str(val) if val is not None else "—")

        VFButton(
            pi, "Update Fitness Profile", command=self.show_survey, style="accent",
        ).pack(anchor="e", pady=(SPACING_16, 0))

        tk.Frame(page, bg=BG_COLOR, height=SPACING_32).pack()

    def _profile_row(self, parent, label, value):
        row = tk.Frame(parent, bg=CARD_COLOR)
        row.pack(fill="x", pady=SPACING_4)

        tk.Label(
            row, text=label,
            bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_BODY,
            width=18, anchor="w",
        ).pack(side="left")

        tk.Label(
            row, text=value,
            bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_BODY_BOLD,
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        create_separator(row).pack(side="bottom", fill="x")