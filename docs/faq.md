# FAQ

**Does it call models?**
No. It compiles recorded traces and incidents into evaluation assets offline.

**Why a Go binary as well?**
The gate runs in CI on every release, where a static binary with no runtime
dependencies is the least fragile option.
