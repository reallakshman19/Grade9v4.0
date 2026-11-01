"""Build documentation/inventories only; no source, product or archived script execution."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime, timezone
from html import escape
import csv
import hashlib
import json
import re
import shutil
import textwrap

OUT = Path(__file__).resolve().parent
REF = Path(r'C:\CodeC\Grade9v3.5')
WORK = Path(r'D:\CodeD\g9v3.5')
DOWNLOADS = Path(r'C:\Users\reall\Downloads')
PREP = WORK / 'chatgpt/output/WPE_Construction_Handoff_Skill_R1_2026-10-30'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def svg():
    stages = [
        ('Saved book / syllabus / figures', 'Inventory recorded; source truth remains reviewable', 'RETAINED', '#e4f3e9', '#287448'),
        ('Exact source units', 'One WPE-N01 example · 6 sources · 11 exact units', 'CHECKED CANDIDATE', '#e5effb', '#315f9f'),
        ('Core1A preparation requirements', '3 claims · 3 role requirements · 7 native mappings', 'CANDIDATE DELIVERED', '#e5effb', '#315f9f'),
        ('Scientific warrants and conditions', 'Candidate library; semantic review NOT_RUN', 'HOLD', '#fff1d4', '#9b6418'),
        ('Reviewed task + topic-adapter binding', 'No reviewed question join; adapter decision unresolved', 'HOLD', '#fff1d4', '#9b6418'),
        ('Owner approval of completed Core2', 'Latest received proposal: 14 leads / 7 vacancies / 0 admissions', 'PENDING', '#fff1d4', '#9b6418'),
        ('Native Core1A teaching authoring', 'No new lesson, package or manifest emitted', 'NOT STARTED', '#edf0f4', '#626f7d'),
        ('Governed render and teaching checks', 'Native build, browser and academic review NOT_RUN', 'NOT RUN', '#edf0f4', '#626f7d'),
        ('Owner Core1A acceptance', 'Exact build + teaching evidence required', 'PENDING', '#edf0f4', '#626f7d'),
        ('Fresh Core1B reconstruction', 'After Core1A approval; preserve the same decisive operation', 'DEFERRED', '#edf0f4', '#626f7d'),
    ]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1500" viewBox="0 0 1200 1500" role="img" aria-labelledby="title desc">',
        '<title id="title">WPE Source to Core1A progress</title><desc id="desc">One checked preparation candidate is delivered. Scientific qualification, reviewed question and adapter binding, completed Core2 approval, native Core1A authoring and acceptance remain open. D3.1 is paused.</desc>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#7b899a"/></marker></defs>',
        '<rect width="1200" height="1500" fill="#f7f9fc"/>',
        '<g font-family="Segoe UI,Arial,sans-serif" fill="#203047">',
        '<text x="50" y="52" font-size="29" font-weight="700">WPE · Source → Core1A</text>',
        '<text x="50" y="84" font-size="18">30 October 2026 · Progress is evidence-qualified; no completion percentage assigned</text>',
        '<text x="50" y="115" font-size="16">Green = retained · Blue = delivered candidate · Amber = unresolved prerequisite · Grey = future work</text>']
    for i, (title, detail, status, fill, stroke) in enumerate(stages):
        y = 150 + i * 120
        if i:
            parts.append(f'<path d="M450 {y-25}V{y-5}" stroke="#7b899a" stroke-width="2" marker-end="url(#arrow)"/>')
        parts += [f'<rect x="50" y="{y}" width="800" height="95" rx="12" fill="{fill}" stroke="{stroke}"/>',
                  f'<text x="70" y="{y+29}" font-size="21" font-weight="600">{i+1}. {escape(title)}</text>',
                  f'<text x="70" y="{y+57}" font-size="16">{escape(detail)}</text>',
                  f'<text x="70" y="{y+81}" font-size="14" font-weight="700" fill="{stroke}">{escape(status)}</text>']
    notes = [
        (170, 'Parallel source preparation', 'Can continue while Core2 is reviewed. It does not grant teaching-construction approval.'),
        (420, 'Golden comparison', '2 indexed candidates, neither Owner-blessed. References and negative controls are different evidence classes.'),
        (680, 'Mechanical ≠ academic', '50 recorded checks pass, including relocation. Coherent false prose can still pass integrity.'),
        (930, 'Current stop condition', 'Core1A construction waits for completed Core2 approval. No lesson has been built by this route.'),
        (1190, 'D3.1 stays PAUSED', 'No agent, installation, remote write or product rebuild is created by this report.'),
    ]
    for y, title, body in notes:
        parts.append(f'<rect x="885" y="{y}" width="270" height="170" rx="10" fill="white" stroke="#cbd5e2"/>')
        parts.append(f'<text x="902" y="{y+28}" font-size="16" font-weight="700">{escape(title)}</text>')
        for j, line in enumerate(textwrap.wrap(body, width=29)):
            parts.append(f'<text x="902" y="{y+56+j*22}" font-size="15">{escape(line)}</text>')
    parts += ['<text x="50" y="1410" font-size="19" font-weight="600">No accepted WPE Core1A is claimed.</text>',
              '<text x="50" y="1440" font-size="16">Keep source evidence, semantic qualification, native rendering and Owner acceptance separate.</text>', '</g></svg>']
    (OUT / 'progress.svg').write_text('\n'.join(parts), encoding='utf-8')
    (OUT / 'progress.mmd').write_text('''flowchart TD
    A["Book / syllabus / figures: retained"] --> B["Exact units: one WPE-N01 checked candidate"]
    B --> C["Construction requirements: candidate delivered"]
    C --> D["Science / warrant qualification: HOLD"]
    Q["Core2 latest received proposal: 14 leads / 7 vacant / 0 admitted"] --> E["Reviewed task + adapter binding: HOLD"]
    D --> E
    E --> F["Owner approves completed Core2: PENDING"]
    F --> G["Native Core1A authoring: NOT_STARTED"]
    G --> H["Governed render / teaching / runtime review: NOT_RUN"]
    H --> I["Owner Core1A approval: PENDING"]
    I --> J["Fresh Core1B: DEFERRED"]
    classDef candidate fill:#e5effb,stroke:#315f9f,color:#203047;
    classDef hold fill:#fff1d4,stroke:#9b6418,color:#203047;
    classDef future fill:#edf0f4,stroke:#626f7d,color:#203047;
    class B,C candidate;
    class D,E,F,Q hold;
    class G,H,I,J future;
''', encoding='utf-8')


def inline(value):
    tokens = []
    def link(match):
        label, target = match.group(1), match.group(2)
        if re.match(r'^[A-Za-z]:/', target):
            target = Path(target).as_uri()
        require_safe = not re.match(r'(?i)(javascript|data):', target)
        if not require_safe:
            return escape(match.group(0))
        tokens.append('<a href="' + escape(target, quote=True) + '">' + escape(label) + '</a>')
        return f'ZZLINK{len(tokens)-1}ZZ'
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, value)
    value = escape(value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)
    for i, token in enumerate(tokens):
        value = value.replace(f'ZZLINK{i}ZZ', token)
    return value


def markdown_html(text):
    lines = text.splitlines(); parts=[]; i=0
    while i < len(lines):
        line = lines[i]
        if not line.strip(): i+=1;continue
        if line.startswith('```'):
            block=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
            parts.append('<pre>'+escape('\n'.join(block))+'</pre>');i+=1;continue
        image = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)', line)
        if image:
            parts.append('<figure><a href="'+escape(image[2],quote=True)+'"><img src="'+escape(image[2],quote=True)+'" alt="'+escape(image[1],quote=True)+'"></a><figcaption>Open the SVG for full-size viewing.</figcaption></figure>');i+=1;continue
        heading = re.match(r'^(#{1,6}) (.*)', line)
        if heading:
            n=len(heading[1]);parts.append(f'<h{n}>'+inline(heading[2])+f'</h{n}>');i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', x) for x in cells):rows.append(cells)
                i+=1
            parts.append('<div class="table"><table>')
            for k,row in enumerate(rows):
                tag='th' if k==0 else 'td'
                parts.append('<tr>'+''.join(f'<{tag}>'+inline(v)+f'</{tag}>' for v in row)+'</tr>')
            parts.append('</table></div>');continue
        para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```','![')):
            para.append(lines[i]);i+=1
        parts.append('<p>'+inline(' '.join(para))+'</p>')
    return '\n'.join(parts)


def html_page(title, content):
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>body{font:17px/1.6 system-ui,sans-serif;color:#203047;background:#f7f9fc;margin:0}main{max-width:1120px;padding:24px;margin:auto}h1,h2,h3{line-height:1.22}h2{margin-top:40px;padding-top:18px;border-top:1px solid #d5deea}a{color:#174e9c;overflow-wrap:anywhere}nav{padding:14px;background:#e5effb;border-radius:10px}figure{margin:24px 0}img{max-width:100%;height:auto;background:white}figcaption{font-size:14px;color:#596a7c}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf0f4;padding:18px;border-radius:8px;font-size:14px}code{font-size:.9em;overflow-wrap:anywhere}.table{overflow:auto}table{border-collapse:collapse;width:100%;font-size:15px;background:white}th,td{text-align:left;vertical-align:top;padding:11px;border:1px solid #d3dce7;min-width:100px;overflow-wrap:anywhere}th{background:#eaf0f7}p{overflow-wrap:anywhere}</style><main><nav><a href="index.html">Concept report</a> · <a href="progress.svg">Progress diagram</a> · <a href="golden-fixtures.html">Full fixture catalogue</a> · <a href="GOLDEN_FILE_INVENTORY.csv">CSV inventory</a> · <a href="CONCEPT_REPORT.md">Markdown</a></nav>'+content+'</main></html>'


def main():
    receipts=[]
    def capture(source, name):
        dest=OUT/'evidence'/name;dest.parent.mkdir(exist_ok=True)
        shutil.copyfile(source,dest)
        receipts.append(dict(original_path=str(source),sha256=sha(source),retained_copy=dest.relative_to(OUT).as_posix()))
    capture(DOWNLOADS/'WPE_CORE2_R2_AUDIT_CONCEPT_ADDENDUM.md','ATTACHED_CORE2_ADDENDUM.md')
    for rel,name in [('golden/INDEX.md','GOLDEN_INDEX.md'),('golden/TECHNIQUES.md','GOLDEN_TECHNIQUES.md'),
        ('golden/units/G-MATH-LINEAR-CONSTRAINT/GOLDEN.md','G_MATH_DECLARATION.md'),('golden/units/G-CORE2-R2/GOLDEN.md','G_CORE2_DECLARATION.md'),
        ('benchmarks/quality-calibration/manifest.v1.json','CALIBRATION_MANIFEST.json'),
        ('evidence/stress-tests/polynomials-six-core/REPORT.md','POLYNOMIALS_REPORT.md')]:capture(REF/rel,name)
    capture(WORK/'chatgpt/output/WPE_CONSTRUCTION_HANDOFF_R1_DELIVERY_RECEIPT.json','HANDOFF_DELIVERY_RECEIPT.json')
    capture(PREP/'review/EXAMPLE_CHECK.json','HANDOFF_EXAMPLE_CHECK.json')
    capture(PREP/'review/VALIDATION_READBACK.md','HANDOFF_VALIDATION.md')
    rows=[]
    roots=[(REF/'golden','GOLDEN_TREE'),(REF/'evidence/stress-tests/polynomials-six-core','STRESS_CONTROL'),(REF/'tests/fixtures/render','RENDER_ASSET')]
    for root,group in roots:
        for p in sorted(root.rglob('*')):
            if not p.is_file():continue
            rel=p.relative_to(root).as_posix()
            kind=('INDEXED_CANDIDATE_MEMBER' if rel.startswith('units/') else 'REFERENCE_NOT_ACCEPTANCE' if rel.startswith('Reference/') else 'ANTI_EXAMPLE' if rel.startswith('anti/') else 'INDEX_OR_TECHNIQUE') if group=='GOLDEN_TREE' else group
            rows.append(dict(scope=group,kind=kind,relative_path=rel,absolute_path=str(p),bytes=p.stat().st_size,sha256=sha(p),acceptance='NOT_INFERRED',inspection='FILE_BYTES_INVENTORIED; CONTENT_ONLY_WHERE_CITED'))
    assert sum(r['scope']=='GOLDEN_TREE' for r in rows)==152, 'Golden tree changed; reconcile report counts'
    calibration=json.loads((REF/'benchmarks/quality-calibration/manifest.v1.json').read_text(encoding='utf-8'))
    checks=[]
    for specimen in calibration['specimens']:
        for rel,expected in specimen.get('files',{}).items():
            p=REF/'benchmarks/quality-calibration'/rel
            actual=sha(p) if p.is_file() else None
            checks.append(dict(id=specimen['id'],path=str(p),expected=expected,actual=actual,status='MATCH' if actual==expected else 'MISSING' if actual is None else 'DIFFERS'))
            if p.is_file():rows.append(dict(scope='CALIBRATION_NEGATIVE',kind=specimen['id'],relative_path=rel,absolute_path=str(p),bytes=p.stat().st_size,sha256=actual,acceptance='NEGATIVE_CONTROL',inspection='HASH_READBACK_ONLY'))
    reference_status=[]
    for ref in calibration['references']:
        for f in ref.get('source',{}).get('files',[]):
            p=REF/f['path'];actual=sha(p) if p.is_file() else None
            reference_status.append(dict(id=ref['id'],path=str(p),expected=f.get('sha256'),actual=actual,status='ABSENT_IN_CURRENT_CHECKOUT' if actual is None else 'MATCH' if actual==f.get('sha256') else 'PRESENT_UNPINNED' if not f.get('sha256') else 'DIFFERS_FROM_HISTORICAL_PIN'))
    save('CALIBRATION_READBACK.json',dict(negative_files=checks,positive_reference_current_checkout=reference_status,
        R1_exact_pdf='NOT_LOCATED_IN_REPOSITORY per manifest; no all-branch search rerun',behavioral_quality='NOT_RERUN'))
    with (OUT/'GOLDEN_FILE_INVENTORY.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    cat=['# Complete scoped golden fixture catalogue','',
        'All files under the supplied golden tree are listed below. Candidate, reference, negative control and asset membership are distinct from acceptance. No product is promoted by this list.','',
        '## Registered fixture candidates','',
        '| ID | Main source | Owner status |','|---|---|---|',
        '| G-MATH-LINEAR-CONSTRAINT | [Declaration]('+ (REF/'golden/units/G-MATH-LINEAR-CONSTRAINT/GOLDEN.md').as_uri()+') | CANDIDATE; no blessing |',
        '| G-CORE2-R2 | [Declaration]('+(REF/'golden/units/G-CORE2-R2/GOLDEN.md').as_uri()+') | CANDIDATE; no blessing |','',
        '## Calibration set — all seven entries','', '| ID | Kind | Title |','|---|---|---|']
    for x in calibration['specimens']+calibration['references']:cat.append('| '+x['id']+' | '+x['kind']+' | '+x['title']+' |')
    cat+=['','## Anti-example set — all fifteen','', '| ID | Failure mechanism |','|---|---|']
    for p in sorted((REF/'golden/anti').glob('*.md')):
        title=p.read_text(encoding='utf-8').splitlines()[0].lstrip('# ')
        cat.append('| ['+p.stem+']('+p.as_uri()+') | '+title.split(' — ',1)[-1]+' |')
    for group in ['GOLDEN_TREE','CALIBRATION_NEGATIVE','STRESS_CONTROL','RENDER_ASSET']:
        items=[x for x in rows if x['scope']==group]
        cat+=['','## '+group+' — '+str(len(items))+' physical files','', '| Kind | File | Bytes | SHA-256 prefix |','|---|---|---:|---|']
        for x in items:cat.append('| '+x['kind']+' | ['+x['relative_path']+']('+Path(x['absolute_path']).as_uri()+') | '+str(x['bytes'])+' | `'+x['sha256'][:16]+'` |')
    cat+=['','Full hashes and paths are in GOLDEN_FILE_INVENTORY.csv. Historical stress reports are attributed, not newly executed quality tests. Source file links require the original local project; the report ZIP is not a portable copy of the entire source repository.','']
    (OUT/'GOLDEN_FIXTURE_CATALOGUE.md').write_text('\n'.join(cat),encoding='utf-8')
    audit_path=DOWNLOADS/'WPE_CORE2_R2_READONLY_AUDIT.zip';owner_path=DOWNLOADS/'WPE_CORE2_R2_FULL_OWNER_REVIEW_PACKAGE.zip'
    audit={};owner={}
    with ZipFile(audit_path) as z:
        manifest=json.loads(z.read('MANIFEST.json'));failures=[]
        for name,row in manifest['files'].items():
            raw=z.read(name)
            if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:failures.append(name)
        assert not failures and z.testzip() is None
        for name in ['MANIFEST.json','README.md','06_REPRODUCIBLE_GATE_RESULTS.json']:
            (OUT/'evidence'/('AUDIT_'+name)).write_bytes(z.read(name))
        audit=dict(path=str(audit_path),sha256=sha(audit_path),CRC='PASS',manifest_payloads_verified=len(manifest['files']),failures=failures,
                   recorded_summary=json.loads(z.read('06_REPRODUCIBLE_GATE_RESULTS.json'))['summary'],four_input_checker='NOT_RERUN',appointment='UNAPPOINTED_DIAGNOSTIC')
    with ZipFile(owner_path) as z:
        package=json.loads(z.read('PACKAGE_RECEIPT.json'));selection=json.loads(z.read('owner_only/selection_21_places.json'))
        raw=z.read('owner_only/WPE_CORE2_COVERAGE_R1_RETURN.zip');nested_sha=hashlib.sha256(raw).hexdigest()
        assert nested_sha==package['r1_return_sha256_verified']
        with ZipFile(BytesIO(raw)) as nested:
            assert nested.testzip() is None
            dispositions=json.loads(nested.read('dispositions_79.json'))
            receipt=json.loads(nested.read('RETURN_RECEIPT.json'))
            failures=[]
            for f in receipt['output_files']:
                b=nested.read(f['path'])
                if len(b)!=f['bytes'] or hashlib.sha256(b).hexdigest()!=f['sha256']:failures.append(f['path'])
            assert not failures
        places=selection['places'];selected=[x for x in places if x.get('candidate_id')]
        assert len(places)==21 and len(selected)==14 and len({x['candidate_id'] for x in selected})==14
        assert len(dispositions['records'])==79
        identities={x['canonical_counting_id'] for x in dispositions['records']}
        assert len(identities)==78
        alias_pair=[x for x in dispositions['records'] if x['id'] in ['EX-M4','JEE-2026-04-05-S2-Q28']]
        assert len(alias_pair)==2 and len({x['canonical_counting_id'] for x in alias_pair})==1
        assert selection['admitted']==0
        for name in ['PACKAGE_RECEIPT.json','owner_only/RETURN_RECEIPT.json','owner_only/selection_21_places.json']:
            (OUT/'evidence'/('RECEIVED_'+Path(name).name)).write_bytes(z.read(name))
        owner=dict(path=str(owner_path),sha256=sha(owner_path),nested_return_sha256=nested_sha,nested_CRC='PASS',
                   nested_receipt_payloads_verified=len(receipt['output_files']),selection_count=21,conditional_selected=14,vacant=7,admitted=0,
                   source_records=len(dispositions['records']),identity_groups_reported=dispositions['unique_question_identity_count_after_exact_alias_merge'],
                   identity_groups_recomputed=len(identities),alias_pair=[dict(id=x['id'],canonical_counting_id=x['canonical_counting_id']) for x in alias_pair],
                   independent_review='NOT_ESTABLISHED',Owner_approval='NOT_GRANTED')
    save('RECEIVED_CORE2_READBACK.json',dict(audit=audit,owner_package=owner,academic_verdicts='NOT_REPERFORMED'))
    # Verify exact frozen skill package identity without re-running unchanged implementation tests.
    handoff=json.loads((WORK/'chatgpt/output/WPE_CONSTRUCTION_HANDOFF_R1_DELIVERY_RECEIPT.json').read_text())
    assert sha(Path(handoff['archive']['archive']))==handoff['archive']['sha256']
    save('SOURCE_RECEIPT.json',dict(schema='source-core1a-report-evidence/v1',captured_utc=datetime.now(timezone.utc).isoformat(),
        retained_sources=receipts,inventory_rows=len(rows),golden_tree_files=152,registered_candidates=2,
        owner_blessed_among_registered=0,Reference_files=115,anti_examples=15,calibration_entries=7,
        negative_calibration_files=len(checks),negative_hash_counts={s:sum(x['status']==s for x in checks) for s in ['MATCH','MISSING','DIFFERS']},
        stress_files=sum(x['scope']=='STRESS_CONTROL' for x in rows),render_asset_files=sum(x['scope']=='RENDER_ASSET' for x in rows),
        frozen_handoff_archive_sha256=handoff['archive']['sha256'],semantic_qualification='NOT_RUN',source_instructions='TREATED_AS_EVIDENCE_NOT_AUTHORITY'))
    svg()
    (OUT/'index.html').write_text(html_page('WPE Source to Core1A concept report',markdown_html((OUT/'CONCEPT_REPORT.md').read_text(encoding='utf-8'))),encoding='utf-8')
    (OUT/'golden-fixtures.html').write_text(html_page('Complete scoped golden fixture catalogue',markdown_html('\n'.join(cat))),encoding='utf-8')
    print(json.dumps(dict(report=str(OUT/'index.html'),golden_files=152,inventory_rows=len(rows),registered_candidates=2,latest_Core2='14 conditional / 7 vacant / 0 admitted',audit_manifest='10/10 PASS')))


if __name__ == '__main__':main()
