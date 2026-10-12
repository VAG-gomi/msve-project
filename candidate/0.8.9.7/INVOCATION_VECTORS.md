# Invocation-ID Test Vectors (0.8.9.7)

Normative: `enc_str(s) = u32be(len(UTF8(s))) || UTF8(s)`.

## Vector 1

- claim_id: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- claim_kind: `holds`
- query_id: `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`
- query_canon: (see below)
- inputs_ref: `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` (fallback = qid)
- spec_version: `0.8.8.1`
- tool: `z3`
- tool_version: `5.1.0`
- config: `default`
- timeout_ms: `5000`
- nonce: `test-nonce-001`

**Expected invocation_id:** `f082b9833cfbbe7ac316ffe4227c375470089793cfe7d419c040a83a7621fc0b`
