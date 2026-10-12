# msve-project

Canonical project bank for MSVE (Mathematical Structure and Verification Engine).

## What is MSVE?

MSVE is a proposed system for constructing and evaluating mathematical
results while making explicit what each result means, what evidence
supports it, and what remains unverified. Its central purpose is to make
mathematical verification claims traceable and challengeable, rather than
treating every successful calculation, solver response, or test as
equivalent evidence.

It is designed as a three-stage process: **decode** a structured
mathematical input, **validate** it against requirements and declared
scope, and **produce a typed result** linked to the relevant claims and
supporting evidence.

MSVE distinguishes assurance methods with different limits: kernel-checked
proofs, independent recomputation, solver-backed evidence, and test-backed
evidence. A solver observation is not automatically a proof, and passing
tests do not establish universal correctness. Uncertainty, unsupported
cases, and verification failures are preserved rather than silently
converted into successful conclusions.

**Current reality:** MSVE is still a design candidate — a complete engine
has not been authorised for implementation, and no final baseline is approved.
The current correction candidate is
[**0.8.9.10**](candidate/0.8.9.10/MSVE_DESIGN_SPEC_v0.8.9.10.md)
([D3 schema](candidate/0.8.9.10/D3_SOLVER_FRAGMENT_SCHEMA.md),
[manifest](candidate/0.8.9.10/CANDIDATE_MANIFEST_08910.md)).
Status: **CORRECTION CANDIDATE — AWAITING OWNER REVIEW** (see
[PROJECT_STATE.md](PROJECT_STATE.md) and
[KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md)).
0.8.9.10 is a candidate awaiting owner review, not an accepted baseline.
D7 design freeze and release remain unapproved.
Separately, owner ruling D8 authorises a bounded **exploratory prototype**
in the [separate implementation repository](https://github.com/VAG-gomi/msve-engine-prototype)
(experimental evidence only under D9 separation); its experimental status
does not confer approval on the archival candidate, and it does not change the
candidate's status.

## What this is

A version-controlled archive of the MSVE design specification, its formal
model, verification evidence, and project records. This repository is the
single source of truth for MSVE project state. Future work must update and
reference this record rather than reconstructing the project from
conversational memory.

## Where things live

- `candidate/0.8.9.10/` — the current review candidate (spec, Z3 model,
  regression script, D3 schema, invocation vectors, correction report, manifest).
  See `candidate/0.8.9.10/CANDIDATE_MANIFEST_08910.md` for hashes.
- `candidate/0.8.8.1/` (0.8.8.1-FINAL), `candidate/0.8.9/`, `candidate/0.8.9.1/`,
  `candidate/0.8.9.2/`, `candidate/0.8.9.3/`, `candidate/0.8.9.4/`,
  `candidate/0.8.9.5/`, `candidate/0.8.9.6/`, `candidate/0.8.9.7/`,
  `candidate/0.8.9.8/`, `candidate/0.8.9.9/` — preserved historical
  candidates, unchanged.
- `records/continuity-export-01/` — the eight continuity documents prepared
  for independent review (status, timeline, finding ledger, contract,
  verification evidence, review history, owner decisions, source manifest).
  Read the provenance correction notice in `PROJECT_STATE.md` first: some
  preserved continuity statements about review coverage are superseded.
- `history-bank/` — the complete historical artifact bank: every surviving
  versioned document, work-order directory, model, test log, review report,
  and snapshot, with inventory, timeline, provenance, lineage, verification
  history, gap register, and an independent completeness audit
  (`history-bank/COMPLETENESS_AUDIT.md`). Start here for project history.
- `PROJECT_STATE.md` — the current project status.
- `OPEN_DECISIONS.md` — unresolved owner decisions.
- `KNOWN_LIMITATIONS.md` — disclosed limits and attestations.
- `ARTIFACT_REGISTER.md` — every archived artifact with measured hashes.
- `CHANGELOG.md` — truthful record of repository changes.
- `reproducibility/` — repository-wide Python reproducibility records:
  source inventory (46 files), per-era execution evidence (0.8.4–0.8.8.1,
  M8 tests/tools), reconstructed-input provenance, patched harnesses,
  environment register, and known blockers.
- `decision-ledger/` — brainstorm and decision ledger (26 records) plus the
  bounded owner decision packet (D1–D9). Start here for what is decided,
  what is open, and what each choice requires.

## What is NOT authorised

No design freeze. No baseline acceptance. Version 0.8.9.10 is a correction
candidate awaiting owner review, not an approved baseline. No full engine implementation. No
experimental runs beyond the D8-authorised exploratory prototype (separate
workspace; experimental evidence only). See `PROJECT_STATE.md`.

## For reviewers

Start with `PROJECT_STATE.md`, then `records/continuity-export-01/00_START_HERE_AND_CURRENT_STATUS.md`.
