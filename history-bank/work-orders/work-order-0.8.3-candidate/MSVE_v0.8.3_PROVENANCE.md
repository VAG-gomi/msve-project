# Work Order 0.8.3 — Candidate Source Provenance (F-19)

**Date:** 2026-10-09
**Historical limitation (F-19):** the v0.8 reviewer reports (A–D) record
agent/session origins but do not cryptographically anchor the exact
specification bytes each reviewer inspected. No source hash is invented
or backdated here. Historical reviewer conclusions remain distinct from
verification of this corrected candidate.

**New-review anchoring:** every correction in this candidate was made
against the source hashes below. Each F-01–F-19 disposition links to
these hashes.

## Candidate source hashes (SHA-256)

- `MSVE_ACCEPTANCE_PLAN_v0.8.md` — 8935 bytes — `92b234d20f67c10bf74e1f4781dc1dc3214b9530a3eca006ee033a0fc6d8b2d3`
- `MSVE_CAPABILITY_MATRIX_v0.8.md` — 2022 bytes — `28838a24eeae5a81557a86fb3c6beb64e32fb17e27e32aeaea94a017a7691d2f`
- `MSVE_DESIGN_REVIEW_v0.8.md` — 11156 bytes — `d7be8c8db1c1e2f1db73efac8287ec3545c2390829f8c43f008fa46093671015`
- `MSVE_DESIGN_SPEC_v0.8.md` — 83036 bytes — `9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003`
- `MSVE_REGRESSION_LEDGER_v0.8.md` — 34625 bytes — `e04a05e68e92ce541349138395a42308d172998b2fd309fe2963ede6cdf22bf1`
- `MSVE_VISUALISATION_PLAN_v0.8.md` — 6697 bytes — `fb03b6098aecb6b98ca31cf0c9eac092620075480c59def0602f122c449e28dd`
- `MSVE_v0.8.3_CORRECTION_REPORT.md` — 3780 bytes — `49a498e23fda17608876fa03209ce3aac9a90ac5ef46ba2a57e27e7b706aa633`
- `MSVE_v0.8.3_CROSS_DOCUMENT_MATRIX.md` — 2626 bytes — `1cff2f14b7e9699329b784b8959e82eb7cd164e5d119d8c6874d07dc67d0717d`
- `MSVE_v0.8.3_OWNER_HANDOFF.md` — 1838 bytes — `2928b424bbf06c065b848e8085cd083bc0549516b4d25f8cc6b6958153d578ce`
- `MSVE_v0.8.3_RESIDUAL_DEFECT_LEDGER.md` — 3033 bytes — `b3947543bb4245786e550f2743f18e7046236b1fdab0d10ece01efe21d0494d8`
- `MSVE_v0.8.3_VERIFICATION_EVIDENCE.md` — 2988 bytes — `631d0f1e3f3d3e0c127abcaa6c59c715ebb0e4b2c16a720d5a4f364219183457`
- `MSVE_v0.8_DEFECT_TRACEABILITY.md` — 7805 bytes — `bce08e419d38d354bfb61aeb916ea60f8a0fd3a3532bea6190d2ac81477b3b4a`
- `MSVE_v0.8_READINESS_EVIDENCE_MATRIX.md` — 11367 bytes — `608e2c89e03bb1ba13c873a957f34153d1aee597ad1cce021640ac4d15ec077f`
- `m8-candidate/README.md` — 3896 bytes — `772d0993a3782e1fc7a386eb5e787afd708265815cd5e63346f08aafbe71f7ad`
- `m8-candidate/__init__.py` — 67 bytes — `5112fc6e78b2210dd05786169172e4b917f2d1e8457e41699d70cc4c3a0a859b`
- `m8-candidate/canonical.py` — 14085 bytes — `da1734670d6c3d10c03a53699b41d8bce6a74e430bc7c935ba86791151f2bc1c`
- `m8-candidate/cli.py` — 5930 bytes — `000732a10a61903e0173efd10c098a78958c4bdebeedeacef26eb8f1b193e4ec`
- `m8-candidate/grammar.py` — 6321 bytes — `df26d22d8d97c02f2bbd7cc2655b94eb3f1a9bf9d233fcc31b687fb34e814336`
- `m8-candidate/lexer.py` — 6375 bytes — `ef708b0e69c4e97e29221984f3be690463c22619d1e5d28225cf01d2cfbea3b2`
- `m8-candidate/parser.py` — 30216 bytes — `7728b2882a5ee154fc3011a26a7e3c78bb03aadf4beb543cda36e54238a22a1f`
- `m8-candidate/resolve.py` — 7451 bytes — `fbe084d993db67e09c1582d100121ccdd0ca90b68f9def6a601c8de798465bce`
- `m8-candidate/typecheck.py` — 36572 bytes — `55ed38054416dd3e336d297f4efd5b78f667fc0a27d96420ce9fa5377f0c57ea`
- `m8-candidate/corpus/arith-div-int-exact.msve` — 176 bytes — `16835fce950231cb9591a24a6842ad7bdd0df426f12e5a08116ea1964961da96`
- `m8-candidate/corpus/arith-mixed-real-nat.msve` — 180 bytes — `45d99dd2f2b846816a465f9bcc79f7b70d39061fcc181b322a4ddb21106fb7a1`
- `m8-candidate/corpus/arith-nat-int-embed.msve` — 177 bytes — `ed3f28f2faaf8e691742dbde2a9566a2241845eb7339044040a1b3cea4b4783d`
- `m8-candidate/corpus/arith-neg3-plus2.msve` — 174 bytes — `b5098e87e7126a798833494b86f66296192ec1f846bff2174783cb448b7b5d51`
- `m8-candidate/corpus/arith-unary-minus-nat.msve` — 175 bytes — `866adefd32bbce859d0fa8e024c5453dfa6fdf7c156389371f1708acc90b946f`
- `m8-candidate/corpus/bare-quantifier.msve` — 198 bytes — `fde406385f5b510aa39c5fcade88065176df19fb265837947062658173ae71b9`
- `m8-candidate/corpus/call-local-fn.msve` — 245 bytes — `4d4b6de3545eceddebc1fa4c0ae812815ecb72f9392ed1064f853dc1682582cd`
- `m8-candidate/corpus/case-ok.msve` — 203 bytes — `57327cb0b536fa4d6f1e71fd59216de8a104472bfd9ec959f9798d9fc03272cf`
- `m8-candidate/corpus/define-shadow-builtin.msve` — 179 bytes — `a886a3939b0bdc452c080fde0adf01e9cf5bacdc2974e719dcc4970abacc32d7`
- `m8-candidate/corpus/f01-base-code.msve` — 397 bytes — `35aeb61734dd245d4e0a39bb6ce7218de374c8ee9675e34b3b9e2179669d6706`
- `m8-candidate/corpus/f04-is-nan-typed.msve` — 256 bytes — `9acd3cc47a4c83fe6dca0c139d371e53ef4f3b2cb64110bc92c10cd8de8c2507`
- `m8-candidate/corpus/f64-neg-zero-exp.msve` — 193 bytes — `d4086b4a418d34e0c583929f71e686fa2751415b8e00d95dc2d60d5b6e52a2d3`
- `m8-candidate/corpus/f64-normal-form-subnormal.msve` — 205 bytes — `d4e9da4a39bb223b4c693ed4fe9887dd7577629001a698dd7b131c7748990241`
- `m8-candidate/corpus/f64-subtraction-no-spaces.msve` — 226 bytes — `d27bc859be0de5a68ce90195b3aa1549a9413e8e96324c0612c52df16d9f8870`
- `m8-candidate/corpus/f64-upper-hex.msve` — 190 bytes — `34fb34d7579ba7a5ef3b3289db7f5226c9ab4207cd2dbc4cf8ac4c67b5f1cb16`
- `m8-candidate/corpus/f64-valid.msve` — 186 bytes — `be3a0be79268d710d2e520dc854cb082989ab3edc3e574bbede3c76b3f0b6c2e`
- `m8-candidate/corpus/gen_corpus.py` — 6589 bytes — `abb752f4f025e00aa079a5b630a9800329accc3a36f5908457916b493f62d0b4`
- `m8-candidate/corpus/is_some-ok.msve` — 179 bytes — `46429699d75f8feb039fd6df001713098626dc4fe0347d2cba7a4cc4817f0cdc`
- `m8-candidate/corpus/let-ok.msve` — 176 bytes — `4293e41c321e8cc4330fe7a38b7d7a784fb87e241b2eeddcf5017f1f2fddb7b4`
- `m8-candidate/corpus/limits-steps-zero.msve` — 165 bytes — `f335778d3a710073fbc05af36f9a0971a187172a37aeef6d8a9e29f297c6ae95`
- `m8-candidate/corpus/limits-timeout-range.msve` — 160 bytes — `1589216d5d75c8b4d5cafb3dbca9daf93b5545aeb4a058d4e1b19908e0a00229`
- `m8-candidate/corpus/manifest.json` — 4051 bytes — `cb4e8a9fcc4ea63ff79abe518ae5092e118248f4843510f0f0152c1fb8036720`
- `m8-candidate/corpus/proj-path-unresolvable.msve` — 290 bytes — `39fd319917333ddf4e9d8a45c4485774c7cd7d7d94e7144a5a19fee8ba0f7966`
- `m8-candidate/corpus/quant-nested-ok.msve` — 232 bytes — `6a90e918e0b7c9beb72213d8fc959e4b580b81585076b658ac44040e23eb6789`
- `m8-candidate/corpus/quant-option-domain.msve` — 231 bytes — `0ddd766a3bb726547bb938f0cee6415a02ee0449f5f3c500ad1a107d99a0185f`
- `m8-candidate/corpus/quant-parens-ok.msve` — 200 bytes — `76f730bf000712f06369478e2b297e559cc3697fa0daec8ebe844ce1e13eebcd`
- `m8-candidate/corpus/range-ok.msve` — 171 bytes — `835e7931bff351834e043865d5f074a293c28b1217b1d2586faaa3b51202d75d`
- `m8-candidate/corpus/record-dup-field.msve` — 214 bytes — `81de72a6563605a9eda206246e55d318d1982a9fbc5bc1465ce570f6dc5f002e`
- `m8-candidate/corpus/record-field-type-mismatch.msve` — 227 bytes — `40151e4d734a6e4cd9092845c5828ef01a39ea546018081323bebf4e587c482a`
- `m8-candidate/corpus/record-infer.msve` — 175 bytes — `90664295714b6c561a25be47b4dcdb8529e1110dca2b6b0dbb02ee1be90ddcb0`
- `m8-candidate/corpus/record-missing-field.msve` — 212 bytes — `1c88a6801188da519029515da86e08232f89c3543f2f141d7297be43ea796bfe`
- `m8-candidate/corpus/record-nested.msve` — 258 bytes — `abc86bff4f4f57f7e1e6818c090cf6016401fb18e2bd21a8dc1eed1be98b5880`
- `m8-candidate/corpus/record-ok.msve` — 207 bytes — `ebc4558753174eb1b42f45e75424df12950696b6e4e995f9be470550f4f21428`
- `m8-candidate/corpus/record-unknown-field.msve` — 224 bytes — `6a24a88bdaeea39060dbb52b8760a9faffa95634d94bf81d56ab94fc91fc9f14`
- `m8-candidate/corpus/string-escape-not-short.msve` — 186 bytes — `bc14176513025946cd527e1db4d1b21bb2c6fb9fdb7dee9dd3248901c045c756`
- `m8-candidate/corpus/string-escape-upper.msve` — 182 bytes — `c5f6552400dc6e9330cbed014fadd1d3da9d690307692dcdc1cb412ecf861dee`
- `m8-candidate/corpus/string-ok.msve` — 170 bytes — `aa5749091226528167384ccf213304a4f00d942180c30933699b7f21e009e154`
- `m8-candidate/corpus/to_rat-ok.msve` — 172 bytes — `7c0f0199ce55cc6a15f69dbbd6fd1b0a0c3eb3c3438d5b84e2b358fcb8379fb2`
- `m8-candidate/corpus/type-cyclic-alias.msve` — 177 bytes — `5950a0f48ebb47b3c4b13407e6307654a9176b49f8036053e7ba3cfae14e947a`
- `m8-candidate/corpus/type-unbound-name.msve` — 183 bytes — `d919d3a852ef3b87c43717b4af5cb33e4b0d9d94d7804fe3156b1fc35eda92eb`
- `m8-candidate/corpus/unbound-ident.msve` — 179 bytes — `caf261e05e502134838c8a3f6bab12bf8d4c43cbeac1ae15e72c7dfd9e371221`
- `m8-candidate/corpus/v07-ex0.msve` — 246 bytes — `ef4745e1977fd7b945cf5a040772c8773fb5823e4335d2e6b74a671245a59f40`
- `m8-candidate/corpus/v07-ex1.msve` — 324 bytes — `81c16982016c39d1cf7a8d69b1d03aa03d7f7623b3b3ceb9020a30d5c07a257f`
- `m8-candidate/corpus/v07-ex2.msve` — 327 bytes — `58d4b9c90ab46751c27a1bba460f9c3a38432f3dd6dda35cdd00d96bff724ca3`
- `m8-candidate/corpus/v07-ex3.msve` — 1409 bytes — `a8490f13a3276d7ef177e37b8cde9ec259b679e69a846878e810b192291cddc0`
- `m8-candidate/corpus/v07-ex4.msve` — 371 bytes — `6b6b922ce66d9d6e729b8e99da63f5893e48bc9854156aa406864f5e789b4a09`
- `m8-candidate/corpus/v07-ex5.msve` — 2334 bytes — `561b2d4d8802671a4dc97751c7a34b74521062f27a1793bb53d55b00ac29f2d7`
- `m8-candidate/corpus/verif-assurance-level-a-needs-proof.msve` — 200 bytes — `3ee6d939a26bd48f42e5181d2cc48d155f249d0aa0a31845119e7ed87ba5d2a8`
- `m8-candidate/corpus/verif-assurance-level-a-unavailable.msve` — 342 bytes — `6861aacd4af3bd82650c68fe0af5488bfa0d42ae05a4bb5176cb5a3018449778`
- `m8-candidate/corpus/verif-cases-zero.msve` — 207 bytes — `c341436d8bd572cc5e86da40fcc2c06b3e56865930b33b252f1986a246b3594c`
- `m8-candidate/corpus/verif-diff-plus-fuzz.msve` — 263 bytes — `18e9ab0742650f06c22448528ac28d3327c86c3367464ccbbf765c3a597031bc`
- `m8-candidate/corpus/verif-duplicate-test.msve` — 256 bytes — `e6f1eabd5612a45e1800d11d7c3ace39fb6b7e899681e389364ff1eda1a7bd8e`
- `m8-candidate/corpus/verif-proof-conflict.msve` — 209 bytes — `2e079927528f2b6aee46d7df41a827e5185d593c0b466b350d9efe42dcb9425f`
- `m8-candidate/corpus/verif-qualifier-default.msve` — 188 bytes — `5f81757c93cf2b7f76fdaf851346657ec3ceab16d0e98e778ebe3878e6ef6c84`
- `m8-candidate/corpus/verif-recompute-conflict.msve` — 212 bytes — `a1fd871f37084a7e1fa73f0478b0d8e020fee28e49eee884a97f5bf23c7fa021`
- `m8-candidate/corpus/verif-test-none-conflict.msve` — 223 bytes — `3e5a0f59ba93125d48c48f9285897104545dcc246e2ab3ad9f0ce2bdf6ff1968`
- `m8-candidate/corpus/v08/inv-bare-quant.msve` — 216 bytes — `1d81cea39c930f54a9373bce08f6ee19501de243ca9b7fc10b3d7acad5f950b2`
- `m8-candidate/corpus/v08/inv-f64-negzero.msve` — 212 bytes — `13c6f20d48d424988a1e365ab0231901888a35bd2e8fb201c52e06d07cf31ff0`
- `m8-candidate/corpus/v08/inv-mixed-arith.msve` — 192 bytes — `961edd0488022dc32857e4ebe0dae1afa1fefb13178ad19e61f059e5702ec689`
- `m8-candidate/corpus/v08/inv-proof-conflict.msve` — 229 bytes — `8117f902102629d42dd58f72cb650338a4dfba2e7c2abe646dff1abfe858248d`
- `m8-candidate/corpus/v08/inv-unbound.msve` — 205 bytes — `2db5a8b38091c6207026d9739e368acb8d0837864a748ca4be572b5f52a4785a`
- `m8-candidate/corpus/v08/v08-ex0.msve` — 246 bytes — `ee00d8589dec21f233aff23670930b3b05bc2c753ffadf09e385396892b0c3cd`
- `m8-candidate/corpus/v08/v08-ex1.msve` — 324 bytes — `3baf22938deb3b0957b9377367718b3a173e14142aabe2ae0532f5fb53cd06f5`
- `m8-candidate/corpus/v08/v08-ex2.msve` — 327 bytes — `608e97689fc650effad75c604eafc26383eb6dd9319fd7fbd99d468aa31adce1`
- `m8-candidate/corpus/v08/v08-ex3.msve` — 1406 bytes — `42abbf513beae79ff2087b41d5a53b30b7c5cd7a7e8e40a7a3a1171afcecb228`
- `m8-candidate/corpus/v08/v08-ex4.msve` — 371 bytes — `7dada2f68a7da4827dd81db843b6efe271a30a3f4f7c705743ab686bc2edb55a`
- `m8-candidate/corpus/v08/v08-ex5.msve` — 2420 bytes — `f285f44e59f2ad1635dc1bb546fae87cb4fa82ba866e8fdf7b6374f68f9b3c7b`
- `m8-candidate/tests/__init__.py` — 1556 bytes — `671207b454c364a330090bef92fa92bf28eb83f053670499e1d85c2068ad0c6c`
- `m8-candidate/tests/test_canonical.py` — 6018 bytes — `cb67f0b79b61a5cfbf98dc35539d3bff48ddb9c2f6285d1dc6ee1c8a32fa6840`
- `m8-candidate/tests/test_grammar_conformance.py` — 1326 bytes — `c6cda78f566b582f6d4d1675821ee3771c7e7f5a1627dd00a02d7016af03f0d3`
- `m8-candidate/tests/__pycache__/__init__.cpython-312.pyc` — 2585 bytes — `51e82a253d8511a365787cea591ac632bafcb17ee726aa31a99d6deae0f1c414`
- `m8-candidate/tests/__pycache__/test_canonical.cpython-312.pyc` — 6074 bytes — `b0402ee95b35dd9b3a04a79860b8361d4251f624dfb3e9dafb7bfea46b209b34`
- `m8-candidate/tests/__pycache__/test_grammar_conformance.cpython-312.pyc` — 2357 bytes — `9fe60d1924bf1995efe223872a1a5f422a4b79aa160b662aee82e92c0f5256b4`
- `m8-candidate/runs/2026-10-09-m8-build.md` — 2739 bytes — `8bdf657b670e07b33a32687cc82af46056627814ed3439a55aa2c5974789df92`
- `m8-candidate/runs/phase0-capability-probe.md` — 1694 bytes — `49e820fca06a3ff262fb277fde47d2b098ce98a349fb5e6968a97f7df272d004`
- `m8-candidate/__pycache__/__init__.cpython-312.pyc` — 267 bytes — `cb05fc8109d179e6f312e412165b872468307e187998fca35f4b7e714a3cb812`
- `m8-candidate/__pycache__/canonical.cpython-312.pyc` — 17823 bytes — `9bac0de8de0c8c976a94e3dc6562b190632967b6762e445ddef98df06e1e2f17`
- `m8-candidate/__pycache__/cli.cpython-312.pyc` — 9452 bytes — `621938a1b9a6bb86f5b579b6952f56404d32cb2a9bd8461729793bc0244b6a91`
- `m8-candidate/__pycache__/grammar.cpython-312.pyc` — 6038 bytes — `47b1986ca37af355224161769d5872d101ad2b5739ae6ad75475d59708769dc9`
- `m8-candidate/__pycache__/lexer.cpython-312.pyc` — 7043 bytes — `523b637104162c30278549a57f3181736d7b2d3804910a8ad8a63cfc9fa7731d`
- `m8-candidate/__pycache__/parser.cpython-312.pyc` — 48319 bytes — `e50eb1d0c35f770b8a311b8f786c4a2f5737f82f1f69e263c0e318b0242ecc0c`
- `m8-candidate/__pycache__/resolve.cpython-312.pyc` — 9758 bytes — `c561590733358f1f3e30b9f7b9a5496eb69daeec130abde6e98035bbd0a7b134`
- `m8-candidate/__pycache__/typecheck.cpython-312.pyc` — 51105 bytes — `737b39681ddf50a611502427874b034bb0a3ec95844da4504ff86a1f72fb2566`
