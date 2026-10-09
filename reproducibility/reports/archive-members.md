# Archive-member Python sources

Two preserved ZIP snapshots contain Python sources. Every `.py` member
(excluding `__pycache__` bytecode) was hashed and compared against tracked
repository files.

| Archive | SHA-256 (first 12) | .py members | Byte-identical to tracked |
|---|---|---|---|
| `history-bank/source-snapshots/MSVE_v0.8_OWNER_REVIEW_BUNDLE.zip` | (see manifest) | 12 | 12/12 |
| `history-bank/source-snapshots/MSVE_v0.8.3_CANDIDATE_BUNDLE.zip` | (see manifest) | 12 | 12/12 |

No archive contains a Python source that is not also tracked in the
repository. The ZIP members are therefore covered by the inventory entries
for their tracked counterparts; no separate archive-only inventory rows
were needed. The `.pyc` files in the 0.8.3 bundle are build artifacts,
not sources, and are not inventoried.
