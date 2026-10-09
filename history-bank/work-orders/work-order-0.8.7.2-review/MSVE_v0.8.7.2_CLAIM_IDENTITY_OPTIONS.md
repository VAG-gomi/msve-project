# MSVE v0.8.7.2 — Work 2: Claim-Identity Decision Options

**Constraint:** Neither option may define claim identity solely as the
hash of a computed output when distinct claims could share that output.

## The problem

Two goals, `derive 2+2` and `derive 8/2`, both yield value `4` with
hash `H(4)`. The current claim-key (`DERIVED_VALUE → value hash`)
assigns both the same key. A proof of `2+2=4` would satisfy the
claim-linkage for a result asserting `8/2=4`. For payload-free variants
(`HOLDS`, `NO_SOLUTION`, `CONTRADICTION`, `UNIQUE_UNDER_PROJECTION`)
there is no output hash at all.

## Option A: Canonical claim descriptor (schema change)

**Proposal:** A new normative structure, stored as a new optional field
`claim_descriptor: Option<ClaimDescriptor>` on `ResultRecord`, or as a
new evidence collection:

```
ClaimDescriptor := {
  proposition: String,     # canonical rendering, e.g. "2+2=4" or "∀x. sorted(x)"
  goal_ref: Hash,          # hash of the goal/spec item this claim answers
  inputs_ref: Hash,        # inputs the claim was established from
  assumptions: [String],   # projection, axioms, or ambient assumptions
  interpretation: String,  # query interpretation, e.g. "exact-arithmetic"
}
claim_id: Hash = sha256(canonical_encoding(descriptor))
```

**What must be stored:** The descriptor itself (for audit) and its hash
(as the join key). The hash resolves to the descriptor via a new
`evidence.claim_descriptors: [ClaimDescriptor]` collection (parallel to
`proof_artifacts`).

**How it resolves:** `verification_records[].property` must equal the
`claim_id`; the descriptor is retrieved by hash lookup; a verifier
recomputes the hash to confirm integrity.

**Formal-model changes:** `claim_key` becomes `claim_id` lookup;
`resolves_in` extended to the new collection; the `__no_claim_key__`
sentinel is deleted (every result with a basis must have a descriptor).

**Positive example:** `derive 2+2` → descriptor
`{proposition: "2+2=4", goal_ref: H(goal1), inputs_ref: H(inputs), …}`,
`claim_id = H1`. `derive 8/2` → `claim_id = H2 ≠ H1`. A proof record
for H1 does not satisfy a result with H2.

**Counterexample addressed:** Shared output `4` no longer collides;
`HOLDS` gets a descriptor with its check property and subject.

**Cost:** Schema change (new field + collection); all producers must
construct descriptors; canonical encoding must be specified exactly.

## Option B: Schema-preserving claim identity (no new field)

**Proposal:** Constrain the existing `VerificationRecord.property`
field normatively to a structured claim identifier, and require the
`ResultRecord` to carry the same identifier in a normatively defined
(but not new) location.

The identifier format (normative, not a schema change):
```
claim_ref := "claim:" + sha256(goal_id + "|" + proposition + "|" + inputs_ref)
```
where `goal_id` is the goal's identity from the validated spec,
`proposition` is the canonical claim text, and `inputs_ref` is the
existing evidence-bundle hash.

**How it distinguishes identical outputs:** `derive 2+2` and `derive
8/2` have different `goal_id`s (different spec items), hence different
`claim_ref`s, even though the value hash `H(4)` is shared. The
verification record's `property` must equal the result's `claim_ref`.

**How it supplies a key for payload-free results:** For `HOLDS`, the
`proposition` is the check property (e.g., `"sorted(output)"`) and the
`goal_id` identifies the check goal. `NO_SOLUTION`/`CONTRADICTION` use
the search problem's identity. No output hash is needed because the key
is derived from goal + proposition + inputs, not from the result value.

**Where the identifier lives:** On `VerificationRecord.property`
(existing field, now normatively structured). The `ResultRecord` side
is derived: the result's claim_ref is computed from the goal being
answered (available to the producer) and recorded... 

**Gap in Option B:** The `ResultRecord` schema has no field for the
goal identity or the claim_ref. The producer knows the goal, but the
*record* does not state it. For the invariant `vr.property =
result.claim_ref` to be checkable, the result's claim_ref must be
recoverable from the record. Options: (B1) derive it from
`spec_version` + result contents (fragile); (B2) admit that Option B
requires at minimum a `claim_ref: Hash` field on `ResultRecord` —
which is a smaller schema change than Option A's full descriptor, but
a schema change nonetheless.

**Formal-model changes (B2):** Add `claim_ref: String` to the record;
`claim_key` replaced by direct equality; no sentinel.

**Positive example:** Same as A for the `2+2` vs `8/2` case.
**Counterexample:** If `goal_id` is not unique across specs, collision
remains — mitigated by including `spec_version` in the hash input.

**Cost:** Normative format specification; (B2) one new Hash field —
minimal, but still a schema change. (B1) is fragile and not recommended.

## Recommendation

**Option A** is the least ambiguous path. It makes the claim
first-class (storable, hashable, auditable) rather than encoding it
into a string field by convention. The cost — a new field and
collection — is justified because claim identity is load-bearing for
the central requirement ("evidence for the exact claim"), and
convention-encoded strings (Option B) cannot be validated beyond
equality.

**However:** Option A must not be inserted into the candidate without
owner approval (per work-order constraints). If the owner prefers no
schema change, Option B2 (single `claim_ref: Hash` field) is the
minimum viable alternative; Option B1 (pure convention) should be
rejected as unverifiable.

**What neither option does:** Neither defines *which* propositions are
valid claims — that remains the spec author's responsibility. The
mechanism guarantees identity and linkage, not truth.
