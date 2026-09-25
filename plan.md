# Plan: Streamlit dashboard for the IKSAD bioinformatics-algorithm proceeding

**Target:** runnable Streamlit app in this folder, one panel per algorithm from the manuscript, each panel
driven by a small curated real dataset pulled from NCBI over the public API.

**Source of truth for content:** `IKSAD-Bioalgo-Manuscript-Arli.docx` (Equations 1-9, Boxes 1-3, Table 3).
Nothing new is invented; the app is an executable reading of what the paper already states.

**Note:** the previous `plan.md` (manuscript build plan, logged in MEMORY.md) was renamed to
`plan-manuscript.md`. Nothing was deleted.

---

## 0. Environment, already verified

| Item | Status |
|---|---|
| Python | 3.11.5 |
| streamlit | 1.57.0 installed |
| biopython | 1.84 installed (`Bio.Entrez`, `Bio.SeqIO`) |
| pandas / numpy / requests | 3.0.2 / 1.26.4 / 2.31.0 installed |
| rdkit | NOT installed, and will not be added (no new dependency; PubChem returns precomputed descriptors) |
| NCBI E-utilities | `einfo.fcgi` HTTP 200; `efetch` on NC_005816.1 returns FASTA |
| NCBI PubChem PUG-REST | HTTP 200; returns MolecularWeight, XLogP, HBD, HBA, TPSA per compound |
| Sandbox note | outbound hosts `eutils.ncbi.nlm.nih.gov` and `pubchem.ncbi.nlm.nih.gov` must be allowed when run from inside the Claude sandbox; no restriction when the user runs it in their own shell |

---

## 1. Files to create (4 code files, 2 support files)

```
app.py                     # Streamlit entry: sidebar + 4 tabs
ncbi.py                    # all network access, on-disk cache, Entrez etiquette
algos.py                   # the algorithms, pure functions, no Streamlit import
tests/test_algorithms.py   # one runnable check per algorithm (assert-based, no framework)
requirements.txt
README.md
data/ncbi_cache/           # committed pre-fetched payloads so the app opens offline
```

Deliberately NOT created: Streamlit multipage `pages/` directory (tabs cover it), config classes,
plugin registry, Dockerfile, separate figure module. `figures/fig2_synthesis.png` from the manuscript
build is reused as-is on the overview tab rather than regenerated.

---

## 2. Data, real and curated (no simulated sequences)

| Panel | NCBI resource | Accession / query | Why this record |
|---|---|---|---|
| 1. CRISPR-Cas | E-utilities `efetch`, db=nuccore | `NC_000898.1` region + user-selectable from a fixed list incl. *M. tuberculosis* H37Rv `NC_000962.3` gene slices (e.g. *katG*, *rpoB*, *inhA*) | TB drug-resistance genes are the local research context; real PAM density and real off-target load in the real H37Rv genome |
| 1. off-target scan | same H37Rv record, fetched once, cached | full 4.4 Mb genome is too large for a cached demo, so a declared 200 kb window around each gene is used as the search space | keeps the demo honest: the panel states the search space is a window, not the whole genome |
| 2. Drug discovery | PubChem PUG-REST `property` endpoint | fixed list of ~12 real anti-TB / antibacterial compounds by name (isoniazid, rifampicin, ethambutol, pyrazinamide, bedaquiline, ciprofloxacin, moxifloxacin, linezolid, delamanid, clofazimine, streptomycin, amikacin) | real measured/curated descriptors (MW, XLogP, HBD, HBA, TPSA), so the Lipinski and drug-likeness terms of Equation 6 run on real chemistry |
| 3. Phage design | E-utilities `efetch`, db=nuccore | training set: 3 real phage genomes (lambda `NC_001416.1`, T7 `NC_001604.1`, Mycobacteriophage D29 `NC_001900.1`); held-out test: T4 `NC_000866.4` vs a non-phage control (*Y. pestis* plasmid pPCP1 `NC_005816.1`) | lets Equation 8 be computed for real, on real genomes, and compared between a phage and a non-phage sequence |

All accessions are re-verified by fetch during implementation. Any that does not resolve is replaced and
the substitution recorded here before the app ships. NCBI etiquette: `tool=` and `email=` set on every
request, <=3 requests/second, responses cached to `data/ncbi_cache/` keyed by accession so a
demonstration never hammers the API.

---

## 3. Panel-by-panel: what is computed, and what is honestly out of reach

### Tab 0 - Overview
Static: the shared skeleton claim (score + search + constraint), Table 3 rendered from the manuscript,
`figures/fig2_synthesis.png`, and the prototype disclaimer. No computation.

### Tab 1 - CRISPR-Cas guide design (Equations 1-3, Box 1)
Fully implementable on real data, no modelling gap.
- Eq 1: mismatch count as an indicator sum, exact.
- Eq 2: CFD as a position-weighted product. **The published Doench 2016 weight table is not reproduced
  from memory.** The app ships a declared, clearly labelled monotonic positional weight vector
  (tolerance rising towards the 5' distal end, as Hsu 2013 reports) and says on screen that it is an
  illustrative stand-in, that the real CFD table must be taken from the published supplement, and that
  rankings will differ. This is the one place the panel is a teaching model rather than the tool.
- Eq 3: aggregate specificity S = 100 / (1 + sum of per-site CFD), exact as written in the paper.
- Box 1: the sliding-window PAM scan and ranking loop, run live on the real fetched sequence.
- On-screen: candidate table sorted by S, PAM-site histogram, the pseudocode box verbatim from the paper,
  and a stated-limits panel (no chromatin accessibility, no delivery, no repair outcome).

### Tab 2 - Constrained generative screening (Equations 4-6, Box 2)
- Eq 5: ΔG = -RT ln(1/Kd) computed exactly; the user moves a pKd slider and reads kJ/mol, which makes
  the "one log unit ≈ 5.7 kJ/mol" statement in the paper interactive and needs no model at all.
- Eq 6 constraint term: computed for real from the real PubChem descriptors (Lipinski Ro5 violations +
  a transparent property-distance penalty), so `penalty(m)` in Box 2 is live on real chemistry.
- Eq 4 score term: **no trained affinity model is shipped and none is faked.** The panel exposes the
  real measured/reported activity where the curated list has one, and otherwise leaves the affinity
  column empty with the label "not modelled in this prototype". The λ slider then shows how the ranking
  moves as the constraint weight changes. The scientific point of the panel is exactly that: an
  unconstrained score produces unmakeable molecules, which is visible without inventing an affinity net.
- On-screen: property table, Ro5 pass/fail, ranking under varying λ, Box 2 pseudocode, stated limits.

### Tab 3 - Generative phage design (Equations 7-9, Box 3)
- Eq 7/8: a genuine autoregressive model, order-k Markov chain with Laplace smoothing, fitted by counting
  on the real phage training genomes. Eq 8 (sum of per-position log-probabilities) is then computed for
  real. Held-out T4 genome vs the non-phage control gives a real, checkable separation in mean
  log-likelihood per base.
- This is an order-k count model, not a genome language model. The panel says so plainly: same
  factorisation as Equation 7, far less capacity, and it stands in for the trained model the paper cites.
- Eq 9 (f + β·log p): the host-fitness term f has no offline ground truth, so it is **not fabricated**.
  The β slider instead operates on a real, computable quantity, GC-content match to the target host
  genome, which is declared on screen as a crude proxy and not as a lytic-activity prediction.
- Box 3 loop shown; sampling from the fitted Markov model demonstrates the novelty-control behaviour of
  β (high β returns near-copies of training genomes, low β drifts) on real training data.
- Structural viability filter: the paper's `structure_valid()` needs ESMFold. Not shipped. The panel
  states that the filter is omitted and what its omission means.

Every panel carries a short "what this does not model" block. That is the paper's own argument applied
to the app.

---

## 4. The one runnable check (ponytail rule)

`tests/test_algorithms.py`, assert-based, no pytest fixtures, runs in seconds with no network by reading
the committed cache:
1. Eq 1 mismatch count on a hand-checked pair.
2. Eq 3 monotonicity: adding an off-target site strictly lowers S; S is bounded in (0, 100].
3. PAM scan finds exactly the known NGG sites in a short hand-written sequence.
4. Eq 5 round-trip: pKd 6 -> ΔG within 0.1 kJ/mol of the hand-computed value; 1 log unit ≈ 5.7 kJ/mol.
5. Lipinski count on a known-failing and known-passing real compound from the cache.
6. Eq 8: log-likelihood is negative, order-k model scores held-out phage above the non-phage control,
   and probabilities at each position sum to 1 within 1e-9.

If the model in 6 does not separate phage from control, that is reported as a negative result in the
README rather than tuned until it looks good.

---

## 5. README.md contents (instruction 4, 5, 6, 7, 8)

- What the app is, and that it is an executable companion to the proceeding, not a tool for production use.
- Install: venv, `pip install -r requirements.txt`, `streamlit run app.py`. Python 3.11+, versions pinned
  to what was verified above.
- NCBI usage policy, the `NCBI_EMAIL` environment variable, rate limits, and how the cache works offline.
- Background and motivation, with contextual citation of the three requested papers:
  - Parikesit, Ratnasari & Anurogo (2020) on AI-based computation in health sciences, for why algorithmic
    methods moved to the centre of pandemic-era biomedical response;
  - Widjaja, Wibowo & Parikesit (2025) comparing logistic regression and CNN for MDR-TB prediction, for
    why the TB drug-resistance genes and anti-TB compounds were chosen as the curated data, and for the
    "simpler calibrated model can match a deeper one" point that the dashboard's own stand-in models make;
  - Valeska et al. (2019) on bioinformatics in personalised medicine, for the translational framing and
    for why clinical claims need ethics review rather than a dashboard.
- Conference statement: presented at the III. International Conference on Engineering Sciences,
  https://ices.kongrepark.org/ , with the proceeding citation for the manuscript in this repository.
- Per-algorithm section: equation, what the panel computes, what it does not model.
- Prototype and clinical disclaimer: not validated, not for clinical translation, ethical clearance
  required for any human-subject or clinical use, computational output is hypothesis-generating only.
- AI Assistance Disclaimer, verbatim as CLAUDE.md requires.
- The three citations are re-validated against Crossref/DOI before the README ships; the two DOIs already
  flagged as odd (`10.11594/jbbi.12.1` looks like an issue-level rather than article-level DOI, and
  `10.5281/zenodo.4460835` is a Zenodo deposit rather than a journal DOI) are reported as given by the
  user with a note, not silently corrected.

---

## 6. Order of work

1. `ncbi.py` + verify every accession resolves; populate `data/ncbi_cache/`.
2. `algos.py` + `tests/test_algorithms.py`; run the checks; fix or report.
3. `app.py` tabs 0-3.
4. Launch `streamlit run app.py`, confirm it renders and each tab computes.
5. `README.md` + `requirements.txt`; validate the three citations.
6. Append the decision block to MEMORY.md.

## 7. Known ceilings, stated once

| Ceiling | Consequence | Upgrade path |
|---|---|---|
| Illustrative CFD weights, not the Doench table | guide rankings are indicative, not tool-grade | drop in the published supplement table |
| No trained affinity model | Equation 4 column is empty, ranking driven by the constraint term | load a published DTA checkpoint |
| Order-k Markov model, not a genome LM | Equation 8 values are far from a real LM's | swap in Evo or an equivalent checkpoint |
| Host fitness is GC-content match | Equation 9's f term is a placeholder proxy, declared as such | real host-range predictor |
| Off-target search over a declared window, not whole genome | specificity values are window-local | index the full genome |
| No `structure_valid()` filter | phage candidates are unscreened for fold | ESMFold pass over encoded proteins |
