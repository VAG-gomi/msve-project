# MSVE v0.8.7.2 — Work 1: Source Identity and Execution Provenance Audit

**Mode:** Read-only forensic review. No files modified.

## Hash discrepancy resolved

**Report C** (`MSVE_v0.8.7_TRANSFER_MODEL_LINKAGE.md`) states:
- Model hash: `e49aee04a0c2b5ecee8d4981d0abc46b5d3b355bc9f23ed721b2eb6a7acaac56`
- Bytes: 18,391

**Transfer manifest** states for `audit_model_087.py`:
- Hash: `7239f6060378b90adffe8de2dd43982ea117d0506a39c85bbe7c19cb000a77df`
- Bytes: 18,391

**Current file** (`audit_model_087.py`):
- Hash: `7239f6060378b90adffe8de2dd43982ea117d0506a39c85bbe7c19cb000a77df`
- Bytes: 18,391
- mtime: 2026-10-09 14:08:11 UTC

**Resolution:** The manifest is correct. Report C contains a **stale
hash**: `e49aee04…` was the hash of the model *before* the R1-4 fix
(adding `v['checker'] != StringVal('')` to invariant 25), at which point
the file was 18,333 bytes. Report C incorrectly pairs the old hash
with the new byte count (18,391). The error was introduced when Report C
was written from an earlier-recorded hash rather than re-hashing the
final file. The manifest's hash (`7239f606…`) identifies the current
source model.

## Execution provenance

| Artefact | mtime (UTC) | Ties to |
|---|---|---|
| `run_audit_087_raw.log` | 14:05:50 (timestamp 14:05:48Z) | **First** run — model *before* R1-4 fix |
| `audit_model_087.py` (current) | 14:08:11 | R1-4 fix applied |
| `sat_models_087.json` | 14:08:14 | **Second** run — final model |

**Finding:** The preserved 18/18 raw log (14:05:48Z) **cannot be tied
to the final model file**. It records a run against the pre-R1-4 model
(`e49aee04…`, 18,333 bytes), which lacked the `checker ≠ ""`
requirement in invariant 25. The final model (`7239f606…`, 18,391
bytes) was verified by a second 18/18 run at ~14:08 UTC, but that run's
full stdout was **not** preserved as a raw log — only the tail
(3 lines) was captured in the working notes.

**What the SAT witnesses establish:** `sat_models_087.json`
(14:08:14) was written by the second run and therefore reflects the
final model. The 9 SAT-case witnesses tie to the final model.

**What must be reverified later:** A complete raw log for the final
model (`7239f606…`). The second run's 18/18 verdict is attested in
working notes but not preserved as a raw artefact. Per the work order,
tests are not rerun here; the reverification must occur in a future
work order with raw-log preservation.

## Commands used

```
sha256sum audit_model_087.py
# 7239f6060378b90adffe8de2dd43982ea117d0506a39c85bbe7c19cb000a77df

ls -la --time-style=full-iso audit_model_087.py run_audit_087_raw.log sat_models_087.json

head -8 run_audit_087_raw.log
# timestamp: 2026-10-09T14:05:48Z
```
