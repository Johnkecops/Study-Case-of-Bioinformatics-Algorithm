# -*- coding: utf-8 -*-
import sys, re, collections
sys.path.insert(0,"build")
import content as C, tables as T

CHUNKS=[("ABSTRACT",C.ABSTRACT)]
CHUNKS+= [("INTRO %d"%(i+1),t) for i,t in enumerate(C.INTRO)]
CHUNKS+= [("METH %s"%s,t) for s,ps in C.METHODS for t in ps]
n=0
for it in C.FINDINGS:
    if it[0]=="p": n+=1; CHUNKS.append(("FIND %d"%n,it[1]))
    if it[0]=="box": CHUNKS.append(("BOXNOTE %d"%it[1],it[4]))
CHUNKS+= [("CONCL %d"%(i+1),t) for i,t in enumerate(C.CONCLUSION)]
CHUNKS+= [("CAPTION/TABLE", " ".join([T.TABLE1["caption"],T.TABLE2["caption"],T.TABLE3["caption"]]+
          [c for r in T.TABLE1["rows"]+T.TABLE3["rows"] for c in r]))]

VOCAB = r"\b(delve|delves|crucial|pivotal|vibrant|tapestry|testament|underscore\w*|showcase\w*|garner\w*|intricate|intricacies|interplay|foster\w*|enhanc\w*|align with|landscape|realm|holistic|robust|seamless|leverage|leverages|leveraging|myriad|plethora|paradigm shift|groundbreaking|cutting-edge|state-of-the-art|game-chang\w*|transformative|profound|renowned|nestled|boasts|stands as|serves as|plays a (?:key|vital|crucial|significant) role|it is important to note|it is worth noting|in conclusion|moreover|furthermore|additionally|notably|arguably|ultimately|comprehensive|multifaceted|nuanced|unlock\w*|empower\w*|streamlin\w*|navigat\w* the|shed light|deep dive|at its core|the real question|fundamentally|reflects broader|marking a|setting the stage|evolving)\b"
DASH = r"[—–]"
CURLY = r"[‘’“”]"
NEGPAR = r"\b(not (?:just|only|merely)\b[^.]{0,80}?\bbut\b|it'?s not\b[^.]{0,60}?,\s*it'?s\b)"
ING = r",\s+(highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|contributing to|cultivating|fostering|encompassing|showcasing|demonstrating|paving)\b"
FILLER = r"\b(in order to|due to the fact that|at this point in time|in the event that|has the ability to|a wide range of|a variety of|plays a role)\b"
HEDGE = r"\b(could potentially|may possibly|might potentially|it could be argued|somewhat|rather quite)\b"
INVIS = r"[​‌‍﻿­⁠ ]"

TESTS=[("AI vocabulary",VOCAB),("em/en dash",DASH),("curly quotes",CURLY),
       ("negative parallelism",NEGPAR),("-ing padding",ING),("filler",FILLER),
       ("hedging",HEDGE),("invisible unicode",INVIS)]
hits=collections.Counter(); detail=[]
for name,txt in CHUNKS:
    for lab,pat in TESTS:
        for m in re.finditer(pat,txt,re.I):
            hits[lab]+=1; detail.append((lab,name,m.group(0),txt[max(0,m.start()-45):m.end()+45].replace("\n"," ")))
print("=== SLOP SCAN ===")
for lab,_ in TESTS: print("  %-22s %d"%(lab,hits[lab]))
print()
for lab,name,g,ctx in detail: print("[%s] %s :: '%s'\n    ...%s..."%(lab,name,g,ctx))
# rule of three
print("\n=== rule-of-three candidates (X, Y, and Z) ===")
c=0
for name,txt in CHUNKS:
    for m in re.finditer(r"\b\w[\w\- ]{3,28},\s+\w[\w\- ]{3,28},\s+and\s+\w[\w\- ]{3,28}\b",txt):
        c+=1; print("  %s :: %s"%(name,m.group(0)[:95]))
print("  total:",c)
# sentence length variance
import statistics
sents=[len(s.split()) for _,t in CHUNKS for s in re.split(r"(?<=[.!?])\s+",t) if s.strip()]
print("\nsentences=%d mean=%.1f sd=%.1f min=%d max=%d"%(len(sents),statistics.mean(sents),statistics.pstdev(sents),min(sents),max(sents)))
