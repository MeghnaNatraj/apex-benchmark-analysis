# How this analysis was made

This project analyzes the Apex dataset, a 314 MB collection of 900 complete transcripts of AI models doing professional work. Three models (GPT-5.5, Opus 4.7, and Qwen 3.6) each attempted the same 300 tasks, 100 each in Law, Investment Banking, and Management Consulting, and every attempt was graded against a checklist of 1 to 10 criteria written for that task. The analysis below was built over two days, across about a dozen working sessions, and this page walks through how it came together in the order it actually happened.

## 1. Getting oriented

The first sessions were about understanding what the dataset even was. That meant working out its shape (3 fields of work, 100 tasks per field, 3 models per task, 900 transcripts in all, with 2,920 graded criteria across them) and how each transcript records a model working inside a simulated company, reading files and emails and spreadsheets before turning in a final answer. One detail took some untangling: each model actually attempted every task several times behind the scenes, and the transcript included here is the "representative" one, the attempt whose score sits closest to that model's average for the task.

## 2. A plain-language catalog of all 300 tasks

The raw task descriptions are long and full of company-specific detail, so the next step was translating them. Three automated helpers ran at once, one per field, each reading its 100 tasks and writing a short plain-English summary and a category label for every one. The results were checked for completeness (all 300 present, in order) and assembled into a browsable reference page with a live search box, so anyone can skim what the tasks actually ask for.

## 3. Finding out why the models failed

This was the core of the analysis, planned as a one-hour build and designed before any code was written. Counting showed the scale of the problem: 513 of the 900 transcripts had at least one failed criterion, and there were 1,311 failed criteria in total. Rather than guessing at reasons, the work ran in two passes: first a sample of about 40 failing transcripts was read closely to discover what kinds of failure actually occur, and those observations were consolidated into a fixed list of 11 failure types. Then roughly 50 automated helpers, each assigned its own batch, read every failing transcript and sorted each of the 1,311 failed criteria into one of those types, attaching a quoted piece of evidence from the transcript. A final check confirmed that every failed criterion appeared exactly once with a valid label, and nothing was silently dropped.

## 4. The first analysis dashboard

While the classification ran in the background, the findings were assembled into a single self-contained web page, the first version of the analysis. It shows which failure types are most common, how they differ by model and by field, color-coded score tables, a view of tasks where the models disagree, and a filterable table of all 1,311 failed criteria where clicking any row opens the evidence behind it. The guiding rule was that every summary number should be one click away from its proof.

## 5. A one-page explainer of the dataset itself

Separately from the analysis, a single page was built to explain the dataset's structure to a newcomer in under a minute: how 3 fields fan out into 300 tasks, then 900 transcripts, then 2,920 criteria verdicts, plus a dissection of one real task with its three attempts. The first version used a deliberately hand-drawn, sketchy look, which was rejected as childish, and the page was rebuilt from scratch in a formal printed-document style (Palatino serif type on an ivory background). Every number on the page was then verified directly against the dataset, down to individual scores, criteria counts, and quoted wording, and the layout went through many small rounds of editing (merging sections, removing columns, and settling where the expert reference answer appears).

## 6. A simpler, friendlier dashboard

The original analysis dashboard assumed too much background knowledge, so it was rebuilt as a second version (published here as analysis.html) with plainer wording and a cleaner layout. Several short sessions refined it: bigger section headings, simpler summary cards, a one-line explanation of how scoring works, and the removal of lines that confused more than they explained.

## 7. Changing the headline measure

The main model-by-field table originally showed the share of criteria each model met, which gives partial credit for half-finished work. After weighing the options, it was switched to a stricter measure: the share of tasks a model got fully right, with no partial credit. The change sharpened the story, for example that GPT-5.5 passes the most tasks in every field, and that Opus fully passes only about a third of law tasks despite meeting half of law's individual criteria.

## 8. A close look at where the models disagree

One question drove a final deep dive: are there tasks where one model succeeded and the other two failed, and can we see why? There turned out to be 194 criteria where exactly one model succeeded, and 28 whole tasks where one model got everything right while the other two got everything wrong. The most extreme case was a consulting task that GPT-5.5 passed 10 out of 10 while the other two scored zero: the task's folder contained three similar spreadsheets, and the failing models combined all three when the task expected only the newest one.

## 9. Packaging it all for sharing

The last phase gathered everything (the two dashboards, the explainer page, and the findings) into one public, well-organized project, with a written plan reviewed before the work started and independent checkers verifying accuracy along the way. Part of that effort was rewriting the material in plain language for non-technical readers, including this very page.

## How the work was run

The analysis was directed and reviewed end to end by Meghna Natraj, who made every decision about what to measure, what to build, and what to reject. The heaviest steps, summarizing 300 tasks and classifying 1,311 failed criteria, were run by many automated helpers working in parallel, with checks afterward to confirm nothing was missed.
