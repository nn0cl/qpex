# Quantum machine scale/model envelope intake

- Date: 2026-07-30
- Branch: `codex/liss-0082-design-deepening`
- Operating path: Architecture Path
- Current phase: Phase 0 design intake
- Approved scope: incorporate planned fault-tolerant machines, generalized
  quantum-computation targets, and a future household/local quantum computer
  horizon into the design
- Implementation permission: **none**
- Post-review required: ADR 0109 architecture approval; all implementation
  phases remain separately gated

## Design result

- Define one semantic contract across Personal Quantum Appliance,
  on-premises/laboratory, remote, and modular utility-scale deployments.
- Keep provider roadmap numbers out of language limits.
- Preserve hierarchy, callable regions, symbolic repetition, and symbolic
  resources; prohibit unbudgeted eager flattening.
- Separate semantic, logical, and physical resource levels.
- Treat digital, native evolution, measurement-based/photonic, qudit,
  optimization-specialized, and simulator execution as explicit downstream
  capability profiles.
- Keep Quantum Semantic IR v1 finite; native continuous-variable support needs
  a future reviewed profile.
- Make local compilation/execution network-independent and forbid implicit
  remote or simulator fallback.

## Evidence boundary

Official vendor roadmaps and product pages were used as dated primary claims.
They show facility-scale logical/QEC/modular trends and early local/on-premises
deployment patterns. They do not prove delivery dates or the existence of a
useful general-purpose household quantum PC.

Detailed evidence:
[`docs/research/2026-07-30-quantum-machine-scale-and-model-horizon.md`](../../research/2026-07-30-quantum-machine-scale-and-model-horizon.md).

## Changed design ownership

- LISS-0082: scale-free hierarchy, no deployment/model fields.
- LISS-0083: hierarchical plans and symbolic resources.
- LISS-0087: hierarchy-preserving verified passes.
- LISS-0091: three resource levels and materialization/power/QEC estimates.
- LISS-0099: versioned model/scale/deployment capability profile.
- LISS-0102: local/on-premises/remote workflow with no implicit fallback.
- LISS-0120: review one source across local and utility horizons.

## Stop condition

Stop after documentation verification. No IR, compiler, runtime, target,
provider, network, or sample implementation.
