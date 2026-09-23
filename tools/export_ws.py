"""Extract pinned W-S cached render meshes; requires rhino3dm. No remeshing.
Run: python tools/export_ws.py /path/to/W-S.3dm
"""
import hashlib,json,math,sys
from pathlib import Path
import rhino3dm as r
ROOT=Path(__file__).resolve().parents[1]
p=Path(sys.argv[1]); raw=p.read_bytes()
sha=hashlib.sha1(('blob %d\0'%len(raw)).encode()+raw).hexdigest()
assert sha=='932338ca81fdc2acdd345cd0fc9df09d2a9888b2','Unexpected source file'
m=r.File3dm.Read(str(p)); assert m.Settings.ModelUnitSystem==r.UnitSystem.Millimeters
refs=[o for o in m.Objects if isinstance(o.Geometry,r.InstanceReference)]
assert len(refs)==1
ref=refs[0]; xf=ref.Geometry.Xform
ids=set(next(d for d in m.InstanceDefinitions if d.Id==ref.Geometry.ParentIdefId).GetObjectIds())
assets=[]; audit=[]
labels=['Right side','Left side','Upper crosspiece','Middle crosspiece','Lower crosspiece','Front face','Back face']
offsets=[[350,0,0],[-350,0,0],[0,0,230],[0,0,0],[0,0,-230],[0,-550,0],[0,550,0]]
for o in m.Objects:
 if o.Attributes.Id not in ids: continue
 b=o.Geometry; assert isinstance(b,r.Brep) and b.IsValid and b.IsSolid
 verts=[]; faces=[]; lookup={}; maxerr=0
 for face in b.Faces:
  mesh=face.GetMesh(r.MeshType.Render); assert mesh is not None
  remap=[]
  for v in mesh.Vertices:
   point=r.Point3d(v.X,v.Y,v.Z); point.Transform(xf)
   orig=(point.X,point.Y,point.Z); q=tuple(round(c,6) for c in orig)
   maxerr=max(maxerr,max(abs(a-c) for a,c in zip(orig,q)))
   if q not in lookup: lookup[q]=len(verts); verts.append(q)
   remap.append(lookup[q])
  for f in mesh.Faces:
   a,c,d,e=[remap[k] for k in f]
   # Source instance reflects Z; reverse the triangle winding.
   faces.append([a,d,c])
   if d!=e: faces.append([a,e,d])
 assert all(math.isfinite(c) for v in verts for c in v)
 bb=b.Duplicate(); bb.Transform(xf); bounds=bb.GetBoundingBox()
 vb=[[min(v[k] for v in verts) for k in range(3)],[max(v[k] for v in verts) for k in range(3)]]
 cb=[[bounds.Min.X,bounds.Min.Y,bounds.Min.Z],[bounds.Max.X,bounds.Max.Y,bounds.Max.Z]]
 points=[]
 for v in b.Vertices:
  pt=v.Location; pt.Transform(xf); points.append((pt.X,pt.Y,pt.Z))
 tb=[[fn(v[k] for v in points) for k in range(3)] for fn in (min,max)]
 delta=max(abs(vb[i][k]-tb[i][k]) for i in range(2) for k in range(3)); assert delta<0.01
 i=len(assets)
 assets.append(dict(id=str(o.Attributes.Id),label='P%02d'%(i+1),description=labels[i],kind='source-part',material='plywood',vertices=verts,faces=faces,bounds=vb,explode=offsets[i]))
 audit.append(dict(id=str(o.Attributes.Id),valid=True,solid=True,brep_faces=len(b.Faces),vertices=len(verts),triangles=len(faces),cad_conservative_bounds_mm=cb,cad_vertex_bounds_mm=tb,mesh_bounds_mm=vb,bounds_delta_mm=delta,coordinate_rounding_max_mm=maxerr))
assert len(assets)==7
packet=dict(schema='obtp-source-mesh/1',units='mm',producer='rhino3dm: source cached render meshes',source=dict(repository='wikihouseproject/Skylark',commit='6581cc1de0f4daef81a6b5c5a2eaed3c537d1d8f',path='SKYLARK150/Walls/W-S/W-S_detailed/W-S.3dm',git_blob_sha=sha,license='CC-BY-SA-4.0'),assets=assets,assemblies=[dict(id='W-S',instances=[dict(asset=a['id'],translate=[0,0,0]) for a in assets])])
(ROOT/'dist/ws/model.json').write_text(json.dumps(packet,separators=(',',':')))
report=dict(source_blob_sha=sha,source_units='mm',instance_id=str(ref.Attributes.Id),instance_transform=[[getattr(xf,'M%d%d'%(i,j)) for j in range(4)] for i in range(4)],parts=audit,notes=['Seven definition Breps instantiated once; definition geometry is not counted twice.','Saved render meshes extracted, not regenerated. Six decimal places in mm.','Source reflection applied to coordinates; triangle winding reversed.','P01–P07 and descriptions are OBTP display labels, not CNC part identification.','Exploded translations are viewing aids, not a prescribed assembly sequence.','Brep conservative bounds include untrimmed surface extents; comparison uses topology vertex bounds. This is not a surface deviation test.', 'Rhino 8 interactive and engineering checks not performed.'])
(ROOT/'docs/WS_GEOMETRY_AUDIT.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'parts':len(assets),'vertices':sum(len(a['vertices']) for a in assets),'triangles':sum(len(a['faces']) for a in assets),'max_bounds_delta_mm':max(a['bounds_delta_mm'] for a in audit),'json_bytes':(ROOT/'dist/ws/model.json').stat().st_size}))
