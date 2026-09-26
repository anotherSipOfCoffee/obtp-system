import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.object_library import definition,door_recipe,plan_symbols
from obtp.export import file3dm

class LinkedObjects(unittest.TestCase):
 def test_slots_symbols_and_roundtrip(self):
  for program in range(2):
   for preset in range(6):
    scene=build(parameters(preset,program_type=program));lib=scene['object_library']
    ids={p['id'] for p in scene['parts']};claimed=[]
    for item in lib['instances']:
     self.assertTrue(set(item['part_ids'])<=ids);claimed.extend(item['part_ids'])
    self.assertEqual(len(claimed),len(set(claimed)))
    symbols=plan_symbols(lib)
    self.assertEqual(len(symbols),len([o for o in scene['opening_voids'] if 'window' not in o['id']]))
    self.assertEqual(scene['drawings']['views']['plan']['object_library_sha256'],lib['sha256'])
    self.assertEqual(lib,build(parameters(preset,program_type=program))['object_library'])
 def test_dimensions_and_fail_closed(self):
  a=build(parameters(custom=True,door_width=800));b=build(parameters(custom=True,door_width=900))
  self.assertNotEqual(a['object_library']['sha256'],b['object_library']['sha256'])
  self.assertNotEqual(plan_symbols(a['object_library']),plan_symbols(b['object_library']))
  with self.assertRaises(ValueError):definition('unknown')
  with self.assertRaises(ValueError):definition('obtp.door.study',99)
  with self.assertRaises(ValueError):door_recipe(float('nan'),1900,195)
  bad=json.loads(json.dumps(a['object_library']));bad['symbol_source_sha256']='stale'
  with self.assertRaises(ValueError):plan_symbols(bad)
 def test_3dm_identity(self):
  import rhino3dm
  scene=build(parameters())
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/'linked.3dm';file3dm([scene],path)
   doc=rhino3dm.File3dm.Read(str(path))
   leaves=[o for o in doc.Objects if o.Attributes.Name.endswith('/door-leaf')]
   self.assertTrue(leaves)
   for o in leaves:self.assertEqual(o.Attributes.GetUserString('obtp_object_definition'),'obtp.door.study')
if __name__=='__main__':unittest.main()
