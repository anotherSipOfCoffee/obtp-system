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
scene_json=None;report=''
try:
    original=value('base_scene_json',None)
    if not bool(value('use_layout',False)):
        scene_json=original;report='Existing building controls active; room graph is a separate plan preview.'
    else:
        plan=json.loads(value('plan_json','null'))
        if plan is None:raise ValueError('No valid resolved room plan; structure output cleared')
        base=json.loads(original) if original else None
        if base is None:raise ValueError('No valid base controls for roof/window/foundation; structure output cleared')
        scene=core.build_from_plan(plan,base['config'] if base else None)
        scene_json=json.dumps(scene);report='Structure driven by plan '+plan['plan_sha256'][:12]+'. Roof/window/foundation/height retained from building controls. Plan owns room sizes/storage; passage 900 mm, partition 90 mm. Unsupported layouts stop output.'
except Exception as error:scene_json=None;report=str(error);fail(error)
