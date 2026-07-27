#!/usr/bin/env python3
"""Augment data.json with trajectory-derived stats, then inline it into the template.

Usage: python3 dashboard/build.py  (from the repo root)
"""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASH = ROOT / "dashboard"

data = json.loads((DASH / "data.json").read_text())

# Per model|domain: criterion pass rate from the index, median steps from the traces.
runs = [json.loads(line) for line in (ROOT / "index.jsonl").read_text().splitlines()]
groups = {}
for r in runs:
    g = groups.setdefault(f"{r['model']}|{r['domain']}", {"nc": 0, "nf": 0, "steps": []})
    g["nc"] += r["n_criteria"]
    g["nf"] += r["n_failed"]
    trace = json.loads((ROOT / r["file"]).read_text())
    g["steps"].append(len(trace["trajectory"]))

data["steps"] = {
    key: {
        "med_steps": round(statistics.median(g["steps"]), 1),
        "passrate": round((g["nc"] - g["nf"]) / g["nc"], 4),
        "n_runs": len(g["steps"]),
        "n_crit": g["nc"],
    }
    for key, g in groups.items()
}

# Per-model graded-criteria counts, for confidence intervals on the KPI tiles.
data["n_crit"] = {}
for r in runs:
    data["n_crit"][r["model"]] = data["n_crit"].get(r["model"], 0) + r["n_criteria"]

(DASH / "data.json").write_text(json.dumps(data, separators=(",", ":")))

template = (DASH / "dashboard_template.html").read_text()
html = template.replace("/*__DATA__*/", json.dumps(data, separators=(",", ":")))
(DASH / "dashboard.html").write_text(html)
print(f"built dashboard.html ({len(html):,} bytes), steps groups: {len(data['steps'])}")
