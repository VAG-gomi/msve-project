# Report A — MSVE v0.8 Transfer Index

**Work Order:** 0.8.2 · **Date:** 2026-10-09
**Evidence discipline:** DIRECT ARTEFACT = read from the ZIP by the transfer agent.

## 1. Archive identity (DIRECT ARTEFACT)

- **Path:** `~/workspace/msve-design/MSVE_v0.8_OWNER_REVIEW_BUNDLE.zip`
- **SHA-256:** `8db37d26ed589722d8a6184b8613d1d2423745c5b346b9dd9430adc4dcf20aee`
  (recomputed 2026-10-09 during Work Order 0.8.2 inspection; matches the 0.8.1 record)
- **File count:** 111 files (per `unzip -l`)
- **Top-level layout:** `six-docs/` · `m8/` · `owner-review/`

## 2. Manifest transcription (DIRECT ARTEFACT)

Transcribed from `owner-review/MSVE_v0.8_OWNER_REVIEW_MANIFEST.json` (101 entries).
Hashes below are the manifest's recorded values, reproduced here — reproducing a
hash in Markdown does **not** independently verify the file's bytes.

**Path-prefix note (INFERENCE):** the manifest records workspace-relative paths
(e.g. `MSVE_DESIGN_SPEC_v0.8.md`); inside the ZIP the six documents live under
`six-docs/`. All six hashes were re-verified against the `six-docs/` copies during
0.8.2 inspection: 6/6 MATCH.

### 1. `MSVE_DESIGN_SPEC_v0.8.md`
- Type: design-document · Purpose: normative specification
- Bytes: 75861 · SHA-256: `377e106ef2b00db648c18beeed798bcf91804f1cbe3813853a62c1385474715d`
- Provenance: original · Version: 0.8
### 2. `MSVE_DESIGN_REVIEW_v0.8.md`
- Type: design-document · Purpose: review record and gate decision
- Bytes: 11050 · SHA-256: `d5650027ba245e0c9c6d688960e1322a465527945624fc713d7c5879d7814949`
- Provenance: original · Version: 0.8
### 3. `MSVE_CAPABILITY_MATRIX_v0.8.md`
- Type: design-document · Purpose: capability claims
- Bytes: 2004 · SHA-256: `542fa10cd3a8cee9e5920342f971137c166cad8f0dedd923da2627cfcb420b27`
- Provenance: original · Version: 0.8
### 4. `MSVE_ACCEPTANCE_PLAN_v0.8.md`
- Type: design-document · Purpose: acceptance procedure
- Bytes: 8848 · SHA-256: `8ee1c526f135cce7615612777859859fa3426bc8f281cdaf8b829f73cf490856`
- Provenance: original · Version: 0.8
### 5. `MSVE_VISUALISATION_PLAN_v0.8.md`
- Type: design-document · Purpose: diagrams
- Bytes: 6610 · SHA-256: `3adaf96661df8cbbbbd931b1c23b95a6348236c3a3087725a23b6b617f751615`
- Provenance: original · Version: 0.8
### 6. `MSVE_REGRESSION_LEDGER_v0.8.md`
- Type: design-document · Purpose: defect history
- Bytes: 34625 · SHA-256: `e04a05e68e92ce541349138395a42308d172998b2fd309fe2963ede6cdf22bf1`
- Provenance: original · Version: 0.8
### 7. `m8/__init__.py`
- Type: m8-source · Purpose: audit tool implementation
- Bytes: 67 · SHA-256: `5112fc6e78b2210dd05786169172e4b917f2d1e8457e41699d70cc4c3a0a859b`
- Provenance: original · Version: 0.8
### 8. `m8/lexer.py`
- Type: m8-source · Purpose: audit tool implementation
- Bytes: 6375 · SHA-256: `ef708b0e69c4e97e29221984f3be690463c22619d1e5d28225cf01d2cfbea3b2`
- Provenance: original · Version: 0.8
### 9. `m8/grammar.py`
- Type: m8-source · Purpose: audit tool implementation
- Bytes: 6321 · SHA-256: `df26d22d8d97c02f2bbd7cc2655b94eb3f1a9bf9d233fcc31b687fb34e814336`
- Provenance: original · Version: 0.8
### 10. `m8/parser.py`
- Type: m8-source · Purpose: audit tool implementation
- Bytes: 30216 · SHA-256: `7728b2882a5ee154fc3011a26a7e3c78bb03aadf4beb543cda36e54238a22a1f`
- Provenance: original · Version: 0.8
### 11. `m8/resolve.py`
- Type: m8-source · Purpose: audit tool implementation
- Bytes: 7428 · SHA-256: `a4b29048a580498e41b5e299adec518f2923e2122b9584b0a5e2849300c9a813`
- Provenance: original · Version: 0.8
### 12. `m8/typecheck.py`
- Type: m8-source · Purpose: audit tool implementation
- Bytes: 36470 · SHA-256: `ff280999176918aa0366b7a391636835da80721702300e1bddd8d6706711f975`
- Provenance: original · Version: 0.8
### 13. `m8/canonical.py`
- Type: m8-source · Purpose: audit tool implementation
- Bytes: 13480 · SHA-256: `af9a82bf81e72737f1245c272a7f3f342e3453765d858f699ed3cb6dce995349`
- Provenance: original · Version: 0.8
### 14. `m8/cli.py`
- Type: m8-source · Purpose: audit tool implementation
- Bytes: 5930 · SHA-256: `000732a10a61903e0173efd10c098a78958c4bdebeedeacef26eb8f1b193e4ec`
- Provenance: original · Version: 0.8
### 15. `m8/README.md`
- Type: m8-source · Purpose: audit tool implementation
- Bytes: 3896 · SHA-256: `772d0993a3782e1fc7a386eb5e787afd708265815cd5e63346f08aafbe71f7ad`
- Provenance: original · Version: 0.8
### 16. `m8/tests/__init__.py`
- Type: m8-test · Purpose: audit tool tests
- Bytes: 1556 · SHA-256: `671207b454c364a330090bef92fa92bf28eb83f053670499e1d85c2068ad0c6c`
- Provenance: original · Version: 0.8
### 17. `m8/tests/test_canonical.py`
- Type: m8-test · Purpose: audit tool tests
- Bytes: 4807 · SHA-256: `f7a1ed6a7c01b0627b559bc152d5e3c5bb3e4deffc926d4803dea0179f272c3b`
- Provenance: original · Version: 0.8
### 18. `m8/tests/test_grammar_conformance.py`
- Type: m8-test · Purpose: audit tool tests
- Bytes: 1326 · SHA-256: `c6cda78f566b582f6d4d1675821ee3771c7e7f5a1627dd00a02d7016af03f0d3`
- Provenance: original · Version: 0.8
### 19. `m8/runs/2026-10-09-m8-build.md`
- Type: m8-run-record · Purpose: contemporaneous build/probe record
- Bytes: 2739 · SHA-256: `8bdf657b670e07b33a32687cc82af46056627814ed3439a55aa2c5974789df92`
- Provenance: original · Version: 0.8
### 20. `m8/runs/phase0-capability-probe.md`
- Type: m8-run-record · Purpose: contemporaneous build/probe record
- Bytes: 1694 · SHA-256: `49e820fca06a3ff262fb277fde47d2b098ce98a349fb5e6968a97f7df272d004`
- Provenance: original · Version: 0.8
### 21. `m8/corpus/manifest.json`
- Type: m8-corpus-manifest · Purpose: 46-case index
- Bytes: 3920 · SHA-256: `6e9b0cfc2fac77d91d67f282a29716e04e33d9e44efbf306761ae44bce18249c`
- Provenance: original · Version: 0.8
### 22. `m8/corpus/gen_corpus.py`
- Type: m8-corpus-generator · Purpose: corpus generation script
- Bytes: 6589 · SHA-256: `abb752f4f025e00aa079a5b630a9800329accc3a36f5908457916b493f62d0b4`
- Provenance: generated · Version: 0.8
### 23. `m8/corpus/arith-div-int-exact.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 176 · SHA-256: `16835fce950231cb9591a24a6842ad7bdd0df426f12e5a08116ea1964961da96`
- Provenance: original · Version: 0.8
### 24. `m8/corpus/arith-mixed-real-nat.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 180 · SHA-256: `45d99dd2f2b846816a465f9bcc79f7b70d39061fcc181b322a4ddb21106fb7a1`
- Provenance: original · Version: 0.8
### 25. `m8/corpus/arith-nat-int-embed.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 177 · SHA-256: `ed3f28f2faaf8e691742dbde2a9566a2241845eb7339044040a1b3cea4b4783d`
- Provenance: original · Version: 0.8
### 26. `m8/corpus/arith-neg3-plus2.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 174 · SHA-256: `b5098e87e7126a798833494b86f66296192ec1f846bff2174783cb448b7b5d51`
- Provenance: original · Version: 0.8
### 27. `m8/corpus/arith-unary-minus-nat.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 175 · SHA-256: `866adefd32bbce859d0fa8e024c5453dfa6fdf7c156389371f1708acc90b946f`
- Provenance: original · Version: 0.8
### 28. `m8/corpus/bare-quantifier.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 198 · SHA-256: `fde406385f5b510aa39c5fcade88065176df19fb265837947062658173ae71b9`
- Provenance: original · Version: 0.8
### 29. `m8/corpus/call-local-fn.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 245 · SHA-256: `4d4b6de3545eceddebc1fa4c0ae812815ecb72f9392ed1064f853dc1682582cd`
- Provenance: original · Version: 0.8
### 30. `m8/corpus/case-ok.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 203 · SHA-256: `57327cb0b536fa4d6f1e71fd59216de8a104472bfd9ec959f9798d9fc03272cf`
- Provenance: original · Version: 0.8
### 31. `m8/corpus/define-shadow-builtin.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 179 · SHA-256: `a886a3939b0bdc452c080fde0adf01e9cf5bacdc2974e719dcc4970abacc32d7`
- Provenance: original · Version: 0.8
### 32. `m8/corpus/f64-neg-zero-exp.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 193 · SHA-256: `d4086b4a418d34e0c583929f71e686fa2751415b8e00d95dc2d60d5b6e52a2d3`
- Provenance: original · Version: 0.8
### 33. `m8/corpus/f64-normal-form-subnormal.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 205 · SHA-256: `d4e9da4a39bb223b4c693ed4fe9887dd7577629001a698dd7b131c7748990241`
- Provenance: original · Version: 0.8
### 34. `m8/corpus/f64-subtraction-no-spaces.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 226 · SHA-256: `d27bc859be0de5a68ce90195b3aa1549a9413e8e96324c0612c52df16d9f8870`
- Provenance: original · Version: 0.8
### 35. `m8/corpus/f64-upper-hex.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 190 · SHA-256: `34fb34d7579ba7a5ef3b3289db7f5226c9ab4207cd2dbc4cf8ac4c67b5f1cb16`
- Provenance: original · Version: 0.8
### 36. `m8/corpus/f64-valid.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 186 · SHA-256: `be3a0be79268d710d2e520dc854cb082989ab3edc3e574bbede3c76b3f0b6c2e`
- Provenance: original · Version: 0.8
### 37. `m8/corpus/is_some-ok.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 179 · SHA-256: `46429699d75f8feb039fd6df001713098626dc4fe0347d2cba7a4cc4817f0cdc`
- Provenance: original · Version: 0.8
### 38. `m8/corpus/let-ok.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 176 · SHA-256: `4293e41c321e8cc4330fe7a38b7d7a784fb87e241b2eeddcf5017f1f2fddb7b4`
- Provenance: original · Version: 0.8
### 39. `m8/corpus/limits-steps-zero.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 165 · SHA-256: `f335778d3a710073fbc05af36f9a0971a187172a37aeef6d8a9e29f297c6ae95`
- Provenance: original · Version: 0.8
### 40. `m8/corpus/limits-timeout-range.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 160 · SHA-256: `1589216d5d75c8b4d5cafb3dbca9daf93b5545aeb4a058d4e1b19908e0a00229`
- Provenance: original · Version: 0.8
### 41. `m8/corpus/proj-path-unresolvable.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 290 · SHA-256: `39fd319917333ddf4e9d8a45c4485774c7cd7d7d94e7144a5a19fee8ba0f7966`
- Provenance: original · Version: 0.8
### 42. `m8/corpus/quant-nested-ok.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 232 · SHA-256: `6a90e918e0b7c9beb72213d8fc959e4b580b81585076b658ac44040e23eb6789`
- Provenance: original · Version: 0.8
### 43. `m8/corpus/quant-option-domain.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 231 · SHA-256: `0ddd766a3bb726547bb938f0cee6415a02ee0449f5f3c500ad1a107d99a0185f`
- Provenance: original · Version: 0.8
### 44. `m8/corpus/quant-parens-ok.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 200 · SHA-256: `76f730bf000712f06369478e2b297e559cc3697fa0daec8ebe844ce1e13eebcd`
- Provenance: original · Version: 0.8
### 45. `m8/corpus/range-ok.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 171 · SHA-256: `835e7931bff351834e043865d5f074a293c28b1217b1d2586faaa3b51202d75d`
- Provenance: original · Version: 0.8
### 46. `m8/corpus/record-dup-field.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 214 · SHA-256: `81de72a6563605a9eda206246e55d318d1982a9fbc5bc1465ce570f6dc5f002e`
- Provenance: original · Version: 0.8
### 47. `m8/corpus/record-field-type-mismatch.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 227 · SHA-256: `40151e4d734a6e4cd9092845c5828ef01a39ea546018081323bebf4e587c482a`
- Provenance: original · Version: 0.8
### 48. `m8/corpus/record-infer.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 175 · SHA-256: `90664295714b6c561a25be47b4dcdb8529e1110dca2b6b0dbb02ee1be90ddcb0`
- Provenance: original · Version: 0.8
### 49. `m8/corpus/record-missing-field.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 212 · SHA-256: `1c88a6801188da519029515da86e08232f89c3543f2f141d7297be43ea796bfe`
- Provenance: original · Version: 0.8
### 50. `m8/corpus/record-nested.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 258 · SHA-256: `abc86bff4f4f57f7e1e6818c090cf6016401fb18e2bd21a8dc1eed1be98b5880`
- Provenance: original · Version: 0.8
### 51. `m8/corpus/record-ok.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 207 · SHA-256: `ebc4558753174eb1b42f45e75424df12950696b6e4e995f9be470550f4f21428`
- Provenance: original · Version: 0.8
### 52. `m8/corpus/record-unknown-field.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 224 · SHA-256: `6a24a88bdaeea39060dbb52b8760a9faffa95634d94bf81d56ab94fc91fc9f14`
- Provenance: original · Version: 0.8
### 53. `m8/corpus/string-escape-not-short.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 186 · SHA-256: `bc14176513025946cd527e1db4d1b21bb2c6fb9fdb7dee9dd3248901c045c756`
- Provenance: original · Version: 0.8
### 54. `m8/corpus/string-escape-upper.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 182 · SHA-256: `c5f6552400dc6e9330cbed014fadd1d3da9d690307692dcdc1cb412ecf861dee`
- Provenance: original · Version: 0.8
### 55. `m8/corpus/string-ok.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 170 · SHA-256: `aa5749091226528167384ccf213304a4f00d942180c30933699b7f21e009e154`
- Provenance: original · Version: 0.8
### 56. `m8/corpus/to_rat-ok.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 172 · SHA-256: `7c0f0199ce55cc6a15f69dbbd6fd1b0a0c3eb3c3438d5b84e2b358fcb8379fb2`
- Provenance: original · Version: 0.8
### 57. `m8/corpus/type-cyclic-alias.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 177 · SHA-256: `5950a0f48ebb47b3c4b13407e6307654a9176b49f8036053e7ba3cfae14e947a`
- Provenance: original · Version: 0.8
### 58. `m8/corpus/type-unbound-name.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 183 · SHA-256: `d919d3a852ef3b87c43717b4af5cb33e4b0d9d94d7804fe3156b1fc35eda92eb`
- Provenance: original · Version: 0.8
### 59. `m8/corpus/unbound-ident.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 179 · SHA-256: `caf261e05e502134838c8a3f6bab12bf8d4c43cbeac1ae15e72c7dfd9e371221`
- Provenance: original · Version: 0.8
### 60. `m8/corpus/v07-ex0.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 246 · SHA-256: `ef4745e1977fd7b945cf5a040772c8773fb5823e4335d2e6b74a671245a59f40`
- Provenance: original · Version: 0.8
### 61. `m8/corpus/v07-ex1.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 324 · SHA-256: `81c16982016c39d1cf7a8d69b1d03aa03d7f7623b3b3ceb9020a30d5c07a257f`
- Provenance: original · Version: 0.8
### 62. `m8/corpus/v07-ex2.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 327 · SHA-256: `58d4b9c90ab46751c27a1bba460f9c3a38432f3dd6dda35cdd00d96bff724ca3`
- Provenance: original · Version: 0.8
### 63. `m8/corpus/v07-ex3.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 1409 · SHA-256: `a8490f13a3276d7ef177e37b8cde9ec259b679e69a846878e810b192291cddc0`
- Provenance: original · Version: 0.8
### 64. `m8/corpus/v07-ex4.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 371 · SHA-256: `6b6b922ce66d9d6e729b8e99da63f5893e48bc9854156aa406864f5e789b4a09`
- Provenance: original · Version: 0.8
### 65. `m8/corpus/v07-ex5.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 2334 · SHA-256: `561b2d4d8802671a4dc97751c7a34b74521062f27a1793bb53d55b00ac29f2d7`
- Provenance: original · Version: 0.8
### 66. `m8/corpus/v08/inv-bare-quant.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 216 · SHA-256: `1d81cea39c930f54a9373bce08f6ee19501de243ca9b7fc10b3d7acad5f950b2`
- Provenance: original · Version: 0.8
### 67. `m8/corpus/v08/inv-f64-negzero.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 212 · SHA-256: `13c6f20d48d424988a1e365ab0231901888a35bd2e8fb201c52e06d07cf31ff0`
- Provenance: original · Version: 0.8
### 68. `m8/corpus/v08/inv-mixed-arith.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 192 · SHA-256: `961edd0488022dc32857e4ebe0dae1afa1fefb13178ad19e61f059e5702ec689`
- Provenance: original · Version: 0.8
### 69. `m8/corpus/v08/inv-proof-conflict.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 229 · SHA-256: `8117f902102629d42dd58f72cb650338a4dfba2e7c2abe646dff1abfe858248d`
- Provenance: original · Version: 0.8
### 70. `m8/corpus/v08/inv-unbound.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 205 · SHA-256: `2db5a8b38091c6207026d9739e368acb8d0837864a748ca4be572b5f52a4785a`
- Provenance: original · Version: 0.8
### 71. `m8/corpus/v08/v08-ex0.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 246 · SHA-256: `ee00d8589dec21f233aff23670930b3b05bc2c753ffadf09e385396892b0c3cd`
- Provenance: original · Version: 0.8
### 72. `m8/corpus/v08/v08-ex1.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 324 · SHA-256: `3baf22938deb3b0957b9377367718b3a173e14142aabe2ae0532f5fb53cd06f5`
- Provenance: original · Version: 0.8
### 73. `m8/corpus/v08/v08-ex2.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 327 · SHA-256: `608e97689fc650effad75c604eafc26383eb6dd9319fd7fbd99d468aa31adce1`
- Provenance: original · Version: 0.8
### 74. `m8/corpus/v08/v08-ex3.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 1406 · SHA-256: `42abbf513beae79ff2087b41d5a53b30b7c5cd7a7e8e40a7a3a1171afcecb228`
- Provenance: original · Version: 0.8
### 75. `m8/corpus/v08/v08-ex4.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 371 · SHA-256: `7dada2f68a7da4827dd81db843b6efe271a30a3f4f7c705743ab686bc2edb55a`
- Provenance: original · Version: 0.8
### 76. `m8/corpus/v08/v08-ex5.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 2420 · SHA-256: `f285f44e59f2ad1635dc1bb546fae87cb4fa82ba866e8fdf7b6374f68f9b3c7b`
- Provenance: original · Version: 0.8
### 77. `m8/corpus/verif-assurance-level-a-needs-proof.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 200 · SHA-256: `3ee6d939a26bd48f42e5181d2cc48d155f249d0aa0a31845119e7ed87ba5d2a8`
- Provenance: original · Version: 0.8
### 78. `m8/corpus/verif-assurance-level-a-unavailable.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 342 · SHA-256: `6861aacd4af3bd82650c68fe0af5488bfa0d42ae05a4bb5176cb5a3018449778`
- Provenance: original · Version: 0.8
### 79. `m8/corpus/verif-cases-zero.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 207 · SHA-256: `c341436d8bd572cc5e86da40fcc2c06b3e56865930b33b252f1986a246b3594c`
- Provenance: original · Version: 0.8
### 80. `m8/corpus/verif-diff-plus-fuzz.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 263 · SHA-256: `18e9ab0742650f06c22448528ac28d3327c86c3367464ccbbf765c3a597031bc`
- Provenance: original · Version: 0.8
### 81. `m8/corpus/verif-duplicate-test.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 256 · SHA-256: `e6f1eabd5612a45e1800d11d7c3ace39fb6b7e899681e389364ff1eda1a7bd8e`
- Provenance: original · Version: 0.8
### 82. `m8/corpus/verif-proof-conflict.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 209 · SHA-256: `2e079927528f2b6aee46d7df41a827e5185d593c0b466b350d9efe42dcb9425f`
- Provenance: original · Version: 0.8
### 83. `m8/corpus/verif-qualifier-default.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 188 · SHA-256: `5f81757c93cf2b7f76fdaf851346657ec3ceab16d0e98e778ebe3878e6ef6c84`
- Provenance: original · Version: 0.8
### 84. `m8/corpus/verif-recompute-conflict.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 212 · SHA-256: `a1fd871f37084a7e1fa73f0478b0d8e020fee28e49eee884a97f5bf23c7fa021`
- Provenance: original · Version: 0.8
### 85. `m8/corpus/verif-test-none-conflict.msve`
- Type: m8-corpus-case · Purpose: regression test case
- Bytes: 223 · SHA-256: `3e5a0f59ba93125d48c48f9285897104545dcc246e2ab3ad9f0ce2bdf6ff1968`
- Provenance: original · Version: 0.8
### 86. `owner-review/reviewer-reports/reviewer-A-grammar-type-system.md`
- Type: reviewer-report · Purpose: original Reviewer A findings
- Bytes: 16710 · SHA-256: `6b0ba84a054b5c162a9ce21f8a732684da93be319bc2600ae1506100949277c3`
- Provenance: derived (extracted from sub-agent session records) · Version: 0.8
### 87. `owner-review/reviewer-reports/reviewer-B-canonical-numerics.md`
- Type: reviewer-report · Purpose: original Reviewer B findings
- Bytes: 13127 · SHA-256: `ae19e969e2bcff4e05c3228b4fc0b21c5a6648bb1e66f0fc51ab5108b63d282d`
- Provenance: derived (extracted from sub-agent session records) · Version: 0.8
### 88. `owner-review/reviewer-reports/reviewer-C-validator-contracts.md`
- Type: reviewer-report · Purpose: original Reviewer C findings
- Bytes: 14527 · SHA-256: `492e5abec293c0287678487f2bc813ed393684b0c0f7fd26f29d6052ab753cc5`
- Provenance: derived (extracted from sub-agent session records) · Version: 0.8
### 89. `owner-review/reviewer-reports/reviewer-D-cross-document.md`
- Type: reviewer-report · Purpose: original Reviewer D findings
- Bytes: 7608 · SHA-256: `7fd0b96a44b55f8f294df9f7144510c2a3d9481c11b56e0f188a31e327893ebb`
- Provenance: derived (extracted from sub-agent session records) · Version: 0.8
### 90. `owner-review/reviewer-reports/PROVENANCE.md`
- Type: provenance-note · Purpose: reviewer execution provenance
- Bytes: 1855 · SHA-256: `64cf27bb19f2da2aee92327f7a94fd9afb5641c21c38bc67ced6e3bdad05d2b3`
- Provenance: generated · Version: 0.8
### 91. `owner-review/logs/corpus.log`
- Type: execution-log · Purpose: reproduced check output
- Bytes: 1592 · SHA-256: `ec4ac2624e57e80e9db75968c30fa1f12b1c2b84c8c3bdd2dfb321f5338d8805`
- Provenance: generated (reproduced 2026-10-09) · Version: 0.8
### 92. `owner-review/logs/spec-examples.log`
- Type: execution-log · Purpose: reproduced check output
- Bytes: 397 · SHA-256: `71198002aec6944fb7c71d835384a8911ecf5c68b314af92615b6b4bae7e12b3`
- Provenance: generated (reproduced 2026-10-09) · Version: 0.8
### 93. `owner-review/logs/grammar-conformance.log`
- Type: execution-log · Purpose: reproduced check output
- Bytes: 130 · SHA-256: `e8a81a50f38b57ed706baa536e40db1a2c21f14fb1e1b560ffad91521c1f947a`
- Provenance: generated (reproduced 2026-10-09) · Version: 0.8
### 94. `owner-review/logs/test-canonical.log`
- Type: execution-log · Purpose: reproduced check output
- Bytes: 71 · SHA-256: `3e169d871d00846cb3ab67c210df87141b063a4a9f078511be342198276ba175`
- Provenance: generated (reproduced 2026-10-09) · Version: 0.8
### 95. `owner-review/logs/test-grammar-conformance.log`
- Type: execution-log · Purpose: reproduced check output
- Bytes: 89 · SHA-256: `54b43e44e147848997ff8dd00e95b9ef60a6ab2a54f6ef4662716ae9ed4a13fc`
- Provenance: generated (reproduced 2026-10-09) · Version: 0.8
### 96. `owner-review/logs/corpus-per-case.json`
- Type: execution-log · Purpose: reproduced check output
- Bytes: 6960 · SHA-256: `cb89116b75f0d3fd28025c8e21d76a49e6aab5b4bd52cc1d524a0e5ee7384379`
- Provenance: generated (reproduced 2026-10-09) · Version: 0.8
### 97. `owner-review/logs/runtime.txt`
- Type: execution-log · Purpose: reproduced check output
- Bytes: 196 · SHA-256: `30927729f2ef9c8a8afc4be0a67959c2c4cf1b89d2221946034b111d824b5434`
- Provenance: generated (reproduced 2026-10-09) · Version: 0.8
### 98. `owner-review/MSVE_v0.8_OWNER_REVIEW_MANIFEST.md`
- Type: manifest · Purpose: human-readable manifest
- Bytes: 10713 · SHA-256: `454dfee046f168bba786b8a21a43867f63a65181f43945991b51efcade418061`
- Provenance: generated (Work Order 0.8.1) · Version: 0.8
### 99. `owner-review/MSVE_v0.8_READINESS_EVIDENCE_MATRIX.md`
- Type: evidence-matrix · Purpose: Deliverable D
- Bytes: 10060 · SHA-256: `c7ae4fdfad4568e0f142156906369c34242dc67df94f9df3a8ffe542a4a9840e`
- Provenance: generated (Work Order 0.8.1) · Version: 0.8
### 100. `owner-review/MSVE_v0.8_DEFECT_TRACEABILITY.md`
- Type: traceability · Purpose: Deliverable E
- Bytes: 7805 · SHA-256: `bce08e419d38d354bfb61aeb916ea60f8a0fd3a3532bea6190d2ac81477b3b4a`
- Provenance: generated (Work Order 0.8.1) · Version: 0.8
### 101. `owner-review/MSVE_v0.8_OWNER_REVIEW_HANDOFF.md`
- Type: handoff · Purpose: Deliverable F
- Bytes: 3421 · SHA-256: `2489fcddcf6299cc6647e9df7ffd1efa163ced6baf9ccc7206015574a971cc97`
- Provenance: generated (Work Order 0.8.1) · Version: 0.8

## 3. What was read directly vs copied

- **Read directly from the archive (DIRECT ARTEFACT):** ZIP hash, file count,
  directory layout, manifest JSON contents, the six `six-docs/` hashes re-verified above.
- **Copied from existing reports (REPORT CLAIM):** per-artefact purposes, provenance
  labels, and version identifiers as recorded in the 0.8.1 manifest.

## 4. Six design documents (DIRECT ARTEFACT)

- `six-docs/MSVE_DESIGN_SPEC_v0.8.md` — sha256 `377e106ef2b00db6…` (first 16 chars; full in manifest)
- `six-docs/MSVE_DESIGN_REVIEW_v0.8.md` — sha256 `d5650027ba245e0c9…` (first 16 chars; full in manifest)
- `six-docs/MSVE_CAPABILITY_MATRIX_v0.8.md` — sha256 `542fa10cd3a8cee9…` (first 16 chars; full in manifest)
- `six-docs/MSVE_ACCEPTANCE_PLAN_v0.8.md` — sha256 `8ee1c526f135cce7…` (first 16 chars; full in manifest)
- `six-docs/MSVE_VISUALISATION_PLAN_v0.8.md` — sha256 `3adaf96661df8cbb…` (first 16 chars; full in manifest)
- `six-docs/MSVE_REGRESSION_LEDGER_v0.8.md` — sha256 `e04a05e68e92ce54…` (first 16 chars; full in manifest)

**Byte-identity claim (REPORT CLAIM, verified in 0.8.1 and spot-verified in 0.8.2):**
the `six-docs/` copies are byte-identical to the workspace originals hashed at
0.8.1 collection time. Re-verified 6/6 during 0.8.2 inspection.

## 5. Anomalies

- **Manifest/ZIP path-prefix discrepancy (INFERENCE):** manifest paths omit the
  `six-docs/` prefix used inside the ZIP. Hashes match; no content discrepancy.
- **`BUNDLE_CHECKSUM.txt` absent from the ZIP:** the checksum file was written to
  `owner-review/` after the ZIP was created. The ZIP hash above is the authority.
- **No missing, unreadable, or duplicated artefacts found** among the 101 manifest
  entries during 0.8.2 inspection.
- **Unverifiable from the ZIP alone:** whether the manifest's *provenance* labels
  (original/generated/derived) are accurate — these are REPORT CLAIMs from 0.8.1.
