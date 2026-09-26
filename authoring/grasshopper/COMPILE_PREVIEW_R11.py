"""Local review catalogue. PDF links only expose actually generated proofs."""
import sys,json,hashlib,itertools,shutil
from pathlib import Path
from obtp.model import build,parameters,VERSION
from obtp.export import browser_scene,COLORS
from obtp.cut_view import parts_below
from obtp.drawings import svg
from obtp.suppliers import catalogue
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True);entries=[]
for pr,i,r,w,b,su in itertools.product(range(2),range(6),range(3),(580,880,1180),range(2),(False,True)):
 if pr==0 and su:continue
 s=build(parameters(i,program_type=pr,roof_type=r,window_width=w,foundation_type=b,studio_winter_closed=not su))
 key=s['config']['id']+f'-r{r}-t2-w{w}-f0-b{b}'+('-summer' if su else '')
 web=browser_scene(s);cut=dict(s,parts=parts_below(s));clipped=browser_scene(cut);web['cut']=dict(models=clipped['models'],items=clipped['items'])
 for chunk in (web,web['cut']):
  for m in chunk['models']:
   for a in m['assets']:a['color']=[v/255 for v in COLORS.get(a['material'],COLORS['object'])[:3]]
 web.update({k:s[k] for k in ['config','dimensions','checks','drawings','envelope_spec','window_spec','seasonal_spec','object_library','supplier_spec','foundation_spec']})
 web.update(source_revision='R11-local-review',authoring_version=VERSION)
 data=json.dumps(web,separators=(',',':')).encode();(out/(key+'.json')).write_bytes(data)
 (out/(key+'-plan.svg')).write_text(svg(s['drawings']['views']['concept-plan']))
 entries.append(dict(key=key,file=key+'.json',sha256=hashlib.sha256(data).hexdigest(),geometry_sha256=s['geometry_sha256'],pdf=False))
 if len(entries)%30==0:print(len(entries),flush=True)
(out/'manifest.json').write_text(json.dumps(dict(version=VERSION,source_revision='R11-local-review',entries=entries),indent=2))
(out/'suppliers.json').write_text(json.dumps(catalogue()))
shutil.copytree(Path(__file__).parent/'suppliers/assets',out/'supplier-assets',dirs_exist_ok=True)
print('Complete',len(entries))
