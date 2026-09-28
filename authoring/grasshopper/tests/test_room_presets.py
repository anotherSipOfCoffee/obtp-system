import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from obtp import room_presets as rp,room_config as rc,room_structure as rs,room_detail as rd
from obtp.room_documents import DEFAULT_RATES,estimate,recipes,cutting_files

class PresetTests(unittest.TestCase):
 def test_all_preset_controls_and_unchanged_inputs(self):
  for t in range(3):
   for size in range(3):
    for ext in (False,True):
     for window in range(2):
      with self.subTest(t=t,size=size,extension=ext,window=window):
       plan=rp.generate(t,size,ext,window);original=copy.deepcopy(plan)
       sk=rs.skeleton(plan);saved=copy.deepcopy(sk)
       scene=rd.build(sk,paneling=2)
       self.assertEqual(plan,original);self.assertEqual(sk,saved)
       self.assertEqual(len(scene['parts']),len({p['id'] for p in scene['parts']}))
       self.assertTrue(all(min(p['size'])>0 for p in scene['parts']))
       self.assertEqual(plan['window_frame_mm'],580 if window==0 else 1180)
 def test_studio_extension_is_a_real_block_and_windows_replace_sliders(self):
  yes=rd.build(rs.skeleton(rp.generate(1,1,True)))
  no=rd.build(rs.skeleton(rp.generate(1,1,False)))
  self.assertEqual(yes['dimensions']['length_mm']-no['dimensions']['length_mm'],1800)
  self.assertTrue(any(p['id'].startswith('studio-slider-') for p in yes['parts']))
  self.assertFalse(any(p['id'].startswith(('studio-slider-','studio-preparation/')) for p in no['parts']))
  for host in ('front-window-product','back-window-product'):
   self.assertTrue(any(p['id'].startswith(host) and p['material']=='glass' for p in no['parts']))
  self.assertTrue(any(p['id'].startswith('hot-end/') and p['material']=='object' for p in no['parts']))
 def test_downstream_does_not_require_preset_source(self):
  custom=rc.solve(rc.rules(rc.rules(rc.programme(0,[7,0])),kind='boundary'),length_cells=7)
  bp=rp.generate(0,1,True);bp=rp.reseal(bp,preset_label='External author')
  with patch.object(rp,'generate',side_effect=AssertionError('Preset source called')):
   for plan in (custom,bp):self.assertTrue(rd.build(rs.skeleton(plan))['parts'])
 def test_replacement_skeleton_members_reach_detail(self):
  sk=rs.skeleton(rp.generate());part=next(p for p in sk['parts'] if '/rafter-' in p['id'])
  part['size'][2]+=5;pid=part['id'];sk.pop('sha256');sk=rc.seal('skeleton',**{k:v for k,v in sk.items() if k not in ('schema','stage')})
  result=rd.build(sk);self.assertEqual(next(p for p in result['parts'] if p['id']==pid)['size'][2],150)
 def test_terrace_roof_foundation_and_panels(self):
  plan=rp.generate(0)
  for roof in (0,1):
   for foundation in (0,1):
    sk=rs.skeleton(plan,roof_type=roof,foundation_type=foundation)
    for terrace in (0,1):
     for panel in (0,1,2):
      sk=rs.skeleton(plan,roof_type=roof,foundation_type=foundation,terrace=bool(terrace))
      result=rd.build(sk,paneling=panel)
      self.assertEqual(any(p['family']=='terrace' for p in result['parts']),bool(terrace))
      self.assertEqual(any(p['material']=='mineral-wool' for p in result['parts']),panel>=1)
 def test_documents_and_dxf_are_reconciled(self):
  scene=rd.build(rs.skeleton(rp.generate()),paneling=2);docs,cost=recipes(scene,DEFAULT_RATES)
  self.assertEqual(len(docs),6);self.assertEqual(sum(r['pieces'] for r in cost['rows']),len(scene['parts']))
  self.assertTrue(cost['unpriced_materials']);self.assertGreater(cost['priced_subtotal_eur'],0)
  with tempfile.TemporaryDirectory() as folder:
   rows=cutting_files(scene,folder)
   self.assertEqual(sum(r['pieces'] for r in rows),sum(p['material']=='plywood' for p in scene['parts']))
   import ezdxf
   for row in rows:
    if row['profile']:
     file=ezdxf.readfile(str(Path(folder)/row['profile']));self.assertEqual(file.units,4)
     entity=list(file.modelspace())[0];self.assertTrue(entity.closed)
     self.assertEqual(len(entity),4)
 def test_bad_contract_and_price_rejected(self):
  plan=rp.generate();plan['wall_runs'][0]['length']=-20
  plan=rp.reseal(plan)
  with self.assertRaises(ValueError):rs.skeleton(plan)
  rates=copy.deepcopy(DEFAULT_RATES);rates['rates']['timber']['eur_m3']=-1
  with self.assertRaises(ValueError):estimate(rd.build(rs.skeleton(rp.generate())),rates)
