import json, subprocess, sys
PMIDS = """22745249 23873081 26780180 34265844 29532027 30423097 11259830 36702895 27250768 35065702
23287718 23287722 25184501 24463181 24336571 24336569 25476604 25513782 31634902 27096365
34791371 32084340 31477924 22270643 19499576 34278794 30976107 29366762 38718835 34282049
37433327 30763534 31068712 33876751 36927031 33782057 19621072 27919275 24204232 26978244
28398311 22908215 2231712 7265238 5420325 26527721""".split()
def get(batch):
    url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id="+",".join(batch)
    for _ in range(4):
        r=subprocess.run(["curl","-sS","--http1.1","-m","60","--retry","2",url],capture_output=True,text=True)
        try: return json.loads(r.stdout)["result"]
        except Exception: pass
    return {}
out={}
for i in range(0,len(PMIDS),6):
    d=get(PMIDS[i:i+6])
    for p in PMIDS[i:i+6]:
        r=d.get(p)
        if not r or "error" in r:
            print(p,"NOT FOUND"); continue
        au=[a["name"] for a in r.get("authors",[]) if a.get("authtype")=="Author"]
        doi=next((a["value"] for a in r.get("articleids",[]) if a["idtype"]=="doi"),"")
        out[p]=dict(pmid=p,title=r.get("title","").rstrip("."),journal=r.get("source"),
                    year=(r.get("pubdate") or "")[:4],volume=r.get("volume"),issue=r.get("issue"),
                    pages=r.get("pages"),authors=au,doi=doi)
        print(p,"|",out[p]["year"],"|",out[p]["journal"],"|",out[p]["title"][:88],"| doi:",doi or "-")
json.dump(out,open("build/pubmed_meta.json","w"),indent=1)
print("VERIFIED",len(out),"of",len(PMIDS))
