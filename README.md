# Apex benchmark analysis

How well three AI models (GPT-5.5, Claude Opus 4.7, and Qwen 3.6) do white-collar work across 300 real tasks in Law, Investment Banking, and Management Consulting.

**[View the live report](https://meghnanatraj.github.io/apex-benchmark-analysis/)**

### [The analysis](https://meghnanatraj.github.io/apex-benchmark-analysis/analysis.html)

Which model does the job, what you can trust it with, and why the models fail.

[![The analysis](docs/assets/analysis.png)](https://meghnanatraj.github.io/apex-benchmark-analysis/analysis.html)

### [The dataset, explained](https://meghnanatraj.github.io/apex-benchmark-analysis/explainer.html)

What the 300 tasks look like and how the 900 runs were graded, criterion by criterion.

[![The dataset, explained](docs/assets/explainer.png)](https://meghnanatraj.github.io/apex-benchmark-analysis/explainer.html)

## Key findings

- GPT-5.5 leads in every field. It met 64.9% of grading criteria overall, against 57.6% for Opus 4.7 and 43.2% for Qwen 3.6.
- Counting only tasks passed cleanly (no failed criteria, no partial credit), GPT-5.5 passed 57% of Investment Banking tasks, 57% of Consulting tasks, and 38% of Law tasks.
- Law is the hardest field for every model. All three fell to about a third of law tasks passed (GPT-5.5 38%, Qwen 34%, Opus 32%).
- Qwen 3.6 passed at most 1 in 5 tasks outside Law (20% in Investment Banking, 17% in Consulting).
- Outside Law, which model you pick matters more than which kind of work you give it.

Every task has a gold (correct) answer and 1 to 10 pass/fail grading criteria, 2,920 criteria verdicts in total. A task counts as passed only if it was graded and none of its criteria failed.

**Read with care:** these 300 tasks are a hand-picked slice of the Apex benchmark, deliberately weighted toward tasks where the three models disagree, so the gaps between models are wider here than they would be on a random draw. The numbers compare the three models to each other; they are not official benchmark scores.

## Case study: one model passed, two failed

On 28 tasks, one model got everything right while the other two got everything wrong (GPT-5.5 on 17 of them, Qwen 6, Opus 5). The clearest case is a consulting task with 10 criteria where GPT-5.5 scored 10/10 and both others scored 0/10. The client folder held three sibling spreadsheets, two stale and one current. Opus and Qwen merged all three and got every number wrong despite correct math. GPT-5.5 treated picking the right file as part of the problem: it compared the candidates, noticed only the current file carried the client's own margin tabs, and answered from that file alone, matching the correct answer. The lesson: when two models fail the same task, the cause is usually a shared wrong judgment call made early, not weak math.

## How this was made

The 900 run transcripts were indexed into a results table, and the failures were studied rather than guessed at: a close read of a sample of failing runs produced a list of 11 failure types, then every one of the 1,311 failed criteria was sorted into a type with a quoted piece of evidence from its transcript. Those results became the analysis page, the explainer page was built to walk a newcomer through the dataset in under a minute, and every number on both pages was checked against the data before publishing.

## What's in this repository

| Path | What it is |
|---|---|
| `index.html` | Landing page linking to the two pages above |
| `explainer.html` | The dataset, explained |
| `analysis.html` | The analysis of the results |
| `docs/assets/` | The screenshots used in this README |
| `data/index.jsonl` | The results table, one row per model run with its scores |
| `scripts/data.json` | Every number, task prompt, and criterion verdict the pages display |
| `scripts/dashboard_template.html` | The page shell that `data.json` is injected into |
| `scripts/build.py` | Rebuilds `analysis.html`. Run `python3 scripts/build.py` from the repository root |
| `scripts/preprocess.py`, `scripts/build_dashboard.py` | The earlier failure-analysis pipeline, kept as a record of method. These read the full transcripts and the intermediate files they produced, neither of which is in this repository, so they will not run here |

The full run transcripts are not included in this repository, only the results computed from them. `analysis.html` is fully reproducible from what is here: `python3 scripts/build.py` regenerates it byte-for-byte from `scripts/data.json` and `data/index.jsonl`. The step counts in the "Does working longer help?" chart were measured on the transcripts and are stored in `data.json` as measured.
