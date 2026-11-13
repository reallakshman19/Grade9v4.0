"""Read-only report/input checks; only writes this documentation validation receipt."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
from PIL import Image
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    findings=[]
    data=json.loads((ROOT/'SOURCE_RECEIPT.json').read_text(encoding='utf-8'))
    for row in data['retained_sources']:
        if sha(Path(row['original_path']))!=row['sha256']:findings.append('SOURCE_CHANGED:'+row['original_path'])
        if sha(ROOT/row['retained_copy'])!=row['sha256']:findings.append('RETAINED_COPY_CHANGED:'+row['retained_copy'])
    with (ROOT/'GOLDEN_FILE_INVENTORY.csv').open(encoding='utf-8-sig',newline='') as stream:rows=list(csv.DictReader(stream))
    for row in rows:
        p=Path(row['absolute_path'])
        if not p.is_file() or p.stat().st_size!=int(row['bytes']) or sha(p)!=row['sha256']:
            findings.append('INVENTORY_CHANGED:'+str(p))
    if len(rows)!=256 or sum(x['scope']=='GOLDEN_TREE' for x in rows)!=152:findings.append('COUNT_MISMATCH')
    class Inspect(HTMLParser):
        def __init__(self):super().__init__();self.links=[];self.scripts=0;self.tables=0;self.images=[]
        def handle_starttag(self,tag,attrs):
            attrs=dict(attrs)
            if tag=='script':self.scripts+=1
            if tag=='table':self.tables+=1
            if 'href' in attrs:self.links.append(attrs['href'])
            if tag=='img':self.images.append(attrs.get('src',''))
    checked=0;remote=[];html_reports={}
    for name in ['index.html','golden-fixtures.html']:
        doc=Inspect();doc.feed((ROOT/name).read_text(encoding='utf-8'))
        for href in doc.links+doc.images:
            bits=urlsplit(href)
            if bits.scheme in ['http','https']:remote.append(href);continue
            if bits.scheme=='file':
                value=unquote(bits.path)
                if re.match(r'^/[A-Za-z]:/',value):value=value[1:]
                p=Path(value)
            elif bits.scheme:findings.append('UNEXPECTED_URI:'+href);continue
            else:p=ROOT/unquote(bits.path)
            if not p.exists():findings.append('BROKEN_LINK:'+name+':'+href)
            checked+=1
        if doc.scripts:findings.append('UNEXPECTED_SCRIPT:'+name)
        html_reports[name]=dict(tables=doc.tables,links=len(doc.links),images=len(doc.images),scripts=doc.scripts)
    svg=ET.parse(ROOT/'progress.svg').getroot()
    ids=[x.attrib['id'] for x in svg.iter() if 'id' in x.attrib]
    if len(ids)!=len(set(ids)):findings.append('DUPLICATE_SVG_ID')
    text=' '.join(''.join(x.itertext()) for x in svg if x.tag.endswith('desc'))
    if not text:findings.append('SVG_DESCRIPTION_ABSENT')
    with Image.open(ROOT/'progress.png') as im:
        size=im.size
        if size!=(1200,1500):findings.append('PNG_SIZE_MISMATCH')
        im.verify()
    received=json.loads((ROOT/'RECEIVED_CORE2_READBACK.json').read_text())
    for key in ['audit','owner_package']:
        row=received[key]
        if sha(Path(row['path']))!=row['sha256']:findings.append('RECEIVED_ARCHIVE_CHANGED:'+key)
    report=dict(status='PASS' if not findings else 'FAIL',findings=findings,inventory_rows_verified=len(rows),
        golden_tree_files_verified=152,retained_source_files_verified=len(data['retained_sources']),local_links_checked=checked,
        remote_links=remote,html=html_reports,SVG_XML='PASS',PNG_size=list(size),
        diagram_visual_inspection='PERFORMED by author on rasterized export; readable, no observed clipping',
        browser_layout='NOT_RUN',archive_build_scripts='NOT_EXECUTED',native_product_build='NOT_RUN',
        previous_implementation_tests='RECORDED 50/50; not rerun for documentation',
        independent_academic_review='NOT_RUN',Owner_acceptance='PENDING',
        scope='Report/diagram/catalogue integrity and source preservation, not learner-course or scientific acceptance')
    (ROOT/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=report['status'],inventory_rows=len(rows),links=checked,findings=findings)))
    return 0 if not findings else 1


if __name__=='__main__':raise SystemExit(main())
