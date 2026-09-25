#!/usr/bin/env python3
"""
Module: app
Purpose: Streamlit dashboard for the three algorithm families of the IKSAD proceeding.
Author: Dr. Arli Aditya Parikesit
Date: 2026
Parameters:
    - NCBI_EMAIL: environment variable, forwarded to NCBI with every request
Usage:
    streamlit run app.py
References:
    - Companion to IKSAD-Bioalgo-Manuscript-Arli.docx, presented at the III. International
      Conference on Engineering Sciences (https://ices.kongrepark.org/)
"""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

import algos
import ncbi

HERE = Path(__file__).parent

st.set_page_config(page_title="Bioinformatics Algorithms Dashboard", page_icon=":material/biotech:", layout="wide")


def limits(text):
    """Every panel states what it does not model. That is the paper's argument applied to the app."""
    st.warning(f"**What this does not model.** {text}", icon=":material/warning:")


@st.cache_data(show_spinner="Fetching from NCBI…")
def load_gene(label):
    return ncbi.gene_window(label)


@st.cache_data(show_spinner="Fetching from NCBI…")
def load_genome(accession):
    return ncbi.fasta(accession)


@st.cache_data(show_spinner="Fetching from PubChem…")
def load_compounds():
    return ncbi.compound_properties()


@st.cache_resource(show_spinner="Fitting the order-k model…")
def fit_model(order):
    train = {n: load_genome(a)[1] for n, a in ncbi.PHAGE_TRAIN.items()}
    return algos.MarkovGenome(order=order).fit(train), train


# --------------------------------------------------------------------------- sidebar
with st.sidebar:
    st.header("Data provenance")
    st.caption(
        "Every sequence and descriptor on this dashboard is fetched from NCBI. Nothing is simulated "
        "and nothing is hand-entered."
    )
    st.markdown(
        f"""
- **Genome editing**: *M. tuberculosis* H37Rv `{ncbi.H37RV}`, E-utilities `efetch`
- **Drug screening**: {len(ncbi.COMPOUNDS)} real antibacterial agents, PubChem PUG-REST
- **Phage design**: {len(ncbi.PHAGE_TRAIN)} phage genomes + held-out T4 + non-phage control
"""
    )
    cached = len(list((HERE / "data" / "ncbi_cache").glob("*"))) if (HERE / "data" / "ncbi_cache").exists() else 0
    st.metric("Records in local cache", cached)
    st.caption(
        "Responses are cached on disk, so the dashboard opens without network access and a "
        "demonstration does not re-query NCBI on every rerun."
    )
    st.divider()
    st.caption(
        "**Prototype.** Not validated for any clinical, diagnostic or therapeutic use. "
        "Ethical clearance is required before any of this informs work on human subjects."
    )


st.title("Algorithmic Perspectives in Bioinformatics")
st.caption(
    "An executable companion to the conference proceeding. Each panel runs one of the paper's "
    "equations on a small curated set of real NCBI records."
)

tab0, tab1, tab2, tab3 = st.tabs([
    "Overview", "1. CRISPR-Cas guide design", "2. Constrained screening", "3. Phage design",
])

# --------------------------------------------------------------------------- overview
with tab0:
    st.subheader("One skeleton, three application areas")
    st.markdown(
        "The paper's claim is that three areas usually discussed separately run on the same "
        "computational skeleton: **a score** over candidate objects, **a search** over a space too "
        "large to enumerate, and **a constraint term** that keeps proposals inside a region where "
        "laboratory work is plausible. Remove the constraint term in any of the three and you get "
        "high-scoring proposals that fail in the laboratory."
    )
    st.dataframe(pd.DataFrame([
        {"Component": "Candidate object", "CRISPR-Cas": "20-nt spacer next to an NGG motif",
         "Drug discovery": "Small molecule", "Phage design": "Complete phage genome"},
        {"Component": "Score", "CRISPR-Cas": "Aggregate specificity S (Eq. 3)",
         "Drug discovery": "Predicted affinity, log scale (Eq. 4)",
         "Phage design": "Host fitness + model log-likelihood (Eq. 9)"},
        {"Component": "Constraint term", "CRISPR-Cas": "Summed CFD over predicted off-target sites",
         "Drug discovery": "Drug-likeness penalty, weight λ",
         "Phage design": "Model log-likelihood, weight β"},
        {"Component": "Search procedure", "CRISPR-Cas": "Window enumeration + genome scan",
         "Drug discovery": "Rejection sampling from a generative model",
         "Phage design": "Rejection sampling + structural viability filter"},
        {"Component": "Training signal", "CRISPR-Cas": "Measured cleavage at mismatch panels",
         "Drug discovery": "Measured binding constants",
         "Phage design": "Natural phage and prokaryotic genomes"},
        {"Component": "Calibration maturity", "CRISPR-Cas": "High", "Drug discovery": "Moderate",
         "Phage design": "Low"},
        {"Component": "Cost of one test", "CRISPR-Cas": "Days", "Drug discovery": "Months",
         "Phage design": "Months to years, with containment"},
    ]), hide_index=True, width="stretch")

    fig2 = HERE / "figures" / "fig2_synthesis.png"
    if fig2.exists():
        st.image(str(fig2), caption="Figure 2 from the proceeding: shared analyse-to-generate structure.")

    st.subheader("How to read the three panels")
    st.markdown(
        "The paper argues that reporting practice, not model capacity, is the limiting factor for "
        "reproducibility. This dashboard holds itself to that standard: where a component of an "
        "equation cannot be computed honestly from open data on a laptop, the panel says so on screen "
        "rather than substituting a plausible-looking number. Three such gaps exist, and each is "
        "labelled where it occurs:"
    )
    st.dataframe(pd.DataFrame([
        {"Equation": "Eq. 2 (CFD)", "Shipped here": "Illustrative monotonic positional weights",
         "The real thing": "Doench et al. 2016 per-position, per-substitution table",
         "Consequence": "Rankings are indicative, not tool-grade"},
        {"Equation": "Eq. 4 (affinity)", "Shipped here": "No model; the column stays empty",
         "The real thing": "A trained drug-target affinity network",
         "Consequence": "Ranking is driven by the constraint term alone"},
        {"Equation": "Eq. 9 (host fitness f)", "Shipped here": "GC-content match to the host genome",
         "The real thing": "A trained host-range predictor",
         "Consequence": "Scores are a talking point, not a prediction of lytic activity"},
    ]), hide_index=True, width="stretch")

# --------------------------------------------------------------------------- CRISPR
with tab1:
    st.subheader("Equations 1-3 and Box 1, on a real *M. tuberculosis* resistance gene")
    st.markdown(
        "Guide design is the most mature of the three areas: its scoring functions are fitted to "
        "measured cleavage, and independent assays exist that measure the same outcome another way. "
        "The genes offered here are the ones that carry drug resistance in *M. tuberculosis*, "
        "which is the local research context for this work."
    )

    col_a, col_b = st.columns([3, 2])
    with col_a:
        gene_label = st.selectbox("Target gene (NCBI Gene, real coordinates)", list(ncbi.TB_GENES))
    with col_b:
        max_mm = st.slider("Mismatch budget for the off-target scan", 1, 5, 4)
        n_guides = st.slider("Candidate guides to score", 5, 100, 30, step=5)

    w = load_gene(gene_label)
    g = ncbi.TB_GENES[gene_label]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Gene length", f"{len(w['gene']):,} bp")
    c2.metric("Search window", f"{len(w['window']):,} bp")
    c3.metric("Strand", w["strand"])
    c4.metric("NCBI Gene ID", g["gene_id"])
    st.caption(
        f"`{ncbi.H37RV}`:{w['window_start']:,}-{w['window_stop']:,}, gene at "
        f"{w['gene_start']:,}-{w['gene_stop']:,}. The window, not the full 4.41 Mb genome, is the "
        "off-target search space, so every specificity value below is window-local."
    )

    st.info(
        "**Equation 2 uses illustrative weights.** The published CFD table gives a weight per position "
        "*and per substituted base*, estimated from measured cleavage at mismatch panels. It is not "
        "reproduced here from recall. The vector below encodes only the direction the experimental "
        "record agrees on (Hsu et al., 2013): PAM-proximal mismatches are tolerated least. Substitute "
        "the published supplement before using any ranking for real work.",
        icon=":material/info:",
    )
    st.bar_chart(
        pd.DataFrame({"tolerance weight": algos.CFD_WEIGHTS_ILLUSTRATIVE},
                     index=pd.Index(range(1, 21), name="spacer position (20 = PAM-proximal)")),
        height=180,
    )

    if st.button("Run Box 1 on this gene", type="primary"):
        with st.spinner("Scanning the window for off-target sites…"):
            guides = algos.design_guides(w["gene"], w["window"], max_mismatch=max_mm, limit=n_guides)
        if not guides:
            st.error("No NGG site found in this gene, which should not happen; check the fetched record.")
        else:
            df = pd.DataFrame(guides)
            df["mismatch_hist"] = df["mismatch_hist"].apply(
                lambda d: ", ".join(f"{k}mm:{v}" for k, v in d.items() if v))
            st.dataframe(
                df.rename(columns={
                    "spacer": "Spacer (20 nt)", "position": "Position in gene",
                    "S": "S (Eq. 3)", "n_offtargets": "Off-target sites",
                    "mismatch_hist": "By mismatch count", "exact_sites": "Exact matches in window"}),
                hide_index=True, width="stretch",
                column_config={"S (Eq. 3)": st.column_config.NumberColumn(format="%.2f")},
            )
            k1, k2, k3 = st.columns(3)
            k1.metric("Best S", f"{df['S'].max():.2f}")
            k2.metric("Median S", f"{df['S'].median():.2f}")
            k3.metric("Guides with zero off-targets", int((df["n_offtargets"] == 0).sum()))
            st.bar_chart(df.set_index("position")[["S"]], height=220,
                         x_label="position in gene", y_label="aggregate specificity S")

    with st.expander("Box 1: Guide design with aggregate off-target specificity (verbatim)"):
        st.code("""design_guides(target, genome, w):
    guides = []
    for window in slide(target, length = 23):        # 20 nt spacer + NGG motif
        if window[21:23] != "GG":                    # motif requirement not met
            continue
        g  = window[0:20]
        OT = scan_offtargets(g, genome, max_mismatch = 4)
        S  = 100 / (1 + sum(cfd(g, s, w) for s in OT))
        guides.append((g, S))
    return sort(guides, by = S, descending = True)""", language="text")
        st.latex(r"m(g, s) = \sum_{i=1}^{20} \mathbb{1}[g_i \neq s_i]")
        st.latex(r"\mathrm{CFD}(g, s) = \prod_{i \,:\, g_i \neq s_i} w_i")
        st.latex(r"S(g) = \frac{100}{1 + \sum_{s \in \mathrm{OT}(g)} \mathrm{CFD}(g, s)}")

    limits(
        "The specificity value is a prediction from a model of cleavage, and it says nothing about "
        "chromatin accessibility, delivery efficiency or repair outcome at the intended site. "
        "Aggregation by Equation 3 ignores *where* each predicted cut falls, so a predicted cut in an "
        "essential exon and one in an intergenic region carry the same penalty. Genome-wide "
        "double-strand break mapping remains the only way to confirm a highly ranked guide behaves as "
        "ranked. Pooled screen analysis is a separate count-based statistical problem, not shown here."
    )

# --------------------------------------------------------------------------- screening
with tab2:
    st.subheader("Equations 4-6 and Box 2, on real PubChem descriptors")

    st.markdown("#### Equation 5: what one log unit of affinity is worth")
    st.markdown(
        "Affinity is quoted on a logarithmic scale because that is the scale on which model error is "
        "roughly constant, and because it maps directly onto a free energy. Move the slider to see "
        "why a model accurate to one log unit is accurate to roughly 6 kJ/mol, which is the "
        "difference between a promising and an uninteresting compound."
    )
    cc1, cc2 = st.columns([2, 3])
    with cc1:
        pkd = st.slider("pK_d", 3.0, 12.0, 7.0, 0.1)
        temp = st.slider("Temperature (K)", 277.0, 320.0, 310.15, 0.15)
    with cc2:
        m1, m2 = st.columns(2)
        m1.metric("ΔG° (Eq. 5)", f"{algos.delta_g(pkd, temp):.1f} kJ/mol")
        m2.metric("Per log unit", f"{algos.log_unit_kj(temp):.2f} kJ/mol")
        st.latex(r"\Delta G^\circ = RT \ln K_d, \qquad K_d = 10^{-pK_d}")
    st.divider()

    st.markdown("#### Equation 6: the constraint term, on real chemistry")
    st.error(
        "**Equation 4 is not modelled in this prototype.** No trained drug-target affinity network is "
        "shipped, and none is invented, so the affinity column below stays empty and the ranking is "
        "driven entirely by the constraint term. That is not a workaround: the point Equation 6 makes "
        "is that unconstrained maximisation of a learned score reliably yields molecules that score "
        "well and cannot be made, and the constraint term is visible here without an affinity model.",
        icon=":material/block:",
    )
    lam = st.slider("lambda, weight on the drug-likeness penalty", 0.0, 10.0, 1.0, 0.25)
    rows = load_compounds()
    missing = [r["name"] for r in rows if "error" in r]
    if missing:
        st.warning(f"PubChem did not return descriptors for: {', '.join(missing)}")
    ranked = algos.screen(rows, lam=lam)
    df = pd.DataFrame([{
        "Compound": r["name"], "CID": r.get("CID"),
        "MW": r.get("MolecularWeight"), "XLogP": r.get("XLogP"),
        "HBD": r.get("HBondDonorCount"), "HBA": r.get("HBondAcceptorCount"),
        "TPSA": r.get("TPSA"), "RotB": r.get("RotatableBondCount"),
        "Ro5 violations": r["lipinski_violations"], "Failed rules": r["lipinski_failed"],
        "penalty(m)": r["penalty"],
        "Affinity (Eq. 4)": "not modelled",
        "score = a − λ·penalty": r["score"],
    } for r in ranked])
    st.dataframe(
        df, hide_index=True, width="stretch",
        column_config={
            "penalty(m)": st.column_config.NumberColumn(format="%.4f"),
            "score = a − λ·penalty": st.column_config.NumberColumn(format="%.4f"),
            "MW": st.column_config.NumberColumn(format="%.2f"),
        },
    )
    st.caption(
        "Descriptors are PubChem's curated values, fetched by compound name; CID links every row to a "
        "real source record. Ro5 thresholds follow Lipinski et al. (2001); `penalty(m)` is a "
        "transparent mean-squared-distance-outside-range term, not the QED score, which would need a "
        "cheminformatics toolkit this app deliberately does not depend on."
    )
    st.bar_chart(df.set_index("Compound")[["penalty(m)"]], height=240)

    with st.expander("Box 2: Constrained generative screening loop (verbatim)"):
        st.code("""discover(target, N, k, lambda_):
    pool = []
    repeat N times:
        m = generator.sample()                        # propose a structure
        if not drug_like(m):                          # property filter, Eq. 6 penalty
            continue
        a = model.predict(m, target)                  # predicted pKd, Eq. 4
        pool.append((m, a - lambda_ * penalty(m)))
    top = sort(pool, by = score, descending = True)[:k]
    return top                                        # hand off to wet-lab assay""", language="text")
        st.latex(r"\hat{a}_\theta(m, t) = -\log_{10} K_d^{\text{pred}}")
        st.latex(r"m^\star = \arg\max_m \left[ \hat{a}_\theta(m, t) - \lambda \cdot \mathrm{penalty}(m) \right]")

    limits(
        "There is no generator and no affinity model here, so this is the loop's *filter and rank* "
        "stage over a fixed real candidate list, not de novo design. Rule-of-five compliance is a "
        "statistical statement about oral bioavailability, not a prediction that a compound works: "
        "bedaquiline and rifampicin violate it and are both clinically used drugs, which is visible "
        "in the table. Predicted affinity is separated from therapeutic effect by several further "
        "steps, and most computationally nominated compounds fail on testing."
    )

# --------------------------------------------------------------------------- phage
with tab3:
    st.subheader("Equations 7-9 and Box 3, on real phage genomes")
    st.markdown(
        "This is the least mature of the three areas, and the panel is built to show why rather than "
        "to hide it. The model below is a genuine autoregressive model using the same factorisation "
        "as Equation 7, fitted by counting on real phage genomes. It is also a very small one, and "
        "the difference between it and a trained genome language model is the subject of the finding "
        "further down this panel."
    )

    order = st.slider("Model order k (bases of context)", 1, 7, 5)
    model, train = fit_model(order)
    t4_name, t4_acc = next(iter(ncbi.PHAGE_TEST.items()))
    ctrl_name, ctrl_acc = next(iter(ncbi.NONPHAGE_CONTROL.items()))
    t4 = load_genome(t4_acc)[1]
    ctrl = load_genome(ctrl_acc)[1]

    st.caption("Fitted on: " + "; ".join(model.trained_on))

    scored = [{"Sequence": n, "Role": "training", "GC %": algos.gc_fraction(s) * 100,
               "Length (bp)": len(s), "log p per base (Eq. 8)": model.log_likelihood(s)[1]}
              for n, s in train.items()]
    scored += [
        {"Sequence": t4_name, "Role": "held-out phage", "GC %": algos.gc_fraction(t4) * 100,
         "Length (bp)": len(t4), "log p per base (Eq. 8)": model.log_likelihood(t4)[1]},
        {"Sequence": ctrl_name, "Role": "non-phage control", "GC %": algos.gc_fraction(ctrl) * 100,
         "Length (bp)": len(ctrl), "log p per base (Eq. 8)": model.log_likelihood(ctrl)[1]},
    ]
    sdf = pd.DataFrame(scored)
    st.dataframe(sdf, hide_index=True, width="stretch", column_config={
        "GC %": st.column_config.NumberColumn(format="%.1f"),
        "Length (bp)": st.column_config.NumberColumn(format="%d"),
        "log p per base (Eq. 8)": st.column_config.NumberColumn(format="%.4f"),
    })
    st.bar_chart(sdf.set_index("Sequence")[["log p per base (Eq. 8)"]], height=240)

    per_t4 = model.log_likelihood(t4)[1]
    per_ctrl = model.log_likelihood(ctrl)[1]
    if per_ctrl > per_t4:
        st.error(
            f"**A real negative result, reported rather than tuned away.** At k={order} the non-phage "
            f"control scores **{per_ctrl:.4f}** nats/base and the held-out phage T4 scores "
            f"**{per_t4:.4f}**. The control wins. The reason is in the GC column: the training genomes "
            f"run 48-64% GC, the control plasmid at 45% sits inside that range, and T4 at 35% is an "
            f"outlier. An order-k count model learns composition, not phage identity. This is exactly "
            f"the paper's point about Equation 9: a plausibility score that has not been anchored to "
            f"independent measurement cannot be read as a prediction. Try every value of k: the "
            f"ordering does not change.",
            icon=":material/trending_down:",
        )
    else:
        st.success(
            f"At k={order} the held-out phage now outscores the control ({per_t4:.4f} vs "
            f"{per_ctrl:.4f}). Check whether that is signal or a change in the training set before "
            f"reporting it."
        )

    st.divider()
    st.markdown("#### Equation 9: the design objective, and what β controls")
    st.warning(
        "The host fitness term **f** is a declared stand-in: GC-content match to the host genome. "
        "The real term needs host-range data this app does not have. Substituting a compositional "
        "statistic keeps Equation 9's arithmetic runnable and makes the substitution visible. Any "
        "ranking it produces is a talking point, not a prediction of lytic activity.",
        icon=":material/warning:",
    )
    beta = st.slider("beta, weight on the model log-likelihood (novelty control)", 0.0, 5.0, 1.0, 0.1)
    host = load_gene("inhA (Rv1484) - isoniazid/ethionamide, enoyl-ACP reductase")["window"]
    st.caption(
        f"Host reference: *M. tuberculosis* H37Rv window, {algos.gc_fraction(host) * 100:.1f}% GC. "
        "Mycobacterium phage D29 in the training set is the one genome with a matching host."
    )
    rows9 = []
    for name, seq in list(train.items()) + [(t4_name, t4), (ctrl_name, ctrl)]:
        d = algos.design_score(seq, host, model, beta)
        rows9.append({"Sequence": name, "f (GC-match proxy)": d["f"],
                      "log p per base": d["loglik_per_base"],
                      "score = f + β·log p": d["score"]})
    st.dataframe(pd.DataFrame(rows9).sort_values("score = f + β·log p", ascending=False),
                 hide_index=True, width="stretch", column_config={
                     c: st.column_config.NumberColumn(format="%.4f") for c in
                     ["f (GC-match proxy)", "log p per base", "score = f + β·log p"]})
    st.latex(r"p(x) = \prod_{i=1}^{L} p(x_i \mid x_{<i}) \qquad \log p(x) = \sum_{i=1}^{L} \log p(x_i \mid x_{<i})")
    st.latex(r"x^\star = \arg\max_x \left[ f(x, h) + \beta \log p(x) \right]")

    st.divider()
    st.markdown("#### Box 3: sampling from the fitted model")
    sc1, sc2 = st.columns([2, 3])
    with sc1:
        n_sample = st.slider("Sample length (bp)", 200, 5000, 1000, step=100)
        seed = st.number_input("Random seed", value=0, step=1)
    if st.button("Draw a candidate sequence", type="primary"):
        seed_seq = train["Mycobacterium phage D29"]
        sampled = model.sample(n_sample, seed_seq=seed_seq, rng=np.random.default_rng(int(seed)))
        d = algos.design_score(sampled, host, model, beta)
        q1, q2, q3 = st.columns(3)
        q1.metric("GC of sample", f"{algos.gc_fraction(sampled) * 100:.1f}%")
        q2.metric("log p per base", f"{d['loglik_per_base']:.4f}")
        q3.metric("score (Eq. 9)", f"{d['score']:.4f}")
        st.code("\n".join(sampled[i:i + 80] for i in range(0, len(sampled), 80)), language="text")
        st.caption(
            "This is what an order-k model's idea of a phage genome looks like. It reproduces local "
            "composition and nothing else: no genes, no coordinated structural proteins, no viable "
            "particle. The gap between this and the generative design results the paper reviews is "
            "the gap between a count model and a trained genome language model."
        )

    with st.expander("Box 3: Generative phage design with a viability filter (verbatim)"):
        st.code("""design_phage(host, model, beta, k):
    accepted = []
    while len(accepted) < k:
        x  = model.sample()                           # candidate genome
        ll = model.log_likelihood(x)                  # Eq. 8
        f  = host_fitness(x, host)                    # lytic match proxy
        if not structure_valid(x):                    # fold check on encoded proteins
            continue
        accepted.append((x, f + beta * ll))           # Eq. 9
    return sort(accepted, by = score, descending = True)[:k]""", language="text")

    limits(
        "The `structure_valid()` filter of Box 3 is **not implemented**: it needs a fast structure "
        "predictor over every encoded protein, which this app does not ship. Sequence plausibility "
        "and structural viability are different properties, so candidates drawn above are unscreened "
        "for fold. A phage genome is also evaluated as a whole, and one non-functional structural "
        "gene yields no particle, so the effective success rate is the product of per-gene rates, "
        "not their average. Work with engineered lytic phages carries biosafety obligations that "
        "compound screening does not."
    )

st.divider()
st.caption(
    "Prototype built as a companion to a conference proceeding. Computational output is "
    "hypothesis-generating only and requires experimental validation. Not for clinical use."
)
