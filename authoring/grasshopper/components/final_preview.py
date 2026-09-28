#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
core=importlib.import_module(name+'.checkpoints')
def value(key,default):
 v=globals().get(key,default)
 if hasattr(v,'Value'):v=v.Value
 return default if v is None else v
def fail(error):
 import Grasshopper
 ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,str(error))
geometry=[];part_ids=[];materials=[];type_ids=[];legend=[];preview_status='No valid assembly output'
try:
 data=json.loads(value('display_json','null'))
 if data is None:raise ValueError('CP5: no assembly output; preview cleared')
 shown=core.view(data,value('preview_scope',2),bool(value('type_colours',False)),str(value('assembly_filter','')))
 adapter=importlib.import_module(name+'.rhino_adapter')
 geometry,part_ids=adapter.preview(dict(parts=shown['parts'],geometry_sha256=data['source_geometry_sha256'],dimensions=data['dimensions']),True,False,0)
 from System.Drawing import Color
 import Rhino
 from Grasshopper.Kernel.Types import GH_Material
 cache={}
 for rgba in shown['rgba']:
  rgba=tuple(rgba)
  if rgba not in cache:
   rr,gg,bb,aa=rgba;cache[rgba]=GH_Material(Rhino.Display.DisplayMaterial(Color.FromArgb(rr,gg,bb),1-aa/255.0))
  materials.append(cache[rgba])
 type_ids=shown['type_ids'];legend=shown['legend'];preview_status=shown['status']
except Exception as error:
 geometry=[];part_ids=[];materials=[];type_ids=[];legend=[];preview_status=str(error);fail(error)
