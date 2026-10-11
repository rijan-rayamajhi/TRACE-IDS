# TRACE-IDS — Guardrails (No Drift, No Hallucination)

Read this before each work session. If an action breaks a rule here, stop.

## Part A — No scope drift

1. **Single source of truth.** `PUBLICATION_PLAN.md` is the plan (`PLAN.md` is retired). Work its
   steps in order; don't open a step until the previous step's boxes are checked.
2. **Scope is frozen.** Experiments E1–E5 (+ ablation, shared-scaling check) are complete; the
   remaining deliverable is the paper. No new experiment unless a reviewer-level objection forces it.
3. **New ideas go to the backlog, not the branch.** Any "wouldn't it be cool to also…" gets one
   line in `BACKLOG.md` and is dropped for now. No mid-phase pivots.
4. **Fixed models and datasets.** RF, gradient-boosted trees, small MLP × the four NetFlow v3
   datasets (NF-CICIDS2018, NF-UNSW-NB15, NF-ToN-IoT, NF-BoT-IoT). No new model, dataset, or
   dependency without writing one line here saying which rule forced it.
   - 2026-10-10: GBT + MLP added — "pooling is a weak baseline" objection (E2).
   - 2026-10-10: ToN-IoT + BoT-IoT added — "one cherry-picked pair" objection (E3).
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
