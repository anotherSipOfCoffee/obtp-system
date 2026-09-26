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
for module in ['suppliers','export','plan_styles','drawings','insulation','envelope']:
    importlib.reload(importlib.import_module(name+'.'+module))
core=importlib.reload(importlib.import_module(name+'.model'))
scene_json=None
report=""
try:
    system_type=globals().get('system_type',0)
    program_type=globals().get('program_type',0)
    # Generic script inputs may arrive as Grasshopper goo in some Rhino builds.
    def scalar(value):
        return value.Value if hasattr(value, 'Value') else value
    for _input in ['preset_index','room_depth_steps','sauna_length_steps','hall_length_steps',
                   'roof_type','terrace_steps','window_width','facade_type','system_type','program_type','storage_length_steps','wall_height','partition_depth','door_width','door_height',
                   'sauna_door_offset','bench_depth','bench_height','foot_bench_height']:
        globals()[_input]=float(scalar(globals()[_input]))
    for _input in ['custom','storage','include_foundation']:
        globals()[_input]=bool(scalar(globals()[_input]))
    p=core.parameters(int(preset_index),bool(custom),
        program_type=program_type,system_type=system_type,roof_type=roof_type,terrace_steps=terrace_steps,window_width=window_width,facade_type=facade_type,
        room_depth_steps=room_depth_steps,sauna_length_steps=sauna_length_steps,hall_length_steps=hall_length_steps,
        storage=bool(storage),storage_length_steps=storage_length_steps,wall_height=wall_height,
        partition_depth=partition_depth,door_width=door_width,door_height=door_height,
        sauna_door_offset=sauna_door_offset,bench_depth=bench_depth,bench_height=bench_height,
        foot_bench_height=foot_bench_height,include_foundation=bool(include_foundation))
    scene=core.build(p);scene_json=json.dumps(scene)
    m=scene['metrics']
    report='{} | {}\nArea bound {:.2f}/50 m² | Height {:.0f} / 5000 mm | Span {:.0f} / 6000 mm\nModeled wood (structure + finishes, excludes furniture) {:.3f} m³\nREVIEW CANDIDATE; not construction documentation\n{}'.format(
        p['id'],'custom controls active' if custom else 'saved preset; custom controls ignored',m['building_area_bound_m2'],m['height_mm'],
        m['max_bearing_line_span_mm'],m['total_wood_m3'],'\n'.join(scene['holds']))
except Exception as error:
    report='INVALID: '+str(error)
    import Grasshopper
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,report)
