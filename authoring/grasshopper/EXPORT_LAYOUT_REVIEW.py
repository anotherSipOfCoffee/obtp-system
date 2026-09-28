"""Regenerate bounded layout plans and an offline visual review. No website writes."""
import html,json,sys
from pathlib import Path
from obtp import layout
COLORS={'sauna':'#cb9975','entrance':'#89a9bc','outdoor':'#a3b889'}

def svg(p,title):
 width,height=p['bounds_mm'][2:];scale=min(950/width,330/height);ox=50;oy=95
 def point(x,y):return ox+x*scale,oy+(height-y)*scale
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="660" viewBox="0 0 1050 660"><rect width="1050" height="660" fill="#f6f4ee"/>',
  '<g font-family="Arial" fill="#242823"><text x="35" y="35" font-size="24">'+html.escape(title)+'</text><text x="35" y="62" font-size="16">'+('CANONICAL CONSTRUCTION ADAPTER AVAILABLE' if p['construction_compatible'] else 'PLAN STUDY — CONSTRUCTION OUTPUT BLOCKED')+'</text>']
 for r in p['rooms']:
  x,y,w,h=r['bounds_mm'];xx,yy=point(x,y+h)
  parts.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="#343c32" stroke-width="2"/>'%(xx,yy,w*scale,h*scale,COLORS[r['id']]))
  cx,cy=point(x+w/2,y+h/2);parts.append('<text x="%g" y="%g" text-anchor="middle" font-size="17">%s</text><text x="%g" y="%g" text-anchor="middle" font-size="13">%d × %d mm</text>'%(cx,cy,r['id'].upper(),cx,cy+23,w,h))
 for r in p['finished_room_rectangles']:
  x,y,w,h=r['bounds_mm'];xx,yy=point(x,y+h);parts.append('<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="#343c32" stroke-dasharray="5 4"/>'%(xx,yy,w*scale,h*scale))
 for o in p['openings']:
  x,y=o['origin_mm'];w=o['width_mm'];a=point(x,y);b=point(x+(w if o['axis']=='x' else 0),y+(w if o['axis']=='y' else 0));parts.append('<path d="M%g,%g L%g,%g" stroke="#c34332" stroke-width="6"/>'%(*a,*b))
 parts.append('<text x="50" y="455" font-size="14">Solid: coordination zones · dashed: finished-room rectangles / provisional deductions · red: opening</text>')
 centres={r:(150+i*340,540) for i,r in enumerate(layout.ROOM_IDS) if p['programme']['active'][r]}
 for e in p['graph']['edges']:
  (x,y),(u,v)=centres[e['a']],centres[e['b']];parts.append('<path d="M%g,%g L%g,%g" stroke="#465144" stroke-width="2"/><text x="%g" y="%g" text-anchor="middle" font-size="12">%s</text>'%(x,y,u,v,(x+u)/2,y-25,html.escape(e['kind'])))
 for r,(x,y) in centres.items():parts.append('<circle cx="%g" cy="%g" r="38" fill="%s" stroke="#343c32"/><text x="%g" y="%g" text-anchor="middle" font-size="14">%s</text>'%(x,y,COLORS[r],x,y+65,r))
 parts.append('<text x="35" y="645" font-size="13">900 × 1200 mm coordination · room graph ≠ approved circulation or structural design</text></g></svg>');return ''.join(parts)

def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 cases=[('01_existing_sauna',layout.programme(),0),('02_two_rooms',layout.programme(outdoor=False),0),('03_sauna_outdoor',layout.programme(entrance=False),0),('04_alternative_order',layout.programme(),1)]
 cards=[]
 for name,programme,index in cases:
  p=layout.solve(layout.relationships(programme),index);(out/(name+'.json')).write_text(json.dumps(p,indent=2));(out/(name+'.svg')).write_text(svg(p,name.replace('_',' ')))
  cards.append('<article><img src="'+name+'.svg"><details><summary>Scope and constraints</summary><pre>'+html.escape('\n'.join(p['holds']))+'</pre></details></article>')
 (out/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>OBTP R23 constrained floor plans</title><style>body{font:16px system-ui;max-width:1200px;margin:30px auto;padding:20px;background:#f6f4ee}img{width:100%}article{border:1px solid #bbb;margin-bottom:24px}pre{white-space:pre-wrap;padding:15px}</style><h1>R23 · room graph to floor plan</h1><p>Activation controls the programme. Edges control relationships. Arrangement selects a feasible strip order. The existing two-room Sauna, with optional outdoor zone, remains the verified geometry bridge.</p>'+''.join(cards))
 print('Four plan reviews:',out)
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'review-r23')
