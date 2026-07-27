#!/usr/bin/env python3
"""Build compact per-trace digests for failing traces + index-level aggregates.

Outputs (under OUT):
  digests/batch_NN.json   — list of ~10 trace digests each (for classifier agents)
  sample_discovery.json   — stratified sample of digests for taxonomy discovery
  aggregates.json         — index-level stats for the dashboard shell
"""
import json, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "rca_work")
BATCH = 10

os.makedirs(os.path.join(OUT, "digests"), exist_ok=True)

rows = [json.loads(l) for l in open(os.path.join(ROOT, "index.jsonl"))]


def clip(s, n):
    if s is None:
        return None
    s = str(s)
    return s if len(s) <= n else s[:n] + " …[truncated]"


def digest(row):
    t = json.load(open(os.path.join(ROOT, row["file"])))
    traj = t["trajectory"]
    tools = defaultdict(int)
    n_errors = 0
    final = None
    for e in traj:
        if e.get("type") == "tool_call":
            tools[e.get("tool", "?")] += 1
        if e.get("role") == "tool":
            c = str(e.get("content", ""))
            if "error" in c[:400].lower() or "traceback" in c[:400].lower():
                n_errors += 1
        if e.get("type") == "final_answer":
            final = e.get("content")
    if final is None:
        # qwen format: last substantive assistant message (skip trailing lead-ins
        # like "Let me provide the final answer:")
        for e in reversed(traj):
            if e.get("role") == "assistant" and e.get("content") and len(str(e["content"])) >= 300:
                final = e["content"]
                break
        if final is None:
            cands = [e.get("content") for e in traj
                     if e.get("role") == "assistant" and e.get("content")]
            if cands:
                final = max(cands, key=lambda c: len(str(c)))
    last_steps = []
    for e in traj[-6:]:
        last_steps.append({
            "role": e.get("role"), "type": e.get("type"), "tool": e.get("tool"),
            "content": clip(e.get("content") or json.dumps(e.get("arguments", ""))[:300], 300),
        })
    failed = [
        {"idx": i, "criterion": c["criterion"], "rationale": clip(c.get("rationale"), 500)}
        for i, c in enumerate(t["grades"]["criteria"]) if c["verdict"] == "fail"
    ]
    passed = [c["criterion"] for c in t["grades"]["criteria"] if c["verdict"] == "pass"]
    return {
        "task_id": row["task_id"], "task_name": row["task_name"], "domain": row["domain"],
        "model": row["model"], "file": row["file"], "score": row["score"],
        "prompt": clip(t["task"]["prompt"], 2000),
        "gold_response_excerpt": clip(t["task"].get("gold_response"), 1500),
        "failed_criteria": failed,
        "passed_criteria": [clip(c, 150) for c in passed[:10]],
        "final_answer": clip(final, 3500) if final else None,
        "trajectory_stats": {
            "n_steps": len(traj), "tool_calls": dict(tools),
            "n_tool_errors": n_errors, "has_final_answer": final is not None,
        },
        "last_steps": last_steps,
    }


failing = [r for r in rows if r["n_failed"] > 0]
digests = []
for i, r in enumerate(failing):
    try:
        digests.append(digest(r))
    except Exception as ex:
        digests.append({"task_id": r["task_id"], "model": r["model"], "file": r["file"],
                        "domain": r["domain"], "digest_error": str(ex),
                        "failed_criteria": [{"idx": None, "criterion": "?", "rationale": None}]})
    if (i + 1) % 100 == 0:
        print(f"  {i+1}/{len(failing)}")

for b in range(0, len(digests), BATCH):
    with open(os.path.join(OUT, "digests", f"batch_{b//BATCH:02d}.json"), "w") as f:
        json.dump(digests[b:b+BATCH], f, indent=1)

# Stratified discovery sample: spread over domain x model, mix partial & total failures
bykey = defaultdict(list)
for d in digests:
    bykey[(d["domain"], d["model"])].append(d)
sample = []
for key, ds in sorted(bykey.items()):
    ds = sorted(ds, key=lambda d: d.get("score", 0))
    picks = [ds[0], ds[len(ds)//2], ds[-1], ds[len(ds)//4]][:4]
    seen = set()
    for p in picks:
        if id(p) not in seen:
            sample.append(p); seen.add(id(p))
sample = sample[:40]
json.dump(sample, open(os.path.join(OUT, "sample_discovery.json"), "w"), indent=1)

# Aggregates from index
models = sorted({r["model"] for r in rows})
domains = sorted({r["domain"] for r in rows})
agg = {
    "models": models, "domains": domains,
    "mean_score": {m: round(sum(r["score"] for r in rows if r["model"] == m) /
                            sum(1 for r in rows if r["model"] == m), 4) for m in models},
    "crit_pass_rate": {}, "cell": {}, "tasks": {},
}
for m in models:
    sub = [r for r in rows if r["model"] == m]
    tot = sum(r["n_criteria"] for r in sub)
    agg["crit_pass_rate"][m] = round(1 - sum(r["n_failed"] for r in sub) / tot, 4)
for m in models:
    for dm in domains:
        sub = [r for r in rows if r["model"] == m and r["domain"] == dm]
        tot = sum(r["n_criteria"] for r in sub)
        agg["cell"][f"{dm}|{m}"] = {
            "mean_score": round(sum(r["score"] for r in sub) / len(sub), 4),
            "crit_pass_rate": round(1 - sum(r["n_failed"] for r in sub) / tot, 4),
            "n_tasks": len(sub), "n_failed": sum(r["n_failed"] for r in sub), "n_criteria": tot,
        }
per_task = defaultdict(dict)
meta = {}
for r in rows:
    per_task[r["task_id"]][r["model"]] = r["score"]
    meta[r["task_id"]] = {"task_name": r["task_name"], "domain": r["domain"],
                          "n_criteria": r["n_criteria"], "file8": r["file"].split("__")[0].split("/")[-1]}
for tid, sc in per_task.items():
    vals = [sc[m] for m in models]
    agg["tasks"][tid] = {**meta[tid], "scores": sc,
                         "spread": round(max(vals) - min(vals), 4),
                         "all_pass": all(v == 1 for v in vals), "all_fail": all(v == 0 for v in vals)}
json.dump(agg, open(os.path.join(OUT, "aggregates.json"), "w"), indent=1)

sizes = [os.path.getsize(os.path.join(OUT, "digests", f)) for f in os.listdir(os.path.join(OUT, "digests"))]
print(f"digests: {len(digests)} traces, {len(sizes)} batches, "
      f"batch sizes {min(sizes)//1024}-{max(sizes)//1024}KB")
print(f"failed criteria in digests: {sum(len(d['failed_criteria']) for d in digests)}")
print(f"all-pass tasks: {sum(1 for t in agg['tasks'].values() if t['all_pass'])}, "
      f"all-fail: {sum(1 for t in agg['tasks'].values() if t['all_fail'])}")
