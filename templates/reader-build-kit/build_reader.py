from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
RUNTIME=ROOT/'runtime'
sys.path.insert(0,str(RUNTIME))
from Shared.tools import render_core
# The preserved native snapshot intentionally lacks public/. Use the exact
# retained tablet CSS resource without changing any native renderer bytes.
render_core.TABLET_CSS=ROOT/'css/tablet-12-7.css'
result=render_core.main(sys.argv[1:])
if result==0 and '--out' in sys.argv:
    import shutil
    output=Path(sys.argv[sys.argv.index('--out')+1])
    for folder in ('css','js'):
        shutil.copytree(ROOT/folder,output/folder,dirs_exist_ok=True)
    for page in output.glob('*.html'):
        html=page.read_text(encoding='utf-8')
        html=html.replace('"../css/','"css/').replace('"../js/','"js/')
        page.write_text(html,encoding='utf-8')
raise SystemExit(result)
