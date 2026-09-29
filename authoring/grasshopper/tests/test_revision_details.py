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
  for prefix in ('terrace-fascia-front/','bench-upper/front-cover-','bench-lower/other-end-cover-','facade-niche-shower-back/board-','facade-niche-seat/board-soffit-'):
   self.assertTrue(any(id.startswith(prefix) for id in ids),prefix)
  seat=next(p for p in s['parts'] if p['id']=='outside-seat/seat')
  self.assertEqual(seat['size'][1],300)
  self.assertEqual(seat['origin'][1]+seat['size'][1],s['dimensions']['width_mm'])

 def test_floor_and_terrace_share_actual_member_faces(self):
  for program in (0,1):
   scene=build(parameters(3,program_type=program))
   floors=[p for p in scene['parts'] if p['family']=='floor' and '/edge-' in p['id']]
   terrace=[p for p in scene['parts'] if p['id'].startswith('terrace/joist-')]
   for a in floors:
    self.assertTrue(any(a['origin'][0]==b['origin'][0] and a['size'][0]==b['size'][0] for b in terrace),a['id'])
 def test_niches_have_full_depth_returns_and_flat_soffits(self):
  scene=build(parameters(3));F=scene['dimensions']['floor_top_mm'];H=scene['config']['door_height']
  for label in ('shower','seat'):
   for side in ('left','right','back'):
    boards=[p for p in scene['parts'] if p['id'].startswith('facade-niche-'+label+'-'+side+'/board-')]
    self.assertTrue(boards)
    self.assertTrue(all(p['origin'][2]==F and p['size'][2]==H for p in boards))
   soffit=[p for p in scene['parts'] if p['id'].startswith('facade-niche-'+label+'/board-soffit-')]
   self.assertTrue(all(p['origin'][2]==F+H for p in soffit))
   depth=max(p['origin'][1]+p['size'][1] for p in soffit)-min(p['origin'][1] for p in soffit)
   self.assertGreater(depth,300)
