#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
core=importlib.import_module(name+'.layout')
def value(key,default):
    v=globals().get(key,default)
    if hasattr(v,'Value'):v=v.Value
    return default if v is None else v
def fail(error):
    import Grasshopper
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,str(error))
programme_json=None;report=''
try:
    p=core.programme(**{k:bool(value(k,True)) for k in ('sauna','entrance','outdoor')},**{k:int(value(k,d)) for k,d in [('sauna_cells',3),('entrance_cells',3),('outdoor_cells',1),('depth_cells',2)]})
    programme_json=json.dumps(p);report='Active rooms: '+', '.join(k for k,v in p['active'].items() if v)+'\nGrid: 900 x 1200 mm. Activation does not depend on connections.'
except Exception as error:report=str(error);fail(error)
