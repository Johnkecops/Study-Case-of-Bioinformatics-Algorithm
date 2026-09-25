import json, subprocess, urllib.parse, difflib, re
meta=json.load(open("build/pubmed_meta.json"))
def norm(s): return re.sub(r'[^a-z0-9]+',' ',(s or "").lower()).strip()
res={}
for p,m in meta.items():
    doi=m.get("doi","")
    if not doi:
        res[p]=dict(status="no-doi"); print(p,"NO DOI |",m["title"][:60]); continue
    u="https://api.crossref.org/works/"+urllib.parse.quote(doi)+"?mailto=arli.parikesit@i3l.ac.id"
    code=""; ct=""
    for _ in range(3):
        r=subprocess.run(["curl","-sS","--http1.1","-m","45","-w","\n%{http_code}",u],capture_output=True,text=True)
        parts=r.stdout.rsplit("\n",1)
        code=parts[-1].strip()
        if code=="200":
            try:
                j=json.loads(parts[0])["message"]
                ct=(j.get("title") or [""])[0]
                m["cr_container"]=(j.get("container-title") or [""])[0]
                m["cr_year"]=str((j.get("issued",{}).get("date-parts") or [[""]])[0][0])
                break
            except Exception: code="parse-err"
        elif code=="404": break
    sim=difflib.SequenceMatcher(None,norm(ct),norm(m["title"])).ratio() if ct else 0
    verdict = "MATCH" if code=="200" and sim>0.80 else ("TITLE-DIFF" if code=="200" else "FAIL")
    res[p]=dict(status=code, sim=round(sim,2), verdict=verdict, cr_title=ct)
    m["cr_verdict"]=verdict; m["cr_status"]=code; m["cr_sim"]=round(sim,2)
    if verdict!="MATCH": print(p,verdict,code,round(sim,2),"|",m["title"][:55],"||",ct[:55])
json.dump(meta,open("build/pubmed_meta.json","w"),indent=1)
from collections import Counter
print(Counter(v.get("verdict",v["status"]) for v in res.values()))
