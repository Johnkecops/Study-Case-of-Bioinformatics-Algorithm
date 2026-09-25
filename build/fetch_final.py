import json, subprocess
SEARCH="26780180 40262634 40739008 35341983 37980345 37469443 40468633 38199209 37697042 40816267 33779453 38663579 38066301 39737570 37794737 34082136 35889440 42561074 34174831 39418300 40359589".split()
CHAIN="22745249 23873081 25184501 24463181 29945655 29998038 25513782 25476604 31634902 27096365 34265844 34791371 36927031 33876751 37433327 30423097 29532027 11259830 22270643 19499576 30976107 31477924 32084340 36702895 39541441 27250768 30763536 31068712 34428079 35065702 39299261 33782057 27919275 24204232 26978244 26151137 2231712 7265238 26017442 42191274 42064452 33450856".split()
meta=json.load(open("build/pubmed_meta.json"))
need=[p for p in SEARCH+CHAIN if p not in meta]
def call(u):
    for _ in range(4):
        r=subprocess.run(["curl","-sS","--http1.1","-m","60","--retry","2",u],capture_output=True,text=True)
        try: return json.loads(r.stdout)
        except Exception: pass
    return {}
for i in range(0,len(need),6):
    b=need[i:i+6]
    d=call("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id="+",".join(b)).get("result",{})
    for p in b:
        r=d.get(p)
        if not r or "error" in r: print("MISSING",p); continue
        au=[a["name"] for a in r.get("authors",[]) if a.get("authtype")=="Author"]
        doi=next((a["value"] for a in r.get("articleids",[]) if a["idtype"]=="doi"),"")
        meta[p]=dict(pmid=p,title=r.get("title","").rstrip("."),journal=r.get("source"),
                     year=(r.get("pubdate") or "")[:4],volume=r.get("volume"),issue=r.get("issue"),
                     pages=r.get("pages"),authors=au,doi=doi)
        print("added",p,meta[p]["year"],meta[p]["title"][:70])
json.dump(meta,open("build/pubmed_meta.json","w"),indent=1)
json.dump({"search":SEARCH,"chain":CHAIN},open("build/final_refs.json","w"),indent=1)
print("meta size",len(meta),"final refs",len(SEARCH)+len(CHAIN))
