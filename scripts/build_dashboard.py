#!/usr/bin/env python3
"""Merge aggregates + taxonomy + classifications + findings into the final dashboard.

Validates that every failed criterion from the digests appears exactly once;
anything missing or malformed becomes category "unclassified" (never dropped).
"""
import json, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, "rca_work")

agg = json.load(open(os.path.join(W, "aggregates.json")))
tax = json.load(open(os.path.join(W, "taxonomy.json")))["categories"]
findings = []
fp = os.path.join(W, "findings.json")
if os.path.exists(fp):
    findings = json.load(open(fp))

# ground truth: every failed criterion, keyed (task_id, model, idx)
truth = {}
prompts = {}
for f in sorted(glob.glob(os.path.join(W, "digests", "batch_*.json"))):
    for d in json.load(open(f)):
        prompts[d["task_id"]] = (d.get("prompt") or "")[:600]
        for fc in d.get("failed_criteria", []):
            truth[(d["task_id"], d["model"], fc["idx"])] = {
                "tid": d["task_id"], "task_name": d.get("task_name", "?"),
                "domain": d.get("domain", "?"), "model": d["model"],
                "criterion": fc.get("criterion", "?"), "rationale": fc.get("rationale"),
                "file": d.get("file", ""), "score": d.get("score", 0), "idx": fc["idx"],
            }

raw = json.load(open(os.path.join(W, "classifications.json")))
valid_cats = {c["short_name"] for c in tax}
merged, dupes, unknown = {}, 0, 0
for c in raw:
    key = (c.get("task_id"), c.get("model"), c.get("idx"))
    if key not in truth:
        unknown += 1
        continue
    if key in merged:
        dupes += 1
        continue
    cat = c.get("category") if c.get("category") in valid_cats else "other"
    merged[key] = {**truth[key], "category": cat,
                   "evidence": (c.get("evidence") or "")[:300],
                   "explanation": (c.get("explanation") or "")[:250],
                   "confidence": c.get("confidence") or "medium"}

missing = [k for k in truth if k not in merged]
for k in missing:
    merged[k] = {**truth[k], "category": "unclassified", "evidence": "",
                 "explanation": "Classifier did not return a result for this criterion.",
                 "confidence": "low"}

cls = sorted(merged.values(), key=lambda r: (r["domain"], r["task_name"], r["model"], r["idx"]))
n_unc = sum(1 for r in cls if r["category"] == "unclassified")
if n_unc:
    tax = tax + [{"short_name": "unclassified", "label": "Unclassified",
                  "definition": "No classifier result; shown for completeness."}]

# ---- validation ----
assert len(cls) == len(truth) == 1311, f"coverage mismatch: {len(cls)} vs {len(truth)} vs 1311"
index_failed = sum(json.loads(l)["n_failed"] for l in open(os.path.join(ROOT, "index.jsonl")))
assert index_failed == len(truth), f"index says {index_failed} failed, digests have {len(truth)}"
print(f"validation OK: {len(cls)} classified rows == {index_failed} failed criteria in index")
print(f"  duplicates ignored: {dupes} · unknown keys ignored: {unknown} · unclassified: {n_unc}")
from collections import Counter
print("  category counts:", dict(Counter(r['category'] for r in cls).most_common()))

data = {
    "agg": agg,
    "taxonomy": [{"short_name": t["short_name"], "label": t["label"], "definition": t["definition"]} for t in tax],
    "cls": cls,
    "prompts": prompts,
    "findings": findings,
    "n_unclassified": n_unc,
    "meta": "Generated 2026-07-25.",
}
tpl = open(os.path.join(ROOT, "scripts", "dashboard_template.html")).read()
out = tpl.replace("__DATA_JSON__", json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
dst = os.path.join(ROOT, "apex-rca-dashboard.html")
open(dst, "w").write(out)
print(f"wrote {dst} ({os.path.getsize(dst)//1024} KB)")
