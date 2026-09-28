import copy,itertools,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp import layout
from obtp.model import build,parameters

class LayoutTests(unittest.TestCase):
 def test_all_nonempty_programmes(self):
  for flags in itertools.product((False,True),repeat=3):
   if not any(flags):continue
   g=layout.relationships(layout.programme(*flags));p=layout.solve(g)
   self.assertEqual({r['id'] for r in p['rooms']},{k for k,v in zip(layout.ROOM_IDS,flags) if v})
   for index in range(p['candidate_count']):
    alternative=layout.solve(g,index)
    for i,a in enumerate(alternative['rooms']):
     self.assertGreater(min(a['bounds_mm'][2:]),0)
     for b in alternative['rooms'][i+1:]:self.assertFalse(a['bounds_mm'][0]<b['bounds_mm'][0]+b['bounds_mm'][2] and b['bounds_mm'][0]<a['bounds_mm'][0]+a['bounds_mm'][2])
 def test_edges_do_not_delete_rooms(self):
  g=layout.relationships(layout.programme(),0,0,0);p=layout.solve(g)
  self.assertEqual(len(p['rooms']),3);self.assertTrue(p['construction_compatible'])
 def test_adjacent_is_not_passage(self):
  p=layout.solve(layout.relationships(layout.programme(outdoor=False),1,0,0))
  self.assertTrue(p['construction_compatible']);self.assertFalse(any(o['kind']=='passage' for o in p['openings']))
 def test_existing_s_m_l_geometry_exact(self):
  for hall,index in ((2,0),(3,2),(4,4)):
   for outdoor in (False,True):
    for roof in (0,1):
     plan=layout.solve(layout.relationships(layout.programme(outdoor=outdoor,entrance_cells=hall)))
     old=build(parameters(index+int(outdoor),roof_type=roof))
     scene=layout.build_from_plan(plan,old['config'])
     if outdoor:
      self.assertEqual(scene['geometry_sha256'],old['geometry_sha256']);self.assertEqual(scene['config'],old['config']);self.assertEqual(scene['parts'],old['parts']);self.assertEqual(scene['drawings'],old['drawings'])
     else:
      self.assertEqual(scene['parts'],[part for part in old['parts'] if not part['id'].startswith('shower/')])
      self.assertEqual(len(scene['parts']),len(old['parts'])-3)
      self.assertEqual(scene['wall_regions'],old['wall_regions']);self.assertEqual(scene['opening_voids'],old['opening_voids'])
 def test_custom_dimensions_feed_structure(self):
  p=layout.solve(layout.relationships(layout.programme(sauna_cells=4,entrance_cells=2,outdoor_cells=2,depth_cells=3)))
  s=layout.build_from_plan(p);self.assertEqual(s['dimensions']['length_mm'],5400);self.assertEqual(s['dimensions']['width_mm'],3600);self.assertEqual(s['dimensions']['annex_length_mm'],1800)
 def test_reject_stale_and_unsupported(self):
  p=layout.solve(layout.relationships(layout.programme()));p['rooms'][0]['bounds_mm'][2]+=900
  with self.assertRaises(ValueError):layout.build_from_plan(p)
  p=layout.solve(layout.relationships(layout.programme(sauna=False,entrance=False)))
  with self.assertRaisesRegex(ValueError,'Outdoor-only'):layout.build_from_plan(p)
 def test_conflicting_graph_and_bad_parameters(self):
  with self.assertRaises(ValueError):layout.programme(False,False,False)
  with self.assertRaises(ValueError):layout.programme(sauna_cells=2)
  with self.assertRaises(ValueError):layout.relationships(layout.programme(),2,2,0)
  with self.assertRaises(ValueError):layout.solve(layout.relationships(layout.programme(),1,1,1))
  with self.assertRaises(ValueError):layout.solve(layout.relationships(layout.programme(outdoor=False)),5)
 def test_immutable_and_repeatable(self):
  graph=layout.relationships(layout.programme());before=json.dumps(graph,sort_keys=True)
  a=layout.solve(graph);b=layout.solve(graph);self.assertEqual(a,b);layout.build_from_plan(a)
  self.assertEqual(before,json.dumps(graph,sort_keys=True))
  self.assertEqual(a,b)
if __name__=='__main__':unittest.main()
