# Run reports — Z3 eras

All runs: Python 3.12.3, `z3-solver==5.1.0.0`, Z3 runtime 5.1.0,
reconstructed code lists (`82485364…`, RECONSTRUCTED — NOT THE HISTORICAL
ORIGINAL), patched scratch driver copies (originals untouched).

## 0.8.8.1-repro-001

Catalogued from the verified MSVE-REPRO-001 artifacts (not re-run).
9/9 PASS, exit 0; outcome lines identical to
`candidate/0.8.8.1/run_audit_0881_raw.log`. Full evidence in
`runs/0.8.8.1-repro-001/REPRODUCTION_REPORT.md`.

## 0.8.8-repro-001

`runs/0.8.8-repro-001/r088-stdout.txt`: 16/16 PASS, exit 0. Extracted
PASS/FAIL/summary lines byte-identical to the archived
`run_audit_088_raw.log`.

## 0.8.7-repro-001

`runs/0.8.7-repro-001/r087-stdout.txt`: 18/18 PASS, exit 0. Extracted
lines byte-identical to the archived `run_audit_087_raw.log`.

## 0.8.6-repro-001

`runs/0.8.6-repro-001/r086-stdout.txt`: 13/13 PASS, exit 0. Matches the
13/13 reported in `MSVE_v0.8.6_CORRECTION_REPORT.md`; no raw log was
preserved for this era.

## 0.8.5-repro-001

- `r085-dump-assignment.txt`: S1 assignment dump ran, exit 0.
- `r085-f20.txt`: `F-20 adjudication checks: ALL AS EXPECTED`, exit 0.

## 0.8.5.2-repro-001

`r0852-f21.txt`: all six F-21 solver checks `sat`, exit 0 — including the
three gap-demonstrating sats (F21-2, F21-3b, F21-5), confirming the
assurance-evidence gaps as documented.

## 0.8.4-repro-001

`runs/0.8.4-repro-001/r084-stdout.txt`: **45/46** checks behaved as
expected, with `FAIL [joint-SAT] solver=unknown expected=sat` — the same
documented miss as the historical record. The driver exits 1 by its own
logic (`sys.exit(0 if n_ok == len(results) else 1)`); this is the
expected behaviour for a 45/46 run, not a reproduction failure.
`r084-dump-witnesses.txt`: witness dump ran, exit 0.

## What these runs establish

Each run shows the pinned model bytes execute today and produce the
documented outcomes under the reconstructed input. They do not recreate
the historical runs, validate the original input bytes, or prove anything
about an engine (none exists).
