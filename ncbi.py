#!/usr/bin/env python3
"""
Module: ncbi
Purpose: Fetch the curated real records used by the dashboard from NCBI, with an on-disk cache.
Author: Dr. Arli Aditya Parikesit
Date: 2026
Parameters:
    - NCBI_EMAIL: environment variable, sent with every request as NCBI etiquette requires
    - NCBI_API_KEY: optional environment variable; raises the rate ceiling from 3 to 10 requests/second
References:
    - Sayers, E. W. et al. (2022). Database resources of the NCBI. Nucleic Acids Res, 50(D1), D20-D26.
      https://doi.org/10.1093/nar/gkab1112
    - Kim, S. et al. (2023). PubChem 2023 update. Nucleic Acids Res, 51(D1), D1373-D1380.
      https://doi.org/10.1093/nar/gkac956
"""

import hashlib
import json
import os
import re
import time
from pathlib import Path

import requests

from algos import revcomp

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PUGREST = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
CACHE = Path(__file__).parent / "data" / "ncbi_cache"
TOOL = "iksad-bioalgo-dashboard"
TIMEOUT = 60

# Verified against NCBI on 25 September 2026: esummary on db=gene for each symbol restricted to
# txid83332 (M. tuberculosis H37Rv), coordinates converted from 0-based chrstart/chrstop to 1-based
# inclusive. katG and pncA are on the minus strand, so start > stop in the source record; the pairs
# below are stored low-to-high with the strand recorded separately.
TB_GENES = {
    "katG (Rv1908c) - isoniazid, catalase-peroxidase": {
        "gene_id": "885638", "start": 2153889, "stop": 2156111, "strand": "-",
    },
    "rpoB (Rv0667) - rifampicin, RNA polymerase beta": {
        "gene_id": "888164", "start": 759807, "stop": 763325, "strand": "+",
    },
    "inhA (Rv1484) - isoniazid/ethionamide, enoyl-ACP reductase": {
        "gene_id": "886523", "start": 1674202, "stop": 1675011, "strand": "+",
    },
    "pncA (Rv2043c) - pyrazinamide, amidase": {
        "gene_id": "888260", "start": 2288681, "stop": 2289241, "strand": "-",
    },
    "embB (Rv3795) - ethambutol, arabinosyltransferase": {
        "gene_id": "886126", "start": 4246514, "stop": 4249810, "strand": "+",
    },
}
H37RV = "NC_000962.3"
H37RV_LENGTH = 4_411_532   # slen of the record, same esummary call

# Verified by esummary on db=nuccore, 25 September 2026; lengths in the comments are the returned slen.
PHAGE_TRAIN = {
    "Enterobacteria phage lambda": "NC_001416.1",      # 48,502 bp
    "Enterobacteria phage T7": "NC_001604.1",          # 39,937 bp
    "Mycobacterium phage D29": "NC_001900.1",          # 49,136 bp
}
PHAGE_TEST = {"Enterobacteria phage T4": "NC_000866.4"}            # 168,903 bp, held out
NONPHAGE_CONTROL = {"Y. pestis plasmid pPCP1": "NC_005816.1"}      # 9,609 bp, negative control

# Real anti-TB and antibacterial agents. Descriptors are not stored here; they are fetched from
# PubChem so that every number on screen has a traceable source record.
COMPOUNDS = [
    "isoniazid", "rifampicin", "ethambutol", "pyrazinamide", "bedaquiline",
    "ciprofloxacin", "moxifloxacin", "linezolid", "delamanid", "clofazimine",
    "streptomycin", "amikacin",
]
# ConnectivitySMILES, not CanonicalSMILES: PUG-REST renamed the property and returns the new key, so
# asking for the old name silently yields a record without the field requested.
PROPERTIES = [
    "MolecularWeight", "XLogP", "HBondDonorCount", "HBondAcceptorCount",
    "TPSA", "RotatableBondCount", "ConnectivitySMILES",
]
# The cache key carries the property set: changing PROPERTIES must not serve a payload fetched for a
# different one, which would drop the new descriptor with no error anywhere.
_PROP_TAG = hashlib.sha256(",".join(PROPERTIES).encode()).hexdigest()[:8]

_last_call = [0.0]


def _throttle():
    """NCBI allows 3 requests/second without a key, 10 with one."""
    gap = 0.11 if os.environ.get("NCBI_API_KEY") else 0.40
    wait = gap - (time.monotonic() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    _last_call[0] = time.monotonic()


def _identify(params):
    params = dict(params, tool=TOOL, email=os.environ.get("NCBI_EMAIL", ""))
    key = os.environ.get("NCBI_API_KEY")
    if key:
        params["api_key"] = key
    return params


def _cached(name, fetch, parse):
    """Return the parsed cached record for `name`, calling `fetch()` once on a miss.

    The cache is what lets the dashboard open without network access, and what keeps a demonstration
    from re-querying NCBI on every Streamlit rerun. `parse` runs before the write, so a malformed
    200 response (a truncated body, an HTML error page) raises and is never committed to disk; a
    cached file that cannot be parsed would otherwise be permanent.
    """
    path = CACHE / name
    if path.exists():
        return parse(path.read_text())
    text = fetch()
    parsed = parse(text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return parsed


def _get(url, params):
    _throttle()
    r = requests.get(url, params=_identify(params), timeout=TIMEOUT)
    r.raise_for_status()
    return r.text


def _parse_fasta(text, accession):
    lines = text.strip().splitlines()
    if not lines or not lines[0].startswith(">"):
        raise ValueError(f"{accession}: efetch did not return FASTA")
    seq = re.sub(r"[^A-Za-z]", "", "".join(lines[1:])).upper()
    if not seq:
        raise ValueError(f"{accession}: FASTA record carried no sequence")
    return lines[0][1:], seq


def fasta(accession, start=None, stop=None):
    """Fetch one nuccore record, or a 1-based inclusive slice of it, as (header, uppercase sequence)."""
    span = f"_{start}_{stop}" if start else ""
    params = {"db": "nuccore", "id": accession, "rettype": "fasta", "retmode": "text"}
    if start:
        params |= {"seq_start": start, "seq_stop": stop}
    return _cached(f"nuccore_{accession}{span}.fasta",
                   lambda: _get(f"{EUTILS}/efetch.fcgi", params),
                   lambda t: _parse_fasta(t, accession))


def gene_window(label, flank=100_000):
    """Fetch a TB resistance gene plus `flank` bp either side, as the declared off-target search space.

    The full 4.41 Mb H37Rv genome is not used as the search space: a window keeps the cached payload
    small enough to ship. The panel states on screen that specificity values are window-local.
    ponytail: window scan, index the whole genome if the values need to be tool-grade.
    """
    g = TB_GENES[label]
    start = max(1, g["start"] - flank)
    stop = min(H37RV_LENGTH, g["stop"] + flank)
    header, seq = fasta(H37RV, start, stop)
    gene = seq[g["start"] - start:g["stop"] - start + 1]
    if g["strand"] == "-":
        gene = revcomp(gene)   # the slice is the plus strand; the gene reads the other way
    return {
        "header": header, "window": seq, "gene": gene, "window_start": start,
        "window_stop": stop, "gene_start": g["start"], "gene_stop": g["stop"],
        "strand": g["strand"], "gene_id": g["gene_id"],
    }


def compound_properties(names=None):
    """Fetch PubChem's curated descriptors for the compound list. Returns a list of dicts."""
    names = names or COMPOUNDS
    rows = []
    for name in names:
        url = f"{PUGREST}/compound/name/{name}/property/{','.join(PROPERTIES)}/JSON"
        try:
            rec = _cached(f"pubchem_{name}_{_PROP_TAG}.json", lambda u=url: _get(u, {}),
                          lambda t: json.loads(t)["PropertyTable"]["Properties"][0])
        except (requests.HTTPError, KeyError, IndexError, ValueError) as exc:
            # A missing compound must not take the panel down; it is reported as missing instead.
            rows.append({"name": name, "error": str(exc)[:120]})
            continue
        rec["name"] = name
        if "MolecularWeight" in rec:
            rec["MolecularWeight"] = float(rec["MolecularWeight"])
        rows.append(rec)
    return rows


def prefetch():
    """Populate the cache for every record the dashboard uses. Run once, with network access."""
    got = []
    for label in TB_GENES:
        w = gene_window(label)
        got.append(f"{label.split(' ')[0]}: window {len(w['window']):,} bp, gene {len(w['gene']):,} bp")
    for name, acc in {**PHAGE_TRAIN, **PHAGE_TEST, **NONPHAGE_CONTROL}.items():
        _, seq = fasta(acc)
        got.append(f"{name} ({acc}): {len(seq):,} bp")
    props = compound_properties()
    ok = [r for r in props if "error" not in r]
    got.append(f"PubChem: {len(ok)}/{len(props)} compounds resolved")
    for r in props:
        if "error" in r:
            got.append(f"  MISSING {r['name']}: {r['error']}")
    return got


if __name__ == "__main__":
    for line in prefetch():
        print(line)
