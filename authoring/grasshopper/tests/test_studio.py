import itertools,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.drawings import section
from obtp.analysis import prepare,inputs
class Studio(unittest.TestCase):
 def test_catalogue_and_open_centre(self):
  for i,roof,width in itertools.product(range(6),range(3),[580,880,1180]):
   s=build(parameters(i,program_type=1,roof_type=roof,window_width=width));p=s['config'];z=p['studio_zones'];bs=z['bridge_start'];be=z['bridge_end'];F=s['dimensions']['floor_top_mm'];W=s['dimensions']['width_mm']
   self.assertTrue(all(s['checks'].values()));self.assertLessEqual(s['metrics']['building_area_bound_m2'],50)
   self.assertEqual(s['system_spec']['wall_depth'],195);self.assertEqual(s['system_spec']['pitch'],600)
   self.assertFalse(any(a['id'].startswith(('heater/','bench-','shower/','sauna-partition/')) for a in s['parts']))
   self.assertFalse(any(a['family'] in ('walls','interior','facade','insulation') and section(a,0,(bs+be)/2) and a['origin'][2]<F+1100<a['origin'][2]+a['size'][2] for a in s['parts']))
   self.assertFalse(any(a['family']=='furniture' and not a['id'].startswith(('studio-slider-','studio-stove/')) and a['origin'][0]<be and a['origin'][0]+a['size'][0]>bs for a in s['parts']))
   self.assertEqual(len([v for v in s['opening_voids'] if 'entry' in v['id']]),2)
   self.assertEqual(len([a for a in s['parts'] if a['id'].startswith('studio-storage/')]),5 if p['storage'] else 0)
   for a in s['parts']:
    if (a['id'].startswith('insulation-floor') or a['id'].startswith('insulation-ceiling')) and '-centre/' not in a['id']:
     self.assertTrue(a['origin'][0]+a['size'][0]<=bs+1e-6 or a['origin'][0]>=be-1e-6)
   self.assertEqual(s['drawings']['source_geometry_sha256'],s['geometry_sha256'])
   self.assertNotIn('Pirtis',[a['text'] for a in s['drawings']['views']['plan']['labels']])
 def test_program_isolation_and_rejection(self):
  before=build(parameters());studio=build(parameters(program_type=1));after=build(parameters())
  self.assertEqual(before['geometry_sha256'],after['geometry_sha256'])
  a=prepare(studio);self.assertIsNone(a['inputs']['heater']);self.assertEqual(a['inputs']['stages'],[])
  gh=prepare(studio,inputs());self.assertIsNone(gh['inputs']['heater']);self.assertEqual(gh['inputs']['stages'],[]);self.assertTrue(gh['inputs']['input_notes'])
  self.assertFalse(any(p['id']=='heater-harvia' for p in studio['supplier_spec']['products']))
  with self.assertRaises(ValueError):build(parameters(program_type=2))
  with self.assertRaises(ValueError):build(parameters(program_type=1,custom=True,room_depth_steps=8,sauna_length_steps=8,hall_length_steps=8,storage_length_steps=4))
if __name__=='__main__':unittest.main()
