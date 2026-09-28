"""Portable visual review of the authoritative R24 sequence, without site writes."""
import html,json,sys
from pathlib import Path
from obtp import sauna_workflow as flow
from EXPORT_LAYOUT_REVIEW import svg

def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);cards=[];summary=[]
 for i,label in enumerate(flow.PRESETS):
  document=flow.resolve(flow.select(i));scene=flow.construct(document)
  name='%02d_'%(i+1)+label.lower().replace(' / ','_').replace(' ','_')
  (out/(name+'.json')).write_text(json.dumps(document,indent=2));(out/(name+'.svg')).write_text(svg(document['plan'],label))
  summary.append(dict(preset=i,label=label,plan_sha256=document['plan']['plan_sha256'],geometry_sha256=scene['geometry_sha256'],pieces=len(scene['parts']),dimensions=scene['dimensions']))
  cards.append('<article><h2>'+html.escape(label)+'</h2><img src="'+name+'.svg"><p>Preset → layout → cassette → 3D. '+str(len(scene['parts']))+' modelled pieces including separately scheduled cladding.</p></article>')
 (out/'summary.json').write_text(json.dumps(summary,indent=2))
 (out/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>R24 Sauna workflow</title><style>body{font:16px system-ui;max-width:1100px;margin:30px auto;background:#f6f4ee;padding:20px}article{border:1px solid #bbb;margin:24px 0;padding:15px}img{width:100%}</style><h1>R24 · Sauna preset → layout → cassette → 3D</h1><p>Six saved presets and Custom. Saved presets ignore custom room controls. These are room-planning diagrams; detailed architectural drawings come from the resulting cassette scene. Original outdoor shower fixtures on saved no-storage models are retained outside the room zones.</p>'+''.join(cards))
 print('Seven Sauna workflow reviews:',out)
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'review-r24')
