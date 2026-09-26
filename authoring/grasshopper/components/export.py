#! python 3
# Explicit false -> true transition exports one new review folder.
# Changing sliders while Export remains true does not write files again.
import hashlib
import importlib
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
import scriptcontext
for _input in ['scene_json', 'run_export']:
    _value=globals()[_input]
    if hasattr(_value, 'Value'):globals()[_input]=_value.Value
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')])
    package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
key='OBTP-export-'+str(ghenv.Component.InstanceGuid)
previous=scriptcontext.sticky.get(key,True) # On first solve require an explicit false state.
scriptcontext.sticky[key]=bool(run_export)
receipt='Set Export false, then true to save a new review snapshot.'
if run_export and not previous:
    if not scene_json:raise ValueError('No valid model to export')
    scene=json.loads(scene_json)
    adapter=importlib.reload(importlib.import_module(name+'.rhino_adapter'))
    exporter=importlib.reload(importlib.import_module(name+'.export'))
    audit=adapter.audit(scene)
    destination=root/'rhino-exports'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    files=exporter.export_one(scene,destination,adapter.Api)
    drawings=importlib.reload(importlib.import_module(name+'.native_drawings'))
    try:
        layout=drawings.bake(scene)
    except Exception as error:
        layout='Native layout not created: '+str(error)
    (destination/'rhino-audit.json').write_text(json.dumps(audit,indent=2))
    receipt='Saved review snapshot: '+str(destination)+'\n'+audit['status']+'\n'+layout
    scriptcontext.sticky[key+'-receipt']=receipt
elif previous and run_export:
    receipt=scriptcontext.sticky.get(key+'-receipt','Export already triggered; reset false to export again.')
