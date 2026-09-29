#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
STAGE='programme'
data_json=None;report=''
def value(key,default=None):
    v=globals().get(key,default)
    return getattr(v,'Value',v)
try:
    exchange=importlib.import_module(name+'.room_exchange')
    data_json,report=exchange.transfer(STAGE,value('upstream'),value('file_path',''),value('read_file',False),value('write_file',False))
except Exception as error:
    data_json=None;report=str(error)
    import Grasshopper
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,report)
