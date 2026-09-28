import copy,json,sys,unittest,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp import room_config as r,room_structure as s,room_detail as d,checkpoints
from obtp.manufacturing import cladding

class RoomConfigTests(unittest.TestCase):
 def plan(self,t=0,fs=(7,0,2),adj=(),boundary=(),**kw):return r.solve(r.rules(r.rules(r.programme(t,fs),adj),boundary,'boundary'),**kw)
 def test_duplicates_and_six_limit(self):
  p=self.plan(2,[17,17,0],length_cells=10);self.assertEqual(len({a['id'] for a in p['rooms']}),3)
  self.assertNotEqual(p['rooms'][0]['label'],p['rooms'][1]['label'])
  self.assertEqual(len(self.plan(0,[0,1,4,5,6,13],length_cells=14)['rooms']),6)
  with self.assertRaises(ValueError):r.programme(0,[0]*7)
  with self.assertRaises(ValueError):r.programme(0,[])
 def test_adjacency_and_impossible_cycle(self):
  p=self.plan(adj=['R01 R03 must','R01 R02 cannot']);order=[a['id'] for a in p['rooms']]
  self.assertEqual(abs(order.index('R01')-order.index('R03')),1);self.assertNotEqual(abs(order.index('R01')-order.index('R02')),1)
  with self.assertRaisesRegex(ValueError,'No single-row'):self.plan(adj=['R01 R02 must','R02 R03 must','R01 R03 must'])
  with self.assertRaises(ValueError):self.plan(adj=['R01 R04 must'])
 def test_open_and_closed_boundaries(self):
  p=self.plan(boundary=['R01 R02 open']);sk=s.skeleton(p)
  self.assertFalse(any(x['id']=='partition-R01-R02' for x in sk['runs']))
  p=self.plan(fs=[0,9],boundary=['R01 R02 partition'],length_cells=6)
  self.assertEqual(len(p['entries']),2);sk=s.skeleton(p)
  self.assertFalse(next(x for x in sk['runs'] if not x['external']).get('door_width'))
 def test_grid_bounds_and_typed_values(self):
  for kw in (dict(length_cells=3),dict(length_cells=8.5),dict(width_cells=4),dict(arrangement=99)):
   with self.assertRaises(ValueError):self.plan(**kw)
  for ny in (2,3):
   p=self.plan(width_cells=ny);self.assertEqual(p['bounds_mm'][3],ny*1200)
   self.assertEqual(sum(x['bounds_mm'][2] for x in p['rooms']),p['bounds_mm'][2])
 def test_plan_fit_before_geometry(self):
  with patch('obtp.model.prepare',side_effect=AssertionError('No early structure')):self.plan()
  with self.assertRaisesRegex(ValueError,'opening and jambs'):self.plan(fs=[0,2],length_cells=3,boundary=['R01 R02 partition'])
 def test_summer_passage_two_double_doors(self):
  p=self.plan(1,[10,1,12],length_cells=10,summer_passage=True);sk=s.skeleton(p);scene=d.build(sk)
  products=[x for x in scene['detail']['products'] if x['leaf_count']==2]
  self.assertTrue(all(p['summer_passage'] not in (order[0],order[-1]) for order in p['candidate_orders']))
  with self.assertRaisesRegex(ValueError,'at least three'):self.plan(1,[1,10],summer_passage=True)
  self.assertEqual(len(products),2);self.assertTrue(all(x['rough_opening_mm']==[1800,1900] for x in products))
  for t in (0,2):
   with self.assertRaisesRegex(ValueError,'Studio-only'):self.plan(t,summer_passage=True)
 def test_plan_is_sole_geometry_source(self):
  with patch('obtp.model.build',side_effect=AssertionError('Hidden preset')),patch('obtp.model.arrange',side_effect=AssertionError('Programme recipe')):
   a=s.skeleton(self.plan());b=s.skeleton(self.plan(length_cells=10))
  self.assertNotEqual(a['parts'],b['parts']);self.assertEqual(a['dimensions']['length_mm'],7200)
  self.assertEqual({x['material'] for x in a['parts']},{'timber','concrete-study'})
  self.assertTrue(a['panel_parts'])
  slope=s.skeleton(self.plan(),roof_type=1)
  self.assertNotEqual([v for v in a['parts'] if v['id'].startswith('weather')],[v for v in slope['parts'] if v['id'].startswith('weather')])
 def test_u_terrace_contains_entrance_and_no_overlap(self):
  for side in range(4):
   p=self.plan(entrance_side=side);rects=d.terrace_rects(p,4,1)
   self.assertEqual(len(rects),3);self.assertTrue({'front','back',p['entrance_side']}<={x[0] for x in rects})
   for i,(_,a) in enumerate(rects):
    for _,b in rects[i+1:]:self.assertFalse(d.overlaps(a,b))
 def test_detail_quantities_and_no_mutation(self):
  sk=s.skeleton(self.plan());before=copy.deepcopy(sk);a=d.build(sk,terrace=4,outdoor_shower=True,outdoor_bench=True);b=d.build(sk,facade=False)
  self.assertEqual(sk,before);self.assertFalse(any(cladding(x) for x in b['parts']))
  q=a['manufacturing'];self.assertEqual(q['physical_pieces']+q['cladding']['physical_pieces'],len(a['parts']))
  self.assertEqual(len(a['detail']['features']),2)
  for x in a['parts']:
   if x['id'].startswith('deck-') and '/board-' in x['id']:
    self.assertGreater(x['size'][0],x['size'][1]);self.assertLessEqual(x['size'][0],1800)
  self.assertEqual(len(checkpoints.assembly(a,100)['parts']),len(a['parts']))
  self.assertFalse(checkpoints.assembly(a,0)['parts'])
  with self.assertRaises(ValueError):d.build(sk,terrace=0,outdoor_shower=True)
 def test_remaining_detail_controls(self):
  for mode in range(5):
   sk=s.skeleton(self.plan(),roof_type=mode%2,foundation_type=mode%2)
   scene=d.build(sk,terrace=mode,paneling=mode%3,facade=bool(mode%2))
   self.assertTrue(all(min(v['size'])>0 for v in scene['parts']))
   self.assertTrue(scene['detail']['foundation_nodes'])
   self.assertEqual(len(scene['detail']['terraces']),[0,1,2,2,3][mode])
 def test_stale_and_inactive_type_features(self):
  p=self.plan();p['bounds_mm'][2]+=900
  with self.assertRaises(ValueError):s.skeleton(p)
  sk=s.skeleton(self.plan(1))
  with self.assertRaisesRegex(ValueError,'Sauna-only'):d.build(sk,outdoor_bench=True)
 def test_portable_export(self):
  from obtp.export import export_one
  import rhino3dm
  sc=d.build(s.skeleton(self.plan(2,[16,6],length_cells=7)),paneling=2)
  with tempfile.TemporaryDirectory() as folder:
   export_one(sc,folder);doc=rhino3dm.File3dm.Read(str(Path(folder)/(sc['config']['id']+'.3dm')))
   self.assertEqual(len(doc.Objects),len(sc['parts']));self.assertTrue(all(obj.Geometry.IsSolid for obj in doc.Objects))

class RoomHostTests(unittest.TestCase):
 def test_actual_stage_wrappers_and_clear(self):
  import types
  root=Path(__file__).resolve().parents[1];messages=[]
  class Goo:
   def __init__(self,v):self.Value=v
  env=types.SimpleNamespace(Component=types.SimpleNamespace(OnPingDocument=lambda:types.SimpleNamespace(FilePath=str(root/'R28.gh')),AddRuntimeMessage=lambda *x:messages.append(x)))
  gh=types.SimpleNamespace(Kernel=types.SimpleNamespace(GH_RuntimeMessageLevel=types.SimpleNamespace(Error='error')))
  code=(root/'components/config_stage.py').read_text()
  def run(stage,**args):
   ns=dict(ghenv=env,**args)
   with patch.dict(sys.modules,{'Grasshopper':gh}):exec(code.replace("STAGE='programme'",'STAGE='+repr(stage)),ns)
   return ns
  room=run('programme',building_type=Goo(1.0),functions=[Goo(10.0),Goo(1.0),Goo(12.0)])
  adj=run('adjacency',upstream=Goo(room['data_json']),rules=[Goo('R01 R02 must')])
  edges=run('boundaries',upstream=Goo(adj['data_json']),rules=[])
  plan=run('plan',upstream=Goo(edges['data_json']),length_cells=Goo(10.0),summer_passage=Goo(True))
  frame=run('skeleton',upstream=Goo(plan['data_json']));detail=run('detail',upstream=Goo(frame['data_json']))
  self.assertFalse(messages);self.assertTrue(json.loads(detail['data_json'])['parts'])
  bad=run('plan',upstream=Goo(edges['data_json']),length_cells=Goo(3.0));self.assertIsNone(bad['data_json']);self.assertTrue(messages)
  bad=run('skeleton',upstream=None,data_json='old');self.assertIsNone(bad['data_json'])
