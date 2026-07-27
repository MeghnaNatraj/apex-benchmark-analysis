# Apex benchmark analysis

An analysis of how well three AI models do white-collar work. The Apex benchmark is a set of 300 real-world work tasks, 100 each in Law, Investment Banking, and Management Consulting. Each task has a correct answer and a set of pass/fail grading criteria. Three models (OpenAI's GPT-5.5, Anthropic's Claude Opus 4.7, and Alibaba's Qwen 3.6) each attempted all 300 tasks, for 900 runs in total. This repository holds the two pages that present the results, the write-ups behind them, and the scripts and scores used to compute every number.

## View the pages

The pages are published at https://meghnanatraj.github.io/apex-benchmark-analysis/

1. [The dataset, explained](https://meghnanatraj.github.io/apex-benchmark-analysis/explainer.html), start here. What the 300 tasks look like, how the 900 runs were graded, and what a grading criterion is.
2. [The analysis](https://meghnanatraj.github.io/apex-benchmark-analysis/analysis.html), the results. Which model does the job, what you can trust it with, and why the models fail.

## Key findings

- GPT-5.5 leads in every field. It met 64.9% of grading criteria overall, against 57.6% for Opus 4.7 and 43.2% for Qwen 3.6.
- Counting only tasks passed cleanly (no failed criteria, no partial credit), GPT-5.5 passed 58% of Investment Banking tasks, 55% of Law tasks, and 58% of Consulting tasks.
- Opus 4.7 falls hardest in Law. It passed only about a third of law tasks completely (32%), against 50% in Investment Banking and 48% in Consulting.
- Qwen 3.6 passed at most 1 in 5 tasks outside Law (20% in Investment Banking, 17% in Consulting, 34% in Law).
- Which model you pick matters more than which kind of work you give it.
- Of the 2,920 criteria verdicts, 1,311 failed and 19 were left ungraded. On 194 criteria, exactly one model succeeded where the other two failed. GPT-5.5 was that sole survivor 83 times, Opus 43, Qwen 38.

## How the grading works

Every task comes with a gold (correct) answer and 1 to 10 pass/fail grading criteria, 2,920 criteria verdicts in total. A model's answer is graded against each criterion separately, and each criterion either passes or fails. The task-level numbers use no partial credit: a task counts as passed only if none of its criteria failed. The few criteria that could not be graded do not count against a model.

## Further reading

- [docs/deep-dive.md](docs/deep-dive.md), a case study of one task where one model passed and two failed, and why.
- [docs/process.md](docs/process.md), how this analysis was produced.

## What's in this repository

| Path | What it is |
|---|---|
| `index.html` | Landing page linking to the two pages below |
| `explainer.html` | The dataset, explained |
| `analysis.html` | The analysis of the results |
| `docs/` | The deep-dive case study and the process notes |
| `scripts/` | The scripts used to compute the numbers on the pages |
| `data/index.jsonl` | The results table, one row per model run with its scores |

The full run transcripts are not included in this repository, only the scores computed from them.
