# -*- coding: utf-8 -*-
"""Strip AI/provenance metadata from the built DOCX and set authoritative document properties."""
import zipfile, shutil, re, sys, datetime, os

SRC = sys.argv[1]
TMP = SRC + ".tmp"
DROP_PREFIX = ("customXml/",)
DROP_EXACT  = ("docProps/thumbnail.jpeg",)
AUTHOR = "Arli Aditya Parikesit"
TITLE  = ("Algorithmic perspectives in bioinformatics: a review of computational methods "
          "interpreting emerging trends in biotechnology")
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

CORE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
 '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"'
 ' xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"'
 ' xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
 '<dc:title>%s</dc:title><dc:subject>Bioinformatics algorithms</dc:subject>'
 '<dc:creator>%s</dc:creator><cp:keywords>Bioinformatics algorithms; CRISPR-Cas; drug discovery; '
 'bacteriophage design; antibiotic resistance</cp:keywords><dc:description></dc:description>'
 '<cp:lastModifiedBy>%s</cp:lastModifiedBy><cp:revision>1</cp:revision>'
 '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
 '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified>'
 '<cp:category></cp:category></cp:coreProperties>') % (TITLE, AUTHOR, AUTHOR, NOW, NOW)

APP = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
 '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"'
 ' xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
 '<Template>Normal.dotm</Template><TotalTime>0</TotalTime><Application>Microsoft Word</Application>'
 '<DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company></Company><LinksUpToDate>false</LinksUpToDate>'
 '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion>'
 '</Properties>')

zin = zipfile.ZipFile(SRC)
names = zin.namelist()
dropped = [n for n in names
           if n.startswith(DROP_PREFIX) or n in DROP_EXACT]

with zipfile.ZipFile(TMP, "w", zipfile.ZIP_DEFLATED) as zout:
    for n in names:
        if n in dropped: continue
        data = zin.read(n)
        if n == "docProps/core.xml": data = CORE.encode()
        elif n == "docProps/app.xml": data = APP.encode()
        elif n == "[Content_Types].xml":
            t = data.decode()
            t = re.sub(r'<Override PartName="/customXml[^>]*/>', "", t)
            t = re.sub(r'<Override PartName="/docProps/thumbnail\.jpeg"[^>]*/>', "", t)
            t = re.sub(r'<Default Extension="jpeg"[^>]*/>', "", t)
            data = t.encode()
        elif n.endswith(".rels"):
            t = data.decode()
            t = re.sub(r'<Relationship[^>]*Target="[^"]*customXml[^"]*"[^>]*/>', "", t)
            t = re.sub(r'<Relationship[^>]*Target="[^"]*thumbnail\.jpeg"[^>]*/>', "", t)
            data = t.encode()
        zout.writestr(n, data)
zin.close()
shutil.move(TMP, SRC)
print("dropped parts:", dropped or "none")
print("core.xml and app.xml replaced; creator set to", AUTHOR)
