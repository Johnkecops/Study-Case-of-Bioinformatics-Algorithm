# -*- coding: utf-8 -*-
TABLE1 = dict(
 num=1,
 caption="Table 1. Inclusion and exclusion criteria applied at title, abstract and full-text screening",
 head=["Domain", "Inclusion criterion", "Exclusion criterion"],
 rows=[
  ["Publication type",
   "Peer-reviewed primary study, methodological report or review article",
   "Editorial, news item, foreword, conference abstract without full text"],
  ["Methodological content",
   "Algorithm specified at the level of an objective function, scoring scheme or named model class",
   "Tool announcement or application note with no stated method; full text without algorithmic detail"],
  ["Application area",
   "CRISPR-Cas guide design, off-target prediction or screen analysis; machine learning for molecular design or affinity estimation; computational design, engineering or characterisation of bacteriophages",
   "Application outside the three defined areas, including diagnostics, imaging and clinical outcome prediction"],
  ["Study design",
   "Any design with a computational component reported in sufficient detail to be reimplemented",
   "Laboratory-only study with no computational component"],
  ["Language and window",
   "English; published between 1 January 2012 and 4 September 2026",
   "Non-English; published outside the window"],
  ["Record status",
   "Peer-reviewed version where both a preprint and a published version exist",
   "Preprint superseded by a peer-reviewed version; duplicate book chapter; retracted record"],
  ["Redundancy",
   "Widest-scope or earliest primary description retained where several records cover the same methodological ground",
   "Record topically redundant with a retained record"],
 ])

TABLE2 = dict(
 num=2,
 caption="Table 2. Composition of the 65 sources included in the synthesis, by application area and publication period",
 head=["Application area", "n", "1981-2017", "2018-2021", "2022-2026", "Dominant article type"],
 rows=[
  ["CRISPR-Cas genome editing", "18", "8", "3", "7", "Primary method reports"],
  ["Machine-learning drug discovery", "18", "3", "8", "7", "Method reports and reviews"],
  ["Bacteriophage design and therapy", "14", "1", "3", "10", "Reviews and burden estimates"],
  ["Shared methodological ground", "15", "7", "3", "5", "Primary method reports"],
  ["Total", "65", "19", "17", "29", ""],
 ])

TABLE3 = dict(
 num=3,
 caption="Table 3. Correspondence between the three application areas at the level of the objective function",
 head=["Component", "CRISPR-Cas genome editing", "Machine-learning drug discovery", "Bacteriophage design"],
 rows=[
  ["Candidate object", "20-nucleotide spacer adjacent to a protospacer adjacent motif",
   "Small molecule structure", "Complete phage genome"],
  ["Score", "Aggregate specificity S (Equation 3)", "Predicted affinity on a logarithmic scale (Equation 4)",
   "Host fitness proxy combined with model log-likelihood (Equation 9)"],
  ["Constraint term", "Summed cutting frequency determination score over predicted off-target sites",
   "Drug-likeness penalty weighted by lambda", "Model log-likelihood weighted by beta"],
  ["Search procedure", "Exhaustive window enumeration followed by genome scan",
   "Rejection sampling from a generative model", "Rejection sampling with a structural viability filter"],
  ["Training signal", "Measured cleavage at panels of mismatched sites", "Measured binding constants",
   "Natural phage and prokaryotic genome sequence"],
  ["Independent verification", "Genome-wide double-strand break mapping",
   "Binding and phenotypic assays", "Particle recovery and lytic activity assays"],
  ["Calibration maturity", "High: score fitted to and testable against the predicted outcome",
   "Moderate: benchmarked retrospectively, fewer prospective confirmations",
   "Low: neither term anchored to a comparable independent measurement"],
  ["Approximate cost of one test", "Days", "Months", "Months to years, with containment requirements"],
 ])
