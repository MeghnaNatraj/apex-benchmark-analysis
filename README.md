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

## Further reading

- [docs/deep-dive.md](docs/deep-dive.md), a case study of one task where one model passed and two failed, and why.
- [docs/process.md](docs/process.md), how this analysis was produced.

## What's in this repository

| Path | What it is |
|---|---|
| `index.html` | Landing page linking to the two pages above |
| `explainer.html` | The dataset, explained |
| `analysis.html` | The analysis of the results |
| `docs/` | The deep-dive case study and the process notes |
| `scripts/` | The scripts used to compute the numbers on the pages |
| `data/index.jsonl` | The results table, one row per model run with its scores |

The full run transcripts are not included in this repository, only the scores computed from them.
