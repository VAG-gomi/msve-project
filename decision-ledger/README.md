# Decision ledger — README

## What this is

An evidence-linked index of every distinct MSVE proposal and decision
extracted from the repository's work orders, reviews, findings, and
records during work order 0.9 (2026-10-09). It does not replace the
original sources; it points at them.

## Files

- `MSVE_BRAINSTORM_DECISION_LEDGER.csv` — 26 records. Each has a stable
  ID (DEC-001…DEC-026), the proposal stated neutrally, its source with a
  path/section locator, the problem it addresses, its epistemic status,
  supporting and counter evidence, related spec/model items, dependencies,
  conflicts, what would verify or refute it, its disposition, and whether
  owner approval is required.
- `OWNER_DECISION_PACKET.md` — the bounded decision set: nine questions
  (D1–D9) with options, strongest arguments each way, spec constraints,
  consequences, the smallest exposing test, a labelled recommendation,
  and the exact choice reserved for the owner.

## Tracing a record to its source

The `source` column gives a repository-relative path plus section or
identifier (e.g. `OPEN_DECISIONS.md §1`, `candidate/0.8.8.1/
MSVE_DESIGN_SPEC_v0.8.md §E.5`). Open that path at the commit recorded in
the changelog entry for this work order and read the cited section. The
ledger's `status` column paraphrases; the source is authoritative.

## Dispositions

- **ACCEPTED-BY-OWNER** — an explicit owner decision supports it. Not
  reopened without new contradictory evidence.
- **SUPPORTED** — evidence supports the claim; not thereby a requirement.
- **PROPOSED** — plausible, not established.
- **CONFLICTED** — incompatible statements remain unreconciled; see the
  `conflicts` and `verification_needed` columns.
- **DEFERRED** — deliberately postponed by an identifiable record.
- **REJECTED-BY-OWNER** — explicitly rejected (none in this pass).
- **UNRESOLVED** — evidence or authority insufficient.

Owner acceptance is never inferred from discussion frequency, AI
agreement, test-harness implementation, or draft inclusion.

## Scope note

The ledger covers proposals and decisions present in the inspected
source universe (repository at the work-order commit plus banked
work-order records). It does not claim exhaustive brainstorm coverage:
summary-only material is marked as such, and unavailable sources are
recorded rather than reconstructed.
