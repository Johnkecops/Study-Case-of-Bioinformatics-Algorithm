# -*- coding: utf-8 -*-
"""Minimal Office Math (OMML) builder for python-docx."""
MNS = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
WNS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

def r(t, upright=False):
    sty = '<m:rPr><m:sty m:val="p"/></m:rPr>' if upright else ''
    t = (t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))
    return ('<m:r>%s<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
            '<w:sz w:val="24"/></w:rPr><m:t xml:space="preserve">%s</m:t></m:r>' % (sty, t))

def sub(base, s):  return '<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>' % (base, s)
def sup(base, s):  return '<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>' % (base, s)
def subsup(b, sb, sp): return '<m:sSubSup><m:e>%s</m:e><m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>'%(b,sb,sp)

def nary(chr_, sb, sp, body, undovr=True):
    loc = 'undOvr' if undovr else 'subSup'
    pr = ('<m:naryPr><m:chr m:val="%s"/><m:limLoc m:val="%s"/>'
          '<m:subHide m:val="0"/><m:supHide m:val="%s"/><m:grow m:val="1"/></m:naryPr>'
          % (chr_, loc, '1' if sp is None else '0'))
    return ('<m:nary>%s<m:sub>%s</m:sub><m:sup>%s</m:sup><m:e>%s</m:e></m:nary>'
            % (pr, sb, sp or '', body))

def frac(num, den):
    return '<m:f><m:fPr><m:type m:val="bar"/></m:fPr><m:num>%s</m:num><m:den>%s</m:den></m:f>' % (num, den)

def delim(body, beg="(", end=")"):
    return ('<m:d><m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/></m:dPr>'
            '<m:e>%s</m:e></m:d>' % (beg, end, body))

def acc(base, chr_="&#x0302;"):
    return '<m:acc><m:accPr><m:chr m:val="%s"/></m:accPr><m:e>%s</m:e></m:acc>' % (chr_, base)

def omath(body):
    return '<m:oMath %s %s>%s</m:oMath>' % (MNS, WNS, body)

# ----- the nine equations -----
def build():
    E = {}
    # 1  d(g,s) = SUM_{i=1..20} 1[ g_i != s_i ]
    E["eq1"] = (r("d") + delim(r("g")+r(", ")+r("s")) + r(" = ")
        + nary("&#x2211;", r("i")+r(" = ")+r("1"), r("20"),
               r("&#x1D7D9;", True) + delim(sub(r("g"), r("i")) + r(" &#x2260; ") + sub(r("s"), r("i")), "[", "]")))
    # 2  CFD(g,s) = PROD_{i : g_i != s_i} w_i ,  0 <= w_i <= 1
    E["eq2"] = (r("CFD", True) + delim(r("g")+r(", ")+r("s")) + r(" = ")
        + nary("&#x220F;", r("i : ")+sub(r("g"),r("i"))+r(" &#x2260; ")+sub(r("s"),r("i")), None,
               sub(r("w"), r("i")))
        + r(",     ") + r("0 &#x2264; ") + sub(r("w"), r("i")) + r(" &#x2264; 1"))
    # 3  S = 100 / (1 + SUM_{s in OT} CFD(g,s))
    E["eq3"] = (r("S") + r(" = ") + frac(r("100"),
        r("1 + ") + nary("&#x2211;", r("s ")+r("&#x2208;")+r(" ")+r("OT", True), None,
                         r("CFD", True) + delim(r("g")+r(", ")+r("s")))))
    # 4  yhat = f_theta(m,t) ~ pKd = -log10 Kd
    E["eq4"] = (acc(r("y")) + r(" = ") + sub(r("f"), r("&#x03B8;")) + delim(r("m")+r(", ")+r("t"))
        + r(" &#x2248; ") + r("p", True) + sub(r("K"), r("d", True)) + r(" = &#x2212;")
        + sub(r("log", True), r("10")) + r(" ") + sub(r("K"), r("d", True)))
    # 5  dG = RT ln Kd
    E["eq5"] = (r("&#x0394;") + r("G") + r(" = ") + r("RT") + r(" ") + r("ln", True) + r(" ")
        + sub(r("K"), r("d", True)))
    # 6  m* = argmax_m [ f_theta(m,t) - lambda pen(m) ]
    E["eq6"] = (sup(r("m"), r("&#x2217;")) + r(" = ")
        + nary(" ", r("m"), None, "", True).replace('<m:chr m:val=" "/>','')  # placeholder removed below
        )
    E["eq6"] = (sup(r("m"), r("&#x2217;")) + r(" = ") + r("arg max", True)
        + sub(r(""), r("m")) + r(" ")
        + delim(sub(r("f"), r("&#x03B8;")) + delim(r("m")+r(", ")+r("t"))
                + r(" &#x2212; ") + r("&#x03BB;") + r(" &#xB7; ") + r("pen", True) + delim(r("m")),
                "[", "]"))
    # 7  P(x) = PROD_{i=1..L} P(x_i | x_<i)
    E["eq7"] = (r("P") + delim(r("x")) + r(" = ")
        + nary("&#x220F;", r("i")+r(" = ")+r("1"), r("L"),
               r("P") + delim(sub(r("x"), r("i")) + r(" | ") + sub(r("x"), r("&lt; i")))))
    # 8  log P(x) = SUM_{i=1..L} log P(x_i | x_<i)
    E["eq8"] = (r("log", True) + r(" ") + r("P") + delim(r("x")) + r(" = ")
        + nary("&#x2211;", r("i")+r(" = ")+r("1"), r("L"),
               r("log", True) + r(" ") + r("P") + delim(sub(r("x"), r("i")) + r(" | ") + sub(r("x"), r("&lt; i")))))
    # 9  x* = argmax_x [ phi_host(x) + beta log P(x) ]
    E["eq9"] = (sup(r("x"), r("&#x2217;")) + r(" = ") + r("arg max", True)
        + sub(r(""), r("x")) + r(" ")
        + delim(sub(r("&#x03C6;"), r("host", True)) + delim(r("x"))
                + r(" + ") + r("&#x03B2;") + r(" &#xB7; ") + r("log", True) + r(" ") + r("P") + delim(r("x")),
                "[", "]"))
    return {k: omath(v) for k, v in E.items()}
