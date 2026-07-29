# B13 — Host Job API

Teaches the provider-neutral Host boundary: `submit_source` returns a `Job`,
and `JobResult` exposes terminal measurements without leaking Kernel internals
(LISS-0022 / ADR 0065).

## Run (Kernel CLI)

```bash
python3 -m compiler.staqex run examples/basics/B13_host_job_api/main_host_job.sqx --seed 0
```

## Run via Host Job helper

```bash
python3 examples/basics/B13_host_job_api/run_as_job.py
```

The helper is the pedagogical surface for future provider adapters; no network
or SDK is involved in the local target.
