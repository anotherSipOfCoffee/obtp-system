import sys,unittest,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.export import vertices
from obtp.drawings import svg
class R05(unittest.TestCase):
 def test_buyer_geometry_and_linked_views(self):
  for i,roof,w in itertools.product(range(6),range(3),[580,880,1180]):
   s=build(parameters(i,roof_type=roof,window_width=w));v=s['drawings']['views'];c=v['concept-plan']
   self.assertEqual(c['source_geometry_sha256'],s['geometry_sha256']);self.assertTrue(c['wall_loops'])
   self.assertFalse(any(p['family'] in ['interior','facade','insulation','partitions'] for p in c['polygons']))
   self.assertFalse(any(p['family']=='walls' and not p['id'].startswith('window/') for p in c['polygons']))
   self.assertTrue(any(p['material']=='mineral-wool' for p in v['section-a']['polygons']))
   self.assertEqual(s['window_spec']['frame_width_mm'],w)
   void=next(x for x in s['opening_voids'] if x['id']=='front-window/opening');self.assertEqual(void['size'][0],w+20)
   self.assertEqual(s['window_spec']['frame_height_mm'],1880)
   if roof==2:
    end=s['dimensions']['length_mm']+s['dimensions']['annex_length_mm'];W=s['dimensions']['width_mm']
    for p in s['parts']:
     if p['family']=='roof':
      for x,y,z in vertices(p):self.assertTrue(-84-1e-5<=x<=end+84+1e-5 and -84-1e-5<=y<=W+84+1e-5,p['id'])
    self.assertAlmostEqual(s['metrics']['height_mm'],4480)
   out=svg(c);self.assertIn('fill-rule="evenodd"',out)
 def test_retired_parameters_rejected(self):
  for kw in [dict(terrace_steps=1),dict(window_width=1200),dict(window_width=600)]:
   with self.assertRaises(ValueError):build(parameters(**kw))
 def test_union_hole(self):
  from obtp.plan_styles import union_loops
  loops=union_loops([(0,0,100,10),(0,90,100,100),(0,10,10,90),(90,10,100,90)])
  self.assertEqual(len(loops),2)
  area=sum(sum(p[0]*loop[(i+1)%len(loop)][1]-p[1]*loop[(i+1)%len(loop)][0] for i,p in enumerate(loop))/2 for loop in loops)
  self.assertEqual(area,3600)
if __name__=='__main__':unittest.main()
