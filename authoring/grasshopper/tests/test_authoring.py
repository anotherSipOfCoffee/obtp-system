"""Geometry checks can run outside Rhino; host acceptance is a separate gate."""
import itertools
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters,PRESETS
from obtp.export import export_one,browser_scene
from test_r02 import collide


overlap=collide

class AuthoringTests(unittest.TestCase):
    def assert_geometry(self,s):
        structure=[a for a in s['parts'] if a['material'] in ['timber','plywood']]
        for a,b in itertools.combinations(structure,2):
            self.assertFalse(overlap(a,b),(s['config']['id'],a['id'],b['id']))
        for void in s['opening_voids']:
            self.assertFalse(any(overlap(a,void) for a in structure),void['id'])
        for a in structure:
            self.assertTrue(all(math.isfinite(v) for v in a['origin']+a['size']))
            if a['material']=='plywood':
                spans=sorted(a['size']);self.assertLessEqual(spans[-1],2440);self.assertLessEqual(spans[-2],1220)
        self.assertFalse(s['website_ready']);self.assertFalse(s['manufacturing_release'])
        self.assertTrue(all(s['checks'].values()))
        self.assertTrue(all(i['capacity'] is None and i['fasteners'] is None for i in s['interfaces']))

    def test_six(self):
        hashes=[]
        for i in range(6):
            s=build(parameters(i));self.assert_geometry(s);hashes.append(s['geometry_sha256'])
            self.assertEqual(s['geometry_sha256'],build(parameters(i))['geometry_sha256'])
            self.assertEqual(len(s['opening_voids']),4 if i%2 else 3)
            self.assertEqual(s['dimensions']['width_mm'],2190)
            self.assertEqual(sum(1 for p in s['parts'] if p['id']=='shower/head'),1)
        self.assertEqual(len(set(hashes)),6)
        self.assertEqual(build(parameters(0))['geometry_sha256'],build(parameters(0))['geometry_sha256'])

    def test_custom(self):
        accepted=0;rejected=0
        for depth,hot,hall,storage,height in itertools.product([3,4,6],[3,4,6],[2,3,5],[False,True],[2100,2700]):
            try:s=build(parameters(2,True,room_depth_steps=depth,sauna_length_steps=hot,hall_length_steps=hall,storage=storage,wall_height=height))
            except ValueError:rejected+=1;continue
            self.assert_geometry(s);accepted+=1
        self.assertGreater(accepted,6)
        print('Custom cases:',accepted,'accepted geometry candidates,',rejected,'rejected')

    def test_invalid(self):
        for kwargs in [dict(room_depth_steps=10),dict(room_depth_steps=8,sauna_length_steps=8,hall_length_steps=8),
                       dict(door_width=1300),dict(sauna_door_offset=1700),dict(hall_length_steps=1),
                       dict(room_depth_steps=3.2),dict(wall_height=5000),dict(bench_depth=800)]:
            with self.assertRaises(ValueError,msg=kwargs):build(parameters(0,True,**kwargs))
        with self.assertRaises(ValueError):parameters(6)
        with self.assertRaises(ValueError):parameters(0,True,unknown=1)

    def test_export_identity_and_solids(self):
        import rhino3dm
        with tempfile.TemporaryDirectory() as temp:
            for i in range(6):
                s=build(parameters(i));files=export_one(s,temp)
                self.assertEqual(len(files),4)
                model=rhino3dm.File3dm.Read(str(Path(temp)/(PRESETS[i]['id']+'.3dm')))
                self.assertEqual(model.Settings.ModelUnitSystem,rhino3dm.UnitSystem.Millimeters)
                self.assertEqual(len(model.Objects),len(s['parts']))
                for p,obj in zip(s['parts'],model.Objects):
                    self.assertTrue(obj.Geometry.IsValid and obj.Geometry.IsSolid)
                    self.assertEqual(obj.Attributes.GetUserString('obtp_id'),p['id'])
                    if p.get('slope_y') or p.get('top_slope_y'):continue
                    bb=obj.Geometry.GetBoundingBox()
                    self.assertEqual([bb.Min.X,bb.Min.Y,bb.Min.Z],p['origin'])
                    self.assertEqual([bb.Max.X-bb.Min.X,bb.Max.Y-bb.Min.Y,bb.Max.Z-bb.Min.Z],p['size'])
                b=browser_scene(s)
                self.assertEqual(b['source_geometry_sha256'],s['geometry_sha256'])
                self.assertEqual(len(b['items']),len(model.Objects))
                self.assertEqual([x['id'] for x in b['items']],[x['id'] for x in s['parts']])
                self.assertEqual(len(json.loads((Path(temp)/(PRESETS[i]['id']+'.json')).read_text())['parts']),len(s['parts']))

if __name__=='__main__':unittest.main()
