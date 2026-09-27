#! python 3
# View operations do not change the exported source geometry or quantities.
import hashlib
import importlib
import importlib.util
import json
import sys
from pathlib import Path
for _input in ['scene_json','assembly_stage','core_frame']:
    _value=globals()[_input]
    if hasattr(_value, 'Value'):globals()[_input]=_value.Value
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')])
    package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
adapter=importlib.reload(importlib.import_module(name+'.rhino_adapter'))
styles=importlib.reload(importlib.import_module(name+'.preview_stages'))
geometry=[];part_ids=[];materials=[];type_ids=[];legend=[];preview_status='No model'
if scene_json:
    import Rhino
    from System.Drawing import Color
    from Grasshopper.Kernel.Types import GH_Material
    scene=json.loads(scene_json)
    display=styles.prepare(scene,8 if assembly_stage is None else assembly_stage,0 if core_frame is None else core_frame)
    shown=dict(scene);shown['parts']=display['parts']
    geometry,part_ids=adapter.preview(shown,True,False,0)
    type_ids=display['type_ids'];legend=display['legend'];preview_status=display['status']
    cache={}
    for rgba in display['rgba']:
        if rgba not in cache:
            r,g,b,a=rgba
            cache[rgba]=GH_Material(Rhino.Display.DisplayMaterial(Color.FromArgb(r,g,b),1-a/255.0))
        materials.append(cache[rgba])
