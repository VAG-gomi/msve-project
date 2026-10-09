# MSVE v0.8 Owner-Review Manifest

**Work Order:** 0.8.1 · **Date:** 2026-10-09

Total artefacts: 101

| # | Path | Type | Bytes | SHA-256 | Provenance |
|---|---|---|---|---|---|
| 1 | `MSVE_DESIGN_SPEC_v0.8.md` | design-document | 75861 | `377e106ef2b00db6…` | original |
| 2 | `MSVE_DESIGN_REVIEW_v0.8.md` | design-document | 11050 | `d5650027ba245e0c…` | original |
| 3 | `MSVE_CAPABILITY_MATRIX_v0.8.md` | design-document | 2004 | `542fa10cd3a8cee9…` | original |
| 4 | `MSVE_ACCEPTANCE_PLAN_v0.8.md` | design-document | 8848 | `8ee1c526f135cce7…` | original |
| 5 | `MSVE_VISUALISATION_PLAN_v0.8.md` | design-document | 6610 | `3adaf96661df8cbb…` | original |
| 6 | `MSVE_REGRESSION_LEDGER_v0.8.md` | design-document | 34625 | `e04a05e68e92ce54…` | original |
| 7 | `m8/__init__.py` | m8-source | 67 | `5112fc6e78b2210d…` | original |
| 8 | `m8/lexer.py` | m8-source | 6375 | `ef708b0e69c4e97e…` | original |
| 9 | `m8/grammar.py` | m8-source | 6321 | `df26d22d8d97c02f…` | original |
| 10 | `m8/parser.py` | m8-source | 30216 | `7728b2882a5ee154…` | original |
| 11 | `m8/resolve.py` | m8-source | 7428 | `a4b29048a580498e…` | original |
| 12 | `m8/typecheck.py` | m8-source | 36470 | `ff280999176918aa…` | original |
| 13 | `m8/canonical.py` | m8-source | 13480 | `af9a82bf81e72737…` | original |
| 14 | `m8/cli.py` | m8-source | 5930 | `000732a10a61903e…` | original |
| 15 | `m8/README.md` | m8-source | 3896 | `772d0993a3782e1f…` | original |
| 16 | `m8/tests/__init__.py` | m8-test | 1556 | `671207b454c364a3…` | original |
| 17 | `m8/tests/test_canonical.py` | m8-test | 4807 | `f7a1ed6a7c01b062…` | original |
| 18 | `m8/tests/test_grammar_conformance.py` | m8-test | 1326 | `c6cda78f566b582f…` | original |
| 19 | `m8/runs/2026-10-09-m8-build.md` | m8-run-record | 2739 | `8bdf657b670e07b3…` | original |
| 20 | `m8/runs/phase0-capability-probe.md` | m8-run-record | 1694 | `49e820fca06a3ff2…` | original |
| 21 | `m8/corpus/manifest.json` | m8-corpus-manifest | 3920 | `6e9b0cfc2fac77d9…` | original |
| 22 | `m8/corpus/gen_corpus.py` | m8-corpus-generator | 6589 | `abb752f4f025e00a…` | generated |
| 23 | `m8/corpus/arith-div-int-exact.msve` | m8-corpus-case | 176 | `16835fce950231cb…` | original |
| 24 | `m8/corpus/arith-mixed-real-nat.msve` | m8-corpus-case | 180 | `45d99dd2f2b84681…` | original |
| 25 | `m8/corpus/arith-nat-int-embed.msve` | m8-corpus-case | 177 | `ed3f28f2faaf8e69…` | original |
| 26 | `m8/corpus/arith-neg3-plus2.msve` | m8-corpus-case | 174 | `b5098e87e7126a79…` | original |
| 27 | `m8/corpus/arith-unary-minus-nat.msve` | m8-corpus-case | 175 | `866adefd32bbce85…` | original |
| 28 | `m8/corpus/bare-quantifier.msve` | m8-corpus-case | 198 | `fde406385f5b510a…` | original |
| 29 | `m8/corpus/call-local-fn.msve` | m8-corpus-case | 245 | `4d4b6de3545ecedd…` | original |
| 30 | `m8/corpus/case-ok.msve` | m8-corpus-case | 203 | `57327cb0b536fa4d…` | original |
| 31 | `m8/corpus/define-shadow-builtin.msve` | m8-corpus-case | 179 | `a886a3939b0bdc45…` | original |
| 32 | `m8/corpus/f64-neg-zero-exp.msve` | m8-corpus-case | 193 | `d4086b4a418d34e0…` | original |
| 33 | `m8/corpus/f64-normal-form-subnormal.msve` | m8-corpus-case | 205 | `d4e9da4a39bb223b…` | original |
| 34 | `m8/corpus/f64-subtraction-no-spaces.msve` | m8-corpus-case | 226 | `d27bc859be0de5a6…` | original |
| 35 | `m8/corpus/f64-upper-hex.msve` | m8-corpus-case | 190 | `34fb34d7579ba7a5…` | original |
| 36 | `m8/corpus/f64-valid.msve` | m8-corpus-case | 186 | `be3a0be79268d710…` | original |
| 37 | `m8/corpus/is_some-ok.msve` | m8-corpus-case | 179 | `46429699d75f8feb…` | original |
| 38 | `m8/corpus/let-ok.msve` | m8-corpus-case | 176 | `4293e41c321e8cc4…` | original |
| 39 | `m8/corpus/limits-steps-zero.msve` | m8-corpus-case | 165 | `f335778d3a710073…` | original |
| 40 | `m8/corpus/limits-timeout-range.msve` | m8-corpus-case | 160 | `1589216d5d75c8b4…` | original |
| 41 | `m8/corpus/proj-path-unresolvable.msve` | m8-corpus-case | 290 | `39fd319917333ddf…` | original |
| 42 | `m8/corpus/quant-nested-ok.msve` | m8-corpus-case | 232 | `6a90e918e0b7c9be…` | original |
| 43 | `m8/corpus/quant-option-domain.msve` | m8-corpus-case | 231 | `0ddd766a3bb72654…` | original |
| 44 | `m8/corpus/quant-parens-ok.msve` | m8-corpus-case | 200 | `76f730bf000712f0…` | original |
| 45 | `m8/corpus/range-ok.msve` | m8-corpus-case | 171 | `835e7931bff35183…` | original |
| 46 | `m8/corpus/record-dup-field.msve` | m8-corpus-case | 214 | `81de72a6563605a9…` | original |
| 47 | `m8/corpus/record-field-type-mismatch.msve` | m8-corpus-case | 227 | `40151e4d734a6e4c…` | original |
| 48 | `m8/corpus/record-infer.msve` | m8-corpus-case | 175 | `90664295714b6c56…` | original |
| 49 | `m8/corpus/record-missing-field.msve` | m8-corpus-case | 212 | `1c88a6801188da51…` | original |
| 50 | `m8/corpus/record-nested.msve` | m8-corpus-case | 258 | `abc86bff4f4f57f7…` | original |
| 51 | `m8/corpus/record-ok.msve` | m8-corpus-case | 207 | `ebc4558753174eb1…` | original |
| 52 | `m8/corpus/record-unknown-field.msve` | m8-corpus-case | 224 | `6a24a88bdaeea390…` | original |
| 53 | `m8/corpus/string-escape-not-short.msve` | m8-corpus-case | 186 | `bc14176513025946…` | original |
| 54 | `m8/corpus/string-escape-upper.msve` | m8-corpus-case | 182 | `c5f6552400dc6e93…` | original |
| 55 | `m8/corpus/string-ok.msve` | m8-corpus-case | 170 | `aa57490912265281…` | original |
| 56 | `m8/corpus/to_rat-ok.msve` | m8-corpus-case | 172 | `7c0f0199ce55cc6a…` | original |
| 57 | `m8/corpus/type-cyclic-alias.msve` | m8-corpus-case | 177 | `5950a0f48ebb47b3…` | original |
| 58 | `m8/corpus/type-unbound-name.msve` | m8-corpus-case | 183 | `d919d3a852ef3b87…` | original |
| 59 | `m8/corpus/unbound-ident.msve` | m8-corpus-case | 179 | `caf261e05e502134…` | original |
| 60 | `m8/corpus/v07-ex0.msve` | m8-corpus-case | 246 | `ef4745e1977fd7b9…` | original |
| 61 | `m8/corpus/v07-ex1.msve` | m8-corpus-case | 324 | `81c16982016c39d1…` | original |
| 62 | `m8/corpus/v07-ex2.msve` | m8-corpus-case | 327 | `58d4b9c90ab46751…` | original |
| 63 | `m8/corpus/v07-ex3.msve` | m8-corpus-case | 1409 | `a8490f13a3276d7e…` | original |
| 64 | `m8/corpus/v07-ex4.msve` | m8-corpus-case | 371 | `6b6b922ce66d9d6e…` | original |
| 65 | `m8/corpus/v07-ex5.msve` | m8-corpus-case | 2334 | `561b2d4d8802671a…` | original |
| 66 | `m8/corpus/v08/inv-bare-quant.msve` | m8-corpus-case | 216 | `1d81cea39c930f54…` | original |
| 67 | `m8/corpus/v08/inv-f64-negzero.msve` | m8-corpus-case | 212 | `13c6f20d48d42498…` | original |
| 68 | `m8/corpus/v08/inv-mixed-arith.msve` | m8-corpus-case | 192 | `961edd0488022dc3…` | original |
| 69 | `m8/corpus/v08/inv-proof-conflict.msve` | m8-corpus-case | 229 | `8117f902102629d4…` | original |
| 70 | `m8/corpus/v08/inv-unbound.msve` | m8-corpus-case | 205 | `2db5a8b38091c620…` | original |
| 71 | `m8/corpus/v08/v08-ex0.msve` | m8-corpus-case | 246 | `ee00d8589dec21f2…` | original |
| 72 | `m8/corpus/v08/v08-ex1.msve` | m8-corpus-case | 324 | `3baf22938deb3b09…` | original |
| 73 | `m8/corpus/v08/v08-ex2.msve` | m8-corpus-case | 327 | `608e97689fc650ef…` | original |
| 74 | `m8/corpus/v08/v08-ex3.msve` | m8-corpus-case | 1406 | `42abbf513beae79f…` | original |
| 75 | `m8/corpus/v08/v08-ex4.msve` | m8-corpus-case | 371 | `7dada2f68a7da482…` | original |
| 76 | `m8/corpus/v08/v08-ex5.msve` | m8-corpus-case | 2420 | `f285f44e59f2ad16…` | original |
| 77 | `m8/corpus/verif-assurance-level-a-needs-proof.msve` | m8-corpus-case | 200 | `3ee6d939a26bd48f…` | original |
| 78 | `m8/corpus/verif-assurance-level-a-unavailable.msve` | m8-corpus-case | 342 | `6861aacd4af3bd82…` | original |
| 79 | `m8/corpus/verif-cases-zero.msve` | m8-corpus-case | 207 | `c341436d8bd572cc…` | original |
| 80 | `m8/corpus/verif-diff-plus-fuzz.msve` | m8-corpus-case | 263 | `18e9ab0742650f06…` | original |
| 81 | `m8/corpus/verif-duplicate-test.msve` | m8-corpus-case | 256 | `e6f1eabd5612a45e…` | original |
| 82 | `m8/corpus/verif-proof-conflict.msve` | m8-corpus-case | 209 | `2e079927528f2b6a…` | original |
| 83 | `m8/corpus/verif-qualifier-default.msve` | m8-corpus-case | 188 | `5f81757c93cf2b7f…` | original |
| 84 | `m8/corpus/verif-recompute-conflict.msve` | m8-corpus-case | 212 | `a1fd871f37084a7e…` | original |
| 85 | `m8/corpus/verif-test-none-conflict.msve` | m8-corpus-case | 223 | `3e5a0f59ba93125d…` | original |
| 86 | `owner-review/reviewer-reports/reviewer-A-grammar-type-system.md` | reviewer-report | 16710 | `6b0ba84a054b5c16…` | derived (extracted from sub-agent session records) |
| 87 | `owner-review/reviewer-reports/reviewer-B-canonical-numerics.md` | reviewer-report | 13127 | `ae19e969e2bcff4e…` | derived (extracted from sub-agent session records) |
| 88 | `owner-review/reviewer-reports/reviewer-C-validator-contracts.md` | reviewer-report | 14527 | `492e5abec293c028…` | derived (extracted from sub-agent session records) |
| 89 | `owner-review/reviewer-reports/reviewer-D-cross-document.md` | reviewer-report | 7608 | `7fd0b96a44b55f8f…` | derived (extracted from sub-agent session records) |
| 90 | `owner-review/reviewer-reports/PROVENANCE.md` | provenance-note | 1855 | `64cf27bb19f2da2a…` | generated |
| 91 | `owner-review/logs/corpus.log` | execution-log | 1592 | `ec4ac2624e57e80e…` | generated (reproduced 2026-10-09) |
| 92 | `owner-review/logs/spec-examples.log` | execution-log | 397 | `71198002aec6944f…` | generated (reproduced 2026-10-09) |
| 93 | `owner-review/logs/grammar-conformance.log` | execution-log | 130 | `e8a81a50f38b57ed…` | generated (reproduced 2026-10-09) |
| 94 | `owner-review/logs/test-canonical.log` | execution-log | 71 | `3e169d871d00846c…` | generated (reproduced 2026-10-09) |
| 95 | `owner-review/logs/test-grammar-conformance.log` | execution-log | 89 | `54b43e44e1478489…` | generated (reproduced 2026-10-09) |
| 96 | `owner-review/logs/corpus-per-case.json` | execution-log | 6960 | `cb89116b75f0d3fd…` | generated (reproduced 2026-10-09) |
| 97 | `owner-review/logs/runtime.txt` | execution-log | 196 | `30927729f2ef9c8a…` | generated (reproduced 2026-10-09) |
| 98 | `owner-review/MSVE_v0.8_OWNER_REVIEW_MANIFEST.md` | manifest | 10713 | (this file; hash in JSON) | generated (Work Order 0.8.1) |
| 99 | `owner-review/MSVE_v0.8_READINESS_EVIDENCE_MATRIX.md` | evidence-matrix | 10060 | `c7ae4fdfad4568e0…` | generated (Work Order 0.8.1) |
| 100 | `owner-review/MSVE_v0.8_DEFECT_TRACEABILITY.md` | traceability | 7805 | `bce08e419d38d354…` | generated (Work Order 0.8.1) |
| 101 | `owner-review/MSVE_v0.8_OWNER_REVIEW_HANDOFF.md` | handoff | 3421 | `2489fcddcf6299cc…` | generated (Work Order 0.8.1) |

Full digests in the JSON manifest.
