import copy,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp import sauna_workflow as flow,checkpoints as cp
from obtp.model import build
from obtp.manufacturing import cladding

class CheckpointsTests(unittest.TestCase):
 def test_studio_saved_models_and_plan(self):
  for index in range(7,13):
   for roof in (0,1):
    selection=flow.select(index,roof_type=roof)
    with patch('obtp.model.build',side_effect=AssertionError('Early geometry')):document=flow.resolve(selection)
    scene=flow.construct(document);original=build(flow.studio_config(selection))
    self.assertEqual(scene['parts'],original['parts']);self.assertEqual(scene['drawings'],original['drawings'])
    self.assertEqual(scene['geometry_sha256'],original['geometry_sha256'])
    actual={o['id']:o for o in scene['opening_voids']}
    for opening in document['plan']['openings']:
     axis=0 if opening['axis']=='x' else 1
     match=actual[opening['id']]
     self.assertEqual(opening['origin_mm'][axis],match['origin'][axis])
     self.assertEqual(opening['width_mm'],match['size'][axis])
    self.assertEqual(selection,flow.select(index,roof_type=roof,sauna=False,arrangement=99,sauna_cells=-1))
 def test_display_contract_and_no_mutation(self):
  for index in (3,10):
   scene=flow.construct(flow.resolve(flow.select(index)));before=copy.deepcopy(scene)
   full=cp.assembly(scene,100);empty=cp.assembly(scene,0)
   self.assertEqual(len(full['parts']),len(scene['parts']));self.assertFalse(empty['parts']);self.assertTrue(full['steps'])
   views=[cp.view(full,float(i),True) for i in range(3)]
   self.assertTrue(all(not cladding(p) for p in views[1]['parts']))
   self.assertTrue(any(cladding(p) for p in views[2]['parts']))
   self.assertTrue(any(p['material']=='plywood' for p in views[0]['parts']))
   ids=[set(p['id'] for p in v['parts']) for v in views];self.assertTrue(ids[0]<=ids[1]<=ids[2])
   colors={p['id']:c for p,c in zip(views[2]['parts'],views[2]['rgba'])}
   for progress in (25,50,75):
    v=cp.view(cp.assembly(scene,progress),0,True)
    self.assertTrue(all(colors[p['id']]==c for p,c in zip(v['parts'],v['rgba'])))
   aid=full['assembly_ids'][0];v=cp.view(full,2,False,aid)
   self.assertTrue(v['parts']);self.assertTrue(all(p['assembly']==aid for p in v['parts']))
   with self.assertRaisesRegex(ValueError,'Unknown assembly'):cp.view(full,assembly_filter='BAD')
   self.assertTrue(cp.inspect(scene)['assembly_ids']);self.assertEqual(scene,before)
if __name__=='__main__':unittest.main()

class HostCheckpointTests(unittest.TestCase):
 def test_new_components_and_error_clear(self):
  import json,types,hashlib
  root=Path(__file__).resolve().parents[1];messages=[]
  gh=types.SimpleNamespace(Kernel=types.SimpleNamespace(GH_RuntimeMessageLevel=types.SimpleNamespace(Error='error')))
  env=types.SimpleNamespace(Component=types.SimpleNamespace(OnPingDocument=lambda:types.SimpleNamespace(FilePath=str(root/'r26.gh')),AddRuntimeMessage=lambda *a:messages.append(a)))
  scene=flow.construct(flow.resolve(flow.select(10)))
  ns=dict(ghenv=env,scene_json=json.dumps(scene),assembly_stage=50.0)
  package='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
  def preview(data,*args):
   self.assertIn('dimensions',data);self.assertEqual(data['geometry_sha256'],scene['geometry_sha256'])
   return [object() for p in data['parts']],[p['id'] for p in data['parts']]
  mocks={'Grasshopper':gh,'System.Drawing':types.SimpleNamespace(Color=types.SimpleNamespace(FromArgb=lambda *a:a)), 'Rhino':types.SimpleNamespace(Display=types.SimpleNamespace(DisplayMaterial=lambda *a:a)), 'Grasshopper.Kernel.Types':types.SimpleNamespace(GH_Material=lambda x:x), package+'.rhino_adapter':types.SimpleNamespace(preview=preview)}
  with patch.dict(sys.modules,mocks):
   exec((root/'components/assembly_checkpoint.py').read_text(),ns)
   self.assertTrue(ns['display_json']);self.assertTrue(ns['steps'])
   ns.update(preview_scope=2.0,type_colours=True,assembly_filter='')
   exec((root/'components/final_preview.py').read_text(),ns)
   self.assertTrue(ns['geometry']);self.assertEqual(len(ns['geometry']),len(ns['materials']));self.assertFalse(messages)
   ns['display_json']=None
   exec((root/'components/final_preview.py').read_text(),ns)
   self.assertFalse(ns['geometry']);self.assertTrue(messages)
