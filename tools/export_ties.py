import ezdxf,json,hashlib,numpy as np,mapbox_earcut as earcut
from ezdxf.path import make_path
from shapely.geometry import Polygon
from shapely.ops import unary_union
from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'source-cad/official/SKYLARK150/Other/Ties/TIES.dxf';raw=p.read_bytes();sha=hashlib.sha1(('blob %d\0'%len(raw)).encode()+raw).hexdigest();assert sha=='44e40004134b1210d289cd8bd382b4ff04d5ed0e'
d=ezdxf.readfile(p);m=d.modelspace()
def poly(e):return Polygon([(v.x,v.y) for v in make_path(e).flattening(.01)]).buffer(0)
pockets=[poly(e) for e in m if e.dxf.layer.startswith('5_')]
for name,handle in [('TIE-FULL','4B1'),('TIE-HALF','142F')]:
 e=d.entitydb[handle];outer=poly(e);cuts=[v.intersection(outer) for v in pockets if v.intersects(outer)];upper=outer.difference(unary_union(cuts));x0,y0,x1,y1=outer.bounds;cx=(x0+x1)/2;cy=(y0+y1)/2
 verts=[];faces=[]
 def extrude(p,z0,z1):
  for polygon in ([p] if p.geom_type=='Polygon' else p.geoms):
   rings=[list(polygon.exterior.coords)[:-1]]+[list(r.coords)[:-1] for r in polygon.interiors];v=np.array([v for ring in rings for v in ring],dtype=np.float64);ends=np.cumsum([len(r) for r in rings]).astype(np.uint32);indices=earcut.triangulate_float64(v,ends).reshape(-1,3);base=len(verts);n=len(v)
   verts.extend([[round(x-cx,5),round(y-cy,5),z] for z in [z0,z1] for x,y in v])
   faces.extend([[base+int(i) for i in f[::-1]] for f in indices]);faces.extend([[base+n+int(i) for i in f]for f in indices]);start=0
   for ring in rings:
    for j in range(len(ring)):
     a=base+start+j;b=base+start+(j+1)%len(ring);faces.extend([[a,b,b+n],[a,b+n,a+n]])
    start+=len(ring)
 extrude(outer,0,9);extrude(upper,9,18)
 packet=dict(schema='obtp-source-mesh/1',units='mm',id=name,producer='OBTP extrusion of official CNC profile and 9 mm pockets',source=dict(repository='wikihouseproject/Skylark',commit='6581cc1de0f4daef81a6b5c5a2eaed3c537d1d8f',path='SKYLARK150/Other/Ties/TIES.dxf',git_blob_sha=sha,license='CC-BY-SA-4.0',handle=handle,units_note='DXF unit flag unset; millimetres inferred from 2440 × 1220 × 18 sheet layer and source terms',changes='Bulge arcs tessellated at 0.01 mm; profile extruded to source 18 mm stock with source 9 mm pockets; display derivative, not CNC output'),bounds=[[x0-cx,y0-cy,0],[x1-cx,y1-cy,18]],assets=[dict(id='DXF-'+handle,label=name,vertices=verts,faces=faces,bounds=[[x0-cx,y0-cy,0],[x1-cx,y1-cy,18]],explode=[0,0,0])])
 (root/'dist/catalogue'/f'{name}.json').write_text(json.dumps(packet,separators=(',',':')))
 print(name,'pockets',len(cuts),'area',outer.area,'upperarea',upper.area,'bounds',packet['bounds'])
 (root/'source-cad'/f'{name}-polygons.json').write_text(json.dumps(dict(outer=list(outer.exterior.coords),upper=[list(p.exterior.coords) for p in ([upper] if upper.geom_type=='Polygon'else upper.geoms)],center=[cx,cy])))
