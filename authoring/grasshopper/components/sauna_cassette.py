#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
core=importlib.import_module(name+'.sauna_workflow')
def value(key,default):
    v=globals().get(key,default)
    if hasattr(v,'Value'):v=v.Value
    return default if v is None else v
def fail(error):
    import Grasshopper
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,str(error))
scene_json=None;report=''
try:
    document=json.loads(value('plan_json','null'))
    if document is None:raise ValueError('No resolved plan; cassette output cleared')
    scene=core.construct(document);scene_json=json.dumps(scene)
    report='Cassette from '+document['selection']['preset_name']+' / plan '+document['plan']['plan_sha256'][:12]+'\n'+str(len(scene['parts']))+' physical pieces; full scene, including separately scheduled cladding.\nNo bypass or fallback building. Engineering holds remain in the scene.'
except Exception as error:scene_json=None;report=str(error);fail(error)
