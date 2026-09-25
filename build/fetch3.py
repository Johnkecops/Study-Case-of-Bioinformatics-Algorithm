import json, subprocess, urllib.parse
def run(u):
    for _ in range(4):
        r=subprocess.run(["curl","-sS","--http1.1","-m","60","--retry","2",u],capture_output=True,text=True)
        try: return json.loads(r.stdout)
        except Exception: pass
    return {}
u="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=8&sort=date&term="+urllib.parse.quote("Parikesit AA[Author]")
ids=run(u).get("esearchresult",{}).get("idlist",[])
print("Parikesit PMIDs:",ids)
ADD="29945655 29998038 38361822 39418300 35868275 39299261 39146948 39541441 38663579 27401684 33450856".split()+ids
DROP="30107853 30801254 31448179 30819575 34079000 37059067 33578201 39590827 12824337".split()
out=json.load(open("build/pubmed_meta.json"))
for d in DROP: out.pop(d,None)
for i in range(0,len(ADD),6):
    b=ADD[i:i+6]
    d=run("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id="+",".join(b)).get("result",{})
    for p in b:
        r=d.get(p)
        if not r or "error" in r: print(p,"NOT FOUND"); continue
        au=[a["name"] for a in r.get("authors",[]) if a.get("authtype")=="Author"]
        doi=next((a["value"] for a in r.get("articleids",[]) if a["idtype"]=="doi"),"")
        out[p]=dict(pmid=p,title=r.get("title","").rstrip("."),journal=r.get("source"),
                    year=(r.get("pubdate") or "")[:4],volume=r.get("volume"),issue=r.get("issue"),
                    pages=r.get("pages"),authors=au,doi=doi)
        print(p,"|",out[p]["year"],"|",out[p]["journal"],"|",out[p]["title"][:80],"|",", ".join(au[:3]))
json.dump(out,open("build/pubmed_meta.json","w"),indent=1)
print("TOTAL",len(out))
