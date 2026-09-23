"""Sample mesh cross-sections against the source tie profile. Not a volume/strength test."""
import json,numpy as np
from pathlib import Path
from shapely.geometry import LineString,Polygon
from shapely.ops import unary_union,polygonize
root=Path(__file__).resolve().parents[1];models={p.stem:json.loads(p.read_text())for p in (root/'dist/catalogue').glob('*.json')if p.name!='manifest.json'}
I=np.eye(3);defs={'floor':('F-S',I,[600,-732,380]),'front':('W-S',I,[300,-50,380]),'back':('W-S',np.diag([-1,-1,1]),[300,4622,380]),'roof':('R-S',np.array([[0,1,0],[-1,0,0],[0,0,1]]),[1593.397095,-1232,2703.43837])}
cache={}
def section(key,pos):
 if (key,pos)in cache:return cache[key,pos]
 id,mat,off=defs[key];out=[]
 for a in models[id]['assets']:
  verts=np.array(a['vertices'])@mat.T+off;tri=verts[np.array(a['faces'])];below=tri[:,:,1]<pos;tri=tri[np.any(below,axis=1)&~np.all(below,axis=1)];segments=[]
  for ps in tri:
   hits=[]
   for u,v in zip(ps,np.roll(ps,-1,axis=0)):
    if(u[1]<pos)!=(v[1]<pos):
     t=(pos-u[1])/(v[1]-u[1]);p=u+t*(v-u);hits.append((round(p[0],4),round(p[2],4)))
   if len(hits)==2 and hits[0]!=hits[1]:segments.append(LineString(hits))
  polys=list(polygonize(unary_union(segments)))
  if polys:out.append(max(polys,key=lambda p:p.area))
 result=unary_union(out);cache[key,pos]=result;return result
t=json.loads((root/'source-cad/TIE-FULL-polygons.json').read_text());cx,cy=t['center'];report=[]
for pair,level in [(('floor','front'),380),(('front','roof'),2480),(('floor','back'),380),(('back','roof'),2480)]:
 planes=[(0,1),(186,-1)]if 'front'in pair else [(4572,-1),(4386,1)]
 for plane,direction in planes:
  for depth in [4.5,13.5]:
   y=plane+direction*depth;material=unary_union([section(key,y)for key in pair]);rings=[t['outer']]if depth<9 else t['upper']
   for x in [105.1,300,494.9]:
    tie=unary_union([Polygon([(px-cx+x,py-cy+level)for px,py in ring])for ring in rings]);area=material.intersection(tie).area
    report.append(dict(pair=pair,y=y,x=x,z=level,overlap_mm2=area,material_section_area_mm2=material.area))
(root/'docs/BLOCK_INTERFACE_FIT_CHECK.json').write_text(json.dumps(report,indent=2));print('samples',len(report),'worst overlap',max(r['overlap_mm2'] for r in report));print([r for r in report if r['overlap_mm2']>2])
