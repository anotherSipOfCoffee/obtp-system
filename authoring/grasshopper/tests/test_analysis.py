import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.analysis import prepare,inputs,validate_result_identity
class Analysis(unittest.TestCase):
 def test_all_six_preserve_source_identity_and_null_results(self):
  for i in range(6):
   s=build(parameters(i));a=prepare(s)
   self.assertEqual({p['id'] for p in s['parts']},{p['id'] for p in a['solids']})
   self.assertTrue(all(w['status'] in ('not_run','paused_by_owner') and w['results'] is None for w in a['workflows'].values()))
   self.assertTrue(all(p['source_id'] in {q['id'] for q in s['parts']} for v in a['sections'].values() for p in v['polygons']))
   self.assertEqual(a['solids'][0]['size_m'],[x/1000 for x in s['parts'][0]['size']])
 def test_stale_joint_and_boundary_inputs_invalidate(self):
  s=build(parameters(2));a=prepare(s);t=copy.deepcopy(s)
  t['interfaces'][0]['capacity']=1
  self.assertNotEqual(a['source_sha256'],prepare(t)['source_sha256'])
  cfg=inputs();cfg['thermal']['design_external_temperature_C']=-20
  b=prepare(s,cfg);self.assertNotEqual(a['inputs_sha256'],b['inputs_sha256'])
  receipt=dict(source_sha256=a['source_sha256'],inputs_sha256=a['inputs_sha256'],status='executed_unverified')
  with self.assertRaises(ValueError):validate_result_identity(a,receipt)
  receipt.update(status='completed',solver='TEST ONLY',version='test',input_file_sha256='a',output_file_sha256='b',checks={'equilibrium':True})
  self.assertTrue(validate_result_identity(a,receipt))
  with self.assertRaises(ValueError):validate_result_identity(b,receipt)
 def test_duplicate_and_invalid_geometry_rejected(self):
  s=build(parameters());s['parts'].append(copy.deepcopy(s['parts'][0]))
  with self.assertRaises(ValueError):prepare(s)
  s=build(parameters());s['parts'][0]['size'][0]=0
  with self.assertRaises(ValueError):prepare(s)
if __name__=='__main__':unittest.main()
