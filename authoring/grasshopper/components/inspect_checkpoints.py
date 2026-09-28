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
report='';rooms=[];openings=[];assembly_ids=[];assembly_rows=[];part_rows=[];checks=[]
try:
 scene=json.loads(value('scene_json','null'))
 if scene is None:raise ValueError('CP3: no valid construction scene')
 data=core.inspect(scene)
 report=data['report'];rooms=data['rooms'];openings=data['openings'];assembly_ids=data['assembly_ids'];assembly_rows=data['assemblies'];part_rows=data['parts'];checks=data['checks']
except Exception as error:report=str(error);fail(error)
