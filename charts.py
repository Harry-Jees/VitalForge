# charts.py
# Vital Forge — Matplotlib Charts

import math
from datetime import date, timedelta

import matplotlib.dates as mdates
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


def _as_date(value):
    if hasattr(value, "date"):
        return value.date()
    return value


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
        d = _as_date(r.get("assignment_date"))
        if d in dates:
            lookup[d] = bool(r.get("completed", False))

    labels = [d.strftime("%a") for d in dates]
    assigned_positions = [i for i, day in enumerate(dates) if day in lookup]
    values = [1 if lookup[dates[i]] else 0.35 for i in assigned_positions]
    colours = [_C_GREEN if lookup[dates[i]] else _C_MUTED for i in assigned_positions]

    bars = axis.bar(
        [labels[i] for i in assigned_positions],
        values,
        color=colours,
        width=0.5,
        zorder=2,
    )
    for bar, position in zip(bars, assigned_positions):
        status = "Done" if lookup[dates[position]] else "Not done"
        axis.annotate(
            status,
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=7,
            color=MUTED_TEXT,
        )
    axis.set_ylim(0, 1.4)
    axis.set_yticks([0.35, 1])
    axis.set_yticklabels(["Not done", "Done"])
    axis.set_ylabel("Assigned workout")
    axis.grid(axis="y", alpha=_GRID_A, zorder=1)
    axis.text(
        0.5, -0.2, "No bar means no workout was assigned.",
        transform=axis.transAxes, ha="center", va="top",
        color=MUTED_TEXT, fontsize=8,
    )

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
        try:
            weight = float(w)
            if math.isfinite(weight) and weight > 0:
                valid.append((_as_date(d), weight))
        except (ValueError, TypeError):
            continue

    valid.sort(key=lambda x: x[0])

    if valid:
        dates = [item[0] for item in valid]
        weights = [item[1] for item in valid]

        axis.plot(dates, weights, marker="o", linewidth=2,
                  color=_C_BROWN, markerfacecolor=_C_TAN, markersize=5, zorder=3)
        axis.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        axis.set_ylabel("Weight (kg)", labelpad=8)
        axis.grid(axis="y", alpha=_GRID_A, zorder=1)
        axis.annotate(
            f"{weights[-1]:.1f} kg",
            (dates[-1], weights[-1]),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=8,
            color=_C_BROWN,
        )
        figure.autofmt_xdate(rotation=30, ha="right")
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
    figure = Figure(figsize=(6.5, 4.5), dpi=100)
    axes = figure.subplots(3, 1, sharex=True)
    for axis in axes:
        _apply_chart_style(figure, axis)

    today = date.today()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    day_lookup = {}
    for record in records:
        record_date = _as_date(record.get("tracking_date"))
        if record_date in dates:
            day_lookup[record_date] = record

    if not day_lookup:
        _empty_message(axes[1], "No daily tracking data yet.")
    else:
        series = (
            ("water_ml", "Water (ml)", _C_GREEN, "o"),
            ("steps", "Steps", _C_SAGE, "^"),
            ("sleep_hours", "Sleep (hours)", _C_BROWN, "s"),
        )
        labels = [day.strftime("%a %d") for day in dates]
        x_values = list(range(len(dates)))
        for axis, (key, label, color, marker) in zip(axes, series):
            values = []
            for day in dates:
                record = day_lookup.get(day)
                value = record.get(key) if record else None
                try:
                    number = float(value) if value is not None else math.nan
                except (ValueError, TypeError):
                    number = math.nan
                values.append(number if math.isfinite(number) and number >= 0 else math.nan)

            axis.plot(
                x_values, values, marker=marker, linewidth=2,
                color=color, markersize=4, zorder=3,
            )
            for x_value, value in zip(x_values, values):
                if math.isfinite(value):
                    axis.annotate(
                        f"{value:,.0f}" if key != "sleep_hours" else f"{value:.1f}",
                        (x_value, value),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha="center",
                        fontsize=7,
                        color=color,
                    )
            axis.set_ylabel(label, labelpad=8)
            axis.grid(axis="y", alpha=_GRID_A, zorder=1)
            axis.set_xticks(x_values)

        axes[-1].set_xticklabels(labels)

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
        v = r.get("progress_percentage")
        if v is None:
            v = r.get("progress_value")
        if d is None or v is None:
            continue
        try:
            value = float(v)
            if math.isfinite(value):
                valid.append((_as_date(d), max(0.0, min(100.0, value))))
        except (ValueError, TypeError):
            continue

    valid.sort(key=lambda x: x[0])

    if valid:
        dates = [item[0] for item in valid]
        values = [item[1] for item in valid]

        axis.plot(dates, values, marker="o", linewidth=2,
                  color=_C_GREEN, markerfacecolor=_C_SAGE, markersize=5, zorder=3)
        axis.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        axis.set_ylim(0, 100)
        axis.set_ylabel("Progress (%)", labelpad=8)
        axis.grid(axis="y", alpha=_GRID_A, zorder=1)
        axis.annotate(
            f"{values[-1]:.0f}%",
            (dates[-1], values[-1]),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=8,
            color=_C_GREEN,
        )
        figure.autofmt_xdate(rotation=30, ha="right")
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
        pct = float(progress_percentage or 0)
    except (ValueError, TypeError):
        pct = 0.0
    if not math.isfinite(pct):
        pct = 0.0
    else:
        pct = max(0.0, min(100.0, pct))

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