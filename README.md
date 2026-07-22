# QPex

**QPex** (Quantum-Probabilistic Executable) is a programming language where
every value and operation is a probability distribution. Phase 1 targets a
Rust VM / simulator; a QPU-oriented backend is a longer-term goal.

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

at your option. See [LICENSE](LICENSE).

## Status

Architecture and MVP specification are in progress. See:

- [Language axioms](docs/architecture/qpex-language-axioms.md)
- [MVP spec: Discrete PMF arithmetic + observe](docs/specs/qpex-mvp-discrete-pmf-arith-observe.md)
- [Architecture overview](docs/architecture/README.md)

Do not implement language behavior without an accepted specification and an
explicit AT-TDD phase approval (see `AGENTS.md`).
