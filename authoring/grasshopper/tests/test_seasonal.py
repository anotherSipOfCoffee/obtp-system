import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
class Seasonal(unittest.TestCase):
 def test_studio_states_and_roof_selection(self):
  for i in range(6):
   for state in (False,True):
    s=build(parameters(i,program_type=1,roof_type=2,studio_winter_closed=state))
    self.assertEqual(s['config']['roof_type'],2)
    self.assertTrue(s['envelope_spec']['heated_centre'])
    self.assertTrue(any(a['id'].startswith('insulation-floor-centre/') for a in s['parts']))
    self.assertTrue(any(a['id'].startswith('insulation-ceiling-centre/') for a in s['parts']))
    self.assertFalse(any(a['id'].startswith('studio-covered-deck/') for a in s['parts']))
    self.assertIsNone(s['seasonal_spec']['glazing_requirement']['Uw_W_m2K'])
    self.assertEqual(s['seasonal_spec']['state'],'closed' if state else 'open')
    self.assertGreater(s['seasonal_spec']['clear_opening_study_mm'],1000)
    self.assertFalse(any(p['id'].startswith('canopy/post-') for p in s['parts']))
    self.assertEqual(len([p for p in s['parts'] if p['id'].startswith('studio-slider-') and '/glass-' in p['id']]),6)
    self.assertTrue(all(s['checks'].values()))
    self.assertTrue(any(p['id']=='studio-stove/body' for p in s['parts']))
    self.assertTrue(any(p['id'].startswith('firewood-niche/board-') for p in s['parts']))
  a=build(parameters(program_type=1,studio_winter_closed=False));b=build(parameters(program_type=1,studio_winter_closed=True))
  self.assertNotEqual(a['geometry_sha256'],b['geometry_sha256'])
  self.assertEqual(a['metrics']['building_area_bound_m2'],b['metrics']['building_area_bound_m2'])
 def test_sauna_return_and_no_posts(self):
  for i in range(6):
   for roof in range(3):
    s=build(parameters(i,roof_type=roof));parts=s['parts']
    self.assertTrue(all(s['checks'].values()));self.assertIsNone(s['seasonal_spec'])
    self.assertTrue(any(p['id'].startswith('terrace-side/board') for p in parts))
    self.assertFalse(any(p['id'].startswith(('canopy/post-','studio-slider-','studio-stove/')) for p in parts))
    if roof!=2:self.assertTrue(any(p['id']=='canopy/cantilever' and p['capacity'] is None for p in s['interfaces']))
if __name__=='__main__':unittest.main()
