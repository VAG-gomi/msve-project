# Candidate Manifest — MSVE 0.8.9.9

**Work order:** MSVE-WO-1.9I
**Date:** 2026-10-12
**Status:** CORRECTION CANDIDATE — NOT APPROVED, NOT FROZEN

## Repository identities (40-char Git SHAs, verified via git)

| Repository | Commit SHA |
|------------|------------|
| Archival (candidate content) | `0f0ea506ee6cc8a279da5258f59b630335dc2edb` |
| Archival (final) | `de1f603e08e8eb9066ceacb0a1fd16cb7a5724e6` |
| Prototype | `9c865d21169db5e67480faabf8b4bbee491bfa5a` |

## Artifact hashes (SHA-256, verified against candidate-content commit)

| Artifact | SHA-256 |
|----------|---------|
| MSVE_DESIGN_SPEC_v0.8.9.9.md | `cc356118e7496e72fe4b5b545071c9ebb0c3e99f646c1c62481a2219fb9f11d7` |
| D3_SOLVER_FRAGMENT_SCHEMA.md | `0b3445e3903350c989e06da30d45360546543e478080c5acb4506788c4083cb4` |
| INVOCATION_VECTORS.md | `cc9923948bb1a6a63954209c526dcaecb422639929199104b98ac5c31048e967` |
| audit_model_0899.py | `27b0fc325dd863039138e9a9bd226a2cd47a68ef003a46868d7fe3222e99a68d` |
| run_audit_0899.py | `216964e9db351d90495ed73a2f9fbed2d6a6e1f769296133cfe984cba16bf142` |
| codelists.json | `2a6eec1ead342619ef452eb2a24d9e1cfad8165566fb3528fd6a539f98a5e26f` |
| QUERY_ID_VECTORS.md | (in candidate) |

## Verification (reported, not independently reproduced)

- Prototype: 176/176 passed (Python 3.12.3, z3-solver 5.1.0.0, pytest 9.1.1)
- Formal model: 32/32 checks, self-contained runner
- M8: 6/6 inherited from 0.8.9.4 (verified 2026-10-12; grammar unchanged through 0.8.9.9)

## Test command

```
cd ~/workspace/msve-wo19b/prototype
python3 -m pytest tests/ -q
```

## Preservation

Prior candidates unchanged: 0.8.8.1, 0.8.9, 0.8.9.1, 0.8.9.2, 0.8.9.3,
0.8.9.4, 0.8.9.5, 0.8.9.6, 0.8.9.7, 0.8.9.8.
