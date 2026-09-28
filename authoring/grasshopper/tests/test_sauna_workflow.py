import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp import sauna_workflow as flow
from obtp.model import build,parameters
class SaunaWorkflowTests(unittest.TestCase):
 def test_six_presets_match_original(self):
  for preset in range(6):
   for roof in (0,1):
    scene=flow.construct(flow.resolve(flow.select(preset,roof_type=roof)))
    original=build(parameters(preset,roof_type=roof))
    self.assertEqual(scene['parts'],original['parts']);self.assertEqual(scene['geometry_sha256'],original['geometry_sha256']);self.assertEqual(scene['drawings'],original['drawings'])
 def test_native_number_values_normalized(self):
  self.assertEqual(flow.select(2),flow.select(2.0,roof_type=1.0,window_width=1180.0,wall_height=2100.0,foundation_type=0.0))
 def test_saved_presets_ignore_custom(self):
  for i in range(6):
   self.assertEqual(flow.select(i),flow.select(i,sauna=False,entrance=False,outdoor=False,sauna_cells=-7,arrangement=99,sauna_entrance=99))
 def test_custom_controls_drive_plan_and_scene(self):
  document=flow.resolve(flow.select(6,sauna_cells=4,entrance_cells=2,outdoor=False))
  self.assertEqual(document['plan']['bounds_mm'][2],5400)
  scene=flow.construct(document);self.assertFalse(any(p['id'].startswith('shower/') for p in scene['parts']))
  self.assertEqual(scene['dimensions']['length_mm'],5400)
 def test_no_fallback_for_unsupported_custom(self):
  doc=flow.resolve(flow.select(6,sauna=False,entrance=False))
  self.assertEqual(doc['status'],'plan-only')
  with self.assertRaisesRegex(ValueError,'Outdoor-only'):flow.construct(doc)
 def test_stale_plan_and_selection_rejected(self):
  doc=flow.resolve(flow.select());doc['plan']['rooms'][0]['bounds_mm'][2]+=900
  with self.assertRaises(ValueError):flow.construct(doc)
  selection=flow.select();selection['arrangement']=1
  with self.assertRaises(ValueError):flow.resolve(selection)
 def test_invalid_settings_rejected(self):
  for args in (dict(preset_index=7),dict(roof_type=2),dict(window_width=900),dict(wall_height=1900),dict(foundation_type=3)):
   with self.assertRaises(ValueError):flow.select(**args)
 def test_no_model_created_before_construction(self):
  from unittest.mock import patch
  with patch('obtp.model.build',side_effect=AssertionError('Early geometry generation')):
   document=flow.resolve(flow.select(3));self.assertNotIn('parts',document)
 def test_main_canvas_has_single_pipeline(self):
  source=(Path(__file__).resolve().parents[1]/'CREATE_GRASSHOPPER.py').read_text()
  for obsolete in ("'model.py'","'comparison.py'","'layout_bridge.py'",'use_layout','program_type'):
   self.assertNotIn(obsolete,source)
if __name__=='__main__':unittest.main()
