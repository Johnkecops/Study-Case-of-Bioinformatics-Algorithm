import json, subprocess, urllib.parse
Q=["DeepCRISPR optimized CRISPR guide RNA design by deep learning",
   "Elevation prediction of off-target activity CRISPR guide",
   "machine learning prediction bacteriophage host range",
   "synthetic genomics engineering bacteriophage genome design review",
   "antimicrobial resistance Indonesia surveillance",
   "genome language model design DNA sequences Evo",
   "deep generative model de novo drug design review",
   "protein language model phage tail fiber design",
   "reproducibility computational biology software containers",
   "dengue Indonesia bioinformatics computational drug discovery"]
def run(args):
    for _ in range(4):
        r=subprocess.run(["curl","-sS","--http1.1","-m","60","--retry","2"]+args,capture_output=True,text=True)
        try: return json.loads(r.stdout)
        except Exception: pass
    return {}
for q in Q:
    u="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=4&sort=relevance&term="+urllib.parse.quote(q)
    ids=run([u]).get("esearchresult",{}).get("idlist",[])
    if not ids: print("Q:",q,"-> none"); continue
    u2="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id="+",".join(ids)
    d=run([u2]).get("result",{})
    print("Q:",q)
    for i in ids:
        r=d.get(i,{})
        print("   ",i,"|",(r.get("pubdate") or "")[:4],"|",r.get("source"),"|",(r.get("title") or "")[:88])
