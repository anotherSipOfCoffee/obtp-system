"""Extract original cached display meshes, applying source instance transforms once."""
import json,hashlib,math,sys
from pathlib import Path
import rhino3dm as r
ROOT=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1])
lock=json.loads((ROOT/'docs/CATALOGUE_SOURCE_LOCK.json').read_text())
reports=[]
def coords(p):return [p.X,p.Y,p.Z]
def bounds(v):return [[fn(p[k] for p in v) for k in range(3)] for fn in (min,max)]
for rec in lock:
 if not rec['path'].endswith('.3dm'):continue
 p=next(source.rglob(Path(rec['path']).name))
 raw=p.read_bytes();sha=hashlib.sha1(('blob %d\0'%len(raw)).encode()+raw).hexdigest();assert sha==rec['sha'],p
 model=r.File3dm.Read(str(p));assert model.Settings.ModelUnitSystem==r.UnitSystem.Millimeters
 objs={str(o.Attributes.Id):o for o in model.Objects};defs={str(d.Id):d for d in model.InstanceDefinitions};assets=[];audit=[]
 def visit(o,xf,trail):
  g=o.Geometry
  if isinstance(g,r.InstanceReference):
   combined=r.Transform.Multiply(xf,g.Xform)
   for i in defs[str(g.ParentIdefId)].GetObjectIds():visit(objs[str(i)],combined,trail+[str(o.Attributes.Id)])
   return
  if not isinstance(g,(r.Brep,r.Extrusion,r.Mesh)):return
  original=g
  if isinstance(g,r.Extrusion):g=g.ToBrep(True)
  meshes=([original.GetMesh(r.MeshType.Render)] if isinstance(original,r.Extrusion) else [g] if isinstance(g,r.Mesh) else [f.GetMesh(r.MeshType.Render) for f in g.Faces])
  if any(m is None for m in meshes):raise ValueError('Missing cached meshes '+str(o.Attributes.Id))
  verts=[];faces=[];seen={}
  det=xf.M00*(xf.M11*xf.M22-xf.M12*xf.M21)-xf.M01*(xf.M10*xf.M22-xf.M12*xf.M20)+xf.M02*(xf.M10*xf.M21-xf.M11*xf.M20)
  for mesh in meshes:
   remap=[]
   for v in mesh.Vertices:
    pt=r.Point3d(v.X,v.Y,v.Z);pt.Transform(xf);q=tuple(round(n,6) for n in coords(pt))
    if q not in seen:seen[q]=len(verts);verts.append(q)
    remap.append(seen[q])
   for f in mesh.Faces:
    a,b,c,d=[remap[k] for k in f];ts=[[a,b,c]]+([[a,c,d]] if c!=d else [])
    faces.extend([t[::-1] if det<0 else t for t in ts])
  if not verts:return
  bb=bounds(verts);id=str(o.Attributes.Id);index=len(assets)
  assets.append(dict(id=id,instancePath=trail,label='P%02d'%(index+1),vertices=verts,faces=faces,bounds=bb,name=o.Attributes.Name or '',kind='source-part',material='plywood'))
  top=[]
  if isinstance(g,r.Brep):
   for v in g.Vertices:
    pt=v.Location;pt.Transform(xf);top.append(coords(pt))
  tb=bounds(top) if top else bb
  audit.append(dict(id=id,valid=g.IsValid,solid=g.IsSolid if isinstance(g,r.Brep) else None,vertices=len(verts),triangles=len(faces),topology_bounds_mm=tb,mesh_bounds_mm=bb,bounds_delta_mm=max(abs(tb[i][j]-bb[i][j]) for i in range(2) for j in range(3))))
 for o in model.Objects:
  if not o.Attributes.IsInstanceDefinitionObject:visit(o,r.Transform.Identity(),[])
 assert assets
 allb=[p for a in assets for p in a['bounds']];bb=bounds(allb);center=[sum(v)/2 for v in zip(*bb)]
 for a in assets:
  c=[sum(v)/2 for v in zip(*a['bounds'])];dims=[a['bounds'][1][i]-a['bounds'][0][i] for i in range(3)];axis=min(range(3),key=lambda i:dims[i]);off=[0,0,0];off[axis]=(1 if c[axis]>=center[axis] else -1)*350;a['explode']=off
 block=p.stem
 packet=dict(schema='obtp-source-mesh/1',units='mm',id=block,producer='rhino3dm: original cached render meshes',source=dict(repository='wikihouseproject/Skylark',commit='6581cc1de0f4daef81a6b5c5a2eaed3c537d1d8f',path=rec['path'],git_blob_sha=sha,license='CC-BY-SA-4.0'),bounds=bb,assets=assets)
 (ROOT/'dist/catalogue'/f'{block}.json').write_text(json.dumps(packet,separators=(',',':')))
 reports.append(dict(id=block,source=packet['source'],bounds=bb,parts=audit,object_count=len(model.Objects),part_count=len(assets)))
 print(block,'parts',len(assets),'bounds',bb,'worst_delta',max(a['bounds_delta_mm'] for a in audit),flush=True)
(ROOT/'docs/CATALOGUE_GEOMETRY_AUDIT.json').write_text(json.dumps(reports,indent=2))
