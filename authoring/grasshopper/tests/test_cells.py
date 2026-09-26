"""New default: catalogue geometry, true repeated lattice and export contracts."""
import itertools,math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters,legacy_parameters
from obtp.cells import opening
from test_r02 import collide


class CellSystemTests(unittest.TestCase):
    def test_full_catalogue(self):
        checked=0
        for program,i,roof,window,winter,foundation in itertools.product(range(2),range(6),range(2),(580,880,1180),(True,False),range(2)):
            if not program and not winter:continue
            s=build(parameters(i,program_type=program,roof_type=roof,window_width=window,studio_winter_closed=winter,foundation_type=foundation))
            self.assertTrue(all(s['checks'].values()))
            self.assertEqual(s['cell_spec']['cell_mm'],[900,1200])
            self.assertEqual(s['dimensions']['length_mm']%900,0)
            self.assertEqual(s['dimensions']['width_mm']%1200,0)
            self.assertEqual(len({a['id'] for a in s['parts']}),len(s['parts']))
            self.assertTrue(all(math.isfinite(v) and v>0 for a in s['parts'] for v in a['size']))
            nodes=s['foundation_spec']['support_nodes_mm']
            xs=sorted(set(x for x,y in nodes));ys=sorted(set(y for x,y in nodes))
            self.assertTrue(all(b-a==900 for a,b in zip(xs,xs[1:])))
            self.assertTrue(all(b-a==1200 for a,b in zip(ys,ys[1:])))
            self.assertEqual(set(map(tuple,nodes)),set(itertools.product(xs,ys)))
            structure=[a for a in s['parts'] if a['material'] in ('timber','plywood')]
            for hole in s['opening_voids']:
                self.assertFalse(any(collide(a,hole) for a in structure),(s['config']['id'],hole['id']))
            for a in structure:
                if a['material']=='plywood':
                    sizes=sorted(a['size']);self.assertLessEqual(sizes[-1],2440);self.assertLessEqual(sizes[-2],1220)
            self.assertTrue(all(a['capacity'] is None and a['fasteners'] is None for a in s['interfaces']))
            self.assertEqual(s['drawings']['source_geometry_sha256'],s['geometry_sha256'])
            checked+=1
        self.assertEqual(checked,216)

    def test_structural_collisions(self):
        for program,i,roof in itertools.product(range(2),range(6),range(2)):
            s=build(parameters(i,program_type=program,roof_type=roof))
            parts=[a for a in s['parts'] if a['material'] in ('timber','plywood')]
            for a,b in itertools.combinations(parts,2):
                self.assertFalse(collide(a,b),(s['config']['id'],a['id'],b['id']))

    def test_opening_rejects_impossible_bay(self):
        with self.assertRaises(ValueError):opening(0,900,900,900,0)

    def test_gh_component_portable_entry(self):
        from types import SimpleNamespace
        import json
        root=Path(__file__).resolve().parents[1]
        scope=dict(parameters(),preset_index=2,custom=False)
        scope['ghenv']=SimpleNamespace(Component=SimpleNamespace(OnPingDocument=lambda:SimpleNamespace(FilePath=str(root/'test.gh'))))
        exec(compile((root/'components/model.py').read_text(encoding='utf-8'),'components/model.py','exec'),scope)
        result=json.loads(scope['scene_json'])
        self.assertEqual(result['cell_spec']['cell_mm'],[900,1200])
        self.assertIn('Linked library:',scope['report'])

    def test_legacy_and_new_are_distinct_and_deterministic(self):
        old=build(legacy_parameters(2));new=build(parameters(2))
        self.assertNotEqual(old['geometry_sha256'],new['geometry_sha256'])
        self.assertNotIn('cell_spec',old)
        self.assertEqual(new['geometry_sha256'],build(parameters(2))['geometry_sha256'])
        self.assertEqual(old['dimensions']['width_mm'],2190)
        self.assertEqual(new['dimensions']['width_mm'],3600)


if __name__=='__main__':unittest.main()
