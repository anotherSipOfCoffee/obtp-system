#! python 3
# Creator substitutes STAGE_NAME once when creating each native component.
STAGE_NAME='structure'
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
core=importlib.import_module(name+'.plan_pipeline')
def read(key):
    v=globals().get(key)
    if hasattr(v,'Value'):v=v.Value
    if v is None:raise ValueError(STAGE_NAME+': connect valid '+key+'; downstream cleared')
    return json.loads(v)
data_json=None;report='';details=[]
try:
    if STAGE_NAME=='structure':result=core.structure(read('plan_json'))
    elif STAGE_NAME in ('floor','roof','walls'):result=core.generate(read('structure_json'),STAGE_NAME)
    elif STAGE_NAME=='framing':result=core.merge(read('structure_json'),read('floor_json'),read('roof_json'),read('walls_json'))
    elif STAGE_NAME=='complete':result=core.finish(read('structure_json'),read('previous_json'))
    else:result=core.enrich(read('structure_json'),read('previous_json'),STAGE_NAME)
    data_json=json.dumps(result)
    report=result.get('report','Complete canonical model: '+str(len(result.get('parts',[])))+' pieces including separate cladding schedule. Drawings and quantities use this scene.')
    if STAGE_NAME=='structure':details=[json.dumps(r,sort_keys=True) for r in result['resolved_plan']['wall_runs']+result['resolved_plan']['opening_hosts']]
    else:details=result.get('added_ids',[])
except Exception as error:
    data_json=None;report=STAGE_NAME+': '+str(error);details=[]
    import Grasshopper
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,report)
