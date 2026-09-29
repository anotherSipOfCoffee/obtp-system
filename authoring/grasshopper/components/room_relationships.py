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
graph_json=None;report=''
try:
    p=json.loads(value('programme_json','null'))
    if p is None:raise ValueError('Connect a valid room programme')
    graph=core.relationships(p,**{k:int(value(k,d)) for k,d in [('sauna_entrance',2),('entrance_outdoor',3),('sauna_outdoor',0)]})
    graph_json=json.dumps(graph);report='\n'.join(e['a']+' / '+e['b']+': '+e['kind'] for e in graph['edges'])+'\n'+'\n'.join(graph['notes'])
except Exception as error:report=str(error);fail(error)
