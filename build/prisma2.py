import json, subprocess, urllib.parse
P=json.load(open("build/prisma_counts.json"))
def call(u):
    for _ in range(4):
        r=subprocess.run(["curl","-sS","--http1.1","-m","90","--retry","2",u],capture_output=True,text=True)
        try: return json.loads(r.stdout)
        except Exception: pass
    return {}
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&"
union="(%s) OR (%s) OR (%s)"%(P["B1_CRISPR"]["query"],P["B2_DRUG"]["query"],P["B3_PHAGE"]["query"])
u=call(E+"retmax=0&term="+urllib.parse.quote(union))
uc=int(u["esearchresult"]["count"]); print("UNION",uc,"DUPES",P["TOTAL_PUBMED"]-uc)
P["UNION"]=uc; P["DUPLICATES"]=P["TOTAL_PUBMED"]-uc
# top-60 per block by relevance -> title/abstract screening pool
pool={}
for k in ["B1_CRISPR","B2_DRUG","B3_PHAGE"]:
    d=call(E+"retmax=60&sort=relevance&term="+urllib.parse.quote(P[k]["query"]))
    ids=d["esearchresult"]["idlist"]; pool[k]=ids; print(k,"pool",len(ids))
allids=[]
for k in pool:
    for i in pool[k]:
        if i not in allids: allids.append(i)
print("SCREEN POOL (deduped across blocks):",len(allids))
P["POOL_PER_BLOCK"]=60; P["SCREEN_POOL"]=len(allids); P["POOL_DUP"]=180-len(allids)
recs={}
for i in range(0,len(allids),8):
    b=allids[i:i+8]
    d=call("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id="+",".join(b)).get("result",{})
    for p in b:
        r=d.get(p,{})
        recs[p]=dict(year=(r.get("pubdate") or "")[:4],journal=r.get("source"),title=(r.get("title") or "").rstrip("."),
                     type=";".join(r.get("pubtype",[])))
json.dump({"pool":pool,"recs":recs},open("build/screen_pool.json","w"),indent=1)
json.dump(P,open("build/prisma_counts.json","w"),indent=1)
print("saved",len(recs))
