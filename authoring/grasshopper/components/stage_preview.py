#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
geometry=[];part_ids=[];report=''
try:
    data=globals().get('data_json')
    if hasattr(data,'Value'):data=data.Value
    if data is None:raise ValueError('No valid stage result; preview cleared')
    data=json.loads(data)
    active=globals().get('show',False)
    if hasattr(active,'Value'):active=active.Value
    core=importlib.import_module(name+'.plan_pipeline')
    parts,floor_top=core.preview_parts(data)
    if active:
        adapter=importlib.import_module(name+'.rhino_adapter')
        geometry,part_ids=adapter.preview(dict(parts=parts,dimensions={'floor_top_mm':floor_top},geometry_sha256=hashlib.sha256(json.dumps(parts,sort_keys=True).encode()).hexdigest()))
    report=str(len(parts))+' stage pieces available. Preview is display-only.'
except Exception as error:
    geometry=[];part_ids=[];report=str(error)
