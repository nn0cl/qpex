# QPex quantum-native compiler / runtime optimizations

Status: **Working baseline** (2026-07-22). ADR **0022**.
Design axis for future IR and engine passes — **not** Kernel PoC A/B scope.
Implementation **Hold** until Adjudicator unseals an IR / optimizer track.

Companions: Language Law (`qpex-positioning.md`), formal semantics
(§Block trace-out, purity until `measure`), `qpex-ast-design.md`, ADR 0016
(amplitude lift), **`qpex-runtime-execution-model.md` (ADR 0032)**.

---

## 0. Thesis

Classical compiler tricks (inline, DCE) matter, but QPex’s decisive
optimizations exploit **linear-algebra / quantum narrative structure** already
forced by **Never Leave the State**:

| Classical framing | QPex framing |
|-------------------|--------------|
| Copy buffers between steps | Fuse operators; apply once |
| Keep dead locals on the stack | Trace out unused joint axes |
| Explore every branch | Merge supports; prune mass / amplitude $0$ |
| Eager eval of every stmt | Build a pure DAG; batch at `measure` |

All four passes below must **preserve denotational semantics** (same joint /
same samples under the same RNG stream after `measure`). They change cost,
not meaning.

---

## 1. Operator Fusion (Unitary / Pushforward Collapse)

### Physics idea

A chain of pure state transformers

\[
U_n \cdots U_2 U_1 \lvert \psi \rangle
\]

need not materialize intermediate joints. Compose the operators first:

\[
U_{\mathrm{fused}} = U_n \cdots U_2 U_1,
\]

then apply $U_{\mathrm{fused}}$ once.

### Surface example

```qpex
state w = z
    |> (s => s + 10)
    |> (s => s * 2)
    |> (s => s - 5)
```

(`|>` remains reserved surface; fusion applies equally to desugared `map` /
nested pure kernels.)

### Pass behavior

1. Algebraically collapse the pipeline (MVP: affine / polynomial rewrite on
   carriers, e.g. `(s + 10) * 2 - 5` → `2*s + 15`).
2. Emit one pushforward over the support of `z` (single pass; no mid-chain
   joint allocation).

### Effect

Zero intermediate joint copies for fused pure chains.

### Laws

- Only fuse **measure-free** kernels ($\mathsf{Joint}\to\mathsf{Joint}$).
- Fusion must respect the **correlation law** (shared axes are not independent
  copies).
- After amplitude lift (ADR 0016), matrix / circuit fusion is the same idea
  on unitary factors.

---

## 2. Trace-Out GC (Partial Trace of Dead Axes)

### Physics idea

Subsystems never referenced again need not stay in the joint. Static
**liveness** of joint coordinates drives automatic **partial trace**.

### Surface example

```qpex
state w = evolve (z) {
    let temp1 = z * 2
    let temp2 = temp1 + 5
    temp2
}
```

### Pass behavior

At block / evolve exit (semantics §Block already requires this):

\[
\rho_{\mathrm{out}}
  = \mathrm{Tr}_{\{\ell \notin R\}}(\rho_{\mathrm{ext}})
\]

Dead axes (`temp1`, inbound `z` if unused outside) are marginalized and
dropped from the in-memory joint representation immediately.

Style cue (ADR 0023): prefer `let _temp1 = …` for axes expected to be traced
out; naming documents intent, liveness still decides GC.

### Effect

Cuts exponential blow-up from ancilla / temporary axes.

### Laws

- Trace-out ≠ `measure` and ≠ `project` (no RNG; no renormalize-by-predicate).
- Must match formal §Block / §Evolve; optimizer only **eagerly realizes** the
  semantic obligation.
- Interprocedural / `system` field liveness is a later IR analysis.

---

## 3. Interference Pruning & Support Merging

### Physics idea

`when` and product expansions grow world-lines; many collide on the same
carrier value, and (under amplitudes) some cancel to exact zero.

### Surface example

```qpex
state c = coin()
state z = span (c) {
    0 => x + 10,
    1 => x + 10
}
```

### Pass behavior

1. **Support merge:** when distinct paths yield the same atom, add masses
   (MVP) or amplitudes (lift) into one support entry.
2. **Prune:** drop atoms with mass / amplitude exactly $0$ (or below a
   documented numeric epsilon policy — open for `f64` vs exact rational).

### Effect

Smaller supports before later pushforwards; destructive interference pays
off only after amplitude IR, but **merge + zero-prune** already help PMF.

### Laws

- Merge must be associative / commutative on the monoid of masses (or $\mathbb{C}$).
- Do not prune before cancellation is proven for that representation.
- Distinct from `project` (no predicate subspace renorm).

---

## 4. Deferred Pushforward (Lazy DAG until `measure`)

### Physics idea

Language Law: **RNG = 0** until `measure`. Evaluation of pure programs is a
function on joints; the engine may defer *materializing* joints and only
build a **computation DAG** (AST / IR tasks).

### Surface example

```qpex
state a = coin()
state b = a + 10
state c = span (b) { /* … */ }
measure c
```

Until `measure c`, the runtime may hold only graph nodes. At `measure`, run
fused / traced / pruned batch evaluation, then one `RngPort` draw.

### Pass behavior

1. Lower pure stmts to IR nodes (`Pushforward`, `SpanMix`, `Project`, …).
2. Schedule fusion + trace-out + merge passes on the DAG.
3. Materialize the joint needed for the measured expression; sample once.

### Effect

Avoids eager work on dead pure prefixes; enables whole-program batch opts.

### Laws

- Observable behavior under a fixed RNG stream equals eager pure eval +
  terminal sample (semantics §Measure / deferred RNG law).
- Side-effecting ports other than RNG remain forbidden in pure regions.
- Debugging / tracing modes may force eager materialization without changing
  denotation.

---

## 5. Pass ordering (suggested)

```text
parse → typed AST
     → build pure DAG (defer materialization)
     → Operator Fusion
     → Interference merge / prune (local)
     → Trace-Out GC (liveness)
     → (repeat local opts)
     → materialize joint for measure
     → RngPort sample + Dirac collapse
```

Exact IR shape is **open** (future amplitude / QPU IR under ADR 0016).

---

## 5b. Engine parallelism (not surface threads)

Independent support atoms under Deferred Pushforward may be scheduled on
multi-core / GPU workers. This does **not** add `Thread`/`async` to the
source language (ADR 0028). Full implementer narrative: ADR **0032** /
`qpex-runtime-execution-model.md` (DAG + data-parallel, not Promise VM).

## 6. Non-goals (this note)

- Classical-only opts without joint semantics (still welcome later; not the wedge).
- Approximate sampling before `measure`.
- Equating `project` with prune/merge.
- Implementing passes in Kernel PoC A/B.

---

## 7. Open questions

- Exact rational masses vs `f64` prune thresholds.
- Fusion algebra for non-polynomial carriers (`String`, structured `T`).
- Whole-program vs block-local fusion under `system.step` loops.
- When amplitude IR lands: gate fusion vs PMF pushforward fusion coexistence.
- Whether deferred mode is default or an `--optimize` / engine profile.
