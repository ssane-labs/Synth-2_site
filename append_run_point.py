#!/usr/bin/env python3
"""Дописать одну точку в run-log.json — лог обучения, который читает лендинг.

Запускать после сессии, когда известны шаг и отложенный лосс:

    python append_run_point.py --step 86000 --loss 2.0290 \
        --note "первая сессия после починки router_bias"

Необязательные поля:
    --date 2026-09-12      дата сессии (по умолчанию сегодня)
    --trend 0.0018         наклон на 1000 шагов, если он померен
    --trend-note "МНК по 17 замерам"
    --lr-event "LR / 3"    подпись вертикальной метки на графике
    --log path/to/run-log.json

Точка с тем же шагом перезаписывается, а не дублируется.
"""

import argparse
import datetime as dt
import json
import pathlib
import sys

DEFAULT_LOG = pathlib.Path(__file__).with_name("run-log.json")


def main() -> int:
    # консоль Windows по умолчанию в cp1252 и на кириллице падает
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    p = argparse.ArgumentParser(description="Дописать точку в run-log.json")
    p.add_argument("--step", type=int, required=True, help="номер шага")
    p.add_argument("--loss", type=float, required=True, help="отложенный лосс")
    p.add_argument("--date", default=dt.date.today().isoformat(), help="дата сессии, YYYY-MM-DD")
    p.add_argument("--note", default=None, help="что произошло за сессию")
    p.add_argument("--trend", type=float, default=None, help="наклон на 1000 шагов")
    p.add_argument("--trend-note", default=None, help="как наклон померен")
    p.add_argument("--lr-event", default=None, help="метка события на графике")
    p.add_argument("--log", type=pathlib.Path, default=DEFAULT_LOG)
    a = p.parse_args()

    if not a.log.exists():
        print(f"не нашёл {a.log}", file=sys.stderr)
        return 1

    data = json.loads(a.log.read_text(encoding="utf-8"))
    points = data.setdefault("points", [])

    point = {"step": a.step, "loss": a.loss, "recordedOn": a.date}
    if a.note:
        point["note"] = a.note
    if a.trend is not None:
        point["trendPer1k"] = a.trend
    if a.trend_note:
        point["trendNote"] = a.trend_note
    if a.lr_event:
        point["lrEvent"] = a.lr_event

    # тот же шаг — это уточнение прежнего замера, а не вторая точка
    replaced = False
    for i, existing in enumerate(points):
        if int(existing.get("step", -1)) == a.step:
            points[i] = point
            replaced = True
            break
    if not replaced:
        points.append(point)

    points.sort(key=lambda q: q["step"])
    a.log.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    verb = "заменил" if replaced else "добавил"
    print(f"{verb} точку: шаг {a.step:,}, лосс {a.loss:.4f} — всего {len(points)} точек")
    print("осталось: git add run-log.json && git commit && git push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
