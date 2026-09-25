# -*- coding: utf-8 -*-
"""Manuscript content. {PMID} -> parenthetical citation, [PMID] -> narrative citation."""

TITLE = ("ALGORITHMIC PERSPECTIVES IN BIOINFORMATICS: A REVIEW OF COMPUTATIONAL "
         "METHODS INTERPRETING EMERGING TRENDS IN BIOTECHNOLOGY")

AUTHOR = dict(
    name="Arli Aditya PARIKESIT",
    lines=[
        "Prof. Dr.rer.nat., Department of Biotechnology, School of Health and Life Sciences, "
        "Indonesia International Institute for Life Sciences (i3L University)",
        "Field of study: Bioinformatics and Computational Biology",
        "Jakarta, Indonesia",
        "ORCID NO: 0000-0001-8716-3926",
        "E-mail: arli.parikesit@i3l.ac.id",
        "Mobile: +62 819 3250 3988",
    ])

ABSTRACT = (
 "Bioinformatics algorithms sit between raw biological measurement and biological interpretation, and the "
 "past decade has changed what they are asked to do. Methods that were built to describe existing data are "
 "now being used to propose new molecules, new edits and new genomes. This review examines that shift across "
 "three areas of biotechnology: CRISPR-Cas genome editing, machine-learning-assisted drug discovery, and the "
 "computational design of bacteriophages. A rapid review following the PRISMA 2020 reporting standard was "
 "conducted in PubMed/MEDLINE, with three Boolean blocks covering the period from January 2012 to September "
 "2026. The search returned 18,868 unique records, of which 178 relevance-ranked records were screened at "
 "title and abstract level and 84 were assessed in full text. Twenty-one studies met the eligibility criteria "
 "from database searching, and a further 44 methodological and primary sources were added through citation "
 "chaining, giving 65 sources in the synthesis. Every source was verified against its PubMed identifier and "
 "its DOI record before inclusion. For each of the three areas the review states the governing objective "
 "function, presents the scoring or likelihood equation in explicit notation, and gives the corresponding "
 "algorithm in pseudocode. The comparison shows that the three areas share one computational skeleton: a "
 "learned or empirically calibrated score over candidate sequences or structures, a search procedure over a "
 "combinatorially large candidate space, and a constraint term that keeps proposals inside a region where "
 "laboratory work is plausible. The differences between the areas lie in how well the score is calibrated and "
 "in how expensive it is to test a proposal experimentally. Guide RNA scoring is the most mature of the three, "
 "with orthogonal empirical measurements available for calibration; generative phage design is the least "
 "mature, and its plausibility scores have not yet been anchored to comparable experimental measurement. The "
 "review argues that reporting practice, not model capacity, is now the limiting factor for reproducibility, "
 "and it sets out what computational and experimental groups working in resource-constrained settings should "
 "report so that algorithm-generated candidates can be independently evaluated.")

KEYWORDS = ("Bioinformatics algorithms, CRISPR-Cas, AI-generated drug discovery, "
            "AI-designed bacteriophages, antibiotic resistance")

INTRO = [
 "Biological measurement now outpaces biological interpretation. Sequencing output has grown faster than the "
 "storage and analysis capacity built to absorb it, and projections made a decade ago placed genomics on a "
 "trajectory comparable to astronomy and particle physics in annual data volume {26151137}. The response to "
 "that growth has been algorithmic rather than manual. Dynamic programming for local sequence similarity "
 "{7265238} and the heuristic database search that followed it {2231712} established a pattern that still "
 "holds: a scoring scheme that encodes a biological assumption, and a search procedure that finds high-scoring "
 "candidates without enumerating every possibility. Almost every method discussed in this review is a variation "
 "on that pattern.",

 "Four families of method carry most of the analytical load in contemporary life sciences research. Sequence "
 "alignment matches nucleic acid and protein sequences against reference data. Structural modeling predicts "
 "three-dimensional shape from sequence, a problem that moved from open to largely tractable for single chains "
 "with the release of deep learning systems trained on the structural archive {34265844} and the proteome-scale "
 "database built on top of them {34791371}. Statistical and machine learning analysis extracts signal from "
 "noisy, high-dimensional measurements, drawing on representation learning methods whose general properties "
 "were consolidated in the middle of the last decade {26017442}. Data integration combines heterogeneous "
 "datasets into a single analytical view. Recent surveys of the field in the Indonesian and wider tropical "
 "research context describe how these four families are being combined in practice, particularly where "
 "molecular simulation and virtual screening are used together {42191274}.",

 "What has changed is not the composition of these families but their direction of use. A model that assigns a "
 "likelihood to an observed sequence can also be sampled to produce sequences that were never observed. "
 "Autoregressive protein language models trained on natural sequence families generate functional enzymes "
 "outside the training distribution {36702895}, and continuous latent representations of small molecules allow "
 "optimisation to be performed in a differentiable space rather than by enumeration over discrete structures "
 "{29532027}. The same inversion has now reached the genome scale, with models trained across prokaryotic and "
 "phage sequence generating coherent multi-gene constructs {39541441}. Analysis and generation have become the "
 "same computational operation applied in opposite directions.",

 "Three application areas make that inversion visible, and they are the subject of this review. Genome editing "
 "with CRISPR-Cas systems depends on computation at nearly every stage, from the programmable targeting rule "
 "established when dual-RNA-guided cleavage was first characterised {22745249} to the ranking of candidate "
 "guides and the interpretation of pooled screens. Drug discovery uses learned models to identify targets, "
 "propose molecules and estimate binding, a set of applications whose scope and limits have been surveyed at "
 "length {30976107}. Bacteriophage engineering is the least established of the three, but it has a decade of "
 "genetic groundwork behind it {27250768} and it has recently acquired generative methods of its own.",

 "The motivation for the third area is not primarily computational. Bacterial antimicrobial resistance was "
 "associated with 4.95 million deaths worldwide in 2019, of which 1.27 million were directly attributable "
 "{35065702}, and the updated burden estimate covering 1990 to 2021 confirms both the scale and the "
 "geographical concentration of that mortality in low- and middle-income regions {39299261}. Southeast Asia "
 "carries a disproportionate share. Phage therapy has re-entered clinical consideration in that context "
 "{30763536}, and the case for engineered rather than naturally isolated phages rests on the ability to match a "
 "therapeutic agent to a resistant strain quickly enough to be clinically useful {34428079}.",

 "A note on presentation is needed before the review proper. Method descriptions in this literature are "
     "frequently given in prose, and prose is not sufficient for reimplementation. A sentence stating that "
     "candidate guides are ranked by a specificity score leaves open how mismatches are weighted, how the "
     "per-site scores are combined, and what the resulting number is bounded by; three published tools can "
     "satisfy that sentence and disagree on which guide is best {35341983}. The convention of writing the "
     "objective as an equation and the procedure as pseudocode is older than any of the methods reviewed here "
     "and is what made the classical alignment algorithms portable across implementations {7265238} {2231712}. "
     "This review therefore states each objective in notation and gives each procedure in a boxed algorithm, "
     "and treats a method whose objective cannot be written down as a method that has not been fully "
     "reported {34082136}.",

 "Reviews of each of these areas exist separately, and several are recent and thorough {35341983} {38663579} "
 "{40359589}. What is less available is a treatment that places the three side by side at the level of the "
 "objective function, so that the shared structure and the genuine differences become visible. This review has "
 "four objectives. First, to identify the computational entry points in each of the three areas through a "
 "reproducible literature search. Second, to state the governing equations in explicit notation rather than in "
 "prose. Third, to give the corresponding algorithms as pseudocode that a reader can implement. Fourth, to "
 "compare the three areas on the calibration of their scoring functions and on the cost of experimental "
 "verification, and to derive reporting recommendations from that comparison. The intended audience includes "
 "wet-laboratory collaborators who will be asked to test algorithm-generated candidates, which is why each "
 "equation is accompanied by a statement of what it does not model.",
]

METHODS = [
 ("Review design", [
  "This work is a rapid review of methodological and primary literature, reported in accordance with the PRISMA "
  "2020 statement {33782057}. A rapid review design was chosen because the objective is methodological "
  "comparison across three application areas rather than effect estimation within one, and because the "
  "eligibility criteria depend on whether an algorithm is specified rather than on study outcome. Two "
  "deviations from a full systematic review are declared in advance and revisited in the limitations. "
  "Screening was performed by a single reviewer, and the pool retrieved for title and abstract screening was "
  "capped at the highest-ranking records per search block rather than covering the full result set. Screening "
  "decisions and their reasons were recorded in a structured file at the time of screening, following the "
  "practice recommended for transparent review workflows {27919275}.",
 ]),
 ("Information sources and search strategy", [
  "PubMed/MEDLINE was searched on 4 September 2026 using three Boolean blocks, one per application area, each "
  "restricted to the publication window 1 January 2012 to 4 September 2026. The start of the window is the year "
  "in which programmable dual-RNA-guided cleavage was reported {22745249}, which is the earliest point at which "
  "all three application areas can be discussed in their present form. The blocks were as follows. Block 1: "
  "(CRISPR[tiab] OR Cas9[tiab] OR \"guide RNA\"[tiab] OR sgRNA[tiab]) AND (algorithm*[tiab] OR \"machine "
  "learning\"[tiab] OR \"deep learning\"[tiab] OR \"computational design\"[tiab] OR \"off-target "
  "prediction\"[tiab] OR score[tiab]). Block 2: (\"drug discovery\"[tiab] OR \"de novo design\"[tiab] OR "
  "\"virtual screening\"[tiab] OR \"binding affinity\"[tiab]) AND (\"deep learning\"[tiab] OR \"machine "
  "learning\"[tiab] OR \"generative model*\"[tiab] OR \"neural network*\"[tiab] OR algorithm*[tiab]). Block 3: "
  "(bacteriophage*[tiab] OR phage*[tiab]) AND (design*[tiab] OR engineer*[tiab] OR \"machine learning\"[tiab] "
  "OR \"deep learning\"[tiab] OR \"generative model*\"[tiab] OR \"language model*\"[tiab] OR algorithm*[tiab]). "
  "A second identification route was used in parallel: citation chaining from the reference list of the "
  "conference presentation on which this paper is based, together with hand-searching for the primary "
  "methodological sources that the retrieved reviews cite. Records reaching the synthesis through this route "
  "are reported separately in the flow diagram, as PRISMA 2020 requires for records identified by methods other "
  "than database searching {33782057}.",
 ]),
 ("Eligibility criteria", [
  "Inclusion and exclusion criteria were fixed before screening, as PRISMA 2020 requires {33782057}, and are given in full in Table 1. A record was "
  "eligible if it was a peer-reviewed primary study, methodological report or review; if it specified an "
  "algorithm at the level of an objective function, a scoring scheme or a named model class rather than "
  "announcing a tool without method; if it was written in English; and if it addressed guide design, off-target "
  "prediction or screen analysis for CRISPR-Cas systems, machine learning applied to molecular design or "
  "affinity estimation, or the computational design, engineering or characterisation of bacteriophages. Records "
  "were excluded if they were editorials, news items, conference abstracts or forewords; if they reported only "
  "laboratory work with no computational component; if the application fell outside the three defined areas; or "
  "if a preprint had been superseded by a peer-reviewed version of the same work, in which case the "
  "peer-reviewed version was retained. One further exclusion was applied at full-text stage. Where several "
  "eligible records covered the same methodological ground, the record with the widest scope or the earliest "
  "primary description was retained and the remainder were excluded as topically redundant, a decision recorded "
  "explicitly for each affected record.",
 ]),
 ("Selection process", [
  "The three blocks returned 1,521, 10,844 and 6,626 records respectively, giving 18,991 records before "
  "deduplication and 18,868 after 123 cross-block duplicates were removed. Screening the full set was outside "
  "the scope of a conference review, so the 60 highest-ranking records per block by PubMed relevance ordering "
  "were retrieved, which after removal of two cross-block duplicates gave 178 records for title and abstract "
  "screening; the remaining 18,690 unique records were not sought for retrieval. Of the 178 screened, 94 were "
  "excluded at title and abstract level, 64 because the application fell outside the three defined areas, 20 "
  "because no algorithm was specified, and 10 because the work was laboratory-only. The remaining 84 records "
  "were assessed in full text, and 63 were excluded, 48 as topically redundant with a retained record, nine as "
  "outside the defined scope on closer reading, three as preprints superseded by peer-reviewed versions, two as "
  "duplicated book chapters, and one because the full text contained no algorithmic detail. Twenty-one records "
  "from database searching entered the synthesis. The parallel citation-chaining route yielded 94 candidate "
  "records, of which 50 were excluded, nine because verification showed the retrieved record did not match the "
  "intended source and 41 as redundant with a retained record, leaving 44. The synthesis therefore rests on 65 "
  "sources. Figure 1 presents the flow in the four-phase format specified by PRISMA 2020 {33782057}.",
 ]),
 ("Reference verification", [
  "Because a review of this kind is of no use if its citations cannot be traced, every candidate record was "
  "verified programmatically before it was allowed into the synthesis. Each record was retrieved from the NCBI "
  "E-utilities summary service by PubMed identifier, and the returned title, journal, year, volume, issue, "
  "pagination and author list were taken as the authoritative metadata rather than any secondary source. The "
  "digital object identifier attached to each record was then resolved against the Crossref REST API, and the "
  "title returned by Crossref was compared with the title returned by PubMed using a sequence similarity "
  "measure. Records whose two titles disagreed, or whose identifier failed to resolve, were removed. All 64 "
  "sources in the final reference list resolved successfully in both services; 63 matched exactly and one "
  "differed only in a publisher-added subtitle. This procedure is a direct application of the reproducibility "
  "practice of recording exact provenance for every input to an analysis {24204232}, extended to the "
  "bibliography itself, and it is consistent with the findability and accessibility requirements of the FAIR "
  "principles {26978244}.",
 ]),
 ("Data extraction and synthesis", [
  "For each included record the following were extracted: application area, publication year, article type, the "
  "algorithm class or model family described, the objective function or scoring scheme where one was stated, "
  "and the form of experimental validation reported, if any. Extraction was tabulated and is summarised in "
  "Table 2. Synthesis was narrative and structured by application area, because the heterogeneity of outcome "
  "measures across the three areas rules out any quantitative pooling. Within each area the governing equations "
  "were reconstructed from the primary sources in a single consistent notation, so that terms carrying the same "
  "meaning across areas are written the same way. Pseudocode was written to correspond directly to the "
  "equations as stated, and is presented in boxed form rather than as running text. No new computational "
  "experiments were performed for this review, and no equation presented below is original to it; each is "
  "attributed to the primary source in which it or its immediate antecedent appears {35341983} {34082136}.",
 ]),
]

CONCLUSION = [
 "Three areas of biotechnology that are usually discussed separately turn out to run on the same computational "
 "skeleton. A score is assigned to candidate sequences or structures, a search procedure explores a space too "
 "large to enumerate, and a constraint term keeps the proposals inside a region where laboratory work remains "
 "plausible. Guide RNA design, molecular design and phage design differ in the biological content of the score "
 "and in the cost of testing a proposal, but not in the shape of the problem being solved. Recognising that "
 "shared structure is useful in practice, because it means that a lesson learned about calibration or "
 "validation in one area transfers to the others rather than having to be rediscovered.",

 "The three areas are not equally mature, and the review is explicit about the ordering. Guide RNA scoring "
 "rests on the largest body of orthogonal empirical measurement, and its failure modes are documented. "
 "Affinity estimation and generative molecular design sit in the middle, with benchmark performance that is "
 "well characterised computationally and a smaller number of prospective successes confirmed in the "
 "laboratory. Generative phage design is the newest, and its plausibility scores have not yet been anchored to "
 "the kind of independent measurement that would allow a reader to convert a model score into an expected "
 "success rate. Presenting the three together makes that gradient legible in a way that separate reviews of "
 "each area do not.",

 "Four recommendations follow. First, computational reports should state the objective function and its "
 "constraint terms explicitly, in notation, rather than describing them in prose, because a described "
 "objective cannot be reimplemented and a stated one can. Second, every algorithm-generated candidate should "
 "be reported together with the calibration evidence available for the score that produced it, so that readers "
 "can distinguish a ranking from a prediction. Third, prospective validation should be reported with the same "
 "completeness as retrospective benchmarking, including the candidates that failed, since selective reporting "
 "of successes makes published success rates uninterpretable. Fourth, parameters, model versions, random "
 "seeds and data splits should be deposited alongside results, which is a low-cost requirement that determines "
 "whether an independent group can repeat the work at all.",

 "For research groups in Indonesia and comparable settings, the practical consequence is favourable. The "
 "computational stage of all three pipelines runs on modest hardware or on public infrastructure, and the "
 "scientific bottleneck has moved to the interface between computation and experiment, where local knowledge "
 "of circulating pathogens and locally available chemical matter carries real weight. The algorithms discussed "
 "here propose candidates and rank them. They do not confirm anything, and treating a ranked list as a result "
 "rather than as a hypothesis is the single error most likely to waste laboratory effort. Closer collaboration "
 "between computational and experimental groups, honest reporting of what was tested and what failed, and "
 "sustained attention to reproducibility are the conditions under which these methods become useful rather "
 "than merely productive.",
]

# ---------------- FINDINGS AND DISCUSSION ----------------
# item kinds: ("sub", heading) ("p", text) ("eq", key, number) ("box", n, title, code, caption_note)
# ("tbl", n) ("fig", n)

FINDINGS = [
 ("sub","Characteristics of the included corpus"),
 ("p","The 65 sources in the synthesis divide unevenly across the three application areas, and the imbalance is "
      "informative rather than incidental. Genome editing contributes 18 sources, machine-learning-assisted drug "
      "discovery 18, and bacteriophage design 14, with the remaining 15 covering shared methodological ground "
      "such as structure prediction, reporting standards and reproducibility practice. Publication years run "
      "from 1981 to 2026, but the distribution is heavily weighted towards the last eight years: 46 of the 65 "
      "sources appeared in 2018 or later. Table 2 summarises the corpus by area, period and article type. The "
      "concentration of drug discovery records reflects the size of that literature rather than its maturity, "
      "since a large proportion of the retrieved records in Block 2 were reviews that restate the same "
      "methodological content, which is why 48 full-text records were excluded as topically redundant "
      "{33779453} {38663579}."),
 ("tbl",2),
 ("p","A second pattern in the corpus concerns validation. Among the genome editing sources, empirical "
      "measurement of off-target activity by orthogonal assays is reported or cited in the majority of records "
      "{25513782}, and scoring functions are trained on measured cleavage or knockout outcomes {26780180} "
      "{25184501}. Among the drug discovery sources, retrospective benchmark performance is near-universal but "
      "prospective laboratory confirmation appears in a minority, most prominently in the antibacterial screening "
      "work that produced a confirmed active compound {32084340} and in kinase inhibitor design confirmed in "
      "cells and animals {31477924}. Among the phage sources, computational characterisation dominates {34174831} "
      "{39418300}, and generative design with laboratory confirmation is represented by a single recent report "
      "{42561074}. This gradient in validation density, rather than any difference in model architecture, is the "
      "main axis along which the three areas differ."),

 ("sub","Genome editing: where computation enters and what it scores"),
 ("p","Computation enters CRISPR-Cas workflows at three points. Before an edit, candidate guides must be "
      "enumerated against the protospacer adjacent motif requirement that follows from the targeting mechanism "
      "{22745249} and ranked for expected on-target activity. As a safety check, the genome must be searched for "
      "sites similar enough to be cut by mistake, and the risk aggregated into a usable number. After a pooled "
      "screen, counts of guide abundance must be turned into statements about which genes matter. Current tool "
      "surveys organise the field along exactly these three axes {35341983}, and the methods have been extended "
      "as the editor repertoire has grown to include base editors {27096365} and prime editors {31634902}, each "
      "of which changes the activity model without changing the structure of the ranking problem."),
 ("p","The simplest measure of similarity between a guide g and a genomic 20-mer s is the number of mismatched "
      "positions, written as an indicator sum in Equation 1. This quantity treats every position as equally "
      "important, which the experimental record contradicts: mismatches near the protospacer adjacent motif are "
      "tolerated far less than mismatches at the distal end of the spacer {23873081}. Exhaustive enumeration of "
      "sites within a mismatch budget is nonetheless the standard first pass, and it is what fast genome-wide "
      "search implementations compute {24463181}."),
 ("eq","eq1",1),
 ("p","Equation 2 replaces the uniform treatment of positions with a position-weighted product. Each mismatched "
      "position contributes a weight between zero and one, estimated from measured cleavage at large panels of "
      "mismatched sites, and the product over mismatched positions gives a cutting frequency determination score "
      "for the site {26780180}. The weights encode the positional asymmetry that Equation 1 ignores, and they "
      "are the component that must be re-estimated whenever the nuclease or the delivery context changes; "
      "machine-learned successors replace the fixed weight table with a trained function over the guide-target "
      "pair while keeping the same output semantics {29945655} {29998038}."),
 ("eq","eq2",2),
 ("p","Equation 3 aggregates the per-site scores across the set of candidate off-target sites into a single "
      "specificity value for the guide, bounded above by 100 and decreasing as predicted off-target activity "
      "accumulates {26780180}. Guides are then ranked by this value. The aggregation is deliberately crude: it "
      "sums risk over sites without regard to where those sites fall in the genome, so a guide with one "
      "predicted cut in an essential coding exon and a guide with one predicted cut in an intergenic region "
      "receive the same penalty. Recent off-target predictors address this by modelling the interaction between "
      "guide and target directly, including insertions and deletions rather than substitutions alone {37980345} "
      "{38199209}, and by making the learned contributions inspectable rather than opaque {40468633}."),
 ("eq","eq3",3),
 ("p","Box 1 gives the design procedure implied by these three equations. The algorithm slides a 23-nucleotide "
      "window across the target region, accepts windows whose final two positions satisfy the motif requirement "
      "{22745249}, scans the genome for candidate off-target sites for each accepted spacer, computes the "
      "aggregate specificity of Equation 3, and returns the candidates in descending order of that value "
      "{26780180}. The genome scan is the expensive step and is the part that production implementations "
      "optimise {24463181}."),
 ("box",1,"Guide design with aggregate off-target specificity",
   "design_guides(target, genome, w):\n"
   "    guides = []\n"
   "    for window in slide(target, length = 23):        # 20 nt spacer + NGG motif\n"
   "        if window[21:23] != \"GG\":                    # motif requirement not met\n"
   "            continue\n"
   "        g  = window[0:20]\n"
   "        OT = scan_offtargets(g, genome, max_mismatch = 4)\n"
   "        S  = 100 / (1 + sum(cfd(g, s, w) for s in OT))\n"
   "        guides.append((g, S))\n"
   "    return sort(guides, by = S, descending = True)",
   "Notation follows Equations 1 to 3. cfd() evaluates Equation 2 with weight table w."),
 ("p","Two limits of this formulation deserve statement, because they determine what a wet-laboratory "
      "collaborator should and should not conclude from a ranked list. The specificity value is a prediction "
      "from a model trained on cleavage measurements in particular cell types, and it does not measure "
      "chromatin accessibility, delivery efficiency or repair outcome at the intended site. Independent "
      "measurement of where cleavage actually occurred, using assays that read out double-strand breaks "
      "genome-wide rather than predicted ones {25513782}, remains the only way to confirm that a highly ranked "
      "guide behaves as ranked. On the analysis side, pooled screen interpretation is a separate statistical "
      "problem, handled by count-based models that account for the variance structure of guide abundance data "
      "{25476604} rather than by the scoring functions used at design time. Machine learning is also now being "
      "applied upstream of guide selection, to engineer nuclease variants with altered motif requirements "
      "{40262634} and to expand the catalogue of usable effector proteins {40739008}, which widens the design "
      "space that Equation 3 is asked to rank {37469443}."),

 ("p","Pooled screen analysis is the third computational entry point and is worth separating from the two "
      "design problems, because it inverts the direction of inference. Design ranks candidate guides before an "
      "experiment; screen analysis takes guide abundance counts after an experiment and asks which genes the "
      "edits affected. The statistical problem is a count-based one, with per-guide variance that grows with "
      "mean abundance and with several guides reporting on each gene, and it is handled by models that pool "
      "information across guides targeting the same gene rather than by testing each guide separately "
      "{25476604}. Two properties of the design stage propagate into this analysis. Guides with poor on-target "
      "activity contribute noise rather than signal, so the activity models used at design time {25184501} "
      "affect the power of the screen that follows; and guides with predicted off-target cutting can produce "
      "phenotypes attributable to the wrong gene, which is why specificity filtering is applied at library "
      "construction rather than at analysis {26780180}."),

 ("sub","Drug discovery: affinity estimation and constrained generation"),
 ("p","In machine-learning-assisted drug discovery the computational task is to narrow a chemical space too "
      "large to enumerate down to a set small enough to assay. Three operations do the narrowing: identifying a "
      "target site, which structure prediction has made tractable for a large fraction of the proteome "
      "{34265844} {34791371}; proposing candidate molecules; and estimating how strongly each might bind. "
      "Surveys of the field agree on this decomposition and on its principal weakness, which is that each stage "
      "introduces error that the next stage cannot detect {30976107} {33779453}."),
 ("p","Equation 4 states the affinity estimation task. A model with parameters θ maps a molecule m and a target "
      "t to a predicted affinity, conventionally expressed on a logarithmic scale as the negative base-ten "
      "logarithm of the dissociation constant {30423097}. Writing the prediction this way matters because the "
      "logarithmic scale is the one on which model error is roughly homoscedastic, and because it connects "
      "directly to the thermodynamic quantity in Equation 5, where the standard free energy of binding is "
      "proportional to the logarithm of the same constant. A model that is accurate to one log unit is "
      "therefore accurate to roughly 5.7 kilojoules per mole at physiological temperature, which is the "
      "difference between a promising and an uninteresting compound. Empirical scoring functions used in "
      "docking approximate the same quantity by a different route, through a weighted sum of geometric and "
      "chemical interaction terms fitted to known complexes {19499576}, and the relationship between learned "
      "and empirical scoring is the subject of continuing comparison {35889440}."),
 ("eq","eq4",4),
 ("eq","eq5",5),
 ("p","Equation 6 states the generative objective. The proposed molecule is the one maximising predicted "
      "affinity minus a weighted penalty for departing from drug-like property ranges, with λ setting the "
      "exchange rate between the two terms {29532027}. The penalty term is not optional. Unconstrained "
      "maximisation of a learned affinity score reliably produces molecules that score well and cannot be "
      "made, because the score was never trained on anything resembling them. In practice the penalty combines "
      "property filters derived from oral bioavailability statistics {11259830} with a continuous "
      "desirability score that aggregates several property distributions into one value {22270643}. Deep "
      "quantitative structure-activity modelling has largely absorbed this framing, treating the property "
      "constraint and the activity prediction as parts of one multi-objective problem {38066301} {34082136}."),
 ("eq","eq6",6),
 ("p","Box 2 gives the corresponding loop. A generator proposes molecules, property filters reject those "
      "outside the acceptable range, a trained model scores the survivors, and the top k are passed to assay "
      "{29532027} {30423097}. The structure is a rejection sampler with a learned objective, and its "
      "behaviour depends almost entirely on the quality of the filter and the calibration of the score."),
 ("box",2,"Constrained generative screening loop",
   "discover(target, N, k, lambda_):\n"
   "    pool = []\n"
   "    repeat N times:\n"
   "        m = generator.sample()                        # propose a structure\n"
   "        if not drug_like(m):                          # property filter, Eq. 6 penalty\n"
   "            continue\n"
   "        a = model.predict(m, target)                  # predicted pKd, Eq. 4\n"
   "        pool.append((m, a - lambda_ * penalty(m)))\n"
   "    top = sort(pool, by = score, descending = True)[:k]\n"
   "    return top                                        # hand off to wet-lab assay",
   "Notation follows Equations 4 and 6. penalty() evaluates the drug-likeness term."),
 ("p","The record of prospective success is real but narrower than the volume of publication suggests. A "
      "trained classifier applied to a large compound library identified an antibacterial compound that was "
      "subsequently confirmed in vitro and in animal models {32084340}, and a generative pipeline produced "
      "kinase inhibitors confirmed experimentally within weeks {31477924}. Later work has extended the "
      "generative approach to antibacterial design explicitly {40816267} and to natural product chemistry, "
      "where the underlying chemical matter is more structurally diverse than typical screening libraries "
      "{37697042}. The same methods have been applied to tuberculosis, with virtual screening nominating "
      "repurposing candidates against mycobacterial targets {39737570}, and to Indonesian target-based work "
      "where computational nomination was followed by explicit experimental planning {33450856}. Reviews of "
      "deep learning for antibiotic discovery are candid about the base rate: most nominated compounds fail "
      "{37794737}. That is the expected behaviour of a ranking procedure and is not a defect, provided the "
      "ranking is reported as a ranking."),

 ("sub","Bacteriophage design: generative sequence models at genome scale"),
 ("p","The third area applies the same machinery to a larger and less forgiving object. A phage genome is tens "
      "of kilobases of coordinated coding sequence, and a design is viable only if the encoded proteins fold, "
      "assemble and act against the intended host. Genetic engineering of phages has a decade of established "
      "technique behind it {27250768}, and the clinical case for strain-matched engineered phages was made "
      "concrete when a three-phage cocktail, one member of which had been engineered to be lytic, was "
      "administered to a patient with a disseminated drug-resistant mycobacterial infection {31068712}. "
      "Reviews of the therapeutic area set out both the promise and the regulatory and manufacturing obstacles "
      "{34428079} {30763536}."),
 ("p","Equation 7 states the generative model in its standard autoregressive form: the probability of a genome "
      "is the product over positions of the probability of each symbol given all preceding symbols. This is the "
      "same factorisation used by protein language models that generate functional enzymes across families "
      "{36702895}, applied at genome rather than protein scale {39541441}. Equation 8 is the logarithm of "
      "Equation 7 and is what is actually computed, both because the product underflows and because the sum "
      "gives an additive per-position plausibility score that can be compared across sequences of similar "
      "length."),
 ("eq","eq7",7),
 ("eq","eq8",8),
 ("p","Equation 9 states the design objective as a sum of two terms: a host fitness term expressing how well "
      "the design is expected to act against the target bacterium, and the model log-likelihood weighted by β, "
      "which keeps proposals inside the region of sequence space the model regards as viable {39541441}. The β "
      "parameter is the novelty control. Set it high and the model returns near-copies of training genomes; set "
      "it low and it returns sequences that optimise the fitness proxy while drifting outside anything the "
      "model has grounds to evaluate. Because neither term is directly measurable at design time, both are "
      "proxies, and the composite score should be read as a prioritisation rather than a prediction of lytic "
      "activity."),
 ("eq","eq9",9),
 ("p","Box 3 gives the sampling loop. Candidate genomes are drawn from the model, scored by the composite "
      "objective of Equation 9, and passed through a structural viability filter before being accepted "
      "{39541441}. The filter matters because sequence plausibility and structural viability are different "
      "properties: a genome can be highly probable under a sequence model and still encode proteins that do "
      "not fold. Fold checking at scale is what makes this step practical, using structure predictors fast "
      "enough to run over every encoded protein in a candidate genome {36927031}, built on representations "
      "learned from unsupervised training over large sequence collections {33876751}."),
 ("box",3,"Generative phage design with a viability filter",
   "design_phage(host, model, beta, k):\n"
   "    accepted = []\n"
   "    while len(accepted) < k:\n"
   "        x  = model.sample()                           # candidate genome\n"
   "        ll = model.log_likelihood(x)                  # Eq. 8\n"
   "        f  = host_fitness(x, host)                    # lytic match proxy\n"
   "        if not structure_valid(x):                    # fold check on encoded proteins\n"
   "            continue\n"
   "        accepted.append((x, f + beta * ll))           # Eq. 9\n"
   "    return sort(accepted, by = score, descending = True)[:k]",
   "Notation follows Equations 7 to 9. structure_valid() screens encoded proteins by predicted fold."),
 ("p","Until recently this loop was largely aspirational, and the published computational phage literature "
      "concentrated on classification and characterisation rather than design: predicting lifecycle from "
      "sequence {39418300}, predicting host range {38361822}, and applying machine learning across phage "
      "research more broadly {34174831} {40359589}. That has now changed. Generative design of complete phage "
      "genomes using genome language models, with laboratory recovery of viable particles, has been reported "
      "{42561074}, which moves the third area from proposal to demonstration. It remains the least mature of "
      "the three by a clear margin. Design methods for proteins have advanced faster, with diffusion-based "
      "backbone generation now producing experimentally validated binders and enzymes {37433327}, and the "
      "genome-scale problem is harder for reasons of coordination rather than of model capacity."),

 ("p","Two practical constraints separate phage design from the two smaller-scale problems and are worth "
      "stating for readers planning experimental work. The first is that a phage genome is evaluated as a "
      "whole. A designed small molecule fails or succeeds as one object, and a designed guide can be replaced "
      "independently of the others in a library, but a genome with one non-functional structural gene yields no "
      "particle at all, so the effective success rate is the product of the per-gene success rates rather than "
      "their average {35868275}. The second is containment. Work with engineered lytic phages carries "
      "biosafety obligations that do not attach to compound screening, and the clinical precedent for "
      "engineered phage administration was established under compassionate-use conditions rather than through "
      "a standard trial pathway {31068712}. Reviews of the therapeutic area treat manufacturing and regulatory "
      "questions as the binding constraints on translation, not the design algorithms {34428079}."),

 ("sub","The common structure and where the three areas diverge"),
 ("p","Setting the nine equations side by side makes the shared skeleton explicit. Each area defines a score "
      "over candidate objects, each searches a space too large to enumerate, and each adds a constraint term "
      "that keeps proposals inside a testable region. Equation 3 scores guides and penalises predicted "
      "off-target cutting {26780180}. Equation 6 scores molecules and penalises departure from drug-like "
      "property ranges {29532027}. Equation 9 scores genomes and penalises departure from the sequence "
      "distribution the model was trained on {39541441}. The constraint term is the component that makes each "
      "objective usable, and in all three cases removing it produces high-scoring proposals that fail in the "
      "laboratory. Table 3 sets out the correspondence, and Figure 2 shows the shared analyse-to-generate "
      "structure across the three areas."),
 ("tbl",3),
 ("fig",2),
 ("p","The divergence between the areas is in calibration and in verification cost, not in architecture. Guide "
      "scoring functions are fitted to direct measurements of the outcome they predict, and independent assays "
      "exist that measure the same outcome by a different route {25513782} {23873081}, so a specificity value "
      "carries an interpretable meaning. Affinity models are fitted to measured binding constants and can be "
      "benchmarked retrospectively, but the quantity they predict is separated from therapeutic effect by "
      "several further steps {30976107} {35889440}. Phage design objectives combine a likelihood under a "
      "generative model with a host fitness proxy, and neither term has yet been calibrated against a "
      "comparable independent measurement {42561074}. Verification cost runs in the same order: a guide can be "
      "tested in days, a compound in months, a designed phage in considerably longer and with more demanding "
      "containment requirements {27250768}."),
 ("p","This ordering has a practical consequence for how outputs should be read. Where the score is well "
      "calibrated and the test is cheap, a ranked list can reasonably drive experimental choice. Where the "
      "score is a proxy for a proxy and the test is expensive, the ranked list is a starting point for "
      "discussion between computational and experimental groups rather than a decision. The failure mode "
      "reviews of all three areas describe is the same: a list of top-ranked candidates presented without the "
      "calibration evidence needed to interpret the ranking {37794737} {40359589}. Reporting practice, not "
      "model capacity, is what separates a usable prediction from an unusable one."),

 ("sub","Reproducibility and the reporting of algorithm-generated candidates"),
 ("p","A ranked list of candidates is reproducible only if a reader can regenerate it, and regenerating it "
      "requires more information than most reports provide. The minimum set is short and specific: the model "
      "identifier and version, the trained weights or a pointer to them, the random seed, the data split used "
      "for any reported performance figure, the thresholds applied by every filter in the pipeline, and the "
      "value of any trade-off parameter such as the lambda of Equation 6 or the beta of Equation 9. None of "
      "these is expensive to record, and the general case for recording them was made for computational "
      "biology more than a decade ago {24204232}. Treating the resulting artefacts as data in their own right, "
      "with identifiers and access conditions attached, is what the FAIR principles ask of any research output "
      "{26978244}, and a candidate list generated by a model is as much a research output as a measurement."),
 ("p","A second reporting problem is specific to learned scoring functions. Retrospective benchmark performance "
      "and prospective success rate are different quantities, and the gap between them is not a constant. A "
      "model evaluated on a random split of a public affinity dataset is being asked an easier question than a "
      "model asked to rank molecules against a target it has not seen, because chemical series recur across "
      "public datasets and a random split places members of the same series on both sides of it {38066301}. "
      "Surveys of generative molecular design have made the same point about sampling metrics, which reward "
      "coverage of a training distribution rather than usefulness of the sampled molecules {34082136}. Reported "
      "performance should therefore always be labelled with the split policy that produced it, and prospective "
      "claims should be separated from retrospective ones rather than presented in the same table {30976107}."),
 ("p","The third problem is selective reporting. When only successful nominations are published, the published "
      "success rate of a method is uninterpretable, because the denominator is missing. The antibacterial "
      "screening literature is unusually good on this point, reporting the size of the screened library and the "
      "number of compounds carried forward alongside the confirmed hit {32084340}, and reviews of the area "
      "state plainly that most nominated compounds do not survive testing {37794737}. That candour is what "
      "allows a reader to convert a published result into an expectation about their own work. Its absence in "
      "the newer generative literature is the main reason the phage results reviewed above should be read as a "
      "demonstration that the approach can work rather than as an estimate of how often it will {42561074}."),

 ("sub","Relevance to Indonesian and tropical disease research"),
 ("p","All of this work is unusually accessible to research groups on constrained budgets, because "
      "the computational stage of each runs on modest hardware or on freely available infrastructure, and "
      "because the reference data are open. Structure prediction for most well-studied proteomes is available "
      "without running the predictor at all {34791371}, and the model weights and code for the sequence models "
      "underlying phage and protein design are published. Regional work already demonstrates the pattern: "
      "immunoinformatic vaccine design against Nipah virus proceeding from public sequence to ranked epitope "
      "candidates {42064452}, and target-based screening for a cancer methyltransferase target with "
      "computational nomination followed by explicit experimental planning {33450856}."),
 ("p","The binding constraint in these settings is experimental capacity rather than computational capacity, "
      "which changes what an algorithmic pipeline should be designed to produce. If a group can assay ten "
      "compounds and not a thousand, the value of a scoring function lies in the precision of its top ten "
      "rather than in its average ranking performance, and that is a different quantity from the one most "
      "benchmarks report. The antimicrobial resistance burden falls disproportionately on the same regions "
      "{39299261} {35065702}, so the areas where local computational work is most useful and the areas where "
      "assay capacity is scarcest coincide. Integrating simulation and virtual screening within a single "
      "workflow, as recent regional reviews describe, is one practical response to that constraint {42191274}."),

 ("sub","Limitations"),
 ("p","Three limitations bear on how this review should be read. The screening pool was capped at the 60 "
      "highest-ranking records per block rather than covering all 18,868 unique records, so the corpus is a "
      "relevance-weighted sample and not an exhaustive census; work that is methodologically important but "
      "poorly matched to the search terms may have been missed. Screening and full-text assessment were "
      "performed by a single reviewer without independent duplication, which the PRISMA 2020 guidance "
      "identifies as a source of selection error {33782057}. The exclusion of topically redundant records, "
      "which accounted for 48 of the 63 full-text exclusions, involved a judgement about which of several "
      "overlapping records was most representative, and a different reviewer would not have made every one of "
      "those judgements the same way."),
 ("p","Two further limitations concern scope. The review restricts itself to three application areas and to "
      "PubMed-indexed literature, so methodological work published in machine learning venues without "
      "biomedical indexing is represented only where a biomedical source cites it; this is a known gap in "
      "coverage for computational topics {26017442}. The equations presented are the core objectives of each "
      "area in their standard form and are not exhaustive: production implementations add terms and "
      "engineering detail that the notation here omits, and the pseudocode is written for legibility rather "
      "than efficiency {35341983}. Finally, no computational experiments were run for this review, so all "
      "performance statements are those of the cited sources rather than independent verification, and readers "
      "should treat reported benchmark figures with the scepticism appropriate to self-reported evaluation "
      "{34082136}."),
]
