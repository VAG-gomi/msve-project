# Invocation-ID Test Vectors (0.8.9.8)

**Encoding rule:** `enc_str(s) = u32be(len(UTF8(s))) || UTF8(s)` for required fields.
Field order: claim_id, claim_kind, query_id, query_canon, inputs_ref,
spec_version, tool, tool_version, config, timeout_ms (u32be), nonce.
Final: `invocation_id = SHA256(preimage)` as 64-char lowercase hex.

**Nonce note:** `test-nonce-001` is a FIXED TEST FIXTURE for reproducibility.
Production invocations use UUID4 random nonces (see spec §E.3).

## Vector 1

### Query object
```json
{
  "language": "msve-arith-v1",
  "declarations": [
    {
      "name": "x",
      "sort": "Int"
    }
  ],
  "assertions": [
    [
      ">",
      "x",
      0
    ]
  ]
}
```

### Canonical query JSON (sorted keys, no whitespace, UTF-8)
```
{"assertions":[[">","x",0]],"declarations":[{"name":"x","sort":"Int"}],"language":"msve-arith-v1"}
```

### Expected query_id
`9e34f1406234b4ed13c7327c6186f895df0121187c8a110043d7e4a588ce015d`

*Verification: SHA-256 of the canonical bytes above equals this query_id.*

### Invocation fields
- claim_id: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- claim_kind: `holds`
- query_id: `9e34f1406234b4ed13c7327c6186f895df0121187c8a110043d7e4a588ce015d`
- query_canon: (canonical JSON above)
- inputs_ref: `9e34f1406234b4ed13c7327c6186f895df0121187c8a110043d7e4a588ce015d` (fallback = query_id)
- spec_version: `0.8.8.1`
- tool: `z3`
- tool_version: `5.1.0`
- config: `default`
- timeout_ms: `5000`
- nonce: `test-nonce-001` (FIXED TEST FIXTURE)

### Preimage bytes (hex)
```
000000406161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616100000005686f6c64730000004039653334663134303632333462346564313363373332376336313836663839356466303132313138376338613131303034336437653461353838636530313564000000627b22617373657274696f6e73223a5b5b223e222c2278222c305d5d2c226465636c61726174696f6e73223a5b7b226e616d65223a2278222c22736f7274223a22496e74227d5d2c226c616e6775616765223a226d7376652d61726974682d7631227d000000403965333466313430363233346234656431336337333237633631383666383935646630313231313837633861313130303433643765346135383863653031356400000007302e382e382e31000000027a3300000005352e312e300000000764656661756c74000013880000000e746573742d6e6f6e63652d303031
```

### Expected invocation_id
`27165e3ccdaef938f5821521544763c6c7537a4d4e9d1847b23e09eb49cd7826`
