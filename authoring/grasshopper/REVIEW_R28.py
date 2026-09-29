"""Regenerate local review for the third GH workflow. Never publishes a website."""
import json,html,sys
from pathlib import Path
from obtp import room_config as r,room_structure as s,room_detail as d
from obtp.drawings import svg
from obtp.documentation import axon
from obtp.export import file3dm
CASES=[('sauna',0,[7,0,2],8,[],dict(terrace=4,outdoor_shower=True,outdoor_bench=True)),('studio-passage',1,[10,1,12],10,[],dict(terrace=2)),('living-studio',2,[16,6,13],9,['R01 R03 open'],dict(terrace=3))]
def main(folder):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);cards=[];stats=[]
 for name,t,functions,n,boundaries,features in CASES:
  p=r.solve(r.rules(r.rules(r.programme(t,functions)),boundaries,'boundary'),length_cells=n,summer_passage=t==1)
  sk=s.skeleton(p);scene=d.build(sk,**features)
  for view,value in [('plan',r.plan_view(p)),('skeleton',axon(sk['parts'])),('detail',axon(scene['parts']))]:(folder/(name+'-'+view+'.svg')).write_text(svg(value))
  q=scene['manufacturing'];stats.append(dict(case=name,order=[x['id']+' '+x['label'] for x in p['rooms']],dimensions_mm=p['bounds_mm'][2:],skeleton_pieces=len(sk['parts']),primary_pieces=q['physical_pieces'],primary_types=q['unique_manufactured_part_candidates'],cladding_pieces=q['cladding']['physical_pieces'],complete_pieces=len(scene['parts']),geometry_sha256=scene['geometry_sha256']))
  cards.append('<article><h2>'+name+'</h2><p>'+html.escape(' → '.join(stats[-1]['order']))+'</p><div>'+''.join('<figure><img src="'+name+'-'+v+'.svg"><figcaption>'+v+'</figcaption></figure>' for v in ['plan','skeleton','detail'])+'</div></article>')
  if t==0:file3dm([scene],folder/'room-config-sauna.3dm')
 (folder/'summary.json').write_text(json.dumps(stats,indent=2))
 (folder/'review.html').write_text('''<!doctype html><meta charset="utf-8"><title>R28 room configurator review</title><style>body{font:16px system-ui;background:#f6f4ee;color:#252825;max-width:1400px;margin:32px auto}article{border-top:1px solid #aaa;padding:20px 0}article>div{display:flex;flex-wrap:wrap}figure{margin:8px;flex:1;min-width:300px}img{width:100%;height:330px;object-fit:contain}figcaption{text-transform:uppercase;font-size:12px}</style><h1>R28 · Third GH definition</h1><p>Repeated room-function lists → neighbour rules → boundary treatments → overall 900 × 1200 mm grid → cassette skeleton → detailing.</p><p>Single row, up to six rooms. These are new configurations, not modifications of a stored Sauna/Studio building. Existing main and research creators remain unchanged. Structural sizing, products, equipment, windows, wet-area layers and SLD eligibility remain unresolved.</p><p>The summer passage has two schematic double-leaf door openings at opposing long sides. Outdoor shower/bench options reserve terrace space; they are not yet the old integrated service niche. U terrace has both long sides and one short side including the entrance edge.</p>'''+''.join(cards))
 print(json.dumps(stats,indent=2))
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'review-r28')
