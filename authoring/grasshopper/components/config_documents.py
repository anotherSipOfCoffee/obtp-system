#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
receipt='Export off'
def value(k,default=None):
 v=globals().get(k,default)
 return getattr(v,'Value',v)
try:
 # Rising edge prevents duplicate Rhino layouts on unrelated GH recomputations.
 key='obtp-doc-export:'+str(ghenv.Component.InstanceGuid)
 import scriptcontext
 enabled=bool(value('generate',False));previous=scriptcontext.sticky.get(key,False)
 scriptcontext.sticky[key]=enabled
 if enabled and not previous:
  code=importlib.import_module(name+'.room_documents')
  result=code.export(json.loads(value('scene_json')),value('destination'),value('rates_path'),native=True)
  receipt='Created Rhino layouts and PDFs: '+result['folder'];scriptcontext.sticky[key+':receipt']=receipt
 elif enabled:receipt=scriptcontext.sticky.get(key+':receipt','Turn Generate off then on to export again')
except Exception as error:
 receipt='Export failed: '+str(error)
 import Grasshopper
 ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,receipt)
