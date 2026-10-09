# Environment register

All executions in this reproducibility pass used one isolated environment.

| Item | Value |
|---|---|
| OS | Linux (container/VM) |
| Python | 3.12.3 (`python3 --version`) |
| Virtualenv | isolated venv, no system packages |
| `z3-solver` package | `5.1.0.0` (pinned exact) |
| Z3 runtime (`z3.get_version_string()`) | `5.1.0` |
| Other packages | none (stdlib only: `re`, `json`, `sys`, `struct`, `random`, `math`, `typing`) |

The `z3-solver` package version and the Z3 runtime version are distinct
identifiers; both are recorded. No newer solver was substituted.

M8 sources (`history-bank/models-and-validators/m8/`) require only the
Python standard library. Z3 model/driver sources require `z3-solver==5.1.0.0`
and the code-list JSON at `/tmp/m8test/codelists.json` (reconstructed; see
`reports/reconstructed-input.md`).
