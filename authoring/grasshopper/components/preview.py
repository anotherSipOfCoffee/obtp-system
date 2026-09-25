#! python 3
# View operations do not change the exported source geometry or quantities.
import hashlib
import importlib
import importlib.util
import json
import sys
from pathlib import Path
for _input in ['scene_json', 'panels', 'cut', 'explode']:
    _value=globals()[_input]
    if hasattr(_value, 'Value'):globals()[_input]=_value.Value
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')])
    package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
adapter=importlib.reload(importlib.import_module(name+'.rhino_adapter'))
geometry=[];part_ids=[]
if scene_json:
    geometry,part_ids=adapter.preview(json.loads(scene_json),bool(panels),bool(cut),float(explode))
