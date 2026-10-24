# Private implementation files (gitignored)

`main.cpp` ships weak stubs so the project always compiles. Drop these in locally to override them:

| File | Implements |
|---|---|
| `hal_private.cpp` | `vdss::halBegin`, `halRead`, `halSetPump`, `halAim` |
| `fusion_private.cpp` | `vdss::fuse` |

Also create `include/config.h` from `config.example.h`.
Back these up in the private repo / drive — they are NOT pushed here.
