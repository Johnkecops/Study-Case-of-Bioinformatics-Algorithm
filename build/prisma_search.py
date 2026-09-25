import json, subprocess, urllib.parse
DATE='AND ("2012/01/01"[PDAT] : "2026/09/04"[PDAT])'
BLOCKS={
"B1_CRISPR":'((CRISPR[tiab] OR Cas9[tiab] OR "guide RNA"[tiab] OR sgRNA[tiab]) AND (algorithm*[tiab] OR "machine learning"[tiab] OR "deep learning"[tiab] OR "computational design"[tiab] OR "off-target prediction"[tiab] OR "score"[tiab])) '+DATE,
"B2_DRUG":'(("drug discovery"[tiab] OR "de novo design"[tiab] OR "virtual screening"[tiab] OR "binding affinity"[tiab]) AND ("deep learning"[tiab] OR "machine learning"[tiab] OR "generative model*"[tiab] OR "neural network*"[tiab] OR algorithm*[tiab])) '+DATE,
"B3_PHAGE":'((bacteriophage*[tiab] OR phage*[tiab]) AND (design*[tiab] OR engineer*[tiab] OR "machine learning"[tiab] OR "deep learning"[tiab] OR "generative model*"[tiab] OR "language model*"[tiab] OR algorithm*[tiab])) '+DATE,
}
def count(term):
    u="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=0&term="+urllib.parse.quote(term)
    for _ in range(4):
        r=subprocess.run(["curl","-sS","--http1.1","-m","60","--retry","2",u],capture_output=True,text=True)
        try: return int(json.loads(r.stdout)["esearchresult"]["count"])
        except Exception: pass
    return -1
res={}
tot=0
for k,v in BLOCKS.items():
    c=count(v); res[k]=dict(query=v,count=c); tot+=c
    print(k,c)
res["TOTAL_PUBMED"]=tot
print("TOTAL",tot)
json.dump(res,open("build/prisma_counts.json","w"),indent=1)
