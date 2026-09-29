"""R27 contract, variant, stage ownership and research regressions."""
import copy,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp import sauna_workflow as flow,plan_pipeline as pipe,model,research_specimens as research

class PlanPipelineTests(unittest.TestCase):
 def document(self,index=2,**kw):return flow.resolve(flow.select(index,**kw))
 def test_saved_geometry_baseline(self):
  import hashlib
  from obtp.manufacturing import analyse
  for row in json.loads(Path(__file__).with_name('r26_baseline.json').read_text()):
   with self.subTest(preset=row['preset'],roof=row['roof']):
    scene=flow.construct(self.document(row['preset'],roof_type=row['roof']));q=analyse(scene,True)
    self.assertEqual(scene['geometry_sha256'],row['geometry'])
    self.assertEqual(hashlib.sha256(json.dumps(scene['drawings'],sort_keys=True).encode()).hexdigest(),row['drawings'])
    self.assertEqual(q['physical_pieces'],row['primary']);self.assertEqual(q['cladding']['physical_pieces'],row['cladding'])
    self.assertEqual(q['unique_manufactured_part_candidates'],row['types'])
 def test_branch_ownership_no_complete_build(self):
  with patch.object(model,'build',side_effect=AssertionError('Hidden complete building')):
   s=pipe.structure(self.document());floor=pipe.generate(s,'floor');roof=pipe.generate(s,'roof');walls=pipe.generate(s,'walls')
  self.assertEqual({p['family'] for p in floor['result']['parts']},{'floor'})
  self.assertEqual({p['family'] for p in roof['result']['parts']},{'roof'})
  self.assertFalse(any(p['family'] in ('floor','roof') for p in walls['result']['parts']))
  frame=pipe.merge(s,floor,roof,walls);before=copy.deepcopy(frame)
  surf=pipe.enrich(s,frame,'surfaces');self.assertEqual(frame,before)
  self.assertGreater(len(surf['state']['parts']),len(frame['state']['parts']))
  self.assertFalse(any(p['id'].startswith('weather-roof') for p in surf['state']['parts']))
 def test_mixed_stage_and_mutation_rejected(self):
  a=pipe.structure(self.document(2));b=pipe.structure(self.document(3))
  with self.assertRaisesRegex(ValueError,'different plan'):pipe.merge(a,pipe.generate(b,'floor'),pipe.generate(a,'roof'),pipe.generate(a,'walls'))
  a['context']['W']=999
  with self.assertRaisesRegex(ValueError,'stale'):pipe.generate(a,'walls')
  with self.assertRaisesRegex(ValueError,'missing'):pipe.generate(None,'walls')
 def test_studio_shared_custom_and_reset(self):
  for base in range(6):
   saved=flow.construct(self.document(base+7));custom=flow.construct(self.document(13,base_preset=base,use_overrides=False,work_cells=-9))
   self.assertEqual(saved['parts'],custom['parts'])
  a=flow.construct(self.document(13,base_preset=2,use_overrides=True,work_cells=3,centre_cells=2,preparation_cells=2))
  b=flow.construct(self.document(13,base_preset=2,use_overrides=True,work_cells=5,centre_cells=3,preparation_cells=3))
  self.assertEqual(a['dimensions']['length_mm'],6300);self.assertEqual(b['dimensions']['length_mm'],9900)
  self.assertNotEqual(a['geometry_sha256'],b['geometry_sha256'])
  self.assertTrue(all(x.get('capacity') is None for x in b['interfaces']))
 def test_typed_boundaries_and_increments(self):
  for kw in [dict(work_cells=2),dict(work_cells=6),dict(work_cells=4.5),dict(centre_cells=4),dict(preparation_cells=1),dict(work_cells=float('nan'))]:
   with self.subTest(kw=kw),self.assertRaises(ValueError):self.document(13,base_preset=2,use_overrides=True,**kw)
  for kw in [dict(sauna_cells=2),dict(sauna_cells=9),dict(entrance_cells=1),dict(outdoor_cells=5),dict(depth_cells=1),dict(depth_cells=5),dict(sauna_cells=3.5),dict(window_shift=2)]:
   with self.subTest(kw=kw),self.assertRaises(ValueError):self.document(6,**kw)
  with self.assertRaises(ValueError):self.document(2.5)
 def test_dependent_limits(self):
  with self.assertRaisesRegex(ValueError,'near selected preset'):flow.construct(self.document(6,sauna_cells=8,entrance_cells=8,depth_cells=4,outdoor_cells=4))
  with self.assertRaisesRegex(ValueError,'Available arrangement'):self.document(6,arrangement=5)
  with self.assertRaisesRegex(ValueError,'Outdoor zone'):self.document(6,outdoor=True,entrance_outdoor=2)
 def test_sauna_reset_and_retained_custom(self):
  for base in (0,3,5):
   a=flow.construct(self.document(6,base_preset=base,use_overrides=False,sauna_cells=99));b=flow.construct(self.document(base))
   # Custom outdoor-off intentionally has no legacy external shower.
   self.assertEqual([p for p in a['parts'] if not p['id'].startswith('shower/')],[p for p in b['parts'] if not p['id'].startswith('shower/')])
  for kw in [dict(entrance=False),dict(arrangement=1),dict(sauna_entrance=0),dict(entrance=False,sauna_cells=4,depth_cells=2)]:
   s=flow.construct(self.document(6,**kw));self.assertTrue(s['parts'])
 def test_window_positions(self):
  a=flow.construct(self.document(13,base_preset=4,use_overrides=False,window_width=580))
  b=flow.construct(self.document(13,base_preset=4,use_overrides=False,window_width=580,window_shift=1))
  oa=next(o for o in a['opening_voids'] if o['id']=='front-window/opening');ob=next(o for o in b['opening_voids'] if o['id']=='front-window/opening')
  self.assertNotEqual(oa['origin'],ob['origin']);self.assertEqual(oa['size'],ob['size'])
  actual=next(o for o in b['resolved_plan']['opening_hosts'] if o['id']=='front-window/opening')
  self.assertEqual(actual['origin_mm'],ob['origin'][:2] if ob['origin'][1]==0 else [ob['origin'][0],0])
 def test_research_has_no_programme(self):
  for kind in range(6):
   scene=research.cassette(kind)
   self.assertTrue(scene['parts']);self.assertFalse(any(p['family']=='furniture' for p in scene['parts']))
   self.assertNotIn('rooms',scene)
  with self.assertRaises(ValueError):research.cassette(span=3000)
  with self.assertRaises(ValueError):research.cassette(sheet=15)
 def test_invalid_component_clears_output(self):
  import types
  messages=[];root=Path(__file__).resolve().parents[1]
  env=types.SimpleNamespace(Component=types.SimpleNamespace(OnPingDocument=lambda:types.SimpleNamespace(FilePath=str(root/'R27.gh')),AddRuntimeMessage=lambda *x:messages.append(x)))
  gh=types.SimpleNamespace(Kernel=types.SimpleNamespace(GH_RuntimeMessageLevel=types.SimpleNamespace(Error='error')))
  ns=dict(ghenv=env,plan_json=None,data_json='stale',details=['stale'])
  with patch.dict(sys.modules,{'Grasshopper':gh}):exec((root/'components/construction_stage.py').read_text(),ns)
  self.assertIsNone(ns['data_json']);self.assertFalse(ns['details']);self.assertTrue(messages)
if __name__=='__main__':unittest.main()
