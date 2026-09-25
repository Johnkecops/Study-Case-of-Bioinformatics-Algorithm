# -*- coding: utf-8 -*-
import os
os.environ.setdefault("MPLCONFIGDIR", os.environ.get("TMPDIR","/tmp")+"/mpl")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({"font.family":"serif","font.serif":["Times New Roman","DejaVu Serif"],"font.size":7.2})
EDGE="#1a1a1a"; FILL="#ffffff"; GREY="#f0f0f0"

def box(ax,x,y,w,h,txt,fill=FILL,fs=7.2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.004,rounding_size=0.006",
                 linewidth=0.7,edgecolor=EDGE,facecolor=fill))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,linespacing=1.32)

def arrow(ax,p,q):
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle="-|>",mutation_scale=7,linewidth=0.7,color=EDGE,
                                 shrinkA=0,shrinkB=0))

def prisma(path):
    fig,ax=plt.subplots(figsize=(6.4,7.4)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    for yy,lab in [(0.935,"Identification"),(0.700,"Screening"),(0.400,"Eligibility"),(0.130,"Included")]:
        ax.text(0.008,yy,lab,rotation=90,ha="center",va="center",fontsize=7.4,style="italic")
    L,W=0.055,0.415; X,XW=0.500,0.265; O,OW=0.785,0.207
    cx=L+W/2; ox=O+OW/2
    box(ax,L,0.880,W,0.115,"Records identified through database searching\nPubMed/MEDLINE, 4 September 2026 (n = 18,991)\nBlock 1 CRISPR-Cas n = 1,521\nBlock 2 drug discovery n = 10,844\nBlock 3 bacteriophage n = 6,626",GREY,6.8)
    box(ax,O,0.880,OW,0.115,"Records identified\nthrough other methods\nCitation chaining and\nhand searching\n(n = 94)",GREY,6.8)
    box(ax,O,0.730,OW,0.100,"Records excluded after\nmetadata verification\n(n = 50)\nSource mismatch 9;\nredundant 41",FILL,6.8)
    box(ax,O,0.600,OW,0.070,"Sources included from\nother methods\n(n = 44)",FILL,6.8)
    box(ax,L,0.795,W,0.045,"Duplicate records removed across blocks (n = 123)",FILL,6.9)
    box(ax,L,0.705,W,0.045,"Unique records after deduplication (n = 18,868)",FILL,6.9)
    box(ax,L,0.610,W,0.048,"Records not sought for retrieval,\noutside the relevance-ranked cap (n = 18,690)",FILL,6.9)
    box(ax,L,0.505,W,0.048,"Records screened at title and abstract (n = 178)",FILL,6.9)
    box(ax,X,0.470,XW,0.115,"Records excluded at title\nand abstract (n = 94)\nOutside the three domains 64;\nno algorithm specified 20;\nlaboratory-only 10",FILL,6.8)
    box(ax,L,0.380,W,0.048,"Full-text records assessed for eligibility (n = 84)",FILL,6.9)
    box(ax,X,0.320,XW,0.135,"Full-text records excluded (n = 63)\nTopically redundant with a\nretained record 48; outside scope 9;\npreprint superseded 3;\nduplicate book chapter 2;\nno algorithmic detail 1",FILL,6.8)
    box(ax,L,0.255,W,0.048,"Studies included from database searching (n = 21)",FILL,6.9)
    box(ax,L,0.060,W,0.055,"Total sources included in the synthesis (n = 65)",GREY,7.3)
    for a,b in [(0.880,0.840),(0.795,0.750),(0.705,0.658),(0.610,0.553),(0.505,0.428),(0.380,0.303),(0.255,0.115)]:
        arrow(ax,(cx,a),(cx,b))
    arrow(ax,(L+W,0.529),(X,0.529))
    arrow(ax,(L+W,0.404),(X,0.404))
    arrow(ax,(ox,0.880),(ox,0.830))
    arrow(ax,(ox,0.730),(ox,0.670))
    ax.plot([ox,ox],[0.600,0.0875],lw=0.7,color=EDGE)
    arrow(ax,(ox,0.0875),(L+W,0.0875))
    fig.savefig(path,dpi=400,bbox_inches="tight",facecolor="white"); plt.close(fig)

def synthesis(path):
    fig,ax=plt.subplots(figsize=(6.4,3.5)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    cols=[("CRISPR-Cas\ngenome editing","Measured cleavage at\nmismatched target sites","Aggregate specificity\nscore S (Eq. 3)","Ranked guide RNAs","Genome-wide break\nmapping assays"),
          ("Machine-learning\ndrug discovery","Measured binding\nconstants","Affinity minus drug-\nlikeness penalty (Eq. 6)","Ranked candidate\nmolecules","Binding and\nphenotypic assays"),
          ("Bacteriophage\ndesign","Natural phage and\nprokaryotic genomes","Host fitness plus\nlog-likelihood (Eq. 9)","Ranked genome\ndesigns","Particle recovery and\nlytic activity assays")]
    rows=[("Training",0.610),("Objective",0.425),("Output",0.240),("Validation",0.055)]
    w=0.285
    for j,c in enumerate(cols):
        x=0.055+j*0.312
        box(ax,x,0.855,w,0.100,c[0],GREY,7.8)
        for i,(lab,y) in enumerate(rows):
            box(ax,x,y,w,0.120,c[i+1],GREY if i==1 else FILL,7.0)
        for a,b in [(0.855,0.735),(0.610,0.550),(0.425,0.365),(0.240,0.180)]:
            arrow(ax,(x+w/2,a),(x+w/2,b))
    for lab,y in rows:
        ax.text(0.028,y+0.060,lab,rotation=90,ha="center",va="center",fontsize=6.9,style="italic")
    fig.savefig(path,dpi=400,bbox_inches="tight",facecolor="white"); plt.close(fig)

if __name__=="__main__":
    prisma("figures/fig1_prisma.png"); synthesis("figures/fig2_synthesis.png")
    print("figures written")
