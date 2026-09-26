import sys,unittest,itertools,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.export import vertices
from test_r02 import collide
class R04(unittest.TestCase):
 def test_catalogue_drawings_and_insulation(self):
  for i,roof,terrace,window in itertools.product(range(6),range(3),[1,2],[600,900,1200]):
   s=build(parameters(i,roof_type=roof,terrace_steps=terrace,window_width=window));d=s['drawings']
   self.assertEqual(d['source_geometry_sha256'],s['geometry_sha256'])
   if roof==2:self.assertAlmostEqual(s['metrics']['height_mm'],4480)
   self.assertEqual(d['views']['window']['dimensions'][0]['value_mm'],window)
   self.assertEqual(d['views']['window']['dimensions'][1]['value_mm'],s['config']['door_height'])
   for view in d['views'].values():
    self.assertTrue(view['polygons'])
    for dim in view['dimensions']:
     self.assertGreater(dim['value_mm'],0);self.assertAlmostEqual(dim['value_mm'],abs(dim['b'][dim['axis']]-dim['a'][dim['axis']]))
   for a in s['parts']:
    if a['family']!='insulation':continue
    for v in s['opening_voids']:self.assertFalse(collide(a,v),a['id'])
    for b in s['parts']:
     if b['material']=='timber' and not (b.get('slope_y') or b.get('top_slope_y')):self.assertFalse(collide(a,b),(a['id'],b['id']))
 def test_section_vertices(self):
  from obtp.drawings import section
  part=dict(origin=[0,0,0],size=[100,100,10],slope_y=.5)
  poly=section(part,0,50);self.assertEqual(set(poly),{(0,0),(100,50),(100,60),(0,10)})
if __name__=='__main__':unittest.main()
