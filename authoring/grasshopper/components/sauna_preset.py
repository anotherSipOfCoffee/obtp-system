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
    inputs={k:value(k,d) for k,d in [('sauna',True),('entrance',True),('outdoor',True),('sauna_entrance',2),('entrance_outdoor',3),('sauna_outdoor',0),('arrangement',0),('roof_type',1),('window_width',1180),('wall_height',2100),('foundation_type',0),('include_foundation',True)]}
    inputs.update({k:value(k,d) for k,d in [('base_preset',2),('use_overrides',False),('window_shift',0)]})
    for key in ['sauna_cells','entrance_cells','outdoor_cells','work_cells','centre_cells','preparation_cells']:
        inputs[key+'_delta']=value(key+'_delta',0)
    selection=core.select(value('preset_index',2),**inputs)
    workflow_json=json.dumps(selection)
    report=selection['preset_name']+'\n'+('Custom inputs active when Use overrides is True. False resets to the selected base preset.' if selection['custom'] else 'Saved dimensions. Custom controls are inactive; select Custom Sauna or Custom Studio to use them.')+'\nMillimetres; grid 900 X / 1200 Y. Geometric candidate only. Roof/window/height/foundation settings apply to all presets.'
    if selection['custom']:
        plan=core.resolve(selection)['plan']
        report+='\nEffective room lengths: '+', '.join(r['id']+' '+str(r['bounds_mm'][2])+' mm' for r in plan['rooms'])+'\nWidth fixed at '+str(plan['bounds_mm'][3])+' mm. Deltas are ignored while overrides are off.'
except Exception as error:report=str(error);fail(error)
