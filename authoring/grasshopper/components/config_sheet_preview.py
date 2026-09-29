#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
geometry=[];labels=[];label_points=[];label_sizes=[];report='Sheet preview off'
def value(k,default=None):
 v=globals().get(k,default)
 return getattr(v,'Value',v)
try:
 if value('show',True):
  import Rhino
  code=importlib.import_module(name+'.room_documents')
  scene=json.loads(value('scene_json'));kind=int(value('document_set',3))
  data=code.modelspace(code.selected_recipe(scene,kind))
  for line in data['lines']:geometry.append(Rhino.Geometry.PolylineCurve([Rhino.Geometry.Point3d(*q) for q in line]))
  for t in data['texts']:
   labels.append(t['text']);label_points.append(Rhino.Geometry.Point3d(*t['at']));label_sizes.append(t['height'])
  report=str(data['sheets'])+' drawing sheets in model space, below the building. Zoom Extents if outside the viewport. Display only.'
except Exception as error:
 geometry=[];labels=[];label_points=[];label_sizes=[];report=str(error)
 import Grasshopper
 ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,report)
