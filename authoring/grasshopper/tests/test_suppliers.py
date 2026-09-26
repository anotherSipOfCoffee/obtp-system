import sys,unittest,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.analysis import prepare
from obtp.drawings import section
class Suppliers(unittest.TestCase):
 def test_no_relabelled_fallback(self):
  self.assertEqual(build(parameters())['supplier_spec']['active_system']['key'],'obtp-cassette')
  for value in [1,2,-1]:
   with self.assertRaises(ValueError):build(parameters(system_type=value))
 def test_vertical_details_all_catalogue(self):
  for i,roof,width in itertools.product(range(6),range(3),[580,880,1180]):
   s=build(parameters(i,roof_type=roof,window_width=width));views=s['drawings']['views'];parts={p['id']:p for p in s['parts']}
   self.assertNotIn('window-plan',views);self.assertNotIn('window-jamb',views)
   full=views['window-section'];self.assertEqual(full['axis'],0)
   self.assertEqual({p['id'] for p in full['polygons']},{'window/top','window/bottom','window/glazing-0','window/glazing-1','window/glazing-2'})
   for name in ['window-head','window-sill']:
    v=views[name];self.assertEqual(v['axis'],0);self.assertEqual(v['source_geometry_sha256'],s['geometry_sha256'])
    for p in v['polygons']:
     self.assertIn(p['id'],parts);poly=section(parts[p['id']],0,v['level_mm']);self.assertTrue(poly)
     for y,z in p['points']:
      self.assertTrue(v['crop'][0]-1e-6<=y<=v['crop'][2]+1e-6);self.assertTrue(v['crop'][1]-1e-6<=z<=v['crop'][3]+1e-6)
   self.assertIn('window/bottom',{p['id'] for p in views['window-sill']['polygons']})
   self.assertIn('window/top',{p['id'] for p in views['window-head']['polygons']})
   for product in s['supplier_spec']['products']:
    self.assertTrue(set(product['source_part_ids'])<=set(parts))
   self.assertEqual(any(p['id']=='roof-ruukki' for p in s['supplier_spec']['products']),roof!=0)
 def test_paused_actions_are_not_zero(self):
  a=prepare(build(parameters()));self.assertEqual(a['workflows']['wind']['status'],'paused_by_owner')
  for key in ['wind','snow']:
   self.assertEqual(a['actions'][key]['status'],'paused_by_owner');self.assertIsNone(a['actions'][key]['values'])
if __name__=='__main__':unittest.main()
