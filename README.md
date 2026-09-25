# Algorithmic Perspectives in Bioinformatics: an interactive companion

A Streamlit dashboard that runs the equations and boxed algorithms from the submitted conference proceeding on small curated sets of real records fetched from NCBI.

Three panels, one per application area covered in the paper: CRISPR-Cas guide design, machine-learning
drug screening, and generative bacteriophage design. Each panel states the governing equation, runs it
on real data, and says plainly what it does not model.

No sequence or descriptor in this application is simulated. Everything is fetched from NCBI
E-utilities or PubChem PUG-REST and cached locally.

---

## Why this exists

The submitted paper argues that three areas of biotechnology usually discussed separately share one
computational skeleton: a score over candidate objects, a search over a space too large to enumerate,
and a constraint term that keeps proposals inside a region where laboratory work is plausible. That
argument is easier to believe when you can move the constraint weight and watch the ranking change.

Reading an equation in a submitted paper tells you what a method computes. Running it on a real
*Mycobacterium tuberculosis* gene tells you what the method is like to use, including the parts that
do not work. This dashboard exists for the second kind of understanding, and it was built for teaching
and discussion rather than for production analysis.

The motivation comes from three earlier pieces of work.

Parikesit, Ratnasari and Anurogo (2020) surveyed how artificial-intelligence-based computation was
brought to bear on the COVID-19 pandemic across the health sciences, at a point when the gap between
computational capacity and clinical usefulness was unusually visible. The lesson that carried forward
into this dashboard is that algorithmic output becomes useful only when its calibration is stated
alongside it, which is why every panel here carries a "what this does not model" block rather than
presenting a ranked list on its own.

Widjaja, Wibowo and Parikesit (2025) compared logistic regression against a convolutional neural
network for multi-drug-resistant tuberculosis prediction. Two things in that paper shaped this one.
It is the reason the curated data here are TB resistance genes (*katG*, *rpoB*, *inhA*, *pncA*,
*embB*) and real anti-TB compounds rather than generic demonstration sequences: the local disease
burden is the point. It is also the reason the stand-in models in this dashboard are small and
declared rather than hidden, since that comparison found that a simpler, well-understood model can be
competitive with a deeper one once you account for what each is actually being asked to do.

Valeska et al. (2019) set out the role of bioinformatics in personalised medicine for a clinical
readership. That framing is why the disclaimers in this repository are specific rather than
boilerplate: the distance between a ranked computational candidate and a treatment decision is
several validated steps long, and a dashboard is not one of them.

---

## Conference presentation

The paper this dashboard accompanies was presented at the **III. International Conference on
Engineering Sciences**, https://ices.kongrepark.org/ .

Suggested citation for the proceeding:

> Parikesit, A. A. (2026). Algorithmic perspectives in bioinformatics: A review of computational
> methods interpreting emerging trends in biotechnology. _Status: Accepted_. In *Proceedings of the III. International
> Conference on Engineering Sciences (ICES)*. https://ices.kongrepark.org/

Author: Dr.rer.nat. Arli Aditya Parikesit, Department of Biotechnology, School of Health and Life
Sciences, i3L University, Jakarta, Indonesia. ORCID
[0000-0001-8716-3926](https://orcid.org/0000-0001-8716-3926).

---

## Installation

Requires Python 3.11 or newer. Verified on Python 3.11.5, macOS, 25 September 2026.

```bash
git clone <this-repository>
cd IKSAD-Bioinf-Algo-2026

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Pinned set: `streamlit>=1.57.0`, `pandas>=2.0.0`, `numpy>=1.26.0`, `requests>=2.31.0`. Biopython is
deliberately not a dependency; the NCBI calls are plain HTTP, which keeps the install small.

### Running

```bash
export NCBI_EMAIL="you@institution.edu"    # NCBI asks callers to identify themselves
streamlit run app.py
```

The app opens at http://localhost:8501 (the local computer).

### NCBI usage

Set `NCBI_EMAIL` before the first run. NCBI asks that automated callers identify themselves, and every
request from this app sends both that address and a `tool` string. Requests are throttled to stay
inside the published limits: three per second without an API key, ten with one. To use a key:

```bash
export NCBI_API_KEY="your-key"
```

Responses are cached to `data/ncbi_cache/` on first fetch. The cache is committed, so **the dashboard
opens and every panel computes with no network connection at all**. It also means a live demonstration
does not re-query NCBI on each Streamlit rerun. To refresh, delete the directory and run:

```bash
python3 ncbi.py      # re-fetches everything and prints what it got
```

### Tests

```bash
python3 tests/test_algorithms.py
```

Eleven assert-based checks, no test framework, no fixtures, no network. Runs in under a second and
reads the committed cache. Exit code is non-zero on failure.

---

## The curated data

| Panel | NCBI resource | Records |
|---|---|---|
| CRISPR-Cas | E-utilities `efetch`, db=nuccore | *M. tuberculosis* H37Rv `NC_000962.3`, five drug-resistance genes with coordinates taken from NCBI Gene: *katG* (Rv1908c, 2223 bp), *rpoB* (Rv0667, 3519 bp), *inhA* (Rv1484, 810 bp), *pncA* (Rv2043c, 561 bp), *embB* (Rv3795, 3297 bp) |
| Drug screening | PubChem PUG-REST | Twelve real antibacterial agents: isoniazid, rifampicin, ethambutol, pyrazinamide, bedaquiline, ciprofloxacin, moxifloxacin, linezolid, delamanid, clofazimine, streptomycin, amikacin |
| Phage design | E-utilities `efetch`, db=nuccore | Training: phage lambda `NC_001416.1`, T7 `NC_001604.1`, *Mycobacterium* phage D29 `NC_001900.1`. Held out: T4 `NC_000866.4`. Non-phage control: *Y. pestis* plasmid pPCP1 `NC_005816.1` |

Gene coordinates were read from NCBI Gene rather than transcribed from literature, and the fetched
lengths match the annotated coding sequences. *katG* and *pncA* are on the minus strand, which the
data layer records explicitly.

The off-target search space is a declared 200 kb window around each gene, not the full 4.41 Mb genome.
That keeps the committed cache to about 1.4 MB. Specificity values are therefore window-local, and the
panel says so on screen.

---

## What each panel computes

### Panel 1: CRISPR-Cas guide design (Equations 1 to 3, Box 1)

Runs the full Box 1 loop on a real gene: slides a 23-nucleotide window, keeps windows meeting the NGG
requirement, scans the surrounding genomic window for sites within a mismatch budget, and ranks
candidates by aggregate specificity.

- Equation 1, mismatch count as an indicator sum: computed exactly.
- Equation 2, position-weighted product: **the positional weights are illustrative, not the published
  CFD table.** Doench et al. (2016) give a weight per position *and* per substituted base, estimated
  from measured cleavage at mismatch panels. That table is not reproduced here from recall. The vector
  shipped encodes only the direction the experimental record agrees on (Hsu et al., 2013): mismatches
  near the PAM are tolerated least. Substitute the published supplement before trusting any ranking.
- Equation 3, aggregate specificity bounded by 100: computed exactly as written.

Not modelled: chromatin accessibility, delivery efficiency, repair outcome at the intended site, and
the genomic context of each predicted off-target cut. Equation 3 penalises a predicted cut in an
essential exon and one in an intergenic region identically. Pooled screen analysis is a separate
count-based statistical problem and is not part of this panel.

### Panel 2: Constrained generative screening (Equations 4 to 6, Box 2)

- Equation 5, free energy from pKd: computed exactly, with temperature adjustable. This makes the
  paper's "one log unit is worth about 6 kJ/mol" statement something you can move a slider to check.
- Equation 6 constraint term: computed from real PubChem descriptors. Rule-of-five violations follow
  Lipinski et al. (2001); the penalty is a transparent mean-squared-distance-outside-range term, not
  the QED desirability score, which would require a cheminformatics toolkit this app does not depend on.
- Equation 4, predicted affinity: **not modelled.** No trained drug-target affinity network is
  shipped and none is invented, so the affinity column stays empty and the lambda slider drives the
  ranking through the constraint term alone.

That last gap is less of a loss than it sounds. The point Equation 6 makes is that unconstrained
maximisation of a learned score reliably produces molecules that score well and cannot be made, and
the constraint term is what prevents it. That is visible without an affinity model. The table also
shows rifampicin and bedaquiline failing the rule of five while being clinically used drugs, which is
a useful reminder that a property filter is a statistical statement, not a verdict.

### Panel 3: Generative phage design (Equations 7 to 9, Box 3)

An order-k Markov model over nucleotides, fitted by counting on the three real training genomes with
Laplace smoothing. This uses the same factorisation as Equation 7 and is a genuine autoregressive
model. It is also a very small one, and it stands in for the genome language model the paper cites;
its log-likelihood values are not comparable to that model's.

- Equations 7 and 8: computed for real. Conditionals are verified to normalise; the per-base mean is
  what the panel plots, since the Equation 7 product underflows.
- Equation 9: the arithmetic is exact, but the host fitness term **f is a declared stand-in**, namely
  GC-content match to the host genome. The real term needs host-range data this app does not have.
  Any ranking it produces is a talking point, not a prediction of lytic activity.
- Box 3's `structure_valid()` filter is **not implemented**. It needs a fast structure predictor over
  every encoded protein. Candidates drawn in the panel are therefore unscreened for fold, and
  sequence plausibility and structural viability are different properties.

### A negative result, reported rather than tuned away

The order-k model does not separate phage from non-phage. The non-phage control outscores the held-out
phage genome at every model order tested:

| Model order | Held-out T4 phage | Non-phage control (pPCP1) |
|---|---|---|
| k = 1 | -1.4205 | **-1.3951** |
| k = 3 | -1.4130 | **-1.3879** |
| k = 5 | -1.4329 | **-1.3982** |

Values are nats per base; higher is better. The reason is compositional. The training genomes run
48.4% to 63.5% GC, the control plasmid at 45.3% sits inside that range, and T4 at 35.3% is the
outlier. A count model learns composition, not phage identity.

This is left in place, and the panel displays it, because it demonstrates the paper's argument about
Equation 9 better than a success would have: a plausibility score that has not been anchored to
independent measurement cannot be read as a prediction. `test_eq8_is_confounded_by_composition`
asserts the observed direction, so if a trained genome language model is ever substituted the check
will fail loudly and prompt a rewrite rather than passing silently.

---

## Known ceilings

Each is marked in the source with a `ponytail:` comment naming the ceiling and the upgrade path.

| Ceiling | Consequence | Upgrade path |
|---|---|---|
| Illustrative positional weights, not the Doench 2016 CFD table | Guide rankings are indicative, not tool-grade | Load the published supplementary weight table |
| No trained affinity model | Equation 4 column is empty; ranking is constraint-driven | Load a published drug-target affinity checkpoint |
| Order-k count model, not a genome language model | Equation 8 values are far from a trained model's, and confounded by GC | Substitute a genome LM checkpoint |
| Host fitness is a GC-match proxy | Equation 9's f term is a placeholder | Use a trained host-range predictor |
| Off-target scan over a 200 kb window | Specificity values are window-local | Index the full 4.41 Mb genome |
| No `structure_valid()` filter | Phage candidates are unscreened for fold | Add a fast structure prediction pass |

## Repository layout

```
app.py                     Streamlit dashboard, four tabs
algos.py                   Equations 1 to 9 and Boxes 1 to 3, pure functions
ncbi.py                    NCBI access, throttling, on-disk cache
tests/test_algorithms.py   Eleven assert-based checks, offline
requirements.txt
data/ncbi_cache/           Committed NCBI payloads, about 1.4 MB
figures/                   Figures from the proceeding build
plan.md                    Development plan for this dashboard
plan-manuscript.md         Earlier plan for the manuscript itself
```

---

## Disclaimers

### Prototype status

**This software is a prototype built to illustrate a conference paper. It is not a validated
analytical tool and its output must not be taken for granted.**

Three of its components are declared stand-ins for methods it cannot run offline, as set out above.
Guide rankings, compound rankings and genome scores produced here are teaching illustrations. They are
not fit for experimental prioritisations without substituting the real models named in the upgrade
table, and even then computational output remains hypothesis-generating and requires experimental
validation.

### No clinical translation

**Nothing in this repository may be used for clinical, diagnostic, therapeutic or patient-facing
purposes.** No component has been clinically validated, and the dashboard is not a medical device.

Any work extending this toward human subjects, patient data or clinical decision-making requires
ethical clearance from the appropriate institutional review board or research ethics committee before
it begins. Work with engineered lytic phages additionally carries biosafety obligations and
institutional biosafety committee approval that compound screening does not.

### AI Assistance Disclaimer

AI Assistance Disclaimer: This codebase was developed with the assistance of Claude Code. While the AI
provided code generation, debugging, and structural support, the human developer maintains full
responsibility for reviewing, testing, and maintaining all content and functionality

---

## References

Citations that motivated this dashboard, as supplied by the author:

1. Parikesit, A. A., Ratnasari, N. R. P., & Anurogo, D. (2020). Application of Artificial
   Intelligence-Based Computation in the Health Sciences to Ward off the COVID-19 Pandemic.
   *International Journal of Human and Health Sciences (IJHHS)*, *5*(2), 177.
   https://doi.org/10.31344/ijhhs.v5i2.256
2. Widjaja, A., Wibowo, S., & Parikesit, A. A. (2025). THE COMPARISON BETWEEN LOGISTIC REGRESSION AND
   CONVOLUTIONAL NEURAL NETWORK FOR MULTI-DRUG RESISTANT TUBERCULOSIS PREDICTION. *Jurnal
   Bioteknologi Dan Biosains Indonesia*, *12*(1), 31–44. https://doi.org/10.55981/jbbi.2025.9769
3. Valeska, M. D., Adisurja, G. P., Bernard, S., Wijaya, R., Aldino, M., & Parikesit, A. A. (2019).
   The Role of Bioinformatics in Personalized Medicine: Your Future Medical Treatment. *Cermin Dunia
   Kedokteran*, *46*(12), 785–788. https://doi.org/10.5281/zenodo.4460835

## Note
- Paper will be posted in this repository as soon as it is published
- Methodological sources for the equations implemented here are cited in the module docstrings of `algos.py` and `ncbi.py`, and in full in the proceeding itself.
