"""Exercise real canvas factories against Rhino's minimal creation API."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Params:
    def __init__(self):
        self.Input = [object()]
        self.Output = [object()]
    def UnregisterInputParameter(self, p): self.Input.remove(p)
    def UnregisterOutputParameter(self, p): self.Output.remove(p)
    def RegisterInputParam(self, p): self.Input.append(p)
    def RegisterOutputParam(self, p): self.Output.append(p)

class Component:
    # Deliberately no SetSource: reproduces the reported Rhino 8 API.
    @staticmethod
    def Create(name, code):
        obj = Component()
        obj.name, obj.source, obj.Params = name, code, Params()
        obj.maintained = False
        return obj
    def VariableParameterMaintenance(self): self.maintained = True

class Param:
    def __init__(self, name): self.Name = name
    def CreateAttributes(self): self.attributes_created = True

class FactoryTests(unittest.TestCase):
    def test_creators_need_no_source_setter(self):
        for filename in ('CREATE_GRASSHOPPER.py', 'CREATE_RESEARCH_GRASSHOPPER.py', 'room_canvas.py'):
            with self.subTest(creator=filename):
                tree = ast.parse((ROOT / filename).read_text())
                factory = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'script')
                ns = dict(ROOT=ROOT, Python3Component=Component,
                          ScriptVariableParam=Param, GH_ParamAccess=SimpleNamespace(item='item'),
                          place=lambda obj, x, y: obj)
                exec(compile(ast.Module(body=[factory], type_ignores=[]), filename, 'exec'), ns)
                obj = ns['script']('Preset', 'sauna_preset.py', [('preset_index', int)],
                                   [('workflow_json', 'item'), ('labels', 'list')], 0, 0)
                self.assertEqual(obj.source, (ROOT / 'components/sauna_preset.py').read_text())
                self.assertTrue(obj.maintained)
                self.assertFalse(obj.UsingStandardOutputParam)
                self.assertEqual([p.Name for p in obj.Params.Input], ['preset_index'])
                self.assertEqual([p.Name for p in obj.Params.Output], ['workflow_json', 'labels'])
                self.assertEqual([p.Access for p in obj.Params.Output], ['item', 'list'])
                self.assertTrue(obj.Params.Input[0].Optional)
                self.assertEqual(obj.Params.Input[0].Access, 'item')
                self.assertTrue(all(p.attributes_created for p in obj.Params.Input + obj.Params.Output))

if __name__ == '__main__': unittest.main()
