# Query Identity Golden Vectors (0.8.9.2)

Canonical encoding per D3 §9.1. `query_id = SHA-256(canonical_bytes)`.

## basic

Canonical bytes (UTF-8):
```
{"assertions":[[">=","x",0],["<=","x",10]],"declarations":[{"name":"x","sort":"Int"}],"language":"msve-arith-v1"}
```

`query_id`: `939c95db4667d9aa29045932b6942cf2526cb1f8bf7c8c4495b79618acc1801c`

## reordered-keys

Canonical bytes (UTF-8):
```
{"assertions":[[">=","x",0],["<=","x",10]],"declarations":[{"name":"x","sort":"Int"}],"language":"msve-arith-v1"}
```

`query_id`: `939c95db4667d9aa29045932b6942cf2526cb1f8bf7c8c4495b79618acc1801c`

## unicode-identifier

Canonical bytes (UTF-8):
```
{"assertions":[[">","caf\u00e9",0]],"declarations":[{"name":"caf\u00e9","sort":"Int"}],"language":"msve-arith-v1"}
```

`query_id`: `daa0aff6565fa5619fb3413787d534cca888d51f572cea0e674de73617a315e8`

## nested

Canonical bytes (UTF-8):
```
{"assertions":[["and",[">","x",0],["<","y",100]]],"declarations":[{"name":"x","sort":"Int"},{"name":"y","sort":"Int"}],"language":"msve-arith-v1"}
```

`query_id`: `12ea322a0383ea654e84225187a2fe7242c865e654ddb4912f1e94f1795c9d9f`

**Equivalence:** `basic` and `reordered-keys` have identical `query_id`.
