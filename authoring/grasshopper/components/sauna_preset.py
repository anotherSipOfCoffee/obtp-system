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
workflow_json=None;report=''
try:
    inputs={k:value(k,d) for k,d in [('sauna',True),('entrance',True),('outdoor',True),('sauna_cells',3),('entrance_cells',3),('outdoor_cells',1),('depth_cells',2),('sauna_entrance',2),('entrance_outdoor',3),('sauna_outdoor',0),('arrangement',0),('roof_type',1),('window_width',1180),('wall_height',2100),('foundation_type',0),('include_foundation',True)]}
    selection=core.select(int(value('preset_index',2)),**inputs)
    workflow_json=json.dumps(selection)
    report=selection['preset_name']+'\n'+('Custom room, edge and dimension controls ACTIVE.' if selection['custom'] else 'Saved layout loaded. Custom room, edge, dimension and arrangement controls ignored.')+'\nCassette system fixed. Roof/window/height/foundation settings apply to all presets.\nStudio uses saved room layouts; Custom controls apply only to Custom Sauna.'
except Exception as error:report=str(error);fail(error)
