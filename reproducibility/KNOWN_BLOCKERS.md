# Known blockers and unrecoverable history

No Python source in this pass was left without a disposition. The following
are permanent limitations of the preserved evidence, not failures of this
reproduction work.

## Reconstructed, not original

- `/tmp/m8test/codelists.json` (the code-list input every Z3 model loads at
  import) is unavailable historically. All Z3 runs in this pass used a
  JSON reconstructed mechanically from the pinned specifications
  (27/3/12/2 members, no duplicates). SHA-256:
  `824853642cc0e86be970941e738d1567ea2fa55f4a2c19c97e75cd2d09034adb`.
  Status: **RECONSTRUCTED — NOT THE HISTORICAL ORIGINAL**. The historical
  file's bytes and hash cannot be established.

## Historical outputs not recreated

- The 0.8.4 audit's full original stdout is not preserved as a raw log;
  the 45/46 figure comes from `MSVE_v0.8.4_VERIFICATION_EVIDENCE.md`. The new
  run reproduced 45/46 with the same documented joint-SAT `unknown` miss.
- The 0.8.6 run has no preserved raw log; the 13/13 figure comes from the
  correction report and verification evidence. The new run produced 13/13.
- The F-19 2,998-value sweep script and output were never preserved
  (see `history-bank/GAPS_AND_UNAVAILABLE_RECORDS.md`); nothing here
  recreates them.
- Reviewer B's collision-sweep script is unavailable; `tools/check_f64.py`
  (M6) is a different, preserved check and is not presented as that script.

## Absolute paths in archived drivers

Every Z3 driver hardcodes `/home/hatch/workspace/msve-design/...` paths.
Reproduction used patched scratch copies (see `harnesses/`); archived
originals are unchanged. A clean clone cannot run the drivers unmodified.

## Nothing was marked FAILED or BLOCKED

Every applicable source executed successfully or was correctly classified
as STATIC-ONLY. This reflects the preserved state of these artifacts, not
a claim that all MSVE history is recoverable — the gaps above stand.
