"""Execute the actual host model script using only inputs present on its canvas."""
import ast,json,sys,types,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from obtp.model import parameters

class HostInputTests(unittest.TestCase):
 def test_generated_canvas_inputs_execute_model(self):
  tree=ast.parse((ROOT/'CREATE_RESEARCH_GRASSHOPPER.py').read_text())
  keys=set()
  for node in ast.walk(tree):
   if isinstance(node,ast.Assign):
    for target in node.targets:
     if isinstance(target,ast.Name) and target.id=='controls':keys.update(ast.literal_eval(k) for k in node.value.keys)
     if isinstance(target,ast.Name) and target.id=='values':keys.update(row[0] for row in ast.literal_eval(node.value))
     if isinstance(target,ast.Subscript) and isinstance(target.value,ast.Name) and target.value.id=='controls' and isinstance(target.slice,ast.Constant):keys.add(target.slice.value)
  self.assertNotIn('terrace_steps',keys);self.assertNotIn('facade_type',keys)
  class Goo:
   def __init__(self,value):self.Value=value
  for program in (0,1):
   for custom in (False,True):
    with self.subTest(program=program,custom=custom):
     p=parameters(2,program_type=program);p.update(preset_index=2,custom=custom)
     ns={k:Goo(p[k]) for k in keys};messages=[]
     component=types.SimpleNamespace(OnPingDocument=lambda:types.SimpleNamespace(FilePath=str(ROOT/'test.gh')),AddRuntimeMessage=lambda *a:messages.append(a))
     ns['ghenv']=types.SimpleNamespace(Component=component)
     gh=types.SimpleNamespace(Kernel=types.SimpleNamespace(GH_RuntimeMessageLevel=types.SimpleNamespace(Error='error')))
     with patch.dict(sys.modules,{'Grasshopper':gh}):exec(compile((ROOT/'components/model.py').read_text(),'components/model.py','exec'),ns)
     self.assertEqual(messages,[],ns['report']);self.assertIsNotNone(ns['scene_json'],ns['report'])
     scene=json.loads(ns['scene_json']);self.assertEqual(scene['config']['terrace_steps'],2);self.assertEqual(scene['config']['facade_type'],0)
     self.assertTrue(scene['parts']);self.assertTrue(all(scene['checks'].values()))

 def test_sequential_sauna_host_inputs(self):
  from obtp.sauna_workflow import resolve
  class Goo:
   def __init__(self,value):self.Value=value
  gh=types.SimpleNamespace(Kernel=types.SimpleNamespace(GH_RuntimeMessageLevel=types.SimpleNamespace(Error='error')))
  for index in range(7):
   messages=[]
   component=types.SimpleNamespace(OnPingDocument=lambda:types.SimpleNamespace(FilePath=str(ROOT/'test-r24.gh')),AddRuntimeMessage=lambda *a:messages.append(a))
   ns={'preset_index':Goo(index),'roof_type':Goo(0.0),'wall_height':Goo(2100.0),'ghenv':types.SimpleNamespace(Component=component)}
   with patch.dict(sys.modules,{'Grasshopper':gh}):
    exec(compile((ROOT/'components/sauna_preset.py').read_text(),'sauna_preset.py','exec'),ns)
    self.assertIsNotNone(ns['workflow_json'],ns['report'])
    plan=resolve(json.loads(ns['workflow_json']))
    target={'plan_json':Goo(json.dumps(plan)),'ghenv':ns['ghenv']}
    exec(compile((ROOT/'components/sauna_cassette.py').read_text(),'sauna_cassette.py','exec'),target)
    self.assertEqual(messages,[],target['report']);self.assertIsNotNone(target['scene_json'],target['report'])
    self.assertEqual(json.loads(target['scene_json'])['config']['program_type'],0)
