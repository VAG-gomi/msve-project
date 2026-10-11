# Remaining-Issues Register — Candidate 0.8.9 (WO-1.9)

**Blocking** = must be resolved before any freeze consideration.
**Non-blocking (proposed)** = documented limitations; owner acceptance required
to confirm the classification. Nothing here is marked non-blocking on the
owner's behalf.

## Blocking

1. **Owner review of candidate 0.8.9.** The candidate awaits review;
   nothing in it is approved or frozen.
2. **D7 freeze gates.** Per WO-1.8: gates 1 (blocking decisions), 2
   (spec/model consistency — improved by this WO, still needs owner
   judgment), 5 (issue classification), 6 (owner approval) remain open.
3. **Universal D3 schema.** Only the solver fragment is defined; other
   claim kinds' schemas are deferred by owner scope ruling (Option A).

## Non-blocking (proposed — owner acceptance required)

1. Finite golden vectors do not prove collision resistance (A6).
2. Timeout-induced UNKNOWN portability not demonstrated across
   Z3 versions/platforms (A1).
3. Checker independence does not eliminate common-mode failures;
   lying checker is a trust boundary (A4).
4. Assumption verification out of scope by design (D3).
5. Byte-level framing verified by Python vectors, not by the Z3 model
   (documented expressiveness limit).
6. `max_descriptors` / `max_invocations` prototype-small parameters
   retained alongside the two normative A5 parameters (no conflict;
   documented).

## New findings (none blocking)

- The M8-generated `/tmp/m8test/codelists.json` was not preserved in any
  repository; reconstructed from the spec for this audit. Recommend
  preserving it as a build artefact in future work.
