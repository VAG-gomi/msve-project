# Candidate Manifest — MSVE 0.8.9.10

**Work order:** MSVE-WO-1.9J
**Date:** 2026-10-12
**Status:** CORRECTION CANDIDATE — NOT APPROVED, NOT FROZEN

## Repository identities (verified via git)

| Repository | Role | Commit SHA (40-char) |
|------------|------|----------------------|
| Archival | candidate content | `3e0c87c42533be95c3976e6016a3d9a4f7d658ee` |
| Archival | final (with PROJECT_STATE) | `a9d35b4e138e6082246bb990c269cac9aa4376db` |
| Prototype | implementation (WO-1.9J decoder + tests) | `a89f473275b4cf97bec92106e17d533a0442f574` |

Each SHA verified to resolve in its repository. The prototype commit contains
the duplicate-aware decoder and run_text() regression tests.

## Artifact hashes (SHA-256, verified against published files)

### Archival candidate artifacts

| Artifact | SHA-256 |
|----------|---------|
| MSVE_DESIGN_SPEC_v0.8.9.10.md | `4ce900b58c2d799c6c7697c1b045efc3771fbf45090303a41f7c34d44ea4a699` |
| D3_SOLVER_FRAGMENT_SCHEMA.md | `e629746175f39a93bb9f36a59baaefca6705dea9be4acb1389c645f655976be9` |
| INVOCATION_VECTORS.md | `cc9923948bb1a6a63954209c526dcaecb422639929199104b98ac5c31048e967` |
| QUERY_ID_VECTORS.md | `747e3b899cacfb8b64dc22395bae3888c261d7dddba56c43e9c730419e4e81dd` |
| audit_model_08910.py | `27b0fc325dd863039138e9a9bd226a2cd47a68ef003a46868d7fe3222e99a68d` |
| run_audit_08910.py | `bf213b62bc3b9d59ae31b0f312ba094cdc40f7a49eb42576324b26d912bb40cf` |
| codelists.json | `2a6eec1ead342619ef452eb2a24d9e1cfad8165566fb3528fd6a539f98a5e26f` |
| outputs/pytest_08910.txt | `1a9dc3c4a8802f6ff001c0e9dcf7c3be3d2c544917299997fcd67dc479fadb86` |
| outputs/audit_08910.txt | `48b4fc29113e8364debe4413fa6bb1e1a189e2e658c7ae2459f96bd1eadb5cbd` |

### Prototype implementation artifacts (at prototype commit above)

| Artifact | SHA-256 |
|----------|---------|
| src/msve/decode.py (duplicate-aware) | `ae3a70bfab31f7879a287f6273095ded2e93a75e6f4be4f415ab4563642c4669` |
| src/msve/pipeline.py | `a2df8b05ad74afed5e2c00e394f04979eb63dfe1bd244b147fe142497ad04ace` |
| src/msve/solver.py | `6ccab5abbf0d5e1b148ab5e0f96195d7799f65890b616c3a7dbdb57b8814a29a` |
| src/msve/queries.py | `8fad6036862fb0d40b656ad657e70a432b973bbdfc2199713d3631b603a0afd9` |
| tests/test_wo19a_corrections.py | `d99b0dcdc9cf0b192876412327b8101a7cd908b0e90006e7efe4f1597faf24d9` |

## Verification (reported)

- Prototype: 178/178 passed (see outputs/pytest_08910.txt)
- Formal model: 32/32 checks (see outputs/audit_08910.txt)
- M8: 6/6 inherited from 0.8.9.4 (verified 2026-10-12; grammar unchanged through 0.8.9.10)

## Preservation

Prior candidates unchanged through 0.8.9.9.
