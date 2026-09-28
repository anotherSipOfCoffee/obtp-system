"""Portable R27 acceptance evidence and local visual guide; no deployment."""
import csv,html,json,time,sys
from pathlib import Path
from obtp import sauna_workflow as flow,plan_pipeline as pipe
from obtp.drawings import svg
from obtp.documentation import axon
from obtp.manufacturing import analyse
from obtp.export import file3dm

def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);rows=[];cards=[]
 baseline=json.loads((Path(__file__).parent/'tests/r26_baseline.json').read_text())
 for old in baseline:
  s=flow.construct(flow.resolve(flow.select(old['preset'],roof_type=old['roof'])));q=analyse(s,True)
  rows.append(dict(preset=flow.PRESETS[old['preset']],roof=old['roof'],before_pieces=old['primary'],after_pieces=q['physical_pieces'],before_types=old['types'],after_types=q['unique_manufactured_part_candidates'],before_cladding=old['cladding'],after_cladding=q['cladding']['physical_pieces'],geometry_unchanged=s['geometry_sha256']==old['geometry']))
 with (out/'before-after.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
 cases=[('Sauna M storage',3,{}),('Studio M storage',10,{}),('Custom Sauna',6,dict(base_preset=3,use_overrides=True,sauna_cells_delta=1,entrance_cells_delta=-1,outdoor=True)),('Custom Studio',13,dict(base_preset=3,use_overrides=True,work_cells_delta=1))]
 timings=[]
 for name,index,kw in cases:
  d=flow.resolve(flow.select(index,**kw));t=time.perf_counter();s=flow.construct(d);elapsed=time.perf_counter()-t
  slug=name.lower().replace(' ','-');timings.append(dict(case=name,construction_seconds=round(elapsed,3),pieces=len(s['parts'])))
  for suffix,view in [('plan',s['drawings']['views']['concept-plan']),('model',axon(s['parts']))]:
   (out/(slug+'-'+suffix+'.svg')).write_text(svg(view))
  cards.append('<article><h2>'+html.escape(name)+'</h2><p>'+str(len(s['parts']))+' complete model pieces; '+str(s['dimensions']['width_mm'])+' mm width.</p><div><img src="'+slug+'-plan.svg"><img src="'+slug+'-model.svg"></div></article>')
 # A portable 3DM is a model review asset, not a native GH acceptance result.
 file3dm([flow.construct(flow.resolve(flow.select(10)))],out/'studio-m-storage.3dm')
 (out/'timings.json').write_text(json.dumps(timings,indent=2))
 (out/'review.html').write_text('''<!doctype html><meta charset="utf-8"><title>OBTP R27 acceptance</title><style>body{font:16px system-ui;max-width:1200px;margin:32px auto;background:#f5f3ed;color:#252825}article{border-top:1px solid #aaa;padding:20px 0}article div{display:flex;flex-wrap:wrap}img{width:48%;min-width:280px;height:340px;object-fit:contain}table{border-collapse:collapse}td,th{border:1px solid #bbb;padding:7px}</style><h1>R27 · Room controls to cassette construction</h1><p>Preset → room plan → structural arrangement → parallel floor, roof and wall branches → finishes, terrace, weather roof, foundation and insulation → quantities → assembly → preview.</p><p>Room controls only. Custom lengths vary by at most one existing 900 mm cell from the selected preset; width stays 2400 mm. Minimum room lengths and opening fit may narrow the allowed range. No arbitrary drawn plans or certified structural sizing.</p><p>24 saved preset/roof cases retain R26 geometry and quantities. See before-after.csv. No part reduction is claimed. Preview filters do not change exports.</p>'''+''.join(cards)+'<p>Native Rhino/Grasshopper canvas execution remains unverified. These diagrams use canonical geometry; a drawing group is not a certified lifting unit.</p>')
 print(json.dumps(dict(saved_cases=len(rows),all_geometry_preserved=all(x['geometry_unchanged'] for x in rows),timings=timings),indent=2))
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'review-r27')
