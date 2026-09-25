#!/usr/bin/env python3
"""
Module: algos
Purpose: The nine equations and three boxed algorithms of the proceeding, as runnable functions.
Author: Dr. Arli Aditya Parikesit
Date: 2026
Parameters:
    - see each function; equation numbers refer to IKSAD-Bioalgo-Manuscript-Arli.docx
References:
    - Jinek, M. et al. (2012). Science, 337(6096), 816-821. https://doi.org/10.1126/science.1225829
    - Hsu, P. D. et al. (2013). Nat Biotechnol, 31(9), 827-832. https://doi.org/10.1038/nbt.2647
    - Doench, J. G. et al. (2016). Nat Biotechnol, 34(2), 184-191. https://doi.org/10.1038/nbt.3437
    - Bae, S., Park, J., & Kim, J. S. (2014). Bioinformatics, 30(10), 1473-1475.
      https://doi.org/10.1093/bioinformatics/btu048
    - Lipinski, C. A. et al. (2001). Adv Drug Deliv Rev, 46(1-3), 3-26.
      https://doi.org/10.1016/s0169-409x(00)00129-0
    - Gomez-Bombarelli, R. et al. (2018). ACS Cent Sci, 4(2), 268-276.
      https://doi.org/10.1021/acscentsci.7b00572
    - Nguyen, E. et al. (2024). Science, 386(6723), eado9336. https://doi.org/10.1126/science.ado9336
"""

import numpy as np

R_GAS = 8.314462618e-3   # kJ / (mol K)
T_PHYS = 310.15          # K, 37 C

# ---------------------------------------------------------------------------
# Area 1: CRISPR-Cas guide design. Equations 1-3 and Box 1.
# ---------------------------------------------------------------------------

# Illustrative positional tolerance weights, NOT the published CFD table.
# Doench et al. (2016) supply a weight per position AND per substituted base, estimated from measured
# cleavage at mismatch panels. That table is not reproduced here from recall. This vector encodes only
# the direction the experimental record agrees on: mismatches near the PAM are tolerated far less than
# mismatches at the 5' distal end of the spacer (Hsu et al., 2013). Index 0 is the 5' distal position,
# index 19 is PAM-proximal.
# ponytail: illustrative weights, swap in the Doench 2016 supplementary table for tool-grade rankings.
CFD_WEIGHTS_ILLUSTRATIVE = np.linspace(0.85, 0.05, 20)

_BASE_CODE = np.zeros(256, dtype=np.int8)
_BASE_CODE[:] = -1
for _i, _b in enumerate(b"ACGT"):
    _BASE_CODE[_b] = _i


def encode(seq):
    """Sequence to a uint8 array of ASCII codes."""
    return np.frombuffer(seq.encode("ascii"), dtype=np.uint8)


def mismatch_count(guide, site):
    """Equation 1: the number of mismatched positions, as an indicator sum.

    Every position counts equally, which the experimental record contradicts; this is the first-pass
    filter that genome-wide search implementations compute (Bae et al., 2014).
    """
    if len(guide) != len(site):
        raise ValueError("guide and site must be the same length")
    return int(sum(g != s for g, s in zip(guide.upper(), site.upper())))


def cfd(guide, site, weights=CFD_WEIGHTS_ILLUSTRATIVE):
    """Equation 2: position-weighted product over mismatched positions.

    Returns a value in (0, 1]; 1.0 means a perfect match. With the illustrative weight vector this is a
    teaching model of the cutting frequency determination score, not the published score.
    """
    if len(guide) != len(site):
        raise ValueError("guide and site must be the same length")
    score = 1.0
    for i, (g, s) in enumerate(zip(guide.upper(), site.upper())):
        if g != s:
            score *= float(weights[i])
    return score


def specificity(cfd_scores):
    """Equation 3: aggregate specificity, bounded above by 100 and falling as off-target load rises.

    S = 100 / (1 + sum of per-site CFD). The perfect-match on-target site is excluded by the caller.
    The aggregation is deliberately crude: it ignores where in the genome each predicted cut falls.
    """
    return 100.0 / (1.0 + float(sum(cfd_scores)))


def pam_spacers(seq, pam="GG"):
    """Every 23-mer window whose positions 22-23 satisfy an NGG requirement (Jinek et al., 2012).

    Returns (start_indices, spacer_matrix) where spacer_matrix[i] is the 20-nt spacer as base codes
    0-3, and any window containing a non-ACGT character is dropped.
    """
    codes = _BASE_CODE[encode(seq)]
    n = len(codes) - 22
    if n <= 0:
        return np.empty(0, dtype=int), np.empty((0, 20), dtype=np.int8)
    windows = np.lib.stride_tricks.sliding_window_view(codes, 23)[:n]
    pam_codes = [_BASE_CODE[ord(c)] for c in pam]
    keep = np.ones(n, dtype=bool)
    for offset, code in enumerate(pam_codes):
        keep &= windows[:, 21 + offset] == code
    keep &= (windows >= 0).all(axis=1)
    return np.flatnonzero(keep), windows[keep][:, :20]


def scan_offtargets(spacer_codes, site_matrix, max_mismatch=4):
    """Vectorised genome scan: mismatch count of one spacer against every candidate site.

    Returns the indices of sites within the mismatch budget and their mismatch counts. The scan is the
    expensive step of Box 1 and is what production implementations optimise (Bae et al., 2014).
    """
    if site_matrix.shape[0] == 0:
        return np.empty(0, dtype=int), np.empty(0, dtype=int)
    counts = (site_matrix != spacer_codes).sum(axis=1)
    hits = np.flatnonzero(counts <= max_mismatch)
    return hits, counts[hits]


def design_guides(target, genome, weights=CFD_WEIGHTS_ILLUSTRATIVE, max_mismatch=4, limit=None):
    """Box 1: guide design with aggregate off-target specificity.

    Slides a 23-nt window over `target`, keeps windows meeting the NGG requirement, scans `genome` for
    sites within the mismatch budget, aggregates their CFD by Equation 3, and returns candidates in
    descending order of S.

    Returns a list of dicts: spacer, position in target, S, off-target site count, and the mismatch
    distribution of those sites.
    """
    t_starts, t_spacers = pam_spacers(target)
    if limit:
        t_starts, t_spacers = t_starts[:limit], t_spacers[:limit]
    _, g_sites = pam_spacers(genome)
    w = np.asarray(weights, dtype=float)
    out = []
    for start, spacer in zip(t_starts, t_spacers):
        hits, counts = scan_offtargets(spacer, g_sites, max_mismatch)
        scores = []
        for idx, mm in zip(hits, counts):
            if mm == 0:
                continue  # the intended site, or an exact duplicate of it, is not an off-target
            mismatched = g_sites[idx] != spacer
            scores.append(float(np.prod(w[mismatched])))
        out.append({
            "spacer": "".join("ACGT"[c] for c in spacer),
            "position": int(start) + 1,
            "S": specificity(scores),
            "n_offtargets": len(scores),
            "mismatch_hist": {int(m): int((counts == m).sum()) for m in range(1, max_mismatch + 1)},
            "exact_sites": int((counts == 0).sum()),
        })
    return sorted(out, key=lambda d: d["S"], reverse=True)


# ---------------------------------------------------------------------------
# Area 2: affinity and constrained generation. Equations 4-6 and Box 2.
# ---------------------------------------------------------------------------

def delta_g(pkd, temperature=T_PHYS):
    """Equation 5: standard free energy of binding from pKd, in kJ/mol.

    Kd = 10^-pKd, and dG = R T ln(Kd), which is negative for any pKd above 0. One log unit of pKd is
    worth R T ln(10), about 5.9 kJ/mol at 37 C.
    """
    return R_GAS * temperature * np.log(10.0 ** (-float(pkd)))


def log_unit_kj(temperature=T_PHYS):
    """Free energy equivalent of one log unit of affinity, the quantity quoted in the Discussion."""
    return R_GAS * temperature * np.log(10.0)


def lipinski(row):
    """Rule-of-five violations from PubChem descriptors (Lipinski et al., 2001).

    Returns (violation_count, list_of_failed_rules). Missing descriptors are reported, not guessed.
    """
    rules = [
        ("MW > 500", row.get("MolecularWeight"), lambda v: v > 500),
        ("XLogP > 5", row.get("XLogP"), lambda v: v > 5),
        ("HBD > 5", row.get("HBondDonorCount"), lambda v: v > 5),
        ("HBA > 10", row.get("HBondAcceptorCount"), lambda v: v > 10),
    ]
    failed = []
    for name, value, test in rules:
        if value is None:
            failed.append(f"{name.split()[0]} missing")
        elif test(value):
            failed.append(name)
    return sum(1 for f in failed if "missing" not in f), failed


# Oral-range property centres and half-widths, from the same rule-of-five statistics (Lipinski et al.,
# 2001) plus the polar-surface and flexibility ranges conventionally applied alongside them.
_RANGES = {
    "MolecularWeight": (350.0, 150.0),
    "XLogP": (2.5, 2.5),
    "HBondDonorCount": (2.5, 2.5),
    "HBondAcceptorCount": (5.0, 5.0),
    "TPSA": (75.0, 65.0),
    "RotatableBondCount": (5.0, 5.0),
}


def penalty(row):
    """The drug-likeness penalty of Equation 6: mean squared distance outside each property range.

    Zero for a molecule inside every range, rising with the extent of the departure. This is a
    transparent distance penalty, not the QED desirability score of Bickerton et al. (2012), which
    would require a cheminformatics toolkit the app deliberately does not depend on.
    ponytail: distance penalty, swap for QED if rdkit becomes available.
    """
    terms = []
    for key, (centre, half) in _RANGES.items():
        value = row.get(key)
        if value is None:
            continue
        excess = max(0.0, abs(float(value) - centre) - half) / half
        terms.append(excess ** 2)
    return float(np.mean(terms)) if terms else float("nan")


def screen(rows, lam=1.0, affinity=None, k=None):
    """Box 2: constrained generative screening loop, run over real candidates instead of samples.

    score = a - lam * penalty(m), where `a` is the Equation 4 affinity term. No trained affinity model
    is shipped, so `a` is taken from `affinity` where the caller supplies a measured value and is
    otherwise 0.0, which is recorded per row in `affinity_known`. With no affinity the ranking is driven
    entirely by the constraint term, which is the point the panel makes.
    """
    affinity = affinity or {}
    out = []
    for row in rows:
        if "error" in row:
            continue
        name = row["name"]
        a = affinity.get(name)
        pen = penalty(row)
        viol, failed = lipinski(row)
        out.append(dict(
            row,
            penalty=pen,
            lipinski_violations=viol,
            lipinski_failed=", ".join(failed) if failed else "none",
            drug_like=viol <= 1,
            affinity=a,
            affinity_known=a is not None,
            score=(a if a is not None else 0.0) - lam * pen,
        ))
    out.sort(key=lambda d: d["score"], reverse=True)
    return out[:k] if k else out


# ---------------------------------------------------------------------------
# Area 3: generative sequence model at genome scale. Equations 7-9 and Box 3.
# ---------------------------------------------------------------------------

class MarkovGenome:
    """An order-k autoregressive nucleotide model, fitted by counting with Laplace smoothing.

    Equation 7 factorises the probability of a genome as a product of per-position conditionals. This
    class uses the same factorisation with a fixed-length context, which is a genuine autoregressive
    model and a very small one. It stands in for the genome language model of Nguyen et al. (2024); its
    log-likelihood values are not comparable to that model's.
    ponytail: order-k count model, swap in a trained genome LM checkpoint for real capacity.
    """

    def __init__(self, order=5, alpha=1.0):
        self.order = int(order)
        self.alpha = float(alpha)
        self.counts = np.zeros((4 ** self.order, 4), dtype=np.float64)
        self.trained_on = []

    @staticmethod
    def _codes(seq):
        c = _BASE_CODE[encode(seq)]
        return c[c >= 0]   # ambiguity codes (N, R, Y...) are dropped, not imputed

    def _contexts(self, codes):
        """Rolling base-4 index of the preceding `order` bases, aligned to the predicted base."""
        k = self.order
        if len(codes) <= k:
            return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.int64)
        windows = np.lib.stride_tricks.sliding_window_view(codes, k)[:-1]
        powers = 4 ** np.arange(k - 1, -1, -1)
        return windows @ powers, codes[k:]

    def fit(self, sequences):
        """Accumulate counts over one or more real training genomes."""
        for name, seq in sequences.items():
            ctx, nxt = self._contexts(self._codes(seq))
            np.add.at(self.counts, (ctx, nxt), 1.0)
            self.trained_on.append(f"{name} ({len(seq):,} bp)")
        return self

    def _probs(self):
        smoothed = self.counts + self.alpha
        return smoothed / smoothed.sum(axis=1, keepdims=True)

    def log_likelihood(self, seq):
        """Equation 8: sum over positions of log p(x_i | x_<i). Returns (total, per_base).

        The sum is what is actually computed, both because the Equation 7 product underflows and
        because the per-base mean is comparable across sequences of different length.
        """
        codes = self._codes(seq)
        ctx, nxt = self._contexts(codes)
        if len(ctx) == 0:
            raise ValueError("sequence shorter than the model order")
        lp = np.log(self._probs()[ctx, nxt])
        return float(lp.sum()), float(lp.mean())

    def per_position(self, seq):
        """The per-position log-probabilities behind Equation 8, for plotting."""
        ctx, nxt = self._contexts(self._codes(seq))
        return np.log(self._probs()[ctx, nxt])

    def sample(self, length, seed_seq, rng=None):
        """Draw a sequence from the fitted model, continuing from a real seed context."""
        rng = rng or np.random.default_rng()
        probs = self._probs()
        ctx_codes = list(self._codes(seed_seq)[:self.order])
        if len(ctx_codes) < self.order:
            raise ValueError("seed shorter than the model order")
        out = []
        powers = 4 ** np.arange(self.order - 1, -1, -1)
        for _ in range(length):
            idx = int(np.dot(ctx_codes[-self.order:], powers))
            nxt = int(rng.choice(4, p=probs[idx]))
            out.append(nxt)
            ctx_codes.append(nxt)
        return "".join("ACGT"[c] for c in out)


def gc_fraction(seq):
    """GC content of a real sequence, ignoring ambiguity codes."""
    codes = _BASE_CODE[encode(seq)]
    codes = codes[codes >= 0]
    if codes.size == 0:
        return float("nan")
    return float(((codes == 1) | (codes == 2)).mean())


def host_fitness_proxy(seq, host_seq):
    """A declared proxy for the f term of Equation 9: closeness of GC content to the target host.

    Returns 1.0 for an exact GC match, falling to 0.0 at maximal divergence. This is NOT a prediction
    of lytic activity. The real f term requires host-range data the app does not have; substituting a
    compositional statistic keeps the arithmetic of Equation 9 runnable while making the substitution
    visible. Treat any ranking it produces as a talking point, not a result.
    ponytail: GC-match proxy, replace with a trained host-range predictor.
    """
    return 1.0 - abs(gc_fraction(seq) - gc_fraction(host_seq))


def design_score(seq, host_seq, model, beta):
    """Equation 9: f + beta * log p(x), with the log-likelihood taken per base.

    beta is the novelty control. High beta pins proposals to the training distribution; low beta lets
    the fitness proxy pull them outside anything the model has grounds to evaluate.
    """
    _, per_base = model.log_likelihood(seq)
    f = host_fitness_proxy(seq, host_seq)
    return {"f": f, "loglik_per_base": per_base, "score": f + beta * per_base}
