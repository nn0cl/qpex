# LISS-0231: S01 `impl` interface-mediated dispatch

## Metadata

- Local issue ID: LISS-0231
- GitHub issue: (none yet)
- Status: **proposed**
- Phase: (none — intake)
- Type: chore
- Priority: P2
- Initial planning size: S
- Current planning size: S
- Owner/agent: (unassigned)
- Related branch: (none yet)
- Program: [WP-0072](../work-plans/WP-0072-s01-coverage-residuals.md)

## Summary

`domain/capabilities.sqx` declares `impl Deployable` / `Haulable`, but tonight
spine calls `squad.readiness()` / `truck.load_tag()` **directly**. Scorecard
“basic `impl`” is therefore weak: interface-mediated dispatch is not exercised.

Trait specialization remains Out (scorecard).

## Acceptance Notes

- [ ] Ops story uses interface-typed receiver or call that requires `impl`
- [ ] Runnable main seed 0 green
- [ ] Scorecard notes “interface dispatch” evidence path

## Dependencies

- Existing `domain/capabilities.sqx`
- Does not authorize trait specialization

## Verification

- `python3 -m compiler.staqex run …/main_disaster_response.sqx --seed 0`
