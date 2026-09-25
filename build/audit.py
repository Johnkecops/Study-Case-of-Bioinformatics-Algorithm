# -*- coding: utf-8 -*-
import sys, re, json, collections
sys.path.insert(0,"build")
import content as C, refs as R
from areas import AREAS

CIT=re.compile(r"\{(\d+)\}|\[\[(\d+)\]\]")
def pmids(t): return [m.group(1) or m.group(2) for m in CIT.finditer(t)]

bodies=[]
for i,t in enumerate(C.INTRO): bodies.append(("Introduction para %d"%(i+1),t))
for sub,ps in C.METHODS:
    for i,t in enumerate(ps): bodies.append(("Methods / %s para %d"%(sub,i+1),t))
n=0
for item in C.FINDINGS:
    if item[0]=="p":
        n+=1; bodies.append(("Findings para %d"%n,item[1]))

print("=== AUDIT 1: every body paragraph carries at least one citation (abstract & conclusion exempt) ===")
bad=[(l,t) for l,t in bodies if not pmids(t)]
print("body paragraphs checked:",len(bodies),"| uncited:",len(bad))
for l,_ in bad: print("   UNCITED:",l)

print("\n=== AUDIT 2: abstract and conclusion carry no citations ===")
ac=pmids(C.ABSTRACT)+[p for t in C.CONCLUSION for p in pmids(t)]
print("citations found in abstract/conclusion:",len(ac), "OK" if not ac else ac)

used=set(p for _,t in bodies for p in pmids(t))
listed=set(R.ORDER)
print("\n=== AUDIT 3: reference list vs. in-text usage ===")
print("references in list:",len(listed),"| distinct cited in text:",len(used))
print("listed but never cited:",sorted(listed-used) or "none")
print("cited but not listed:",sorted(used-listed) or "none")

print("\n=== AUDIT 4: equation/pseudocode narration carries citations ===")
items=C.FINDINGS
for i,it in enumerate(items):
    if it[0] in ("eq","box"):
        prev=[items[j] for j in range(i-1,-1,-1) if items[j][0]=="p"]
        label = ("Equation %d"%it[2]) if it[0]=="eq" else ("Box %d"%it[1])
        ok = bool(prev and pmids(prev[0][1]))
        print("  %-12s preceding narrative cited: %s"%(label,"yes" if ok else "NO"))

print("\n=== AUDIT 5: verification status of every reference ===")
M=R.META
bads=[p for p in R.ORDER if M[p].get("cr_verdict") not in ("MATCH","TITLE-DIFF") or not M[p].get("doi")]
print("all 63 have PMID: %s | all have DOI: %s | Crossref resolved: %d/%d"%(
  all(M[p]["pmid"] for p in R.ORDER), all(M[p]["doi"] for p in R.ORDER),
  sum(1 for p in R.ORDER if M[p].get("cr_status")=="200"), len(R.ORDER)))
print("unverified:",bads or "none")

print("\n=== AUDIT 6: adjacent-citation merge false positives ===")
fp=[]
for l,t in bodies:
    s=t
    for m in CIT.finditer(t): pass
    for mm in re.finditer(r"\)\s+\(", re.sub(CIT,"(X)",t)):
        seg=re.sub(CIT,"(X)",t)[max(0,mm.start()-30):mm.end()+30]
        if "(X) (X)" not in seg: fp.append((l,seg))
print("suspicious merges:",fp or "none")
