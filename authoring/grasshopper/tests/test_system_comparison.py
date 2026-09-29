import copy,json,math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp import plate_ribs,system_comparison
from obtp.model import build,parameters
from obtp.export import brep

def overlap(a,b):return all(min(a['origin'][k]+a['size'][k],b['origin'][k]+b['size'][k])-max(a['origin'][k],b['origin'][k])>1e-6 for k in range(3))
class ComparisonTests(unittest.TestCase):
 def test_B_parameter_corners_and_clashes(self):
  for n,p,s,h,t,d in [(1,600,2400,2100,27,180),(4,900,3600,2100,45,240),(8,1200,4800,2700,63,360)]:
   scene=plate_ribs.build(n,p,s,h,t,d);parts=scene['parts']
   self.assertEqual(len({a['id'] for a in parts}),len(parts))
   self.assertEqual(len(scene['joints']),4*(n+1))
   for i,a in enumerate(parts):
    self.assertGreater(min(a['size']),0)
    for b in parts[i+1:]:self.assertFalse(overlap(a,b),(a['id'],b['id']))
   self.assertEqual(scene['manufacturing']['physical_pieces'],len(parts))
   self.assertIsNone(scene['metrics']['fastener_quantity'])
 def test_insulation_volume_conservation(self):
  box=([0,0,0],[10,10,10]);cut=dict(origin=[2,3,4],size=[4,4,4]);out=plate_ribs.subtract(box,cut)
  self.assertAlmostEqual(sum(math.prod(s) for o,s in out),936)
 def test_adjacent_insulation_blanks_merge_without_volume_loss(self):
  boxes=[([0,0,0],[2,4,5]),([2,0,0],[3,4,5])]
  self.assertEqual(plate_ribs.merge_boxes(boxes),[([0,0,0],[5,4,5])])
  self.assertEqual(len(plate_ribs.merge_boxes([([0,0,0],[2,4,5]),([2,0,0],[3,3,5])])),2)
 def test_zero_area_display_faces_leave_source_unchanged(self):
  v=[[0,0,0],[0,0,0],[1,0,0],[0,1,0]];faces=[[0,1,2],[0,2,3]]
  self.assertEqual(system_comparison.display_faces(v,faces),[[0,2,3]])
  self.assertEqual(len(faces),2)
 def test_B_portable_solids(self):
  import rhino3dm
  for p in plate_ribs.build()['parts']:
   solid=brep(p,rhino3dm);self.assertTrue(solid.IsValid);self.assertTrue(solid.IsSolid)
 def test_B_visibility_does_not_change_source_counts(self):
  full=system_comparison.preview(insulation=True);hidden=system_comparison.preview(panels=False,insulation=False,core=True,layer=1)
  self.assertEqual(full['source']['geometry_sha256'],hidden['source']['geometry_sha256'])
  self.assertEqual(full['schedule'],hidden['schedule']);self.assertGreater(len(full['meshes']),len(hidden['meshes']))
 def test_cassette_is_unchanged_studio_source(self):
  scene=build(parameters(3,program_type=1,roof_type=0,studio_winter_closed=False));before=json.dumps(scene,sort_keys=True)
  p=system_comparison.preview(1,scene,insulation=True);self.assertEqual(p['source']['geometry_sha256'],scene['geometry_sha256'])
  self.assertEqual(len(p['meshes']),len(scene['parts']));self.assertEqual(before,json.dumps(scene,sort_keys=True))
  self.assertTrue(system_comparison.preview(1,scene,mode=2)['meshes'])
 def test_wikihouse_source_transform_and_modes(self):
  source=system_comparison.source();before=json.dumps(source,sort_keys=True)
  p=system_comparison.preview(0,mode=1,object_index=0,offset=(0,0,0))
  model=next(m for m in source['models'] if m['id']=='W-S')
  self.assertEqual(p['meshes'][0]['vertices'],model['assets'][0]['vertices'])
  for mode in (0,1,2):self.assertTrue(system_comparison.preview(0,mode=mode)['meshes'])
  self.assertEqual(before,json.dumps(source,sort_keys=True))
 def test_B_joint_context_and_repeatability(self):
  a=plate_ribs.build();b=plate_ribs.build();self.assertEqual(a['geometry_sha256'],b['geometry_sha256'])
  p=system_comparison.preview(2,mode=2);self.assertEqual(len(p['meshes']),4)
 def test_reject_bad_inputs(self):
  for kw in [dict(bays=0),dict(pitch=700),dict(span=100),dict(thickness=-1),dict(height=float('nan'))]:
   with self.assertRaises(ValueError):plate_ribs.build(**kw)
  with self.assertRaises(ValueError):system_comparison.preview(9)
  with self.assertRaises(ValueError):system_comparison.preview(0,mode=1,object_index=999)
if __name__=='__main__':unittest.main()
