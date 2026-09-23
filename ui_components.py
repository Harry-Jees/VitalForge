# ui_components.py
# Vital Forge — Reusable Tkinter UI Components

import tkinter as tk
from tkinter import ttk

from config import (
    BG_COLOR, CARD_COLOR, INPUT_COLOR,
    GREEN, DARK_GREEN, LIGHT_GREEN,
    BROWN, DARK_BROWN, LIGHT_BROWN,
    TEXT_COLOR, MUTED_TEXT, BORDER_COLOR,
    SUCCESS_COLOR, ERROR_COLOR, WARNING_COLOR,
    FONT_SMALL, FONT_BODY, FONT_BODY_BOLD,
    FONT_BUTTON, FONT_SECTION, FONT_HEADING,
    FONT_PAGE_TITLE, FONT_TITLE,
    SPACING_4, SPACING_8, SPACING_16, SPACING_24, SPACING_32,
    CARD_PAD, LABEL_GAP, FIELD_GAP,
)


# =========================================================
# STYLES
# =========================================================

def configure_styles():
    """Configure global ttk widget styles."""

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Combobox
    style.configure(
        "VF.TCombobox",
        fieldbackground=INPUT_COLOR,
        background=INPUT_COLOR,
        foreground=TEXT_COLOR,
        bordercolor=BORDER_COLOR,
        arrowcolor=MUTED_TEXT,
        padding=(SPACING_8, SPACING_8),
        font=FONT_BODY,
        selectbackground=LIGHT_GREEN,
        selectforeground=TEXT_COLOR,
    )
    style.map(
        "VF.TCombobox",
        fieldbackground=[("readonly", INPUT_COLOR)],
        bordercolor=[("focus", GREEN)],
    )

    # Progress bar
    style.configure(
        "VF.Horizontal.TProgressbar",
        troughcolor=LIGHT_GREEN,
        background=GREEN,
        bordercolor=LIGHT_GREEN,
        lightcolor=GREEN,
        darkcolor=GREEN,
        thickness=8,
    )

    # Scrollbar — subtle
    style.configure(
        "Vertical.TScrollbar",
        background=BORDER_COLOR,
        troughcolor=BG_COLOR,
        bordercolor=BG_COLOR,
        arrowcolor=MUTED_TEXT,
        width=10,
    )


# =========================================================
# HELPERS
# =========================================================

def clear_frame(frame):
    """Destroy all children of a frame."""
    for widget in frame.winfo_children():
        widget.destroy()


def get_bg(widget):
    """Safely retrieve the background color of a widget."""
    try:
        return widget.cget("bg")
    except Exception:
        return CARD_COLOR


# =========================================================
# CARD
# =========================================================

class Card(tk.Frame):
    """
    White surface card on an earthy background.
    No visible border — separation comes from color contrast.
    Internal padding follows the 8-point system.
    """

    def __init__(self, parent, title=None, background=CARD_COLOR, **kwargs):
        padding = kwargs.pop("padding", CARD_PAD)

        super().__init__(
            parent,
            bg=background,
            highlightthickness=0,
            bd=0,
            **kwargs,
        )

        self.background = background

        self.content = tk.Frame(self, bg=background)
        self.content.pack(fill="both", expand=True, padx=padding, pady=padding)

        if title:
            tk.Label(
                self.content,
                text=title,
                bg=background,
                fg=TEXT_COLOR,
                font=FONT_SECTION,
                anchor="w",
            ).pack(fill="x", pady=(0, SPACING_16))

    def __getattr__(self, name):
        # Delegate geometry and widget calls to the outer frame itself,
        # but pack/grid/place calls that the caller intends on the Card
        # wrapper will work naturally since Card IS a tk.Frame.
        raise AttributeError(name)


# =========================================================
# BUTTONS
# =========================================================

class VFButton(tk.Button):
    """
    Flat Vital Forge button.
    style: 'primary' | 'secondary' | 'ghost' | 'danger'
    """

    _STYLES = {
        "primary":   (GREEN,        "#FFFFFF",  DARK_GREEN),
        "secondary": (LIGHT_BROWN,  DARK_BROWN, BROWN),
        "ghost":     (BG_COLOR,     TEXT_COLOR, LIGHT_GREEN),
        "danger":    (ERROR_COLOR,  "#FFFFFF",  DARK_BROWN),
        "success":   (SUCCESS_COLOR,"#FFFFFF",  DARK_GREEN),
        "accent":    (LIGHT_GREEN,  DARK_GREEN, GREEN),
    }

    def __init__(self, parent, text, command=None, width=None, style="primary", **kwargs):
        bg_def, fg_def, abg_def = self._STYLES.get(style, self._STYLES["primary"])

        bg  = kwargs.pop("bg", bg_def)
        fg  = kwargs.pop("fg", fg_def)
        abg = kwargs.pop("activebackground", abg_def)

        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=abg,
            activeforeground=fg,
            font=FONT_BUTTON,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=SPACING_16,
            pady=SPACING_8,
            highlightthickness=0,
            **kwargs,
        )

        if width:
            self.config(width=width)


# =========================================================
# LABELS
# =========================================================

def create_title(parent, text, bg=None):
    """Large screen title."""
    return tk.Label(
        parent,
        text=text,
        bg=bg or get_bg(parent),
        fg=TEXT_COLOR,
        font=FONT_TITLE,
        anchor="w",
    )


def create_page_title(parent, text, bg=None):
    """Page-level heading (20pt)."""
    return tk.Label(
        parent,
        text=text,
        bg=bg or get_bg(parent),
        fg=TEXT_COLOR,
        font=FONT_PAGE_TITLE,
        anchor="w",
    )


def create_heading(parent, text, bg=None):
    """Section heading (16pt bold)."""
    return tk.Label(
        parent,
        text=text,
        bg=bg or get_bg(parent),
        fg=TEXT_COLOR,
        font=FONT_HEADING,
        anchor="w",
    )


def create_section_label(parent, text, bg=None):
    """Smaller section label (13pt bold)."""
    return tk.Label(
        parent,
        text=text,
        bg=bg or get_bg(parent),
        fg=TEXT_COLOR,
        font=FONT_SECTION,
        anchor="w",
    )


def create_label(parent, text, bg=None):
    """Standard form label."""
    return tk.Label(
        parent,
        text=text,
        bg=bg or get_bg(parent),
        fg=TEXT_COLOR,
        font=FONT_BODY,
        anchor="w",
    )


def create_muted_label(parent, text, bg=None):
    """Secondary / helper text."""
    return tk.Label(
        parent,
        text=text,
        bg=bg or get_bg(parent),
        fg=MUTED_TEXT,
        font=FONT_SMALL,
        anchor="w",
        wraplength=700,
        justify="left",
    )


def create_message_label(parent, text="", message_type="normal"):
    """Status/feedback label."""
    color_map = {
        "success": SUCCESS_COLOR,
        "error":   ERROR_COLOR,
        "warning": WARNING_COLOR,
    }
    return tk.Label(
        parent,
        text=text,
        bg=get_bg(parent),
        fg=color_map.get(message_type, MUTED_TEXT),
        font=FONT_SMALL,
        anchor="w",
        justify="left",
    )


# =========================================================
# INPUTS
# =========================================================

def create_entry(parent, show=None, bg=None):
    """Single-line text entry with subtle border on focus."""
    entry = tk.Entry(
        parent,
        bg=bg or INPUT_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR,
        font=FONT_BODY,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER_COLOR,
        highlightcolor=GREEN,
    )
    if show:
        entry.config(show=show)
    return entry


def create_combobox(parent, values):
    """Read-only dropdown."""
    combo = ttk.Combobox(
        parent,
        values=values,
        state="readonly",
        style="VF.TCombobox",
        font=FONT_BODY,
    )
    if values:
        combo.current(0)
    return combo


def create_spinbox(parent, from_=0, to=1000, increment=1):
    """Numeric spinbox."""
    return tk.Spinbox(
        parent,
        from_=from_,
        to=to,
        increment=increment,
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        font=FONT_BODY,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER_COLOR,
        highlightcolor=GREEN,
        buttonbackground=LIGHT_BROWN,
    )


# =========================================================
# PROGRESS BAR
# =========================================================

def create_progress_bar(parent, value=0, maximum=100):
    """Horizontal progress bar (0–maximum)."""
    bar = ttk.Progressbar(
        parent,
        orient="horizontal",
        mode="determinate",
        maximum=maximum,
        value=value,
        style="VF.Horizontal.TProgressbar",
    )
    return bar


# =========================================================
# STAT CARD
# =========================================================

class StatCard(tk.Frame):
    """
    Compact metric card for the dashboard.
    Displays: title, big value, optional subtitle, optional progress bar.
    Has a 4 px colored accent stripe at the top.
    """

    def __init__(
        self, parent,
        title, value,
        subtitle="",
        progress=None,   # float 0.0–1.0 or None
        accent=GREEN,
        **kwargs,
    ):
        super().__init__(
            parent,
            bg=CARD_COLOR,
            highlightthickness=0,
            bd=0,
            **kwargs,
        )

        # Accent stripe
        tk.Frame(self, bg=accent, height=4).pack(fill="x", side="top")

        content = tk.Frame(self, bg=CARD_COLOR)
        content.pack(fill="both", expand=True, padx=SPACING_16, pady=SPACING_16)

        # Title
        tk.Label(
            content, text=title.upper(),
            bg=CARD_COLOR, fg=MUTED_TEXT,
            font=("Segoe UI", 8, "bold"), anchor="w",
        ).pack(fill="x")

        # Value
        tk.Label(
            content, text=value,
            bg=CARD_COLOR, fg=TEXT_COLOR,
            font=("Segoe UI", 18, "bold"), anchor="w",
        ).pack(fill="x", pady=(SPACING_4, 0))

        # Subtitle
        if subtitle:
            tk.Label(
                content, text=subtitle,
                bg=CARD_COLOR, fg=MUTED_TEXT,
                font=FONT_SMALL, anchor="w",
            ).pack(fill="x", pady=(SPACING_4, 0))

        # Optional progress bar
        if progress is not None:
            pct = max(0.0, min(1.0, float(progress))) * 100
            bar = create_progress_bar(content, value=pct)
            bar.pack(fill="x", pady=(SPACING_8, 0))


# =========================================================
# SCROLLABLE FRAME
# =========================================================

class ScrollableFrame(tk.Frame):
    """
    Vertically scrollable container.
    Use .scrollable_frame as the parent for content widgets.
    Scroll only fires when the pointer is over this frame (no global conflict).
    """

    def __init__(self, parent, background=BG_COLOR, **kwargs):
        super().__init__(parent, bg=background, **kwargs)

        self.background = background

        self.canvas = tk.Canvas(
            self, bg=background, highlightthickness=0, bd=0
        )

        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview,
            style="Vertical.TScrollbar",
        )

        self.scrollable_frame = tk.Frame(self.canvas, bg=background)

        self.window_id = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_inner_frame)

        # Bind scroll only when pointer is over the canvas
        self.canvas.bind("<Enter>", self._bind_scroll)
        self.canvas.bind("<Leave>", self._unbind_scroll)

    def _update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_inner_frame(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _bind_scroll(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self._mousewheel)
        self.canvas.bind_all("<Button-4>",   self._mousewheel)
        self.canvas.bind_all("<Button-5>",   self._mousewheel)

    def _unbind_scroll(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _mousewheel(self, event):
        try:
            if getattr(event, "num", 0) == 4:
                self.canvas.yview_scroll(-1, "units")
            elif getattr(event, "num", 0) == 5:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass


# =========================================================
# CHECKBOX
# =========================================================

def create_checkbox(parent, text, variable, command=None):
    """Styled checkbox."""
    return tk.Checkbutton(
        parent,
        text=text,
        variable=variable,
        command=command,
        bg=get_bg(parent),
        fg=TEXT_COLOR,
        activebackground=get_bg(parent),
        activeforeground=TEXT_COLOR,
        selectcolor=LIGHT_GREEN,
        font=FONT_BODY,
        anchor="w",
    )


# =========================================================
# SEPARATOR
# =========================================================

def create_separator(parent):
    """1 px horizontal rule."""
    return tk.Frame(parent, bg=BORDER_COLOR, height=1)


# =========================================================
# FORM FIELD BUILDER
# =========================================================

def build_field(parent, label_text, widget_factory, gap=FIELD_GAP):
    """
    Create a stacked label + input pair and return the input widget.
    widget_factory is a callable(parent) -> widget.
    """
    create_label(parent, label_text).pack(anchor="w")
    widget = widget_factory(parent)
    widget.pack(fill="x", pady=(LABEL_GAP, gap))
    return widget