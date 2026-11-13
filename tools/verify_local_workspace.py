"""Read-only migration verification; byte identity is not academic approval."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import argparse,hashlib,json,re,collections,sys

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 return h.hexdigest()
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.add(d['id'])
  if tag=='a' and 'href' in d:self.links.append(d['href'])
  if tag in ('img','script','iframe') and 'src' in d:self.links.append(d['src'])
def valid_relative(root,path):
 target=root/path
 if target.is_absolute() and not target.resolve().is_relative_to(root.resolve()):return None
 return target
def graph_valid(stages):
 by={x['id']:x for x in stages}
 if len(by)!=len(stages):return False
 done=set();grey=set()
 def visit(n):
  if n not in by or n in grey:return False
  if n in done:return True
  grey.add(n)
  if not all(visit(d) for d in by[n]['depends_on']):return False
  grey.remove(n);done.add(n);return True
 return all(visit(n) for n in by)
def verify(root,full_sources=True):
 root=root.resolve();m=root/'workspace/migration';checks=[];failures=[]
 def check(name,value,detail=None):
  row={'name':name,'pass':bool(value)}
  if detail is not None:row['detail']=detail
  checks.append(row)
  if not value:failures.append(row)
 def load(n):return json.loads((m/n).read_text(encoding='utf-8-sig'))
 manifest=load('COPY_MANIFEST.json');rows=manifest['files'];bad=[]
 for i,r in enumerate(rows,1):
  p=root/r['destination'];q=Path(r['source'])
  if not p.is_file() or p.stat().st_size!=r['bytes'] or digest(p)!=r['sha256']:bad.append({'destination':r['destination'],'kind':'DESTINATION_MISSING_OR_CHANGED'})
  if full_sources and (not q.is_file() or q.stat().st_size!=r['bytes'] or digest(q)!=r['sha256']):bad.append({'source':str(q),'kind':'SOURCE_CHANGED_SINCE_COPY'})
  if i%4000==0:print('COPY_READBACK',i,flush=True)
 check('all copied destination bytes match',not any(x['kind'].startswith('DESTINATION') for x in bad),len(rows))
 if full_sources:
  check('all source bytes still match',not any(x['kind'].startswith('SOURCE') for x in bad),'checked')
 else:
  checks.append({'name':'source-byte readback','status':'NOT_RUN','pass':None,'detail':'Omitted in this entrypoint-only repeat; retain the earlier full readback separately'})
 check('copy destinations unique',len({r['destination'].casefold() for r in rows})==len(rows))
 extraction=load('SMART_R2_EXTRACTION.json')
 check('all extracted Smart R2 members match',all((root/x['destination']).is_file() and digest(root/x['destination'])==x['sha256'] for x in extraction['members']),len(extraction['members']))
 register=load('REGISTER_RECONCILIATION.json')
 check('all154 registered inputs accounted',len(register)==154 and not any(x['copy']=='NOT_COPIED_OR_MISSING' for x in register))
 check('all historical registered pins retained',not any(x.get('historical_pin_match') is False for x in register))
 pins=load('UPSTREAM_PIN_RECONCILIATION.json')
 check('all public P03 upstream pins have actual local matches',all(x['matches'] for x in pins),len(pins))
 wf=load('WORKFLOW.json');check('workflow dependencies acyclic and complete',graph_valid(wf['stages']))
 paths=load('PATH_MAP.json')['paths'];missing=[(k,p) for k,p in paths.items() if not (root/p).exists()]
 check('all24 current process paths exist',not missing,missing)
 check('workflow artifacts resolve',all(x in paths for s in wf['stages'] for x in s['artifacts']))
 check('publication authority stays HOLD',wf['remote_publication']=='NOT_AUTHORIZED' and next(s for s in wf['stages'] if s['id']=='publish')['state'].startswith('HOLD'))
 check('private workspace excluded by local Git rule','/workspace/' in (root/'.git/info/exclude').read_text())
 baseline=load('V4_BRANCH_BASELINE.json');unintended=[]
 for r in baseline['files']:
  if r['path']=='AGENTS.md':continue
  p=root/r['path']
  if not p.is_file() or digest(p)!=r['sha256']:unintended.append(r['path'])
 check('received tracked branch bytes unchanged except documented AGENTS pointer',not unintended,unintended)
 check('original AGENTS body preserved',(m/'AGENTS_BEFORE_ENTRYPOINT.md').read_bytes() in (root/'AGENTS.md').read_bytes())
 docs=[root/'index.html',root/'workspace/publish/html/index.html',root/paths['legacy_workflow_hub']]
 docs += [root/'Start_here.md',root/'CURRENT_CHECKPOINT.md',*sorted((root/'docs/agent-entry').glob('*.md'))]
 link_rows=[]
 for p in docs:
  text=p.read_text(encoding='utf-8-sig')
  if p.suffix=='.html':q=Links();q.feed(text);urls=q.links
  else:urls=re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',text)
  for u in urls:
   v=urlsplit(u)
   if v.scheme or u.startswith('mailto:'):continue
   f=p.parent/unquote(v.path) if v.path else p
   ok=f.exists() and f.resolve().is_relative_to(root)
   if ok and v.fragment and f.suffix=='.html':t=Links();t.feed(f.read_text(encoding='utf-8-sig'));ok=unquote(v.fragment) in t.ids
   link_rows.append({'page':p.relative_to(root).as_posix(),'href':u,'pass':ok})
 check('new entry links plus relocated WPE hub links resolve insideV4',all(x['pass'] for x in link_rows),len(link_rows))
 # Falsifiers never change a received source or an expected scientific result.
 sample=rows[0];p=root/sample['destination'];check('changed-byte negative control rejected',hashlib.sha256(p.read_bytes()+b'!').hexdigest()!=sample['sha256'])
 check('missing-path negative control rejected',not (root/'workspace/__deliberately_missing_migration_control__').exists())
 altered=[dict(s,depends_on=list(s['depends_on'])) for s in wf['stages']];altered[0]['depends_on']=[altered[0]['id']]
 check('cyclic workflow negative control rejected',not graph_valid(altered))
 return {'scope':'AUTHOR_MIGRATION_MECHANICAL_CHECKS; not independent semantic/runtime/academic approval','mechanical_status':'PASS' if not failures else 'FAIL','checks':checks,'passed':sum(x.get('pass') is True for x in checks),'not_run':sum(x.get('pass') is None for x in checks),'failed':len(failures),'copied_files':len(rows),'copied_bytes':manifest['bytes'],'full_source_readback':full_sources,'copy_failures':bad,'link_count':len(link_rows),'links':link_rows,'academic_status':'HOLD','remote_publication':'NOT_AUTHORIZED','legacy_absolute_build_paths':'PRESERVED_NOT_GENERAL_RUNTIME_RELOCATION','v4_runtime_tests':'See separately captured pytest log; Windows symlink privilege failures remain recorded'}

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--out',type=Path);ap.add_argument('--skip-source-readback',action='store_true');args=ap.parse_args()
 r=verify(args.root,not args.skip_source_readback)
 if args.out:args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k not in ('checks','links')},indent=2))
 sys.exit(0 if r['mechanical_status']=='PASS' else 1)
