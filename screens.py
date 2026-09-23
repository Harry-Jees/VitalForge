# screens.py
# Vital Forge — Application screens and navigation.

import datetime
import random
import tkinter as tk
from tkinter import messagebox, ttk

from config import (
    APP_NAME,
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
    DEMO_EMAIL, DEMO_PASSWORD,
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

        # App mark
        tk.Label(
            inner, text="🌿", bg=CARD_COLOR, fg=GREEN,
            font=("Segoe UI", 28),
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
                    "Cannot connect to MySQL.\n\nPlease ensure MySQL is running "
                    "and the database is set up (see guides/BUILD.md)."
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
                self.show_error("Registration", "Password must be at least 6 characters.")
                return
            if email == DEMO_EMAIL:
                self.show_error("Registration", "That email is reserved for the demo account.")
                return
            if not test_connection():
                self.show_error("Database", "MySQL could not be reached. Real accounts require MySQL.")
                return
            try:
                if queries.get_user_by_email(email):
                    self.show_error("Registration", "An account with that email already exists.")
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

        # Logo
        tk.Label(
            topbar, text="🌿  Vital Forge",
            font=FONT_SECTION, bg=CARD_COLOR, fg=DARK_GREEN,
        ).pack(side="left", padx=SPACING_24)

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

        wg = self.profile["water_goal_ml"]
        sg = self.profile["steps_goal"]
        lg = self.profile["sleep_goal_hours"]

        stat_row = tk.Frame(page, bg=BG_COLOR)
        stat_row.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
        stat_row.columnconfigure(0, weight=1)
        stat_row.columnconfigure(1, weight=1)
        stat_row.columnconfigure(2, weight=1)

        StatCard(
            stat_row, "Water",
            f"{water:,.0f} ml",
            f"Goal: {wg:,} ml",
            progress=water / wg if wg else 0,
            accent=GREEN,
        ).grid(row=0, column=0, sticky="nsew", padx=(0, SPACING_8))

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
        ).grid(row=0, column=2, sticky="nsew", padx=(SPACING_8, 0))

        # ── Daily tracking form ───────────────────────────────
        tc = Card(page, padding=SPACING_24)
        tc.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_16))
        ti = tc.content

        create_section_label(ti, "Daily Tracking", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_16))

        water_var = tk.StringVar(value=str(int(water)))
        steps_var = tk.StringVar(value=str(int(steps)))
        sleep_var = tk.StringVar(value=str(sleep))

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

        def do_save_tracking():
            try:
                new_water = max(0, float(water_var.get() or 0))
                new_steps = max(0, int(float(steps_var.get() or 0)))
                new_sleep = max(0, float(sleep_var.get() or 0))
            except ValueError:
                self.show_error("Tracking", "Please enter valid numbers.")
                return

            data = {
                "water_ml":    new_water,
                "steps":       new_steps,
                "sleep_hours": new_sleep,
                "weight_kg":   today_data.get("weight_kg"),
                "notes":       today_data.get("notes", ""),
            }

            try:
                if self.demo_mode:
                    self.demo_tracking[str(datetime.date.today())] = data
                else:
                    queries.save_daily_tracking(self.user_id, data)
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

        # ── Long-term goal ────────────────────────────────────
        gc = Card(page, padding=SPACING_24)
        gc.pack(fill="x", padx=PAGE_PAD, pady=(0, SPACING_32))
        gi = gc.content

        goal = self.profile.get("long_term_goal", "")
        create_section_label(gi, "Long-Term Goal", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_8))
        tk.Label(gi, text=goal, bg=CARD_COLOR, fg=DARK_GREEN, font=FONT_BODY_BOLD).pack(anchor="w")
        tk.Label(
            gi, text=get_goal_description(goal),
            bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_BODY,
            wraplength=800, justify="left",
        ).pack(anchor="w", pady=(SPACING_4, 0))

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

    def _get_or_assign_workout(self):
        today = datetime.date.today()
        scheduled = WEEKLY_WORKOUT_SCHEDULE[today.weekday()]

        if not scheduled["exercises"]:
            return {
                "name": scheduled["focus"],
                "description": "Take today as a recovery day. Light walking and mobility are optional.",
                "difficulty": "Recovery",
                "completed": True,
                "day": scheduled["day"],
                "focus": scheduled["focus"],
                "exercises": [],
            }

        if self.demo_mode:
            key = str(today)
            if key in self.demo_workout_history:
                return self.demo_workout_history[key]
            workout = {
                "name": scheduled["focus"],
                "description": f"{scheduled['day']}: complete all three exercises below.",
                "difficulty": "Scheduled",
                "completed": False,
                "day": scheduled["day"],
                "focus": scheduled["focus"],
                "exercises": list(scheduled["exercises"]),
            }
            self.demo_workout_history[key] = workout
            return workout

        existing = queries.get_today_workout(self.user_id)
        if not existing:
            suitable = queries.get_all_workouts()
            if not suitable:
                return None
            queries.assign_workout(self.user_id, suitable[0]["workout_id"], today)
            existing = queries.get_today_workout(self.user_id, today)

        workout = dict(existing)
        workout.update({
            "name": scheduled["focus"],
            "description": f"{scheduled['day']}: complete all three exercises below.",
            "difficulty": "Scheduled",
            "day": scheduled["day"],
            "focus": scheduled["focus"],
            "exercises": list(scheduled["exercises"]),
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
        today = datetime.date.today()
        schedule = WEEKLY_WORKOUT_SCHEDULE[today.weekday()]
        create_page_title(hdr, f"{schedule['day']} Workout").pack(anchor="w")
        create_muted_label(
            hdr, today.strftime("%B %d, %Y") + " | Weekly schedule",
        ).pack(anchor="w", pady=(SPACING_4, 0))

        workout = self._get_or_assign_workout()

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
                checked = self.demo_exercise_logs.get(str(today), {})
            else:
                checked = {
                    row["exercise_index"]: bool(row["completed"])
                    for row in queries.get_exercise_logs(self.user_id, today)
                }
        except Exception as e:
            self.show_error("Workout Error", f"Could not load exercise checklist: {e}")
            return

        exercise_vars = []

        def save_exercise(index, exercise_name, variable):
            try:
                if self.demo_mode:
                    key = str(today)
                    self.demo_exercise_logs.setdefault(key, {})[index] = variable.get()
                else:
                    queries.save_exercise_log(
                        self.user_id, today, index, exercise_name, variable.get(),
                    )

                done = all(var.get() for var in exercise_vars)
                if self.demo_mode:
                    self.demo_workout_history[str(today)]["completed"] = done
                else:
                    queries.complete_workout(self.user_id, today, completed=done)
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

        hdr = tk.Frame(page, bg=BG_COLOR)
        hdr.pack(fill="x", padx=PAGE_PAD, pady=(SPACING_32, SPACING_8))
        create_page_title(hdr, "Food Database").pack(anchor="w")
        create_muted_label(hdr, "Search and log foods to track your nutrition.").pack(anchor="w", pady=(SPACING_4, 0))

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

        def do_search():
            for w in results_wrap.winfo_children():
                w.destroy()

            term = search_e.get().strip()

            if self.demo_mode:
                foods = [f for f in FOODS if (not term or term.lower() in f["name"].lower())][:30]
            else:
                try:
                    foods = queries.search_foods(term, 30)
                except Exception as e:
                    create_muted_label(results_wrap, f"Search error: {e}").pack(pady=SPACING_16)
                    return

            if not foods:
                create_muted_label(results_wrap, "No foods found.").pack(pady=SPACING_32)
                return

            for food in foods:
                self._food_row(results_wrap, food, refresh_logged=render_logged_foods)

        VFButton(search_row, "Search", command=do_search, style="primary").pack(side="right", padx=(SPACING_8, 0))
        search_e.bind("<Return>", lambda e: do_search())

        results_wrap = tk.Frame(search_inner, bg=CARD_COLOR)
        results_wrap.pack(fill="both", expand=True, pady=(SPACING_8, 0))

        log_card = Card(layout, padding=SPACING_16)
        log_card.grid(row=0, column=1, sticky="nsew", padx=(SPACING_8, 0))
        log_inner = log_card.content

        create_section_label(log_inner, "Today's Food Log", bg=CARD_COLOR).pack(anchor="w", pady=(0, SPACING_8))
        logged_wrap = tk.Frame(log_inner, bg=CARD_COLOR)
        logged_wrap.pack(fill="both", expand=True)

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

            for item in foods:
                row = tk.Frame(logged_wrap, bg=CARD_COLOR)
                row.pack(fill="x", pady=SPACING_4)

                name = item.get("name", "Unknown food")
                servings = item.get("servings", 1)
                if servings in (None, ""):
                    servings = 1

                tk.Label(
                    row, text=name,
                    bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_BODY,
                    anchor="w",
                ).pack(side="left", fill="x", expand=True)

                tk.Label(
                    row, text=f"{servings} serving(s)",
                    bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_SMALL,
                    anchor="e",
                ).pack(side="right")

        render_logged_foods()
        do_search()

    def _food_row(self, parent, food, refresh_logged=None):
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
            top, text=f"  {food.get('category', '')}",
            bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_SMALL,
        ).pack(side="left")

        serving = food.get("serving_size", "—")
        cal     = food.get("calories", 0)
        prot    = food.get("protein_g", 0)
        carbs   = food.get("carbohydrates_g", 0)
        fat     = food.get("fat_g", 0)

        info = f"Serving: {serving}   ·   {cal} kcal   ·   P {prot}g   ·   C {carbs}g   ·   F {fat}g"
        tk.Label(
            inner, text=info,
            bg=CARD_COLOR, fg=MUTED_TEXT, font=FONT_SMALL,
            anchor="w",
        ).pack(fill="x", pady=(SPACING_4, SPACING_8))

        def do_log():
            try:
                if self.demo_mode:
                    self.demo_food_logs.append({"name": food["name"], "servings": 1})
                else:
                    queries.add_food_log(self.user_id, food["food_id"], servings=1)
                self.show_info("Food Logged", f"{food['name']} added to today's log.")
                if refresh_logged is not None:
                    refresh_logged()
            except Exception as e:
                self.show_error("Food Log Error", str(e))

        VFButton(inner, "Log Food", command=do_log, style="accent").pack(anchor="e")

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
        create_page_title(hdr, "Progress").pack(anchor="w")
        create_muted_label(hdr, "See how your habits are developing over time.").pack(anchor="w", pady=(SPACING_4, 0))

        if self.demo_mode:
            tracking = self._demo_tracking_history()
            workouts = self._demo_workout_history()
        else:
            try:
                tracking = queries.get_tracking_history(self.user_id, 30)
                workouts = queries.get_workout_history(self.user_id, 30)
            except Exception as e:
                create_muted_label(page, f"Error loading progress data: {e}").pack(padx=PAGE_PAD)
                return

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

        # Goal progress chart
        gpc = chart_card("Long-Term Goal Progress")
        try:
            prog_data = (
                self._demo_goal_progress()
                if self.demo_mode
                else queries.get_goal_progress(self.user_id, 30)
            )
            create_goal_progress_chart(gpc, prog_data)
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
        return [
            {
                "progress_date":  today - datetime.timedelta(days=6 - i),
                "progress_value": 15 + i * 12,
            }
            for i in range(7)
        ]

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