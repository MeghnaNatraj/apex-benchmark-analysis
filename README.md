# Apex benchmark analysis

How well three AI models (GPT-5.5, Claude Opus 4.7, and Qwen 3.6) do white-collar work across 300 real tasks in Law, Investment Banking, and Management Consulting.

## [View the live report](https://meghnanatraj.github.io/apex-benchmark-analysis/)

### [The dataset, explained](https://meghnanatraj.github.io/apex-benchmark-analysis/explainer.html)

What the 300 tasks look like and how the 900 runs were graded, criterion by criterion.

[![The dataset, explained](docs/assets/explainer.png)](https://meghnanatraj.github.io/apex-benchmark-analysis/explainer.html)

### [The analysis](https://meghnanatraj.github.io/apex-benchmark-analysis/analysis.html)

Which model does the job, what you can trust it with, and why the models fail.

[![The analysis](docs/assets/analysis.png)](https://meghnanatraj.github.io/apex-benchmark-analysis/analysis.html)

## Key findings

GPT-5.5 leads in every field. It met 64.9% of the grading criteria, against 57.6% for Opus 4.7 and 43.2% for Qwen 3.6.

Law is the hardest work for all three, and it is where they come closest together: every model passed only about a third of law tasks. Outside law they separate sharply. GPT-5.5 passed 57% of both banking and consulting tasks while Qwen passed 20% and 17%. Which model you pick matters more than what kind of work you hand it.

A task counts as passed only if it was graded and no criterion failed, so there is no partial credit.

**Read with care:** these 300 tasks were hand-picked to favor cases where the models disagree, so the gaps are wider here than they would be on a random draw. The numbers compare the three models to each other and are not official benchmark scores.

## One model passed, two failed

On 28 tasks a single model got everything right while the other two got everything wrong. The clearest case is a consulting task where GPT-5.5 scored 10 out of 10 and both others scored 0.

The client folder held three sibling spreadsheets, two stale and one current. Opus and Qwen merged all three and got every number wrong despite doing the math correctly. GPT-5.5 treated picking the right file as part of the problem, noticed that only the current one carried the client's own margin tabs, and answered from that file alone.

When two models fail the same task, the cause is usually a single wrong judgment made early, not weak math.

## How this was made

All 900 transcripts were indexed into a results table. The failures were then read rather than guessed at: a close look at a sample of failing runs produced 11 failure types, and every one of the 1,311 failed criteria was sorted into a type with a quote from its transcript as evidence. Every number on both pages was checked against the data before publishing.

## What's in this repository

| Path | What it is |
|---|---|
| `index.html` | The landing page |
| `explainer.html` | The dataset, explained |
| `analysis.html` | The analysis |
| `data/index.jsonl` | Every run and its score, one row each |
| `scripts/` | The code that builds the pages |
| `docs/assets/` | The screenshots above |

The 900 transcripts themselves are not included here, only the results computed from them.

## Reproducing the pages

Just run:

```
python3 scripts/build.py
```
