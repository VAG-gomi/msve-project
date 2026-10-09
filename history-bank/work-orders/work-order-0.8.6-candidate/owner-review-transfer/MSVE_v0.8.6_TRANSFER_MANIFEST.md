# MSVE v0.8.6 Transfer Manifest (Report E, part 1)

**Work Order:** 0.8.6.1 · **Date:** 2026-10-09
**Transfer directory:** `~/workspace/msve-design/work-order-0.8.6-candidate/owner-review-transfer/`

All transfer files were created by verbatim extraction or direct copy
from the source artefacts. No content was altered during transfer.

| # | Source path | Transfer path | Bytes | SHA-256 (source = transfer) | Byte-identity | Provenance |
|---|---|---|---|---|---|---|
| 1 | `owner-review-transfer/MSVE_v0.8.6_TRANSFER_NORMATIVE_TEXT.md` (created by verbatim extraction — see provenance) | `owner-review-transfer/MSVE_v0.8.6_TRANSFER_NORMATIVE_TEXT.md` | 17612 | `ff12ddc7859ea78e3cbd0aa73e0ce592ca9e512270b67e2433fa74fcaf4a753a` | IDENTICAL (single artefact) | Verbatim extraction from candidate spec / model / test script |
| 2 | `owner-review-transfer/MSVE_v0.8.6_TRANSFER_FORMAL_MODEL.md` (created by verbatim extraction — see provenance) | `owner-review-transfer/MSVE_v0.8.6_TRANSFER_FORMAL_MODEL.md` | 16425 | `802032b79062feb59ae87e30955cf0715f868677bb64aab028a2389170b9d6cb` | IDENTICAL (single artefact) | Verbatim extraction from candidate spec / model / test script |
| 3 | `owner-review-transfer/MSVE_v0.8.6_TRANSFER_REGRESSION_EVIDENCE.md` (created by verbatim extraction — see provenance) | `owner-review-transfer/MSVE_v0.8.6_TRANSFER_REGRESSION_EVIDENCE.md` | 13895 | `c33d3c8d864661df2b27ba7e53e3c14db65b752c06b48216832d3d08b6dd3448` | IDENTICAL (single artefact) | Verbatim extraction from candidate spec / model / test script |
| 4 | `owner-review-transfer/MSVE_v0.8.6_TRANSFER_VERIFICATION_RECORD.md` (created by verbatim extraction — see provenance) | `owner-review-transfer/MSVE_v0.8.6_TRANSFER_VERIFICATION_RECORD.md` | 3570 | `37d0d17aa9b21ca96ce7088a5a033d2d98577f7b8a745afb40c3736528d78fe6` | IDENTICAL (single artefact) | Verbatim extraction from candidate spec / model / test script |

**Provenance classification:**
- Report A (`..._NORMATIVE_TEXT.md`): programmatically extracted verbatim
  line ranges from `MSVE_DESIGN_SPEC_v0.8.md` (candidate spec, SHA-256
  `13a5aced8bb77cb2...` — see candidate manifest for full value).
- Report B (`..._FORMAL_MODEL.md`): verbatim `invariants(R)` source from
  `audit_model_086.py` (SHA-256
  `99d68de70bddec92e0f45f4cee1863856a7ec7d10e6fec6868d67d472ac562de`)
  plus a source-to-constraint mapping table (analysis, not extraction).
- Report C (`..._REGRESSION_EVIDENCE.md`): verbatim scenario constraint
  functions from `run_audit_086.py` (SHA-256
  `e91cc967e8d39271822b761213d1841e9bec8ee22fb868302b6f288852486ead`)
  plus case summaries.
- Report D (`..._VERIFICATION_RECORD.md`): transcribed execution record;
  no raw log file exists (stated explicitly in the report).

**Note on hashes:** identical transfer hashes establish faithful
reproduction of the transfer files. They do not prove that the formal
model faithfully represents the specification — that judgement rests on
the 0.8.4 two-reviewer convergence and 0.8.6 normative drafting.
