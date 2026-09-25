# Reference validation log

Manuscript: `IKSAD-Bioalgo-Manuscript-Arli.docx`
Generated: 2026-09-04

Every reference in the manuscript was verified twice before inclusion:

1. **PubMed** (NCBI E-utilities ESummary, `db=pubmed`). Title, journal, year, volume, issue, pagination and
   author list were taken from the returned record, not from any secondary source or from recall.
2. **Crossref** (`https://api.crossref.org/works/{DOI}`). The DOI was resolved and the Crossref title compared
   with the PubMed title by sequence similarity. `MATCH` means similarity above 0.80; `TITLE-DIFF` means the
   DOI resolved but the publisher title carries extra text (a subtitle or a note).

Records whose identifiers failed to resolve, or whose two titles disagreed, were removed rather than corrected
by guessing. Nine candidate records were dropped at this stage because the retrieved record was not the intended
source.

| # | First author | Year | PMID | HTTP | Crossref verdict | Similarity | DOI | Route | Area |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Afnani | 2026 | [42064452](https://pubmed.ncbi.nlm.nih.gov/42064452/) | 200 | MATCH | 1.0 | [10.1007/s40203-026-00607-6](https://doi.org/10.1007/s40203-026-00607-6) | Citation chaining | Shared methodological ground |
| 2 | Alkaff | 2021 | [33450856](https://pubmed.ncbi.nlm.nih.gov/33450856/) | 200 | MATCH | 1.0 | [10.3390/molecules26020375](https://doi.org/10.3390/molecules26020375) | Citation chaining | Machine-learning drug discovery |
| 3 | Altschul | 1990 | [2231712](https://pubmed.ncbi.nlm.nih.gov/2231712/) | 200 | MATCH | 1.0 | [10.1016/S0022-2836(05)80360-2](https://doi.org/10.1016/S0022-2836(05)80360-2) | Citation chaining | Shared methodological ground |
| 4 | Antimicrobial Resistance Collaborators | 2022 | [35065702](https://pubmed.ncbi.nlm.nih.gov/35065702/) | 200 | MATCH | 1.0 | [10.1016/S0140-6736(21)02724-0](https://doi.org/10.1016/S0140-6736(21)02724-0) | Citation chaining | Bacteriophage design and therapy |
| 5 | Anzalone | 2019 | [31634902](https://pubmed.ncbi.nlm.nih.gov/31634902/) | 200 | MATCH | 1.0 | [10.1038/s41586-019-1711-4](https://doi.org/10.1038/s41586-019-1711-4) | Citation chaining | CRISPR-Cas genome editing |
| 6 | Bae | 2014 | [24463181](https://pubmed.ncbi.nlm.nih.gov/24463181/) | 200 | MATCH | 1.0 | [10.1093/bioinformatics/btu048](https://doi.org/10.1093/bioinformatics/btu048) | Citation chaining | CRISPR-Cas genome editing |
| 7 | Bickerton | 2012 | [22270643](https://pubmed.ncbi.nlm.nih.gov/22270643/) | 200 | MATCH | 1.0 | [10.1038/nchem.1243](https://doi.org/10.1038/nchem.1243) | Citation chaining | Machine-learning drug discovery |
| 8 | Cao | 2025 | [40468633](https://pubmed.ncbi.nlm.nih.gov/40468633/) | 200 | MATCH | 1.0 | [10.1002/smtd.202500122](https://doi.org/10.1002/smtd.202500122) | Database search | CRISPR-Cas genome editing |
| 9 | Cesaro | 2023 | [37794737](https://pubmed.ncbi.nlm.nih.gov/37794737/) | 200 | MATCH | 1.0 | [10.1080/17460441.2023.2250721](https://doi.org/10.1080/17460441.2023.2250721) | Database search | Machine-learning drug discovery |
| 10 | Chen | 2023 | [37980345](https://pubmed.ncbi.nlm.nih.gov/37980345/) | 200 | MATCH | 1.0 | [10.1038/s41467-023-42695-4](https://doi.org/10.1038/s41467-023-42695-4) | Database search | CRISPR-Cas genome editing |
| 11 | Chuai | 2018 | [29945655](https://pubmed.ncbi.nlm.nih.gov/29945655/) | 200 | MATCH | 1.0 | [10.1186/s13059-018-1459-4](https://doi.org/10.1186/s13059-018-1459-4) | Citation chaining | CRISPR-Cas genome editing |
| 12 | Dedrick | 2019 | [31068712](https://pubmed.ncbi.nlm.nih.gov/31068712/) | 200 | MATCH | 1.0 | [10.1038/s41591-019-0437-z](https://doi.org/10.1038/s41591-019-0437-z) | Citation chaining | Bacteriophage design and therapy |
| 13 | Doench | 2014 | [25184501](https://pubmed.ncbi.nlm.nih.gov/25184501/) | 200 | MATCH | 1.0 | [10.1038/nbt.3026](https://doi.org/10.1038/nbt.3026) | Citation chaining | CRISPR-Cas genome editing |
| 14 | Doench | 2016 | [26780180](https://pubmed.ncbi.nlm.nih.gov/26780180/) | 200 | MATCH | 1.0 | [10.1038/nbt.3437](https://doi.org/10.1038/nbt.3437) | Database search | CRISPR-Cas genome editing |
| 15 | Gangwal | 2024 | [38663579](https://pubmed.ncbi.nlm.nih.gov/38663579/) | 200 | MATCH | 1.0 | [10.1016/j.drudis.2024.103992](https://doi.org/10.1016/j.drudis.2024.103992) | Database search | Machine-learning drug discovery |
| 16 | GBD 2021 Antimicrobial Resistance Collaborators | 2024 | [39299261](https://pubmed.ncbi.nlm.nih.gov/39299261/) | 200 | MATCH | 1.0 | [10.1016/S0140-6736(24)01867-1](https://doi.org/10.1016/S0140-6736(24)01867-1) | Citation chaining | Bacteriophage design and therapy |
| 17 | Gómez-Bombarelli | 2018 | [29532027](https://pubmed.ncbi.nlm.nih.gov/29532027/) | 200 | MATCH | 1.0 | [10.1021/acscentsci.7b00572](https://doi.org/10.1021/acscentsci.7b00572) | Citation chaining | Machine-learning drug discovery |
| 18 | Hatfull | 2022 | [34428079](https://pubmed.ncbi.nlm.nih.gov/34428079/) | 200 | MATCH | 1.0 | [10.1146/annurev-med-080219-122208](https://doi.org/10.1146/annurev-med-080219-122208) | Citation chaining | Bacteriophage design and therapy |
| 19 | Howell | 2024 | [38361822](https://pubmed.ncbi.nlm.nih.gov/38361822/) | 200 | MATCH | 1.0 | [10.1093/ve/vead083](https://doi.org/10.1093/ve/vead083) | Citation chaining | Bacteriophage design and therapy |
| 20 | Hsu | 2013 | [23873081](https://pubmed.ncbi.nlm.nih.gov/23873081/) | 200 | MATCH | 1.0 | [10.1038/nbt.2647](https://doi.org/10.1038/nbt.2647) | Citation chaining | CRISPR-Cas genome editing |
| 21 | Jiménez-Luna | 2021 | [33779453](https://pubmed.ncbi.nlm.nih.gov/33779453/) | 200 | MATCH | 1.0 | [10.1080/17460441.2021.1909567](https://doi.org/10.1080/17460441.2021.1909567) | Database search | Machine-learning drug discovery |
| 22 | Jinek | 2012 | [22745249](https://pubmed.ncbi.nlm.nih.gov/22745249/) | 200 | MATCH | 1.0 | [10.1126/science.1225829](https://doi.org/10.1126/science.1225829) | Citation chaining | CRISPR-Cas genome editing |
| 23 | Jumper | 2021 | [34265844](https://pubmed.ncbi.nlm.nih.gov/34265844/) | 200 | MATCH | 1.0 | [10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2) | Citation chaining | Shared methodological ground |
| 24 | King | 2026 | [42561074](https://pubmed.ncbi.nlm.nih.gov/42561074/) | 200 | MATCH | 1.0 | [10.1126/science.aec2657](https://doi.org/10.1126/science.aec2657) | Database search | Bacteriophage design and therapy |
| 25 | Komor | 2016 | [27096365](https://pubmed.ncbi.nlm.nih.gov/27096365/) | 200 | MATCH | 1.0 | [10.1038/nature17946](https://doi.org/10.1038/nature17946) | Citation chaining | CRISPR-Cas genome editing |
| 26 | Kortright | 2019 | [30763536](https://pubmed.ncbi.nlm.nih.gov/30763536/) | 200 | MATCH | 1.0 | [10.1016/j.chom.2019.01.014](https://doi.org/10.1016/j.chom.2019.01.014) | Citation chaining | Bacteriophage design and therapy |
| 27 | Krishnan | 2025 | [40816267](https://pubmed.ncbi.nlm.nih.gov/40816267/) | 200 | MATCH | 1.0 | [10.1016/j.cell.2025.07.033](https://doi.org/10.1016/j.cell.2025.07.033) | Database search | Machine-learning drug discovery |
| 28 | LeCun | 2015 | [26017442](https://pubmed.ncbi.nlm.nih.gov/26017442/) | 200 | MATCH | 1.0 | [10.1038/nature14539](https://doi.org/10.1038/nature14539) | Citation chaining | Shared methodological ground |
| 29 | Lee | 2023 | [37469443](https://pubmed.ncbi.nlm.nih.gov/37469443/) | 200 | MATCH | 1.0 | [10.3389/fbioe.2023.1226182](https://doi.org/10.3389/fbioe.2023.1226182) | Database search | CRISPR-Cas genome editing |
| 30 | Li | 2014 | [25476604](https://pubmed.ncbi.nlm.nih.gov/25476604/) | 200 | MATCH | 1.0 | [10.1186/s13059-014-0554-4](https://doi.org/10.1186/s13059-014-0554-4) | Citation chaining | CRISPR-Cas genome editing |
| 31 | Li | 2023 | [35341983](https://pubmed.ncbi.nlm.nih.gov/35341983/) | 200 | MATCH | 1.0 | [10.1016/j.gpb.2022.02.006](https://doi.org/10.1016/j.gpb.2022.02.006) | Database search | CRISPR-Cas genome editing |
| 32 | Lin | 2023 | [36927031](https://pubmed.ncbi.nlm.nih.gov/36927031/) | 200 | MATCH | 1.0 | [10.1126/science.ade2574](https://doi.org/10.1126/science.ade2574) | Citation chaining | Shared methodological ground |
| 33 | Lipinski | 2001 | [11259830](https://pubmed.ncbi.nlm.nih.gov/11259830/) | 200 | TITLE-DIFF | 0.65 | [10.1016/s0169-409x(00)00129-0](https://doi.org/10.1016/s0169-409x(00)00129-0) | Citation chaining | Machine-learning drug discovery |
| 34 | Listgarten | 2018 | [29998038](https://pubmed.ncbi.nlm.nih.gov/29998038/) | 200 | MATCH | 1.0 | [10.1038/s41551-017-0178-6](https://doi.org/10.1038/s41551-017-0178-6) | Citation chaining | CRISPR-Cas genome editing |
| 35 | Luo | 2024 | [38199209](https://pubmed.ncbi.nlm.nih.gov/38199209/) | 200 | MATCH | 1.0 | [10.1016/j.compbiomed.2024.107932](https://doi.org/10.1016/j.compbiomed.2024.107932) | Database search | CRISPR-Cas genome editing |
| 36 | Madani | 2023 | [36702895](https://pubmed.ncbi.nlm.nih.gov/36702895/) | 200 | MATCH | 1.0 | [10.1038/s41587-022-01618-2](https://doi.org/10.1038/s41587-022-01618-2) | Citation chaining | Bacteriophage design and therapy |
| 37 | Meyers | 2021 | [34082136](https://pubmed.ncbi.nlm.nih.gov/34082136/) | 200 | MATCH | 1.0 | [10.1016/j.drudis.2021.05.019](https://doi.org/10.1016/j.drudis.2021.05.019) | Database search | Machine-learning drug discovery |
| 38 | Mullowney | 2023 | [37697042](https://pubmed.ncbi.nlm.nih.gov/37697042/) | 200 | MATCH | 1.0 | [10.1038/s41573-023-00774-7](https://doi.org/10.1038/s41573-023-00774-7) | Database search | Machine-learning drug discovery |
| 39 | Nami | 2021 | [34174831](https://pubmed.ncbi.nlm.nih.gov/34174831/) | 200 | MATCH | 1.0 | [10.1186/s12866-021-02256-5](https://doi.org/10.1186/s12866-021-02256-5) | Database search | Bacteriophage design and therapy |
| 40 | Nguyen | 2024 | [39541441](https://pubmed.ncbi.nlm.nih.gov/39541441/) | 200 | MATCH | 1.0 | [10.1126/science.ado9336](https://doi.org/10.1126/science.ado9336) | Citation chaining | Bacteriophage design and therapy |
| 41 | Notin | 2025 | [40739008](https://pubmed.ncbi.nlm.nih.gov/40739008/) | 200 | MATCH | 1.0 | [10.1038/d41586-025-02135-3](https://doi.org/10.1038/d41586-025-02135-3) | Database search | CRISPR-Cas genome editing |
| 42 | Ouzzani | 2016 | [27919275](https://pubmed.ncbi.nlm.nih.gov/27919275/) | 200 | MATCH | 1.0 | [10.1186/s13643-016-0384-4](https://doi.org/10.1186/s13643-016-0384-4) | Citation chaining | Shared methodological ground |
| 43 | Öztürk | 2018 | [30423097](https://pubmed.ncbi.nlm.nih.gov/30423097/) | 200 | MATCH | 1.0 | [10.1093/bioinformatics/bty593](https://doi.org/10.1093/bioinformatics/bty593) | Citation chaining | Machine-learning drug discovery |
| 44 | Page | 2021 | [33782057](https://pubmed.ncbi.nlm.nih.gov/33782057/) | 200 | MATCH | 1.0 | [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71) | Citation chaining | Shared methodological ground |
| 45 | Parikesit | 2026 | [42191274](https://pubmed.ncbi.nlm.nih.gov/42191274/) | 200 | MATCH | 1.0 | [10.1016/bs.ircmb.2025.11.004](https://doi.org/10.1016/bs.ircmb.2025.11.004) | Citation chaining | Shared methodological ground |
| 46 | Pires | 2016 | [27250768](https://pubmed.ncbi.nlm.nih.gov/27250768/) | 200 | MATCH | 1.0 | [10.1128/MMBR.00069-15](https://doi.org/10.1128/MMBR.00069-15) | Citation chaining | Bacteriophage design and therapy |
| 47 | Rives | 2021 | [33876751](https://pubmed.ncbi.nlm.nih.gov/33876751/) | 200 | MATCH | 1.0 | [10.1073/pnas.2016239118](https://doi.org/10.1073/pnas.2016239118) | Citation chaining | Shared methodological ground |
| 48 | Sandve | 2013 | [24204232](https://pubmed.ncbi.nlm.nih.gov/24204232/) | 200 | MATCH | 1.0 | [10.1371/journal.pcbi.1003285](https://doi.org/10.1371/journal.pcbi.1003285) | Citation chaining | Shared methodological ground |
| 49 | Silva | 2025 | [40359589](https://pubmed.ncbi.nlm.nih.gov/40359589/) | 200 | MATCH | 1.0 | [10.1016/j.virol.2025.110559](https://doi.org/10.1016/j.virol.2025.110559) | Database search | Bacteriophage design and therapy |
| 50 | Silverstein | 2025 | [40262634](https://pubmed.ncbi.nlm.nih.gov/40262634/) | 200 | MATCH | 1.0 | [10.1038/s41586-025-09021-y](https://doi.org/10.1038/s41586-025-09021-y) | Database search | CRISPR-Cas genome editing |
| 51 | Smith | 1981 | [7265238](https://pubmed.ncbi.nlm.nih.gov/7265238/) | 200 | MATCH | 1.0 | [10.1016/0022-2836(81)90087-5](https://doi.org/10.1016/0022-2836(81)90087-5) | Citation chaining | Shared methodological ground |
| 52 | Stephens | 2015 | [26151137](https://pubmed.ncbi.nlm.nih.gov/26151137/) | 200 | MATCH | 1.0 | [10.1371/journal.pbio.1002195](https://doi.org/10.1371/journal.pbio.1002195) | Citation chaining | Shared methodological ground |
| 53 | Stokes | 2020 | [32084340](https://pubmed.ncbi.nlm.nih.gov/32084340/) | 200 | MATCH | 1.0 | [10.1016/j.cell.2020.01.021](https://doi.org/10.1016/j.cell.2020.01.021) | Citation chaining | Machine-learning drug discovery |
| 54 | Tropsha | 2024 | [38066301](https://pubmed.ncbi.nlm.nih.gov/38066301/) | 200 | MATCH | 1.0 | [10.1038/s41573-023-00832-0](https://doi.org/10.1038/s41573-023-00832-0) | Database search | Machine-learning drug discovery |
| 55 | Trott | 2010 | [19499576](https://pubmed.ncbi.nlm.nih.gov/19499576/) | 200 | MATCH | 1.0 | [10.1002/jcc.21334](https://doi.org/10.1002/jcc.21334) | Citation chaining | Machine-learning drug discovery |
| 56 | Tsai | 2015 | [25513782](https://pubmed.ncbi.nlm.nih.gov/25513782/) | 200 | MATCH | 1.0 | [10.1038/nbt.3117](https://doi.org/10.1038/nbt.3117) | Citation chaining | CRISPR-Cas genome editing |
| 57 | Vamathevan | 2019 | [30976107](https://pubmed.ncbi.nlm.nih.gov/30976107/) | 200 | MATCH | 1.0 | [10.1038/s41573-019-0024-5](https://doi.org/10.1038/s41573-019-0024-5) | Citation chaining | Machine-learning drug discovery |
| 58 | Varadi | 2022 | [34791371](https://pubmed.ncbi.nlm.nih.gov/34791371/) | 200 | MATCH | 1.0 | [10.1093/nar/gkab1061](https://doi.org/10.1093/nar/gkab1061) | Citation chaining | Shared methodological ground |
| 59 | Venter | 2022 | [35868275](https://pubmed.ncbi.nlm.nih.gov/35868275/) | 200 | MATCH | 1.0 | [10.1016/j.cell.2022.06.046](https://doi.org/10.1016/j.cell.2022.06.046) | Citation chaining | Bacteriophage design and therapy |
| 60 | Watson | 2023 | [37433327](https://pubmed.ncbi.nlm.nih.gov/37433327/) | 200 | MATCH | 1.0 | [10.1038/s41586-023-06415-8](https://doi.org/10.1038/s41586-023-06415-8) | Citation chaining | Shared methodological ground |
| 61 | Wilkinson | 2016 | [26978244](https://pubmed.ncbi.nlm.nih.gov/26978244/) | 200 | MATCH | 1.0 | [10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18) | Citation chaining | Shared methodological ground |
| 62 | Yang | 2022 | [35889440](https://pubmed.ncbi.nlm.nih.gov/35889440/) | 200 | MATCH | 1.0 | [10.3390/molecules27144568](https://doi.org/10.3390/molecules27144568) | Database search | Machine-learning drug discovery |
| 63 | Zhang | 2024 | [39418300](https://pubmed.ncbi.nlm.nih.gov/39418300/) | 200 | MATCH | 1.0 | [10.1371/journal.pcbi.1012525](https://doi.org/10.1371/journal.pcbi.1012525) | Database search | Bacteriophage design and therapy |
| 64 | Zhavoronkov | 2019 | [31477924](https://pubmed.ncbi.nlm.nih.gov/31477924/) | 200 | MATCH | 1.0 | [10.1038/s41587-019-0224-x](https://doi.org/10.1038/s41587-019-0224-x) | Citation chaining | Machine-learning drug discovery |
| 65 | Zheng | 2024 | [39737570](https://pubmed.ncbi.nlm.nih.gov/39737570/) | 200 | MATCH | 1.0 | [10.1093/bib/bbae696](https://doi.org/10.1093/bib/bbae696) | Database search | Machine-learning drug discovery |

## Summary

- References in the manuscript: **65**
- PMID resolved at PubMed: **65 / 65**
- DOI resolved at Crossref (HTTP 200): **65 / 65**
- Exact title match between the two services: **64 / 65**
- Title variant (publisher subtitle only): **1**
- Unresolved or mismatched, retained: **0**

## Cross-reference audit

- Every entry in the reference list is cited in the body text: **yes**
- Every in-text citation appears in the reference list: **yes**
- Abstract and Conclusion contain no citations, by design: **yes**
- Body paragraphs without a citation (Abstract and Conclusion exempt): **0**
