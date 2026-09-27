"""Acceptance checks for display-only assembly poses and visible finish details."""
import copy, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build, parameters
from obtp.documentation import stage, stage_parts, STAGES
from obtp.assembly_pose import display_vertices
from obtp.manufacturing import identity
from obtp.schedule_pdf import included

class RevisionDetails(unittest.TestCase):
 def test_openings_lie_flat_before_insertion_without_changing_identity(self):
  for program in (0,1):
   scene=build(parameters(2,program_type=program));original=copy.deepcopy(scene)
   flat={p['id']:p for p in stage_parts(scene,7)}
   installed={p['id']:p for p in stage_parts(scene,8)}
   openings=[p for p in scene['parts'] if stage(p)==8]
   self.assertTrue(openings)
   for p in openings:
    q=flat[p['id']];self.assertIn('display_transform',q)
    self.assertEqual(identity(q),identity(p));self.assertNotIn('display_transform',installed[p['id']])
    # A vertical product's height lies in the ground plane after rigid rotation.
    vs=display_vertices(q)
    self.assertLessEqual(max(v[2] for v in vs)-min(v[2] for v in vs),max(p['size'][:2])+.001)
   self.assertEqual(scene,original)
 def test_all_facade_and_fascia_are_last(self):
  s=build(parameters(3))
  finish=[p for p in s['parts'] if p['family']=='facade' or p['id'].startswith(('terrace-fascia-','floor-edge-','roof-fascia-'))]
  self.assertTrue(finish);self.assertTrue(all(stage(p)==len(STAGES)-1 for p in finish))
  self.assertEqual({p['id'] for p in stage_parts(s,11)},{p['id'] for p in s['parts']})
 def test_schedule_scope_and_physical_finish_details(self):
  s=build(parameters(3));ids={p['id'] for p in s['parts']}
  selected=[p for p in s['parts'] if included(p)]
  self.assertTrue(any(p['material']=='mineral-wool' for p in selected))
  self.assertFalse(any(p['material'] in ('cladding-wood','glass','object','deck-wood') for p in selected))
  for prefix in ('terrace-fascia-front/','bench-upper/front-cover-','bench-lower/other-end-cover-','facade-niche-shower/board-head-','facade-niche-seat/board-soffit-'):
   self.assertTrue(any(id.startswith(prefix) for id in ids),prefix)
  seat=next(p for p in s['parts'] if p['id']=='outside-seat/seat')
  self.assertEqual(seat['size'][1],300)
  self.assertEqual(seat['origin'][1]+seat['size'][1],s['dimensions']['width_mm'])
