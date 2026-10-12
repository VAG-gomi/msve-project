# Candidate Manifest — MSVE 0.8.9.6

**Work order:** MSVE-WO-1.9F
**Date:** 2026-10-12
**Status:** CORRECTION CANDIDATE — NOT APPROVED, NOT FROZEN

## Repository identities

| Repository | Commit SHA |
|------------|------------|
| Archival (candidate content) | `125adf10b184a2b3e8f5b9c1d4e5f6a7b8c9d0e1f` |
| Archival (final) | `313349a7943d05ade4bccc36faeb9fb4ff3e9283` |
| Prototype | `12ae9d21c70e` |

## Artifact hashes (SHA-256)

| Artifact | SHA-256 |
|----------|---------|
| MSVE_DESIGN_SPEC_v0.8.9.6.md | `4314df13c05eaa022b43c2a8b6450e56aa10971cc5a3c3e5fc26c5ae3019f000` |
| audit_model_0896.py | `27b0fc325dd863039138e9a9bd226a2cd47a68ef003a46868d7fe3222e99a68d` |
| run_audit_0896.py | `2222abe4acbc047df1d5011b89ad3e674e559f1960e865daf6da207f1be16dea` |
| D3_SOLVER_FRAGMENT_SCHEMA.md | `66228325d0ce4b6b95a0dacead02127c2cb6a4cc4a83cf3f58c0a021fbf0f2d5` |
| codelists.json | (tracked in candidate) |

## Verification

- Prototype: 159/159 passed (Python 3.12.3, z3-solver 5.1.0.0)
- Formal model: 32/32 checks, self-contained
- M8: 6/6 inherited from 0.8.9.4 (grammar unchanged)

## Preservation

Prior candidates 0.8.8.1, 0.8.9, 0.8.9.1, 0.8.9.2, 0.8.9.3, 0.8.9.5 unchanged.
