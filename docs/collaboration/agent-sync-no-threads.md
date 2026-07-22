# Agent sync addendum: no threads (ADR 0028)

Date: 2026-07-23.

## Lock

- No `Thread` / `async` / `await` / locks in object language.
- Concurrency = `when` arms + joint / tuple product.
- Engine may SIMD/GPU-parallelize supports invisibly (ADR 0022).

Canonical: `qpex-language-spec.md` §1.4.
