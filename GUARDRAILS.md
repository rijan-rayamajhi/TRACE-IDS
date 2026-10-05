# TRACE-IDS — Guardrails (No Drift, No Hallucination)

Read this before each work session. If an action breaks a rule here, stop.

## Part A — No scope drift

1. **Single source of truth.** `PLAN.md` is the plan. Work the phases in order; don't open a
   phase until the previous phase's boxes are checked.
2. **Scope is frozen.** Core deliverable = Phases 0–3 (RQ1) + 6–7. RQ2 and RQ3 are **stretch**,
   touched only after the core result exists and is written up.
3. **New ideas go to the backlog, not the branch.** Any "wouldn't it be cool to also…" gets one
   line in `BACKLOG.md` and is dropped for now. No mid-phase pivots.
4. **One model, one dataset pair.** Random Forest + {CIC-IDS2017, UNSW-NB15}. No new model,
   dataset, or dependency without writing one line here saying which rule forced it.
5. **Definition of done per phase** = its boxes checked + a committed notebook/script that
   reproduces that phase's output from `data/` with no manual steps.
6. **Timebox.** If a phase runs >1.5× its estimate, stop and cut scope — don't expand it.

## Part B — No hallucination

Research dies on invented numbers and fake citations. These are hard rules.

1. **Every number traces to a cell.** No metric goes into the report, README, LOR, or an email
   unless it was printed by committed, re-runnable code in `results/`. Nothing typed from memory.
2. **The results table is generated, never hand-edited.** It is written by a script that reads
   `results/`. If a number changes, the script re-runs; you don't edit the markdown.
3. **No citation without a verified link.** Every paper/author/claim about prior work must have a
   real URL or DOI that was actually opened. No "this is probably from…". If unverified → delete it.
4. **Observed vs expected are labeled.** Never write a result that hasn't been run. "Expected ~99%"
   is a hypothesis; "observed 98.7%" requires the cell. Keep the words distinct.
5. **Fixed seeds.** All splits/models use a fixed `random_state`. A number you can't reproduce is
   a number you can't report.
6. **No claim beyond the test.** Cross-dataset result ≠ "works in the real world." Report what was
   measured, name what wasn't (real-time, adversarial = out of scope).
7. **Uncertainty is stated, not smoothed.** If a result is weak, say so. A smaller honest gain
   beats an inflated one — and an advisor will catch the inflated one.

## Self-check (run before any write-up or email)

- [ ] Every number in it was produced by committed code
- [ ] Every citation link was opened and is real
- [ ] No result claimed that wasn't actually run
- [ ] Scope still matches PLAN.md (no silent RQ2/RQ3 creep)
