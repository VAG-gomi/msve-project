# Reconstructed code-list input

Every Z3 model in the repository loads its code lists at import time from
the absolute path `/tmp/m8test/codelists.json`:

```python
CODES = json.load(open('/tmp/m8test/codelists.json'))
```

That file was never preserved. For this reproduction pass it was
reconstructed as follows:

1. The four lists were extracted mechanically (regex over backtick-quoted
   codes and the `define is_packaging_error` disjunction) from the pinned
   specification bytes — `candidate/0.8.8.1/MSVE_DESIGN_SPEC_v0.8.md`
   (`dbc610c3…`).
2. Each list was checked against its normative definition: 27 admission
   codes (§B.9), 3 unsupported reasons (§B.9), 12 validation codes (§B.13a),
   2 packaging codes (`output-not-encodable`, `canonicalization-failure`).
   No duplicates; no unsupported entries.
3. The 0.8.8, 0.8.7, and 0.8.3-era specs were checked member-by-member:
   all four lists are identical across eras, so one reconstruction serves
   all runs in this pass.

- SHA-256: `824853642cc0e86be970941e738d1567ea2fa55f4a2c19c97e75cd2d09034adb`
- Size: 1370 bytes
- Status: **RECONSTRUCTED — NOT THE HISTORICAL ORIGINAL**

The temporary file was created only for the runs and removed afterward.
It is not committed to the repository.
