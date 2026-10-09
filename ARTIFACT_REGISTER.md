# ARTIFACT_REGISTER.md

All hashes measured 2026-10-09 during repository establishment (work order
MSVE-REPO-001). "Measured" = independently recalculated from the actual file
bytes. "Reported" = value from an earlier project record.

## Candidate artifacts (0.8.8.1)

| Artifact | Path | SHA-256 (measured) | Bytes | Origin | Verification |
|---|---|---|---|---|---|
| Design spec | `candidate/0.8.8.1/MSVE_DESIGN_SPEC_v0.8.md` | `dbc610c3a97d7107ab0f4de499b240e243f45c49b56f0a1855b7333c80cb7782` | 96366 | `~/workspace/msve-design/work-order-0.8.8.1-candidate/` | Measured; matches reported value |
| Formal model | `candidate/0.8.8.1/audit_model_0881.py` | `fc6eb49f50eae04595495af05058d52f7c27b0d5b29aa3e16254a33f66be31ae` | 21788 | `~/workspace/msve-design/work-order-0.8.8.1-candidate/` | Measured; matches reported value |
| Regression script | `candidate/0.8.8.1/run_audit_0881.py` | `c750ef5c37a132893908c1bfaf4070e67d5a842e7043684e95f05a1936711f83` | 10120 | `~/workspace/msve-design/work-order-0.8.8.1-candidate/` | Measured; matches reported value |
| Raw test log | `candidate/0.8.8.1/run_audit_0881_raw.log` | `525cd40667f96be4d297f5be39a8c02e72ddf7f1644b7e3a31c73006082b480a` | 852 | `~/workspace/msve-design/work-order-0.8.8.1-candidate/` | Measured; matches reported value |

All four artifacts verified byte-identical to their workspace sources at
archival time. No discrepancies found.

## Continuity records

Eight Markdown files under `records/continuity-export-01/`, copied
byte-identical from `~/workspace/msve-design/msve-chatgpt-continuity/`.
See that directory's `07_SOURCE_MANIFEST_AND_CROSS_REFERENCE.md` for the
per-file hashes of the continuity package itself.

## Reported verification result (preserved, not re-executed)

The continuity record reports 9/9 regression tests passing with the raw log
above corresponding to the final candidate hashes (timestamp
2026-10-09T14:52:51Z, Python 3.12.3, Z3 5.1.0, exit 0). This work order did
not re-run the test suite; the result is preserved as a reported
verification result attributable to work order 0.8.8.1-FINAL.
