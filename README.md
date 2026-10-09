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
has not been authorised for implementation. This repository holds the
[design specification](candidate/0.8.8.1/MSVE_DESIGN_SPEC_v0.8.md), formal
model, Python tools, test and reproduction evidence, historical records,
limitations, and open decisions. Status:
**CORRECTION CANDIDATE PREPARED — OWNER REVIEW REQUIRED** (see
[PROJECT_STATE.md](PROJECT_STATE.md) and
[KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md)). The version label
"0.8.8.1-FINAL" does not mean an approved or frozen baseline.

## What this is

A version-controlled archive of the MSVE design specification, its formal
model, verification evidence, and project records. This repository is the
single source of truth for MSVE project state. Future work must update and
reference this record rather than reconstructing the project from
conversational memory.

## Where things live

- `candidate/0.8.8.1/` — the current design candidate (spec, Z3 model,
  regression script, raw test log). See `ARTIFACT_REGISTER.md` for hashes.
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

No design freeze. No baseline acceptance. Version 0.8.8.1 is a correction
candidate, not an approved baseline. No engine implementation. No
experimental runs. See `PROJECT_STATE.md`.

## For reviewers

Start with `PROJECT_STATE.md`, then `records/continuity-export-01/00_START_HERE_AND_CURRENT_STATUS.md`.
