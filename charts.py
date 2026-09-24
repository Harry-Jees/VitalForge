# charts.py
# Vital Forge — Matplotlib Charts

import tkinter as tk
from datetime import date, timedelta

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import (
    CARD_COLOR, BG_COLOR,
    TEXT_COLOR, MUTED_TEXT,
    GREEN, DARK_GREEN, LIGHT_GREEN,
    BROWN, DARK_BROWN,
    BORDER_COLOR,
)

# ── Chart colour palette (earthy, matched to app design) ──────────────────────
_C_GREEN  = "#4A7C59"
_C_BROWN  = "#7D5A3C"
_C_SAGE   = "#8BAF8B"
_C_TAN    = "#B8956A"
_C_MUTED  = "#A89080"
_GRID_A   = 0.12


def _apply_chart_style(figure, axis):
    """Apply consistent earthy appearance to any chart."""
    figure.patch.set_facecolor(CARD_COLOR)
    axis.set_facecolor(CARD_COLOR)

    # Remove top/right spines for a cleaner look
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(BORDER_COLOR)
    axis.spines["bottom"].set_color(BORDER_COLOR)

    axis.tick_params(colors=MUTED_TEXT, labelsize=8, length=3)
    axis.xaxis.label.set_color(TEXT_COLOR)
    axis.yaxis.label.set_color(TEXT_COLOR)


def _embed(figure, parent):
    """Embed the figure in a Tkinter widget and return the canvas."""
    canvas = FigureCanvasTkAgg(figure, master=parent)
    widget = canvas.get_tk_widget()
    widget.pack(fill="x", pady=(0, 0))
    canvas.draw()
    return canvas


def _empty_message(axis, message):
    """Show a centered empty-state message on the axis."""
    axis.text(
        0.5, 0.5, message,
        transform=axis.transAxes,
        ha="center", va="center",
        color=MUTED_TEXT, fontsize=10,
    )
    axis.set_xticks([])
    axis.set_yticks([])


# =========================================================
# WORKOUT COMPLETION CHART
# =========================================================

def create_workout_completion_chart(parent, records):
    """
    Bar chart: completed (1) or not (0) for each day in the last 7 days.

    records: list of dicts with keys:  assignment_date, completed
    """
    figure = Figure(figsize=(6.5, 2.8), dpi=100)
    axis   = figure.add_subplot(111)
    _apply_chart_style(figure, axis)

    today = date.today()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]

    lookup = {}
    for r in records:
        d = r.get("assignment_date")
        if hasattr(d, "date"):
            d = d.date()
        if d is not None:
            lookup[d] = bool(r.get("completed", False))

    values = [1 if lookup.get(d, False) else 0 for d in dates]
    labels = [d.strftime("%a") for d in dates]
    colours = [_C_GREEN if v else _C_MUTED for v in values]

    axis.bar(labels, values, color=colours, width=0.5, zorder=2)
    axis.set_ylim(0, 1.4)
    axis.set_yticks([0, 1])
    axis.set_yticklabels(["—", "Done"])
    axis.grid(axis="y", alpha=_GRID_A, zorder=1)

    figure.tight_layout(pad=1.0)
    return _embed(figure, parent)


# =========================================================
# WEIGHT CHART
# =========================================================

def create_weight_chart(parent, records):
    """
    Line chart: weight_kg over time.

    records: list of dicts with keys:  tracking_date, weight_kg
    """
    figure = Figure(figsize=(6.5, 2.8), dpi=100)
    axis   = figure.add_subplot(111)
    _apply_chart_style(figure, axis)

    valid = []
    for r in records:
        w = r.get("weight_kg")
        d = r.get("tracking_date")
        if w is None or d is None:
            continue
        if hasattr(d, "date"):
            d = d.date()
        try:
            valid.append((d, float(w)))
        except (ValueError, TypeError):
            continue

    valid.sort(key=lambda x: x[0])

    if valid:
        labels  = [item[0].strftime("%d %b") for item in valid]
        weights = [item[1] for item in valid]

        axis.plot(labels, weights, marker="o", linewidth=2,
                  color=_C_BROWN, markerfacecolor=_C_TAN, markersize=5, zorder=3)
        axis.fill_between(
            range(len(labels)), weights,
            alpha=0.08, color=_C_BROWN,
        )
        axis.set_ylabel("Weight (kg)", labelpad=8)
        axis.grid(axis="y", alpha=_GRID_A, zorder=1)

        # Rotate labels if many points
        if len(labels) > 7:
            axis.set_xticklabels(labels, rotation=30, ha="right")
    else:
        _empty_message(axis, "No weight data recorded yet.")

    figure.tight_layout(pad=1.0)
    return _embed(figure, parent)


# =========================================================
# DAILY METRICS CHART
# =========================================================

def create_daily_metrics_chart(parent, records):
    """
    Multi-line chart: water, steps, sleep for last 7 days.

    records: list of dicts with keys:  tracking_date, water_ml, steps, sleep_hours
    """
    figure = Figure(figsize=(6.5, 2.8), dpi=100)
    axis   = figure.add_subplot(111)
    _apply_chart_style(figure, axis)

    recent = records[-7:] if records else []

    if not recent:
        _empty_message(axis, "No daily tracking data yet.")
    else:
        labels = []
        water  = []
        steps  = []
        sleep  = []

        for r in recent:
            d = r.get("tracking_date")
            if hasattr(d, "date"):
                d = d.date()
            labels.append(d.strftime("%a") if d else "—")
            water.append(float(r.get("water_ml",    0) or 0))
            steps.append(float(r.get("steps",        0) or 0))
            sleep.append(float(r.get("sleep_hours",  0) or 0))

        x = range(len(labels))

        ax2 = axis.twinx()
        ax2.set_facecolor(CARD_COLOR)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_color(BORDER_COLOR)
        ax2.tick_params(colors=MUTED_TEXT, labelsize=8)

        axis.plot(x, water, marker="o", linewidth=2,
                  color=_C_GREEN,  label="Water (ml)", markersize=4, zorder=3)
        axis.plot(x, sleep, marker="s", linewidth=2,
                  color=_C_BROWN,  label="Sleep (hrs)", markersize=4, zorder=3)
        ax2.plot(x, steps, marker="^", linewidth=2, linestyle="--",
                 color=_C_SAGE,   label="Steps", markersize=4, zorder=3)

        axis.set_xticks(list(x))
        axis.set_xticklabels(labels)
        axis.set_ylabel("Water / Sleep", labelpad=8)
        ax2.set_ylabel("Steps", labelpad=8)
        axis.grid(axis="y", alpha=_GRID_A, zorder=1)

        # Combine legends
        lines1, labels1 = axis.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        axis.legend(
            lines1 + lines2, labels1 + labels2,
            fontsize=7, frameon=False, loc="upper left",
        )

    figure.tight_layout(pad=1.0)
    return _embed(figure, parent)


# =========================================================
# GOAL PROGRESS CHART
# =========================================================

def create_goal_progress_chart(parent, progress_records):
    """
    Line chart: goal progress % over time.

    progress_records: list of dicts with keys:
        progress_date   (or progress_percentage key used as value)
        progress_value  OR  progress_percentage
    """
    figure = Figure(figsize=(6.5, 2.8), dpi=100)
    axis   = figure.add_subplot(111)
    _apply_chart_style(figure, axis)

    valid = []
    for r in progress_records:
        d = r.get("progress_date")
        # Support both key names
        v = r.get("progress_percentage") or r.get("progress_value")
        if d is None or v is None:
            continue
        if hasattr(d, "date"):
            d = d.date()
        try:
            valid.append((d, float(v)))
        except (ValueError, TypeError):
            continue

    valid.sort(key=lambda x: x[0])

    if valid:
        labels = [item[0].strftime("%d %b") for item in valid]
        values = [item[1] for item in valid]

        axis.plot(labels, values, marker="o", linewidth=2,
                  color=_C_GREEN, markerfacecolor=_C_SAGE, markersize=5, zorder=3)
        axis.fill_between(range(len(labels)), values, alpha=0.08, color=_C_GREEN)
        axis.set_ylim(0, 105)
        axis.set_ylabel("Progress (%)", labelpad=8)
        axis.grid(axis="y", alpha=_GRID_A, zorder=1)
    else:
        _empty_message(axis, "No goal progress recorded yet.")

    figure.tight_layout(pad=1.0)
    return _embed(figure, parent)


# =========================================================
# GOAL PIE CHART
# =========================================================

def create_goal_pie_chart(parent, goal_name="Long-Term Goal", progress_percentage=0.0):
    """
    Donut / Pie chart visualizing percentage progress toward a long-term fitness goal.
    """
    figure = Figure(figsize=(3.6, 2.6), dpi=100)
    figure.patch.set_facecolor(CARD_COLOR)
    axis = figure.add_subplot(111)
    axis.set_facecolor(CARD_COLOR)

    try:
        pct = max(0.0, min(100.0, float(progress_percentage or 0)))
    except (ValueError, TypeError):
        pct = 0.0

    rem = max(0.0, 100.0 - pct)

    if pct == 0 and rem == 0:
        rem = 100.0

    sizes = [pct, rem]
    colors = [_C_GREEN, "#E5DFD5"]

    wedges, _ = axis.pie(
        sizes,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.35, edgecolor=CARD_COLOR, linewidth=2),
    )

    axis.text(
        0, 0, f"{pct:.0f}%\nCompleted",
        ha="center", va="center",
        color=DARK_GREEN, fontsize=11, fontweight="bold",
    )

    title_txt = (goal_name[:22] + "…") if len(goal_name) > 22 else goal_name
    axis.set_title(title_txt, color=TEXT_COLOR, fontsize=10, fontweight="bold", pad=4)

    axis.axis("equal")
    figure.tight_layout(pad=0.5)
    return _embed(figure, parent)


# =========================================================
# UTILITY
# =========================================================

def destroy_chart(canvas):
    """Safely remove a Matplotlib canvas."""
    if canvas is None:
        return
    try:
        canvas.get_tk_widget().destroy()
    except Exception:
        pass