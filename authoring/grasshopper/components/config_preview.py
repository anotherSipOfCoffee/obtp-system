#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
core=importlib.import_module(name+'.room_config')
geometry=[];labels=[];label_points=[];report=''
try:
 v=globals().get('data_json');v=getattr(v,'Value',v);data=json.loads(v) if v else None
 if not data:raise ValueError('No valid upstream output; preview cleared')
 show=globals().get('show',True);show=getattr(show,'Value',show)
 if show:
  import Rhino
  if data.get('stage')=='plan':
   core.require(data,'plan');oy=-6500;positions={}
   for i,r in enumerate(data['rooms']):
    x,y,w,h=r['bounds_mm'];pts=[Rhino.Geometry.Point3d(a,b+oy,0) for a,b in [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]]
    geometry.append(Rhino.Geometry.PolylineCurve(pts));labels.append(r['id']+' / '+str(w)+' x '+str(h));label_points.append(Rhino.Geometry.Point3d(x+w/2,oy+h/2,0))
    point=Rhino.Geometry.Point3d(i*1500,oy-1500,0);positions[r['id']]=point
    geometry.append(Rhino.Geometry.Circle(point,180).ToNurbsCurve());labels.append(r['id']);label_points.append(point)
   for poly in core.plan_view(data)['polygons']:
    if poly['material']!='timber':continue
    mesh=Rhino.Geometry.Mesh()
    for x,y in poly['points']:mesh.Vertices.Add(x,y+oy,5)
    mesh.Faces.AddFace(0,1,2,3);mesh.Normals.ComputeNormals();geometry.append(mesh)
   for e in data['edges']:
    a=positions[e['a']];b=positions[e['b']];geometry.append(Rhino.Geometry.LineCurve(a,b));labels.append(e['boundary']);label_points.append(Rhino.Geometry.Point3d((a.X+b.X)/2,a.Y-300,0))
   for r in core.wall_runs(data):
    if r.get('door_width'):
     a=r['opening_origin'];b=list(a);b[0 if r['axis']=='x' else 1]+=r['door_width']
     geometry.append(Rhino.Geometry.LineCurve(Rhino.Geometry.Point3d(a[0],a[1]+oy,10),Rhino.Geometry.Point3d(b[0],b[1]+oy,10)))
  else:
   if data.get('stage')=='skeleton':core.require(data,'skeleton')
   adapter=importlib.import_module(name+'.rhino_adapter')
   payload=dict(parts=data['parts'],dimensions=data['dimensions'],geometry_sha256=data.get('geometry_sha256',data.get('sha256')))
   geometry,unused=adapter.preview(payload)
 report='Display only; coordinates follow the current source.'
except Exception as error:
 geometry=[];labels=[];label_points=[];report=str(error)
 import Grasshopper
 ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,report)
