# -*- coding: utf-8 -*-
"""APA 6th reference list and in-text citation generation from verified PubMed/Crossref metadata."""
import json, re, unicodedata

def _fold(t):
    return ''.join(c for c in unicodedata.normalize('NFKD', t) if not unicodedata.combining(c)).lower()

META = json.load(open("build/pubmed_meta.json"))
FIN  = json.load(open("build/final_refs.json"))
ALL  = FIN["search"] + FIN["chain"]

def initials(name):
    """'Doench JG' -> ('Doench', 'J. G.')"""
    parts = name.rsplit(" ", 1)
    if len(parts) == 1: return name, ""
    sur, ini = parts
    if not ini.isupper() or len(ini) > 4:      # not an initial block
        return name, ""
    return sur, " ".join(c + "." for c in ini)

def surname(pmid):
    m = META[pmid]
    if m.get("corporate"): return m["corporate"]
    if not m["authors"]: return m["title"].split()[0]
    return initials(m["authors"][0])[0]

def n_authors(pmid):
    m = META[pmid]
    return 1 if m.get("corporate") else len(m["authors"])

def surnames(pmid):
    m = META[pmid]
    if m.get("corporate"): return [m["corporate"]]
    return [initials(a)[0] for a in m["authors"]]

def journal(pmid):
    m = META[pmid]
    c = (m.get("cr_container") or "").strip()
    j = m["journal"]
    return c if len(c) > len(j) else j

def ref_authors(pmid):
    m = META[pmid]
    if m.get("corporate"): return m["corporate"]
    au = m["authors"]
    fmt = []
    for a in au:
        s, i = initials(a)
        fmt.append(("%s, %s" % (s, i)).strip().rstrip(","))
    if len(fmt) == 1: return fmt[0]
    if len(fmt) <= 7: return ", ".join(fmt[:-1]) + ", & " + fmt[-1]
    return ", ".join(fmt[:6]) + ", . . . " + fmt[-1]           # APA 6th: first six, ellipsis, last

def entry(pmid):
    """Return (author_part, year, title, journal, vol_issue_pages, doi) for styled rendering."""
    m = META[pmid]
    vol = m.get("volume") or ""
    iss = m.get("issue") or ""
    pgs = m.get("pages") or ""
    tail = vol + ("(%s)" % iss if iss else "")
    if pgs: tail = (tail + ", " + pgs) if tail else pgs
    return dict(auth=ref_authors(pmid), year=m["year"], title=m["title"],
                journal=journal(pmid), tail=tail, doi=m.get("doi",""), sortkey=(_fold(surname(pmid)), m["year"]))

ORDER = sorted(ALL, key=lambda p: entry(p)["sortkey"])

_seen = set()
def cite(pmid, narrative=False):
    """APA 6th in-text citation. Tracks first vs. subsequent occurrence for 3-5 author works."""
    y = META[pmid]["year"]; n = n_authors(pmid); sn = surnames(pmid)
    first = pmid not in _seen
    _seen.add(pmid)
    if n == 1:      who = sn[0]
    elif n == 2:    who = "%s %s %s" % (sn[0], "and" if narrative else "&", sn[1])
    elif n <= 5 and first:
        who = ", ".join(sn[:-1]) + (", and " if narrative else ", & ") + sn[-1]
    else:           who = sn[0] + " et al."
    return ("%s (%s)" % (who, y)) if narrative else ("(%s, %s)" % (who, y))

def reset(): _seen.clear()
