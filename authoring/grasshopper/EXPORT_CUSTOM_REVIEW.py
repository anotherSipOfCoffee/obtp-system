"""Regenerate R25 local review from canonical scenes. Never deploys a website."""
import html,json,sys
from pathlib import Path
from obtp import sauna_workflow as flow
from obtp.drawings import svg
from obtp.documentation import axon
from obtp.export import file3dm
CASES=[('sauna_only',dict(entrance=False,outdoor=False)),('sauna_outdoor',dict(entrance=False)),('reversed',dict(arrangement=1)),('separate_entries',dict(sauna_entrance=0))]
def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);cards=[];summary=[]
 for name,settings in CASES:
  doc=flow.resolve(flow.select(6,**settings));scene=flow.construct(doc)
  (out/(name+'-plan.svg')).write_text(svg(scene['drawings']['views']['concept-plan']))
  (out/(name+'-model.svg')).write_text(svg(axon(scene['parts'])))
  core=[p for p in scene['parts'] if p['material'] in ('timber','plywood') and p['family'] in ('floor','walls','partitions')]
  (out/(name+'-structure.svg')).write_text(svg(axon(core)))
  file3dm([scene],out/(name+'.3dm'))
  summary.append(dict(name=name,settings=settings,rooms=[r['id'] for r in doc['plan']['rooms']],pieces=len(scene['parts']),geometry_sha256=scene['geometry_sha256'],plan_sha256=doc['plan']['plan_sha256']))
  cards.append('<article><h2>'+html.escape(name.replace('_',' '))+'</h2><p>Room order: '+html.escape(' → '.join(summary[-1]['rooms']))+'</p><div>'+''.join('<figure><img src="'+name+'-'+v+'.svg"><figcaption>'+label+'</figcaption></figure>' for v,label in [('plan','Derived floor plan'),('structure','Structure cutaway: roof and finishes omitted for this view only'),('model','Complete model')])+'</div></article>')
 (out/'summary.json').write_text(json.dumps(summary,indent=2))
 (out/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>R25 Custom cassette review</title><style>body{font:16px system-ui;margin:30px;background:#f6f4ee}article{padding:20px;border:1px solid #aaa;margin:20px 0}article>div{display:flex;flex-wrap:wrap}figure{margin:10px;flex:1;min-width:280px}img{width:100%;height:320px;object-fit:contain}figcaption{font-size:13px}</style><h1>R25 · Custom layout → cassette → 3D</h1><p>Canonical model geometry. Rectangular strip layouts only. Engineering, supplier acceptance and lifting remain unresolved. Separate .3dm files contain the complete models.</p>'+''.join(cards))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'review-r25')
