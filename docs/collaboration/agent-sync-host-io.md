# Agent sync addendum: host I/O boundary (ADR 0029)

Date: 2026-07-23.

## Lock

- No mid-pure OS writes that sample the joint.
- Input: `File.readAsState` → `State<T>` (prep / lift).
- Output: `measure e` / `measure e to File(…)` (collapse + sink).
- Checkpoint: `snapshot e to …` logs joint **without** RngPort / without Dirac replace.
- Debug: `inspect` — same non-collapse law; passthrough (ADR 0030).

Canonical: `staqex-language-spec.md` §5.
