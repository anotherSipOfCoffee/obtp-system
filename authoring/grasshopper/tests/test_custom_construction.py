"""Room-boundary construction, model/plan agreement and erection integrity."""
import copy,itertools,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp import sauna_workflow as flow
from obtp.documentation import stage,stage_parts
from obtp.wall_erection import sequence

class CustomConstructionTests(unittest.TestCase):
 def build(self,**kw):
  doc=flow.resolve(flow.select(6,**kw));scene=flow.construct(doc)
  self.assertTrue(all(scene['checks'].values()))
  self.assertEqual(scene['drawings']['source_geometry_sha256'],scene['geometry_sha256'])
  self.assertEqual(len(scene['parts']),len({p['id'] for p in scene['parts']}))
  self.assertTrue(all(min(p['size'])>0 for p in scene['parts']))
  return doc,scene
 def test_frozen_r24_1_presets(self):
  import json,hashlib
  rows=json.loads(Path(__file__).with_name('r24_preset_hashes.json').read_text())
  for row in rows:
   with self.subTest(preset=row['preset'],roof=row['roof']):
    scene=flow.construct(flow.resolve(flow.select(row['preset'],roof_type=row['roof'])))
    self.assertEqual(scene['geometry_sha256'],row['geometry'])
    self.assertEqual(hashlib.sha256(json.dumps(scene['drawings'],sort_keys=True).encode()).hexdigest(),row['drawings'])
 def test_all_supported_room_sets_and_orders(self):
  for flags in itertools.product((False,True),repeat=3):
   if not any(flags[:2]):continue
   args=dict(zip(('sauna','entrance','outdoor'),flags))
   doc=flow.resolve(flow.select(6,**args))
   for index in range(doc['plan']['candidate_count']):
    with self.subTest(flags=flags,arrangement=index):
     d,s=self.build(**args,arrangement=index)
     ids={r['id'].replace('hall','entrance') for r in s['rooms']}
     self.assertEqual(ids,{k for k,v in args.items() if v and k!='outdoor'})
     self.assertEqual(any(p['id'].startswith('heater/') for p in s['parts']),flags[0])
     self.assertEqual(any(p['id'].startswith('bench-') for p in s['parts']),flags[0])
     self.assertEqual(any(p['id'].startswith('shower/') for p in s['parts']),flags[2])
     self.assertEqual(any(p['id'].startswith('sauna-partition/') for p in s['parts']),flags[0] and flags[1])
     if s['config'].get('layout_rooms'):
      for room in d['plan']['finished_room_rectangles']:
       actual=next(r for r in s['rooms'] if r['id']==room['id'])
       self.assertEqual(actual['bounds_mm'],room['bounds_mm'])
 def test_disconnected_is_not_a_hidden_passage(self):
  for relation in (0,1,3):
   d,s=self.build(sauna_entrance=relation)
   self.assertFalse(any(v['id']=='sauna-partition/opening' for v in s['opening_voids']))
   self.assertEqual({v['id'] for v in s['opening_voids'] if v['id'].startswith('entry-')},{'entry-sauna/opening','entry-entrance/opening'})
 def test_settings_and_dimension_changes(self):
  for kw in [dict(entrance=False,sauna_cells=4,depth_cells=2,wall_height=2700,roof_type=0),dict(sauna=False,entrance_cells=2,window_width=580,foundation_type=1),dict(arrangement=1,sauna_cells=4,entrance_cells=4,outdoor_cells=2,include_foundation=False)]:
   self.build(**kw)
 def test_opening_fit_failure_is_explicit(self):
  with self.assertRaisesRegex(ValueError,'Opening and framing'):
   self.build(sauna=False,entrance_cells=2,window_width=1180,outdoor=False)
 def test_structure_and_openings_do_not_clash(self):
  from test_r02 import collide
  for kw in [dict(entrance=False),dict(sauna=False),dict(arrangement=1),dict(sauna_entrance=0),dict(outdoor=False,arrangement=1)]:
   _,scene=self.build(**kw)
   parts=[p for p in scene['parts'] if p['material'] in ('timber','plywood')]
   for a,b in itertools.combinations(parts,2):
    if any(a['origin'][k]+a['size'][k]<=b['origin'][k]+1e-6 or b['origin'][k]+b['size'][k]<=a['origin'][k]+1e-6 for k in range(2)):continue
    self.assertFalse(collide(a,b),(a['id'],b['id']))
   for void in scene['opening_voids']:
    self.assertFalse(any(collide(p,void) for p in parts),void['id'])
   window=next(o for o in scene['modularity']['openings'] if 'window' in o['id'])
   self.assertEqual(window['modeled_installation_gaps_left_right_bottom_top_mm'],[10,10,10,10])
 def test_connected_erection_preserves_source(self):
  _,s=self.build(arrangement=1);original=copy.deepcopy(s['parts'])
  steps=sequence(s,stage,stage_parts)
  self.assertEqual(s['parts'],original)
  self.assertTrue(any('Lay flat' in x['label'] for x in steps))
  self.assertEqual(steps[-1]['label'],'Cladding last')
  self.assertEqual({p['id'] for p in steps[-1]['parts']},{p['id'] for p in s['parts']})
if __name__=='__main__':unittest.main()
