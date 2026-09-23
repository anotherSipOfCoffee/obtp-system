import json,numpy as np
from pathlib import Path
from shapely import make_valid
from shapely.geometry import LineString
from shapely.ops import unary_union,polygonize
BASE=Path(__file__).resolve().parents[1]/'dist/catalogue'
NEW=BASE
def model(id):return json.loads(((NEW if (NEW/(id+'.json')).exists() else BASE)/(id+'.json')).read_text())
def section(id,axis,pos,rotation=np.eye(3),off=(0,0,0)):
 out=[];coords=[i for i in range(3) if i!=axis]
 for a in model(id)['assets']:
  verts=np.array(a['vertices'])@np.array(rotation).T+off
  if pos<=verts[:,axis].min() or pos>=verts[:,axis].max():continue
  tri=verts[np.array(a['faces'])];below=tri[:,:,axis]<pos;tri=tri[np.any(below,axis=1)&~np.all(below,axis=1)];segments=[]
  for ps in tri:
   hits=[]
   for u,v in zip(ps,np.roll(ps,-1,axis=0)):
    if(u[axis]<pos)!=(v[axis]<pos):
     p=u+(pos-u[axis])/(v[axis]-u[axis])*(v-u);hits.append(tuple(round(p[k],4) for k in coords))
   if len(hits)==2 and hits[0]!=hits[1]:segments.append(LineString(hits))
  polys=list(polygonize(unary_union(segments)))
  # Odd/even crossings retain voids and disconnected sections.
  for p in polys:
   q=p.representative_point();n=0
   for s in segments:
    (x1,y1),(x2,y2)=s.coords
    if (y1>q.y)!=(y2>q.y) and q.x<x1+(q.y-y1)*(x2-x1)/(y2-y1):n+=1
   if n%2:out.append(p)
 return make_valid(unary_union(out))
