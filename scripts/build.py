#!/usr/bin/env python3
"""Rebuild analysis.html from the template and the results data.

Usage: python3 scripts/build.py  (from the repository root)

Criterion pass rates and confidence-interval counts are recomputed from
data/index.jsonl. The step counts in the "Does working longer help?" chart
were measured on the full run transcripts, which are not included in this
repository; those numbers are kept as stored in scripts/data.json.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

data = json.loads((ROOT / "scripts" / "data.json").read_text())
runs = [json.loads(line) for line in (ROOT / "data" / "index.jsonl").read_text().splitlines()]

# Per model and field: criterion pass rate from the results table.
groups = {}
for r in runs:
    g = groups.setdefault(f"{r['model']}|{r['domain']}", {"nc": 0, "nf": 0, "n_runs": 0})
    g["nc"] += r["n_criteria"]
    g["nf"] += r["n_failed"]
    g["n_runs"] += 1

for key, g in groups.items():
    s = data["steps"].setdefault(key, {})
    s["passrate"] = round((g["nc"] - g["nf"]) / g["nc"], 4)
    s["n_runs"] = g["n_runs"]
    s["n_crit"] = g["nc"]
    # s["med_steps"] stays as measured from the run transcripts.

# Per-model graded-criteria counts, for the confidence intervals on the tiles.
data["n_crit"] = {}
for r in runs:
    data["n_crit"][r["model"]] = data["n_crit"].get(r["model"], 0) + r["n_criteria"]

(ROOT / "scripts" / "data.json").write_text(json.dumps(data, separators=(",", ":")))

template = (ROOT / "scripts" / "dashboard_template.html").read_text()
html = template.replace("/*__DATA__*/", json.dumps(data, separators=(",", ":")))
(ROOT / "analysis.html").write_text(html)
print(f"built analysis.html ({len(html):,} bytes)")
