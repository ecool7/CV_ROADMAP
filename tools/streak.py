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
README_PATH = ROOT / "README.md"

MARKER_START = "<!-- STREAK:START -->"
MARKER_END = "<!-- STREAK:END -->"

# GitHub-like greens (readable on GitHub light README)
LEVEL_FILL = ["#ebedf0", "#9be9a9", "#40c463", "#30a14e", "#216e39"]
CELL = 11
GAP = 3
LEFT = 28
TOP = 18

SATURDAY = 5  # datetime.weekday(): Mon=0 ... Sat=5 Sun=6


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


def is_scheduled(d: date) -> bool:
    """Mon–Fri + Sunday. Saturday is planned rest and does not break a streak."""
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
    scheduled = scheduled_days_between(start, now)
    total = sum(1 for d in scheduled if d in logged)

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

    # Grace: today not logged yet does not kill the streak until the day ends.
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
    return current, longest, total


def build_svg(data: dict, now: date) -> str:
    start = parse_iso(data["start"])
    grid_start = monday_on_or_before(start)
    n_weeks = 53
    days_map = data.get("days", {})

    width = LEFT + n_weeks * (CELL + GAP) + 4
    height = TOP + 7 * (CELL + GAP) + 8

    rects = []
    month_labels: list[tuple[int, str]] = []
    last_month = None
    month_names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

    for w in range(n_weeks):
        for dow in range(7):  # 0 = Monday
            d = grid_start + timedelta(weeks=w, days=dow)
            x = LEFT + w * (CELL + GAP)
            y = TOP + dow * (CELL + GAP)
            rec = days_map.get(d.isoformat(), {})
            hours = float(rec.get("hours", 0) or 0)
            level = hours_to_level(hours)
            fill = LEVEL_FILL[level]
            note = rec.get("note", "")
            title = d.isoformat()
            if hours:
                title += f" · {hours:g}h"
            if note:
                title += f" · {note}"
            if not is_scheduled(d) and hours <= 0:
                fill = "#f6f8fa"
            rects.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{fill}"><title>{title}</title></rect>'
            )
        first = grid_start + timedelta(weeks=w)
        if w == 0 or (first.month != last_month and first.day <= 7):
            month_labels.append((LEFT + w * (CELL + GAP), month_names[first.month - 1]))
            last_month = first.month

    labels_month = "\n".join(
        f'<text x="{x}" y="12" fill="#57606a" font-size="10" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{name}</text>'
        for x, name in month_labels
    )
    day_names = {0: "Mon", 2: "Wed", 4: "Fri"}
    labels_day = "\n".join(
        f'<text x="0" y="{TOP + dow * (CELL + GAP) + 9}" fill="#57606a" font-size="9" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{name}</text>'
        for dow, name in day_names.items()
    )
    body = "\n".join(rects)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Activity heatmap">\n'
        f"{labels_month}\n{labels_day}\n{body}\n</svg>\n"
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
            'Log a day: `python tools/streak.py log --hours 1.5 --note "what I did"`',
            MARKER_END,
            "",
        ]
    )


def patch_readme(block: str) -> None:
    text = README_PATH.read_text(encoding="utf-8")
    if MARKER_START in text and MARKER_END in text:
        before = text.split(MARKER_START, 1)[0]
        after = text.split(MARKER_END, 1)[1]
        README_PATH.write_text(
            before.rstrip("\n") + "\n\n" + block.strip() + "\n\n" + after.lstrip("\n"),
            encoding="utf-8",
        )
        return
    raise SystemExit("README.md is missing STREAK markers")


def cmd_render(data: dict, now: date) -> None:
    SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(build_svg(data, now), encoding="utf-8")
    patch_readme(readme_block(data, now))
    current, longest, total = streak_stats(data.get("days", {}), parse_iso(data["start"]), now)
    print(f"wrote {SVG_PATH.relative_to(ROOT)}")
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
