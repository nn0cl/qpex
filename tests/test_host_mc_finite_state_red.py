"""AT-TDD: LISS-0195 Host Monte Carlo → finite State inject (ADR 0163)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.host_monte_carlo import (  # noqa: E402
    EqualWidthHistogramMonteCarlo,
    HostRngAdapter,
    MonteCarloInjectError,
    MonteCarloSpec,
    finite_inject_to_joint,
)


def test_uniform_draws_two_bins_near_half() -> None:
    rng = HostRngAdapter(seed=0)
    # Continuous draw: uniform on [0, 1) via rng.random()
    port = EqualWidthHistogramMonteCarlo()
    spec = MonteCarloSpec(
        domain_label="x",
        interval=(0.0, 1.0),
        n_bins=2,
        n_samples=2000,
        approximation="EqualWidthHistogram",
        coordinate="s",
        seed=0,
        provenance={"source": "unit-test"},
    )
    inject = port.sample_to_finite(spec, rng, continuous_draw=lambda r: r.random())
    assert inject.coordinate == "s"
    labels = {label for label, _mass in inject.atoms}
    assert labels <= {0, 1}
    total = sum(m for _l, m in inject.atoms)
    assert abs(total - 1.0) < 1e-12
    # With many samples, both bins should appear with mass near 0.5.
    by_label = dict(inject.atoms)
    assert 0 in by_label and 1 in by_label
    assert abs(by_label[0] - 0.5) < 0.05
    assert abs(by_label[1] - 0.5) < 0.05
    assert inject.provenance["approximation"] == "EqualWidthHistogram"
    assert inject.provenance["n_bins"] == 2


def test_reject_missing_bins_fail_closed() -> None:
    port = EqualWidthHistogramMonteCarlo()
    rng = HostRngAdapter(seed=1)
    try:
        port.sample_to_finite(
            MonteCarloSpec(
                domain_label="x",
                interval=(0.0, 1.0),
                n_bins=0,
                n_samples=10,
                approximation="EqualWidthHistogram",
                coordinate="s",
                provenance={},
            ),
            rng,
            continuous_draw=lambda r: r.random(),
        )
        raise AssertionError("expected MonteCarloInjectError")
    except MonteCarloInjectError as exc:
        assert exc.code == "MONTE_CARLO_SPEC_INVALID"


def test_reject_unknown_approximation() -> None:
    port = EqualWidthHistogramMonteCarlo()
    rng = HostRngAdapter(seed=1)
    try:
        port.sample_to_finite(
            MonteCarloSpec(
                domain_label="x",
                interval=(0.0, 1.0),
                n_bins=4,
                n_samples=10,
                approximation="KDE",
                coordinate="s",
                provenance={},
            ),
            rng,
            continuous_draw=lambda r: r.random(),
        )
        raise AssertionError("expected MonteCarloInjectError")
    except MonteCarloInjectError as exc:
        assert exc.code == "MONTE_CARLO_APPROXIMATION_UNSUPPORTED"


def test_out_of_domain_all_rejected_fails() -> None:
    port = EqualWidthHistogramMonteCarlo()
    rng = HostRngAdapter(seed=1)
    try:
        port.sample_to_finite(
            MonteCarloSpec(
                domain_label="x",
                interval=(0.0, 1.0),
                n_bins=4,
                n_samples=20,
                approximation="EqualWidthHistogram",
                coordinate="s",
                provenance={},
            ),
            rng,
            continuous_draw=lambda _r: 5.0,
        )
        raise AssertionError("expected MonteCarloInjectError")
    except MonteCarloInjectError as exc:
        assert exc.code == "MONTE_CARLO_EMPTY_SUPPORT"


def test_finite_inject_to_joint_amplitudes() -> None:
    rng = HostRngAdapter(seed=2)
    port = EqualWidthHistogramMonteCarlo()
    spec = MonteCarloSpec(
        domain_label="x",
        interval=(0.0, 1.0),
        n_bins=2,
        n_samples=100,
        approximation="EqualWidthHistogram",
        coordinate="s",
        provenance={},
    )
    inject = port.sample_to_finite(spec, rng, continuous_draw=lambda r: r.random())
    joint = finite_inject_to_joint(inject)
    assert not joint.is_vacuum()
    mass = sum(abs(w.amp) ** 2 for w in joint.worlds)
    assert abs(mass - 1.0) < 1e-9
    for w in joint.worlds:
        assert "s" in w.assign
        assert isinstance(w.assign["s"], int)
        # Born mass matches atom mass
        label = w.assign["s"]
        atom_mass = dict(inject.atoms)[label]
        assert abs(abs(w.amp) ** 2 - atom_mass) < 1e-12


def test_integer_bin_labels_only() -> None:
    rng = HostRngAdapter(seed=3)
    port = EqualWidthHistogramMonteCarlo()
    # Always draw into first half → only bin 0
    inject = port.sample_to_finite(
        MonteCarloSpec(
            domain_label="x",
            interval=(0.0, 1.0),
            n_bins=4,
            n_samples=50,
            approximation="EqualWidthHistogram",
            coordinate="s",
            provenance={},
        ),
        rng,
        continuous_draw=lambda _r: 0.1,
    )
    assert list(inject.atoms) == [(0, 1.0)]


if __name__ == "__main__":
    test_uniform_draws_two_bins_near_half()
    print("PASS test_uniform_draws_two_bins_near_half")
    test_reject_missing_bins_fail_closed()
    print("PASS test_reject_missing_bins_fail_closed")
    test_reject_unknown_approximation()
    print("PASS test_reject_unknown_approximation")
    test_out_of_domain_all_rejected_fails()
    print("PASS test_out_of_domain_all_rejected_fails")
    test_finite_inject_to_joint_amplitudes()
    print("PASS test_finite_inject_to_joint_amplitudes")
    test_integer_bin_labels_only()
    print("PASS test_integer_bin_labels_only")
