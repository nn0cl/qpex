# QPU lane boundaries for physicists

This teaching note distinguishes the three Staqex execution surfaces without
turning Host bookkeeping into Kernel physics.

## Static Hilbert Kernel

```staqex
QubitRegister<3> reg = system()

forEach q in reg {
    apply(H, q)
}
```

`3` is a type-level dimension of the system, not a runtime integer. `q` is a
tensor-factor handle, not a classical index. `State<T>` remains the evolving
pre-measurement state; only terminal `measure` exposes a result.

## Parametric Circuit

```staqex
Param<Angle> theta = parameter("theta")
forEach q in reg {
    apply(Rz(theta), q)
}
```

`theta` is symbolic circuit data. Host submission supplies its concrete value;
it cannot alter register shape or control a branch.

## Dynamic QPU lane

```staqex
dynamic qpu {
    State<Int> flag = coin()
    measure flag
    apply(X, flag)
}
```

This is intentionally a separate, currently rejected lane. A real
implementation must specify feed-forward, timing, capability profiles, and
JobResult semantics before it becomes valid Staqex.
