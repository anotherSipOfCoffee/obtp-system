import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.cut_view import parts_below
from obtp.export import vertices
class CutView(unittest.TestCase):
 def test_every_solid_below_plane(self):
  for program in range(2):
   for preset in range(6):
    for roof in range(3):
     s=build(parameters(preset,program_type=program,roof_type=roof));original=s['geometry_sha256'];z=s['dimensions']['floor_top_mm']+1100
     cut=parts_below(s)
     self.assertTrue(cut)
     self.assertTrue(all(v[2]<=z+1e-8 for p in cut for v in vertices(p)))
     self.assertEqual(original,s['geometry_sha256'])
     source={p['id']:p for p in s['parts']}
     self.assertTrue(all(p['id'] in source for p in cut))
 def test_niche(self):
  s=build(parameters(program_type=1));ids={p['id'] for p in s['parts']}
  self.assertFalse(any(i.startswith('firewood-rack/') for i in ids))
  self.assertTrue(any(i.startswith('log-niche-front/') for i in ids))
  self.assertTrue(any(i.startswith('log-niche-back/') for i in ids))
  self.assertTrue(all(s['checks'].values()))
if __name__=='__main__':unittest.main()
