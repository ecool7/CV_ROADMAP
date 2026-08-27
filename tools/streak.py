"""LeetCode-style activity heatmap + streak.

Log a day:
    python tools/streak.py log --hours 1.5 --note "01_arrays passed"

Redraw README + docs/streak.svg:
    python tools/streak.py render
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACTIVITY_PATH = ROOT / "activity.json"
SVG_PATH = ROOT / "docs" / "streak.svg"
WEEK_SVG_PATH = ROOT / "docs" / "streak-week.svg"
README_PATH = ROOT / "README.md"

MARKER_START = "<!-- STREAK:START -->"
MARKER_END = "<!-- STREAK:END -->"
WEEK_START = "<!-- WEEK:START -->"
WEEK_END = "<!-- WEEK:END -->"

LEVEL_FILL = ["#ebedf0", "#9be9a9", "#40c463", "#30a14e", "#216e39"]
CELL = 11
GAP = 3
LEFT = 28
TOP = 18
SATURDAY = 5


def today() -> date:
    return date.today()


def load_activity() -> dict:
    return json.loads(ACTIVITY_PATH.read_text(encoding="utf-8"))


def save_activity(data: dict) -> None:
    ACTIVITY_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def parse_iso(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def monday_on_or_before(d: date) -> date:
    return d - timedelta(days=d.weekday())


def sunday_on_or_before(d: date) -> date:
    # GitHub weeks start on Sunday. datetime.weekday(): Mon=0 … Sun=6
    return d - timedelta(days=(d.weekday() + 1) % 7)


def is_scheduled(d: date) -> bool:
    return d.weekday() != SATURDAY


def hours_to_level(hours: float) -> int:
    if hours <= 0:
        return 0
    if hours < 1.0:
        return 1
    if hours < 1.5:
        return 2
    if hours < 2.0:
        return 3
    return 4


def scheduled_days_between(start: date, end: date) -> list[date]:
    days = []
    d = start
    while d <= end:
        if is_scheduled(d):
            days.append(d)
        d += timedelta(days=1)
    return days


def streak_stats(days: dict, start: date, now: date) -> tuple[int, int, int]:
    logged = {parse_iso(k) for k, v in days.items() if v.get("hours", 0) > 0}

    def streak_ending_at(end: date) -> int:
        n = 0
        d = end
        while d >= start:
            if not is_scheduled(d):
                d -= timedelta(days=1)
                continue
            if d not in logged:
                break
            n += 1
            d -= timedelta(days=1)
        return n

    end = now if now in logged or not is_scheduled(now) else now - timedelta(days=1)
    current = streak_ending_at(end)

    longest = 0
    run = 0
    d = start
    while d <= now:
        if is_scheduled(d):
            if d in logged:
                run += 1
                longest = max(longest, run)
            else:
                run = 0
        d += timedelta(days=1)
    total = sum(1 for d in scheduled_days_between(start, now) if d in logged)
    return current, longest, total


def build_svg(data: dict, now: date) -> str:
    """Past 53 weeks, newest column on the right — same layout as GitHub."""
    n_weeks = 53
    days_map = data.get("days", {})
    grid_start = sunday_on_or_before(now) - timedelta(weeks=n_weeks - 1)

    width = LEFT + n_weeks * (CELL + GAP) + 4
    height = TOP + 7 * (CELL + GAP) + 22

    rects = []
    month_labels: list[tuple[int, str]] = []
    last_month = None
    month_names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

    for w in range(n_weeks):
        week_has_day = False
        for dow in range(7):  # 0 = Sunday
            d = grid_start + timedelta(weeks=w, days=dow)
            if d > now:
                continue
            week_has_day = True
            x = LEFT + w * (CELL + GAP)
            y = TOP + dow * (CELL + GAP)
            rec = days_map.get(d.isoformat(), {})
            hours = float(rec.get("hours", 0) or 0)
            fill = LEVEL_FILL[hours_to_level(hours)]
            note = rec.get("note", "")
            title = d.isoformat()
            if hours:
                title += f" · {hours:g}h"
            if note:
                title += f" · {note}"
            rects.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{fill}"><title>{title}</title></rect>'
            )
        first = grid_start + timedelta(weeks=w)
        if week_has_day and first.month != last_month and first.day <= 13:
            month_labels.append((LEFT + w * (CELL + GAP), month_names[first.month - 1]))
            last_month = first.month

    labels_month = "\n".join(
        f'<text x="{x}" y="12" fill="#57606a" font-size="10" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{name}</text>'
        for x, name in month_labels
    )
    day_names = {1: "Mon", 3: "Wed", 5: "Fri"}
    labels_day = "\n".join(
        f'<text x="0" y="{TOP + dow * (CELL + GAP) + 9}" fill="#57606a" font-size="9" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{name}</text>'
        for dow, name in day_names.items()
    )
    legend_y = TOP + 7 * (CELL + GAP) + 14
    legend_x = width - 5 * (CELL + GAP) - 48
    legend_bits = [
        f'<text x="{legend_x - 28}" y="{legend_y + 9}" fill="#57606a" font-size="9" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">Less</text>'
    ]
    for i, fill in enumerate(LEVEL_FILL):
        lx = legend_x + i * (CELL + GAP)
        legend_bits.append(
            f'<rect x="{lx}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2" fill="{fill}"/>'
        )
    legend_bits.append(
        f'<text x="{legend_x + 5 * (CELL + GAP) + 4}" y="{legend_y + 9}" fill="#57606a" font-size="9" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">More</text>'
    )
    body = "\n".join(rects)
    legend = "\n".join(legend_bits)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Activity heatmap">\n'
        f"{labels_month}\n{labels_day}\n{body}\n{legend}\n</svg>\n"
    )


def build_week_svg(data: dict, now: date) -> str:
    days_map = data.get("days", {})
    monday = monday_on_or_before(now)
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    size = 28
    gap = 10
    top = 22
    width = 8 + 7 * (size + gap)
    height = top + size + 22
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="This week">'
    ]
    for i, name in enumerate(names):
        d = monday + timedelta(days=i)
        rec = days_map.get(d.isoformat(), {})
        hours = float(rec.get("hours", 0) or 0)
        fill = LEVEL_FILL[hours_to_level(hours)]
        if not is_scheduled(d) and hours <= 0:
            fill = "#f6f8fa"
        x = 8 + i * (size + gap)
        stroke = "#0969da" if d == now else "#d0d7de"
        sw = 2 if d == now else 1
        parts.append(
            f'<text x="{x + size / 2}" y="14" text-anchor="middle" fill="#57606a" '
            f'font-size="11" font-family="Segoe UI, Helvetica, Arial, sans-serif">{name}</text>'
        )
        parts.append(
            f'<rect x="{x}" y="{top}" width="{size}" height="{size}" rx="4" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}">'
            f"<title>{d.isoformat()} · {hours:g}h</title></rect>"
        )
        label = f"{hours:g}h" if hours else ("rest" if not is_scheduled(d) else "")
        if label:
            parts.append(
                f'<text x="{x + size / 2}" y="{top + size + 16}" text-anchor="middle" '
                f'fill="#1f2328" font-size="10" '
                f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{label}</text>'
            )
    parts.append("</svg>\n")
    return "\n".join(parts)


def week_markdown_row(data: dict, now: date) -> str:
    days_map = data.get("days", {})
    monday = monday_on_or_before(now)
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    marks = []
    notes = []
    for i in range(7):
        d = monday + timedelta(days=i)
        rec = days_map.get(d.isoformat(), {})
        hours = float(rec.get("hours", 0) or 0)
        if hours > 0:
            marks.append("🟩")
            notes.append(f"{hours:g}h")
        elif not is_scheduled(d):
            marks.append("·")
            notes.append("rest")
        else:
            marks.append("⬜")
            notes.append(" ")
    header = "| " + " | ".join(names) + " |"
    sep = "| " + " | ".join([":---:"] * 7) + " |"
    row = "| " + " | ".join(marks) + " |"
    sub = "| " + " | ".join(notes) + " |"
    return "\n".join([header, sep, row, sub])


def week_block(data: dict, now: date) -> str:
    return "\n".join(
        [
            WEEK_START,
            "### This week",
            "",
            "![This week](docs/streak-week.svg)",
            "",
            week_markdown_row(data, now),
            WEEK_END,
        ]
    )


def readme_block(data: dict, now: date) -> str:
    start = parse_iso(data["start"])
    current, longest, total = streak_stats(data.get("days", {}), start, now)
    return "\n".join(
        [
            MARKER_START,
            "![Activity](docs/streak.svg)",
            "",
            f"**Streak {current}** · longest {longest} · active days **{total}**"
            " · Saturday rest does not break the streak",
            "",
            week_block(data, now),
            "",
            'Log a day: `python tools/streak.py log --hours 1.5 --note "what I did"`',
            MARKER_END,
        ]
    )


def _replace_marked(text: str, start: str, end: str, block: str) -> str:
    if start not in text or end not in text:
        raise SystemExit(f"README.md is missing {start}")
    before = text.split(start, 1)[0]
    after = text.split(end, 1)[1]
    return before.rstrip("\n") + "\n\n" + block.strip() + "\n\n" + after.lstrip("\n")


def patch_readme(data: dict, now: date) -> None:
    text = README_PATH.read_text(encoding="utf-8")
    text = _replace_marked(text, MARKER_START, MARKER_END, readme_block(data, now))
    head, sep, tail = text.partition(MARKER_END)
    if WEEK_START in tail:
        tail = _replace_marked(tail, WEEK_START, WEEK_END, week_block(data, now))
        text = head + sep + tail
    README_PATH.write_text(text, encoding="utf-8")


def cmd_render(data: dict, now: date) -> None:
    SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(build_svg(data, now), encoding="utf-8")
    WEEK_SVG_PATH.write_text(build_week_svg(data, now), encoding="utf-8")
    patch_readme(data, now)
    current, longest, total = streak_stats(data.get("days", {}), parse_iso(data["start"]), now)
    print(f"wrote {SVG_PATH.relative_to(ROOT)} and {WEEK_SVG_PATH.relative_to(ROOT)}")
    print(f"streak={current} longest={longest} active={total}")


def cmd_log(hours: float, note: str, day: date) -> None:
    data = load_activity()
    days = data.setdefault("days", {})
    prev = days.get(day.isoformat(), {})
    days[day.isoformat()] = {
        "hours": hours,
        "note": note or prev.get("note", ""),
    }
    save_activity(data)
    cmd_render(data, today())
    print(f"logged {day.isoformat()} hours={hours:g}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Activity streak heatmap")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_log = sub.add_parser("log", help="record a study day and redraw")
    p_log.add_argument("--hours", type=float, default=1.0)
    p_log.add_argument("--note", default="")
    p_log.add_argument("--date", default="", help="YYYY-MM-DD (default: today)")

    sub.add_parser("render", help="redraw svg + README")

    args = parser.parse_args()
    if args.cmd == "log":
        day = parse_iso(args.date) if args.date else today()
        cmd_log(args.hours, args.note, day)
    else:
        cmd_render(load_activity(), today())


if __name__ == "__main__":
    main()
