# Case study: one model passed, two failed

## Where this comes from

The analysis page has a view called "Two of three failed". It collects every grading criterion where exactly one model succeeded and the other two failed. There are 194 such criteria. GPT-5.5 was the sole survivor 83 times, Opus 4.7 43 times, and Qwen 3.6 38 times. At the whole-task level there are 28 tasks where one model got everything right and the other two got everything wrong: GPT-5.5 on 17 of them, Qwen on 6, Opus on 5.

This page walks through one of those 28 tasks in detail, because the transcripts show exactly where the two failing models went wrong, and it was not the math.

## The task

Task World127_AK_Task03 is a Management Consulting task with 10 grading criteria. The model is asked to compute the weighted average gross margin per vehicle platform from the client's SKU spreadsheet data (SKU means stock keeping unit, one row per product), then the price increase needed for the lowest-margin platform to catch up.

GPT-5.5 scored 10 out of 10. Opus 4.7 and Qwen 3.6 both scored 0 out of 10.

The trap is in the client folder. It contains three sibling spreadsheets with non-overlapping SKU ranges:

| File | SKUs | Status |
|---|---|---|
| Helios_SKU_Master_Reworked (1).xlsx | 400 | Stale |
| Helios_SKU_Additional_2000.xlsx | 2,000 | Stale |
| Helios_SKU_Rebuilt_ICE70plus.xlsx | 2,500 | Current, matches the correct answer |

Only the Rebuilt file reflects the client's current data. The correct answer comes from that file alone: GM Ultium is the lowest-margin platform at 30.8%, and it needs a 1.6% price increase.

## What each model did

**Opus 4.7** merged all three files. Its transcript says it worked from "4,900 unique SKUs pulled from the three client files". On that merged data it found Ford C2 as the lowest-margin platform at 27.1% and computed a 2.62% price increase. Its arithmetic and methodology were correct, but because the inputs were wrong, all 10 of its numbers were wrong, and it failed every criterion.

**Qwen 3.6** made the same call. Its transcript reads "All three files have the same platforms. Now let me combine all data". It also reported Ford C2 as lowest, at 25.95%, and failed every criterion.

**GPT-5.5** treated choosing the right file as part of the problem. It listed every candidate spreadsheet, checked SKU ranges and row counts, and noticed that the Rebuilt file is the only one carrying the client's own margin-calculation tabs. It computed the answer separately for each candidate before committing, then answered from the Rebuilt file alone: GM Ultium lowest at 30.81%, with a 1.57% price increase, matching the correct answer's 1.6%.

## Why it matters

All three models did the calculation competently. The entire 10-point gap between passing and failing came from one decision made early in the run: which spreadsheet to treat as the client's data. Two models silently combined everything. One model treated the folder itself as something to investigate.

## A caveat

The prompt said only "the client's SKU data". That is genuinely ambiguous. A careful human analyst might also have asked which file to use, or might have merged them. So this task measures judgment about which documents to trust as much as it measures calculation skill.

## The lesson

When two models fail the same task, the cause is often a shared wrong judgment call early on, not weak math. Grading criteria catch the wrong final numbers, but the transcripts show that the numbers went wrong at the moment the models decided what to read, before any arithmetic happened.
