import json, subprocess
PMIDS="""26151137 9254694 23329690 30763536 30107853 30801254 31448179 29762716 31106371 23792628
31308553 29309725 29595767 33390943 30887799 35637307 34428079 30819575 34079000 26017442
29618526 30478442 22039361 22388286 25516281 9918945 37059067 33578201 39590827 12824337""".split()
def get(b):
    url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id="+",".join(b)
    for _ in range(4):
        r=subprocess.run(["curl","-sS","--http1.1","-m","60","--retry","2",url],capture_output=True,text=True)
        try: return json.loads(r.stdout)["result"]
        except Exception: pass
    return {}
out=json.load(open("build/pubmed_meta.json"))
out.pop("26527721",None)
new={}
for i in range(0,len(PMIDS),6):
    d=get(PMIDS[i:i+6])
    for p in PMIDS[i:i+6]:
        r=d.get(p)
        if not r or "error" in r: print(p,"NOT FOUND"); continue
        au=[a["name"] for a in r.get("authors",[]) if a.get("authtype")=="Author"]
        doi=next((a["value"] for a in r.get("articleids",[]) if a["idtype"]=="doi"),"")
        new[p]=dict(pmid=p,title=r.get("title","").rstrip("."),journal=r.get("source"),
                    year=(r.get("pubdate") or "")[:4],volume=r.get("volume"),issue=r.get("issue"),
                    pages=r.get("pages"),authors=au,doi=doi)
        print(p,"|",new[p]["year"],"|",new[p]["journal"],"|",new[p]["title"][:88],"| doi:",doi or "-")
out.update(new)
json.dump(out,open("build/pubmed_meta.json","w"),indent=1)
print("TOTAL",len(out))
