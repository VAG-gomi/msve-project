# MSVE v0.8.5.2 Evidence Index

**Work Order:** 0.8.5.2 · **Date:** 2026-10-09
**Directory:** `~/workspace/msve-design/work-order-0.8.5.2-audit/`
(read-only inputs: v0.8.3 candidate, v0.8.4 audit, v0.8.5 reconciliation;
no historical file modified)

## Environment note

The VM was replaced between 0.8.5.1 and 0.8.5.2 (z3 and /tmp wiped).
`z3-solver` 5.1.0 was reinstalled via pip (`z3.get_version_string()` →
`5.1.0`, same version) and `/tmp/m8test/codelists.json` was regenerated
by re-extracting the code lists from the candidate spec (27/3/12/2
counts re-verified). No audit-model logic was changed.

## Commands and results

1. `grep -n "C-02" MSVE_v0.8.5_CHECK_RECONCILIATION.md` (source and
   transfer copies) + `sha256sum` — confirmed F-22: line 89 carries the
   stale "C-02..C-32" range; lines 91–94 carry the corrected range;
   source and transfer hashes identical
   (`4ec9afa1…3eee`). Raw output preserved in working notes.
2. `python3 f21_assurance_tests.py` — exit 0. Raw output:
   F21-1 sat; F21-2 sat; F21-3 sat; F21-3b sat; F21-4 sat; F21-5 sat.
   (Six targeted checks, 30 s timeout each, z3 5.1.0.)
3. `python3 dump_assignment.py` equivalent — `s1_assignment.json`
   re-inspected (0.8.5 artefact, unchanged): LEVEL_A/LEVEL_A,
   KERNEL_PROOF, no proof-artifact resolves fact, empty verification
   records, NOT_RUN.
4. Corrected-copy creation: `cp` + single-string replacement, verified
   zero remaining occurrences of the stale range; SHA-256 recorded in
   the F-22 report.

## Reports in this directory

| File | Content |
|---|---|
| `MSVE_v0.8.5.2_F22_TRANSFER_RECONCILIATION.md` | F-22 byte evidence, corrected-copy path + hash |
| `MSVE_v0.8.5.2_F21_ASSURANCE_EVIDENCE_AUDIT.md` | F-21: JSON/model/spec inspection, 6 solver tests, proposed finding + corrections |
| `MSVE_v0.8.5.2_F20_PROSE_FORMULA_ALIGNMENT.md` | F-20: prose→formula mapping, temporal-weakening analysis, bound-variable invariant |
| `MSVE_v0.8.5.2_EVIDENCE_INDEX.md` | this file |
| `MSVE_v0.8.5_CHECK_RECONCILIATION_CORRECTED.md` | candidate copy with the F-22 range fix (historical 0.8.5 report untouched) |
| `f21_assurance_tests.py` | the six F-21 solver tests |

## What remains assumption or owner judgement

- F-21's proposed corrections add normative content the spec does not
  state; whether the assurance-basis→evidence linkage is intended is an
  owner decision.
- F-20's prose→formula alignment rests on the accepted atemporal
  weakening ("still recorded" → presence); a fully faithful rendering
  would need a temporal record model.
- F-22 is fully resolved mechanically; no judgement remains.
- The 0.8.4/0.8.5 consistency claim now carries the F-21 limitation: the
  S1 witness satisfies the formalized fragment but its Level A claim is
  evidence-free at the record level.
