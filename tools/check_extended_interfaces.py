import json, numpy as np
from pathlib import Path
from mesh_sections import section,model
from shapely.geometry import Polygon
from shapely.ops import unary_union
root=Path(__file__).resolve().parents[1]
t=json.loads((root/'source-cad/TIE-FULL-polygons.json').read_text());cx,cy=t['center']
def shape(depth,fn):
 rings=[t['outer']] if depth<9 else t['upper']
 return unary_union([Polygon([fn(px-cx,py-cy) for px,py in ring]).buffer(0) for ring in rings])
out=[]
# Source floor top skin.
for d in [4.5,13.5]:
 mat=unary_union([section('F-S',2,380-d,off=[600+600*i,-732,380]) for i in range(2)])
 for y in [583.453,988.547,1183.453,1588.547,1783.453,2188.547,2383.453,2788.547,2983.453,3388.547,3583.453,3988.547]:
  out.append(dict(kind='floor-floor',depth=d,translation=[600,y,380],overlap=mat.intersection(shape(d,lambda x,z:(z+600,x+y))).area))
# Source roof skins lie on a one-degree plane. Flatten only for the audit.
th=np.pi/180;c=np.cos(th);s=np.sin(th);rot=[[c,0,s],[0,1,0],[-s,0,c]]
m=model('R-S');v=np.vstack([a['vertices']for i,a in enumerate(m['assets'])if i in [0,1,2,3,11]]);f=v@np.array(rot).T
u=np.unique(f[(f[:,2]>225.45)&(v[:,1]>-1093.397)&(v[:,1]<-1033.397),0]);groups=np.split(u,np.where(np.diff(u)>20)[0]+1);centers=[float((g.min()+g.max())/2)for g in groups if 89<g.max()-g.min()<91]
for d in [4.5,13.5]:
 mat=unary_union([section('R-S',2,225.46-d,rot,[0,600*i,0]) for i in range(2)])
 for u in centers:
  raw=[c*u-s*225.46,-993.397095,s*u+c*225.46]
  out.append(dict(kind='roof-roof',depth=d,translation=[600,-raw[0]-1232,raw[2]+2703.43837],overlap=mat.intersection(shape(d,lambda x,y:(x+u,y-993.397095))).area))
print('floor/roof',max(a['overlap']for a in out),flush=True)
R=[[0,-1,0],[1,0,0],[0,0,1]];flip=[[-1,0,0],[0,-1,0]]
flip=[[-1,0,0],[0,-1,0],[0,0,1]]
for plane,sign in [(-186,1),(0,-1)]:
 for d in [4.5,13.5]:
  x=plane+sign*d;floor=section('E-S',0,x,flip,[-186,4572,0]);walls=unary_union([section('W-S',0,x,R,[50,486+600*j,380])for j in range(7)]);material=unary_union([floor,walls])
  for j in range(7):
   for y in [291.1+600*j,486+600*j,680.9+600*j]:
    out.append(dict(kind='end-floor-wall',depth=d,plane=plane,translation=[plane,y,380],overlap=material.intersection(shape(d,lambda a,b:(a+y,b+380))).area))
  corner=section('C-S-1',0,x,off=[432,-50,380]);wall=section('W-S',0,x,R,[50,486,380]);material=unary_union([corner,wall])
  for z in [195.547,404.453,795.547,1004.453,1395.547,1604.453]:
   out.append(dict(kind='corner-end-wall',depth=d,plane=plane,translation=[plane,186,z+380],overlap=material.intersection(shape(d,lambda a,b:(b+186,a+z+380))).area))
print('closure',[(kind,max(a['overlap']for a in out if a['kind']==kind))for kind in ['end-floor-wall','corner-end-wall']],flush=True)
(root/'docs/EXTENDED_INTERFACE_AUDIT.json').write_text(json.dumps({'method':'Mesh sections at two tie depths; 2D source polygon rings normalized with buffer(0) to remove numerical self-intersections. CAD/mesh unchanged; not full-volume or fabrication validation.','samples':out},indent=2))
