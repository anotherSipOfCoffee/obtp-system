import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.preview_stages import prepare,core_part
from obtp.manufacturing import identity

class PreviewStagesTests(unittest.TestCase):
 def test_stages_are_cumulative_complete_and_do_not_mutate(self):
  for program in (0,1):
   s=build(parameters(2,program_type=program));before=copy.deepcopy(s);previous=set()
   for level in range(9):
    d=prepare(s,level);ids={p['id'] for p in d['parts']}
    self.assertTrue(previous<=ids);previous=ids
   self.assertEqual(len(previous),len(s['parts']));self.assertEqual(prepare(s,0)['parts'],[]);self.assertEqual(s,before)
 def test_core_types_share_materials_and_stage_colours_are_stable(self):
  s=build(parameters(2,program_type=1));d=prepare(s,8,1)
  self.assertTrue(all(core_part(p) for p in d['parts']))
  self.assertLess(len(d['parts']),len(s['parts']))
  mapping={}
  for p,c in zip(d['parts'],d['rgba']):
   k=identity(p)
   if k in mapping:self.assertEqual(mapping[k],c)
   mapping[k]=c
  self.assertEqual(len(set(mapping.values())),len(mapping))
  for level in range(9):
   d=prepare(s,level,1)
   for p,c in zip(d['parts'],d['rgba']):self.assertEqual(mapping[identity(p)],c)
 def test_invalid_controls_rejected(self):
  s=build(parameters(2))
  for level,core in [(-1,0),(9,0),(1.5,0),(8,2)]:
   with self.assertRaises(ValueError):prepare(s,level,core)
