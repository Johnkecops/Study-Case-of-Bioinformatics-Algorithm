import json
d=json.load(open("build/screen_pool.json")); recs=d["recs"]; pool=d["pool"]
order=[]
for k in ["B1_CRISPR","B2_DRUG","B3_PHAGE"]:
    for i in pool[k]:
        if i not in order: order.append(i)

# ---- Title/abstract screening: excluded records with documented reason ----
TA_EXCL={
# outside the three application domains
"35839778":"domain","33096023":"domain","40239646":"domain","41926577":"domain","38443662":"domain",
"37084259":"domain","32286628":"domain","35649413":"domain","39677777":"domain","40866699":"domain",
"40174587":"domain","40709098":"domain","37889037":"domain","39696352":"domain","38340729":"domain",
"42353201":"domain","40261207":"domain","35236300":"domain","36765063":"domain","38091991":"domain",
"39119666":"domain","41253931":"domain","36623998":"domain","29887378":"domain","38499731":"domain",
"36152211":"domain","39316581":"domain","34323201":"domain","37779408":"domain","37031957":"domain",
"41219972":"domain","27885969":"domain","41820158":"domain","41057624":"domain","39002700":"domain",
"38999924":"domain","36374423":"domain","36546891":"domain","33316575":"domain","38499981":"domain",
"41428827":"domain","34900137":"domain","40498839":"domain","38383452":"domain","39504601":"domain",
"41853549":"domain","30659855":"domain","32162265":"domain","36734893":"domain","36845830":"domain",
"39018352":"domain","41238301":"domain","34170506":"domain","25666799":"domain","32858938":"domain",
"41406010":"domain","39663481":"domain","40838049":"domain","36464489":"domain","37896809":"domain",
"41656299":"domain","39110597":"domain","41777249":"domain","40840758":"domain",
# no algorithmic specification / editorial / news / opinion
"38152286":"noalgo","38684833":"noalgo","28757882":"noalgo","35847004":"noalgo","37007046":"noalgo",
"34222205":"noalgo","30028206":"noalgo","32345062":"noalgo","31174387":"noalgo","30888845":"noalgo",
"30288997":"noalgo","33176630":"noalgo","32614747":"noalgo","35301149":"noalgo","36736583":"noalgo",
"37529294":"noalgo","31995074":"noalgo","37728008":"noalgo","29668343":"noalgo","33759121":"noalgo",
# experimental / structural, no computational component
"30804513":"wetlab","36306733":"wetlab","33346713":"wetlab","37526217":"wetlab","27661255":"wetlab",
"33478580":"wetlab","36409909":"wetlab","35880867":"wetlab","30322741":"wetlab","31862543":"wetlab",
"32162265x":"wetlab",
}
# ---- Full-text eligibility exclusions ----
FT_EXCL={
"34731467":"dup-chapter","34731473":"dup-chapter","32455882":"overlap","29644494":"overlap",
"36710911":"overlap","38136570":"overlap","27276584":"overlap","36150044":"scope",
"33844136":"overlap","36768346":"overlap","40451590":"overlap","35708267":"scope","41011141":"overlap",
"30338743":"overlap","37014633":"overlap","40782836":"noalgo-ft","39135699":"scope",
"37374901":"overlap","36903484":"overlap","35950840":"overlap","36659812":"overlap","33045744":"overlap",
"35920769":"overlap","32813660":"overlap","37503040":"preprint-superseded","40666868":"preprint-superseded",
"41174147":"overlap","40475446":"preprint-superseded","34952265":"overlap","39951981":"overlap",
"36353213":"overlap","37185764":"scope","41174147x":"overlap","39344712":"overlap",
"32006410":"overlap","33417623":"scope","38641083":"overlap","32353475":"overlap","31971562":"overlap",
"37847697":"overlap","36271848":"overlap","41203686":"overlap","33616444":"overlap","31890142":"overlap",
"40699706":"overlap","38473785":"overlap","34399578":"overlap","33386098":"overlap","39922803":"scope",
"42446430":"scope","41850287":"scope","41039172":"scope","32725781":"overlap","41260783":"overlap",
"33198233":"overlap","35440144":"overlap","36347444":"overlap","38385768":"overlap","34560276":"overlap",
"38173000":"overlap","34885952":"overlap","30710114":"overlap","40829801":"overlap","32541958":"overlap",
}
inc=[i for i in order if i not in TA_EXCL and i not in FT_EXCL]
ft_pool=[i for i in order if i not in TA_EXCL]
P=json.load(open("build/prisma_counts.json"))
P["TA_SCREENED"]=len(order)
P["TA_EXCLUDED"]=len([i for i in order if i in TA_EXCL])
P["FT_ASSESSED"]=len(ft_pool)
P["FT_EXCLUDED"]=len([i for i in ft_pool if i in FT_EXCL])
from collections import Counter
P["TA_REASONS"]=dict(Counter(TA_EXCL[i] for i in order if i in TA_EXCL))
P["FT_REASONS"]=dict(Counter(FT_EXCL[i] for i in ft_pool if i in FT_EXCL))
P["INCLUDED_FROM_SEARCH"]=len(inc)
P["INCLUDED_IDS"]=inc
json.dump(P,open("build/prisma_counts.json","w"),indent=1)
print("TA screened",P["TA_SCREENED"],"excluded",P["TA_EXCLUDED"],P["TA_REASONS"])
print("FT assessed",P["FT_ASSESSED"],"excluded",P["FT_EXCLUDED"],P["FT_REASONS"])
print("INCLUDED from search:",len(inc))
for i in inc: print("  ",i,recs[i]["year"],recs[i]["journal"][:20],"|",recs[i]["title"][:80])
