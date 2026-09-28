"""Portable visual/document acceptance samples. Never publishes a website."""
from pathlib import Path
import json,sys,html
from obtp.room_presets import generate
from obtp.room_structure import skeleton
from obtp.room_detail import build
from obtp.room_documents import export
from obtp.room_config import plan_view
from obtp.drawings import svg
from obtp.documentation import axon
from obtp.export import file3dm

def main(folder):
 root=Path(__file__).resolve().parent;folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);cards=[];rows=[]
 for name,t,e in [('Sauna_M_extension',0,True),('Studio_M_no_extension',1,False),('Studio_M_extension',1,True),('Living_M_study',2,True)]:
  plan=generate(t,1,e);frame=skeleton(plan);scene=build(frame,paneling=2)
  receipt=export(scene,folder,root/'material-rates.json');target=Path(receipt['folder'])
  for key,view in [('plan',plan_view(plan)),('structure',axon(frame['parts'])),('building',axon(scene['parts']))]:(folder/(name+'-'+key+'.svg')).write_text(svg(view))
  model_path=target/(name+'.3dm');file3dm([scene],model_path)
  import rhino3dm
  check=rhino3dm.File3dm.Read(str(model_path))
  if check is None or len(check.Objects)!=len(scene['parts']):raise IOError('3DM reopen failed: '+str(model_path))
  cards.append('<article><h2>'+name.replace('_',' ')+'</h2><div>'+''.join('<figure><img src="'+name+'-'+k+'.svg"><figcaption>'+k+'</figcaption></figure>' for k in ('plan','structure','building'))+'</div><p>'+''.join('<a href="'+target.name+'/'+d+'.pdf">'+d+'</a> · ' for d in receipt['documents'])+'</p></article>')
  rows.append(dict(name=name,dimensions=plan['bounds_mm'][2:],parts=len(scene['parts']),hash=scene['geometry_sha256'],folder=target.name))
 (folder/'summary.json').write_text(json.dumps(rows,indent=2))
 (folder/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>OBTP R30 review</title><style>body{font:16px system-ui;max-width:1500px;margin:30px auto;background:#f5f3ee;color:#252825}article{border-top:1px solid #aaa;padding:20px}article>div{display:flex}figure{flex:1;margin:8px;min-width:0}img{width:100%;height:320px}a{color:#345747}</style><h1>R30 · Preset plans and independent cassette stages</h1><p>Portable model and PDF proofs; native Rhino execution remains outstanding. Studio without extension retains its central room with two windows and a west-end entrance. Living Studio is a provisional study.</p>'+''.join(cards))
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'review-r30')
