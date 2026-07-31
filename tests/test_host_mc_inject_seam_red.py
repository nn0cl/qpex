"""AT-TDD: LISS-0198 Host MC inject consumption seam (ADR 0164)."""

from __future__ import annotations

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
    run_host_mc_inject,
)


def test_default_label_mode_is_bin_index() -> None:
    rng = HostRngAdapter(seed=0)
    port = EqualWidthHistogramMonteCarlo()
    inject = port.sample_to_finite(
        MonteCarloSpec(
            domain_label="x",
            interval=(0.0, 1.0),
            n_bins=4,
            n_samples=40,
            approximation="EqualWidthHistogram",
            coordinate="s",
            provenance={},
        ),
        rng,
        continuous_draw=lambda _r: 0.1,
    )
    assert list(inject.atoms) == [(0, 1.0)]
    disc = inject.provenance["discretization"]
    assert disc["label_mode"] == "bin_index"
    assert disc["domain"] == "x"
    assert disc["basis"] == "EqualWidthHistogram"
    assert disc["resolution"] == 4
    assert disc["boundary"]["convention"] == "half_open_right"
    assert disc["error_bound"] == "Unbounded"


def test_bin_midpoint_labels() -> None:
    rng = HostRngAdapter(seed=1)
    port = EqualWidthHistogramMonteCarlo()
    # Always draw into bin 1 of [0,1) with n_bins=4 → midpoint 0.375
    inject = port.sample_to_finite(
        MonteCarloSpec(
            domain_label="Position",
            interval=(0.0, 1.0),
            n_bins=4,
            n_samples=30,
            approximation="EqualWidthHistogram",
            coordinate="x",
            provenance={},
            label_mode="bin_midpoint",
        ),
        rng,
        continuous_draw=lambda _r: 0.3,
    )
    assert len(inject.atoms) == 1
    label, mass = inject.atoms[0]
    assert abs(float(label) - 0.375) < 1e-12
    assert abs(mass - 1.0) < 1e-12
    assert inject.provenance["discretization"]["label_mode"] == "bin_midpoint"
    joint = finite_inject_to_joint(inject)
    assert joint.worlds[0].assign["x"] == label


def test_explicit_labels() -> None:
    rng = HostRngAdapter(seed=2)
    port = EqualWidthHistogramMonteCarlo()
    labels = ("a", "b", "c", "d")
    inject = port.sample_to_finite(
        MonteCarloSpec(
            domain_label="x",
            interval=(0.0, 1.0),
            n_bins=4,
            n_samples=20,
            approximation="EqualWidthHistogram",
            coordinate="s",
            provenance={},
            label_mode="explicit_labels",
            bin_labels=labels,
        ),
        rng,
        continuous_draw=lambda _r: 0.1,
    )
    assert list(inject.atoms) == [("a", 1.0)]


def test_explicit_labels_wrong_length_fails() -> None:
    rng = HostRngAdapter(seed=2)
    port = EqualWidthHistogramMonteCarlo()
    try:
        port.sample_to_finite(
            MonteCarloSpec(
                domain_label="x",
                interval=(0.0, 1.0),
                n_bins=4,
                n_samples=5,
                approximation="EqualWidthHistogram",
                coordinate="s",
                provenance={},
                label_mode="explicit_labels",
                bin_labels=("only", "two"),
            ),
            rng,
            continuous_draw=lambda r: r.random(),
        )
        raise AssertionError("expected MonteCarloInjectError")
    except MonteCarloInjectError as exc:
        assert exc.code == "MONTE_CARLO_SPEC_INVALID"


def test_unsupported_label_mode_fails() -> None:
    rng = HostRngAdapter(seed=2)
    port = EqualWidthHistogramMonteCarlo()
    try:
        port.sample_to_finite(
            MonteCarloSpec(
                domain_label="x",
                interval=(0.0, 1.0),
                n_bins=2,
                n_samples=5,
                approximation="EqualWidthHistogram",
                coordinate="s",
                provenance={},
                label_mode="kde_centers",
            ),
            rng,
            continuous_draw=lambda r: r.random(),
        )
        raise AssertionError("expected MonteCarloInjectError")
    except MonteCarloInjectError as exc:
        assert exc.code == "MONTE_CARLO_LABEL_MODE_UNSUPPORTED"


def test_error_bound_from_spec_provenance() -> None:
    rng = HostRngAdapter(seed=3)
    port = EqualWidthHistogramMonteCarlo()
    inject = port.sample_to_finite(
        MonteCarloSpec(
            domain_label="x",
            interval=(0.0, 1.0),
            n_bins=2,
            n_samples=10,
            approximation="EqualWidthHistogram",
            coordinate="s",
            provenance={"error_bound": "Empirical(tol=0.05)"},
            label_mode="bin_index",
        ),
        rng,
        continuous_draw=lambda r: r.random(),
    )
    assert inject.provenance["discretization"]["error_bound"] == "Empirical(tol=0.05)"


def test_run_host_mc_inject_helper() -> None:
    inject, joint = run_host_mc_inject(
        domain_label="x",
        interval=(0.0, 1.0),
        n_bins=2,
        n_samples=200,
        coordinate="s",
        continuous_draw=lambda r: r.random(),
        seed=7,
    )
    assert inject.coordinate == "s"
    assert "discretization" in inject.provenance
    assert not joint.is_vacuum()
    born = sum(abs(w.amp) ** 2 for w in joint.worlds)
    assert abs(born - 1.0) < 1e-9
    # masses match
    for w in joint.worlds:
        label = w.assign["s"]
        assert abs(abs(w.amp) ** 2 - dict(inject.atoms)[label]) < 1e-12


if __name__ == "__main__":
    test_default_label_mode_is_bin_index()
    print("PASS test_default_label_mode_is_bin_index")
    test_bin_midpoint_labels()
    print("PASS test_bin_midpoint_labels")
    test_explicit_labels()
    print("PASS test_explicit_labels")
    test_explicit_labels_wrong_length_fails()
    print("PASS test_explicit_labels_wrong_length_fails")
    test_unsupported_label_mode_fails()
    print("PASS test_unsupported_label_mode_fails")
    test_error_bound_from_spec_provenance()
    print("PASS test_error_bound_from_spec_provenance")
    test_run_host_mc_inject_helper()
    print("PASS test_run_host_mc_inject_helper")
