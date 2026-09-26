import sys,json,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.cut_view import parts_below
from obtp.documentation import component_groups,volume,documents
for program in range(2):
 for roof in range(3):
  for foundation in range(2):
   s=build(parameters(2,program_type=program,roof_type=roof,foundation_type=foundation))
   assert all(s['checks'].values())
   assert s['config']['roof_type']==roof
   assert s['foundation_spec']['type']==foundation
   assert len({p['id'] for p in s['parts']})==len(s['parts'])
   assert any(p['family']=='insulation' for p in s['parts'])
   assert not any(p['id'].startswith('canopy/post-') for p in s['parts'])
   assert math.isclose(sum(r['m3'] for r in component_groups(s)),s['metrics']['total_wood_m3'],abs_tol=1e-6)
   assert all(p['family']!='furniture' or p['id'].startswith(('bench-','outside-seat/','shower/','heater/','studio-stove/')) for p in parts_below(s))
print('12 program / roof / foundation combinations passed; quantities reconcile with model.')
