import copy,sys,unittest,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.documentation import stage,stage_parts,parts_layout
from obtp.wall_erection import groups,pose,sequence
from obtp.assembly_pose import display_vertices
from obtp.manufacturing import identity
class WallErection(unittest.TestCase):
 def test_connected_opening_wall_and_fixed_pivot(self):
  s=build(parameters(2));before=copy.deepcopy(s)
  g=next(g for g in groups(s,stage) if 'front-window' in g['name'])
  self.assertIn('front',g['roots']);self.assertTrue(any('/lintel' in p['id'] for p in g['parts']))
  for angle in (90,45):
   q=pose(g,angle);m=q[0]['display_transform'];k=g['axis'];n=1-k
   pivot=[0.,0.,g['z']];pivot[k]=g['lo'];pivot[n]=g['pivot']
   self.assertTrue(all(abs(sum(row[j]*pivot[j] for j in range(3))+row[3]-pivot[i])<1e-6 for i,row in enumerate(m)))
   for a,b in zip(g['parts'],q):
    self.assertEqual(identity(a),identity(b));vs=display_vertices(b)
    self.assertAlmostEqual(math.dist(vs[0],vs[6]),math.sqrt(sum(v*v for v in a['size'])))
   self.assertEqual(len({str(p['display_transform']) for p in q}),1)
  self.assertEqual(s,before)
 def test_sequence_has_every_part_once_and_cladding_last(self):
  for program in (0,1):
   s=build(parameters(2,program_type=program));seq=sequence(s,stage,stage_parts)
   previous=set()
   for step in seq:
    ids=[p['id'] for p in step['parts']];self.assertEqual(len(ids),len(set(ids)));self.assertTrue(previous<=set(ids));previous=set(ids)
   self.assertEqual(previous,{p['id'] for p in s['parts']})
   self.assertFalse(any(stage(p)==11 for p in seq[-2]['parts']))
   self.assertEqual(seq[-1]['label'],'Cladding last')
   self.assertEqual(len(parts_layout(s)['sheets']),4)
 def test_default_flat_walls_clear_previous_standing_walls(self):
  from test_r02 import collide
  for program in (0,1):
   s=build(parameters(2,program_type=program))
   for step in sequence(s,stage,stage_parts):
    if not step['label'].endswith('/ Lay flat'):continue
    active=[];previous=[]
    for p in step['parts']:
     if stage(p)!=4 or p['material'] not in ('timber','plywood'):continue
     vs=display_vertices(p);lo=[min(v[k] for v in vs) for k in range(3)];hi=[max(v[k] for v in vs) for k in range(3)]
     q=dict(p,origin=lo,size=[hi[k]-lo[k] for k in range(3)])
     (active if p['id'] in step['active'] else previous).append(q)
    for a in active:
     for b in previous:self.assertFalse(collide(a,b),(step['label'],a['id'],b['id']))
