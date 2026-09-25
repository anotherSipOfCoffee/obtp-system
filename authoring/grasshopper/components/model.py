#! python 3
# Editable inputs live on the canvas. The generator is in obtp/model.py.
import hashlib
import importlib
import importlib.util
import json
import sys
from pathlib import Path

root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')])
    package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
core=importlib.reload(importlib.import_module(name+'.model'))
scene_json=None
try:
    p=core.parameters(int(preset_index),bool(custom),
        room_depth_steps=room_depth_steps,sauna_length_steps=sauna_length_steps,hall_length_steps=hall_length_steps,
        storage=bool(storage),storage_length_steps=storage_length_steps,wall_height=wall_height,
        partition_depth=partition_depth,door_width=door_width,door_height=door_height,
        sauna_door_offset=sauna_door_offset,bench_depth=bench_depth,bench_height=bench_height,
        foot_bench_height=foot_bench_height,include_foundation=bool(include_foundation))
    scene=core.build(p);scene_json=json.dumps(scene)
    m=scene['metrics']
    report='{} | {}\nArea bound {:.2f}/50 m² | Height {} / 5000 mm | Span {} / 6000 mm\nStructural wood {:.3f} m³\nREVIEW CANDIDATE; website publication blocked\n{}'.format(
        p['id'],'custom controls active' if custom else 'saved preset; custom controls ignored',m['building_area_bound_m2'],m['height_mm'],
        m['max_bearing_line_span_mm'],m['total_wood_m3'],'\n'.join(scene['holds']))
except Exception as error:
    report='INVALID: '+str(error)
    import Grasshopper
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,report)
