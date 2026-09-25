#!/usr/bin/env python3
"""
Module: test_algorithms
Purpose: One runnable check per algorithm; fails if any equation or loop breaks.
Author: Dr. Arli Aditya Parikesit
Date: 2026
Parameters:
    - none; reads the committed NCBI cache, so it runs with no network access
References:
    - Equation and Box numbers refer to IKSAD-Bioalgo-Manuscript-Arli.docx
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import algos
import ncbi


def test_eq1_mismatch_count():
    """Equation 1 on a hand-checked pair."""
    g = "ACGTACGTACGTACGTACGT"
    assert algos.mismatch_count(g, g) == 0
    assert algos.mismatch_count(g, "TCGTACGTACGTACGTACGT") == 1
    assert algos.mismatch_count(g, "T" * 20) == 15   # G, T positions already match a T run
    try:
        algos.mismatch_count(g, "ACGT")
    except ValueError:
        pass
    else:
        raise AssertionError("length mismatch must raise")


def test_eq2_position_weighting():
    """Equation 2: a PAM-proximal mismatch must cost more than a distal one."""
    g = "ACGTACGTACGTACGTACGT"
    distal = "TCGTACGTACGTACGTACGT"           # position 1, 5' end
    proximal = "ACGTACGTACGTACGTACGA"         # position 20, PAM-proximal
    assert algos.cfd(g, g) == 1.0
    assert algos.cfd(g, distal) > algos.cfd(g, proximal), "positional asymmetry lost"
    assert 0.0 < algos.cfd(g, proximal) < 1.0
    # two mismatches multiply
    two = "TCGTACGTACGTACGTACGA"
    assert abs(algos.cfd(g, two) - algos.cfd(g, distal) * algos.cfd(g, proximal)) < 1e-12


def test_eq3_monotonic_and_bounded():
    """Equation 3: adding an off-target site strictly lowers S; S stays in (0, 100]."""
    assert algos.specificity([]) == 100.0
    s1 = algos.specificity([0.5])
    s2 = algos.specificity([0.5, 0.5])
    assert 0 < s2 < s1 < 100.0, (s1, s2)
    assert algos.specificity([1.0] * 1000) > 0


def test_box1_pam_scan():
    """Box 1: the scan finds exactly the NGG sites in a hand-written sequence."""
    #                     0123456789...
    seq = "A" * 21 + "GG" + "T" * 21 + "GG"
    starts, spacers = algos.pam_spacers(seq)
    # 21 A, GG at 21-22, 21 T, GG at 44-45. Window i qualifies when seq[i+21:i+23] == "GG",
    # which holds for i = 0 and i = 23 only; i = 22 reads "TG".
    assert list(starts) == [0, 23], list(starts)
    assert spacers.shape == (2, 20)
    assert "".join("ACGT"[c] for c in spacers[0]) == "A" * 20
    # a window containing N must be dropped rather than scored
    assert algos.pam_spacers("N" + "A" * 20 + "GG")[0].size == 0


def test_box1_end_to_end_on_real_sequence():
    """Box 1 on the real inhA gene against its real H37Rv window."""
    w = ncbi.gene_window("inhA (Rv1484) - isoniazid/ethionamide, enoyl-ACP reductase")
    guides = algos.design_guides(w["gene"], w["window"], limit=25)
    assert guides, "no guides found in a real 810 bp gene"
    assert all(len(g["spacer"]) == 20 for g in guides)
    assert all(0 < g["S"] <= 100.0 for g in guides)
    assert guides == sorted(guides, key=lambda d: d["S"], reverse=True)
    # every on-target guide must find itself in the window it came from
    assert all(g["exact_sites"] >= 1 for g in guides), "guide not found in its own search space"


def test_eq5_free_energy():
    """Equation 5: pKd to kJ/mol, and the one-log-unit figure quoted in the Discussion."""
    assert abs(algos.delta_g(0)) < 1e-9
    dg6 = algos.delta_g(6)
    assert dg6 < 0, "binding free energy must be negative"
    assert abs(dg6 - (-35.6)) < 0.2, dg6
    per_unit = algos.log_unit_kj()
    assert abs(per_unit - 5.94) < 0.05, per_unit
    assert abs(algos.delta_g(7) - algos.delta_g(6) + per_unit) < 1e-9


def test_eq6_lipinski_and_penalty_on_real_compounds():
    """Equation 6 constraint term on real PubChem descriptors."""
    rows = {r["name"]: r for r in ncbi.compound_properties()}
    assert "error" not in rows["isoniazid"], rows["isoniazid"]
    # isoniazid is small and polar: it passes the rule of five
    assert algos.lipinski(rows["isoniazid"])[0] == 0, rows["isoniazid"]
    # rifampicin is a large natural product: it violates at least one rule
    assert algos.lipinski(rows["rifampicin"])[0] >= 1, rows["rifampicin"]
    # the penalty must order them the same way
    assert algos.penalty(rows["rifampicin"]) > algos.penalty(rows["isoniazid"])
    # a molecule inside every range scores zero
    assert algos.penalty({"MolecularWeight": 350.0, "XLogP": 2.5, "HBondDonorCount": 2,
                          "HBondAcceptorCount": 5, "TPSA": 75.0, "RotatableBondCount": 5}) == 0.0
    # missing descriptors are reported, not silently passed
    assert "MW missing" in algos.lipinski({})[1]


def test_box2_lambda_changes_the_ranking():
    """Box 2: raising lambda must push constraint violators down the list."""
    rows = ncbi.compound_properties()
    loose = algos.screen(rows, lam=0.0)
    tight = algos.screen(rows, lam=10.0)
    assert len(loose) == len(tight) == 12
    assert all(r["affinity"] is None for r in tight), "no affinity model should be implied"
    worst = max(rows, key=lambda r: algos.penalty(r) if "error" not in r else -1)["name"]
    rank = lambda lst, n: [r["name"] for r in lst].index(n)
    assert rank(tight, worst) >= rank(loose, worst), "lambda did not penalise the worst offender"


def test_eq7_eq8_likelihood_invariants():
    """Equations 7-8: conditionals normalise, the sum is negative, and fitted genomes score highest."""
    train = {n: ncbi.fasta(a)[1] for n, a in ncbi.PHAGE_TRAIN.items()}
    model = algos.MarkovGenome(order=5).fit(train)
    assert np.allclose(model._probs().sum(axis=1), 1.0, atol=1e-9), "conditionals do not sum to 1"

    t4 = ncbi.fasta(ncbi.PHAGE_TEST["Enterobacteria phage T4"])[1]
    ctrl = ncbi.fasta(ncbi.NONPHAGE_CONTROL["Y. pestis plasmid pPCP1"])[1]
    total_t4, per_t4 = model.log_likelihood(t4)
    total_ctrl, per_ctrl = model.log_likelihood(ctrl)
    assert total_t4 < 0 and total_ctrl < 0, "log-likelihood must be negative"
    assert abs(total_t4 / len(t4) - per_t4) < 0.01, "total and per-base disagree"
    # The three fitted genomes must outscore both held-out sequences.
    for name, seq in train.items():
        assert model.log_likelihood(seq)[1] > max(per_t4, per_ctrl), f"{name} scored below held-out"


def test_eq8_is_confounded_by_composition():
    """Characterisation of the stand-in model's ceiling: it separates GC content, not phage identity.

    The order-k count model scores the non-phage control ABOVE the held-out phage. This is a real
    negative result, not a tuned one, and it is the reason the panel refuses to present Equation 8 as
    a phage-detection score. Training GC runs 48-64%; the control plasmid at 45% sits inside that
    range while T4 at 35% is an outlier, so composition decides the ranking.

    If a trained genome language model is ever dropped in, this check SHOULD start failing. That is
    the signal to rewrite it, not to delete it.
    """
    train = {n: ncbi.fasta(a)[1] for n, a in ncbi.PHAGE_TRAIN.items()}
    t4 = ncbi.fasta(ncbi.PHAGE_TEST["Enterobacteria phage T4"])[1]
    ctrl = ncbi.fasta(ncbi.NONPHAGE_CONTROL["Y. pestis plasmid pPCP1"])[1]
    gc = {n: algos.gc_fraction(s) for n, s in train.items()}
    assert min(gc.values()) > algos.gc_fraction(t4), "T4 is no longer the GC outlier"
    assert min(gc.values()) > algos.gc_fraction(ctrl) > algos.gc_fraction(t4)

    for order in (1, 3, 5):
        model = algos.MarkovGenome(order=order).fit(train)
        per_t4 = model.log_likelihood(t4)[1]
        per_ctrl = model.log_likelihood(ctrl)[1]
        print(f"    order={order}: held-out T4 {per_t4:.4f} < control {per_ctrl:.4f} nats/base")
        assert per_ctrl > per_t4, (
            f"order-{order} now separates phage from control; update this check and the panel text")


def test_eq9_and_sampling():
    """Equation 9 arithmetic, the GC proxy, and Box 3 sampling from the fitted model."""
    train = {n: ncbi.fasta(a)[1] for n, a in ncbi.PHAGE_TRAIN.items()}
    model = algos.MarkovGenome(order=4).fit(train)
    d29 = train["Mycobacterium phage D29"]
    host = ncbi.gene_window("inhA (Rv1484) - isoniazid/ethionamide, enoyl-ACP reductase")["window"]

    assert algos.host_fitness_proxy(host, host) == 1.0
    assert 0.0 <= algos.host_fitness_proxy(d29, host) <= 1.0
    d = algos.design_score(d29, host, model, beta=1.0)
    assert abs(d["score"] - (d["f"] + d["loglik_per_base"])) < 1e-12
    # beta scales only the likelihood term
    hi = algos.design_score(d29, host, model, beta=2.0)
    assert abs(hi["score"] - (d["f"] + 2 * d["loglik_per_base"])) < 1e-12

    sampled = model.sample(2000, seed_seq=d29, rng=np.random.default_rng(0))
    assert len(sampled) == 2000 and set(sampled) <= set("ACGT")
    # a sample from the model should score better than a uniform-random sequence
    rng = np.random.default_rng(1)
    uniform = "".join(rng.choice(list("ACGT"), 2000))
    assert model.log_likelihood(sampled)[1] > model.log_likelihood(uniform)[1]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"FAIL  {t.__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
