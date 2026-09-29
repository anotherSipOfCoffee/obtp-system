import ast
import json
import tempfile
import unittest
from pathlib import Path
from obtp import room_config as rc, room_structure as rs, room_detail as rd
from obtp.room_exchange import transfer

ROOT=Path(__file__).resolve().parents[1]

class ExchangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=rc.solve(rc.rules(rc.rules(rc.programme(0,[7,0,2])),kind='boundary'))
        cls.skeleton=rs.skeleton(cls.plan)
        cls.scene=rd.build(cls.skeleton)

    def test_roundtrip_all_stages_matches_connected_pipeline(self):
        with tempfile.TemporaryDirectory() as folder:
            for stage,data in [('plan',self.plan),('skeleton',self.skeleton),('scene',self.scene)]:
                path=str(Path(folder)/(stage+'.json'))
                transfer(stage,data,path,write_file=True)
                loaded,_=transfer(stage,None,path,read_file=True)
                self.assertEqual(json.loads(loaded),json.loads(json.dumps(data)))
            plan=json.loads(transfer('plan',None,str(Path(folder)/'plan.json'),True)[0])
            skeleton=rs.skeleton(plan)
            self.assertEqual(skeleton,self.skeleton)
            self.assertEqual(rd.build(skeleton),self.scene)

    def test_wrong_stage_tamper_and_no_stale_fallback(self):
        with tempfile.TemporaryDirectory() as folder:
            path=str(Path(folder)/'plan.json')
            transfer('plan',self.plan,path,write_file=True)
            for args in [('skeleton',None,path,True),('plan','bad',path,True),('plan',None,path,True,True)]:
                with self.assertRaises((ValueError,TypeError)):transfer(*args)
            data=json.loads(Path(path).read_text());data['data']['area_m2']=99
            Path(path).write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'checksum'):transfer('plan',None,path,True)

    def test_live_priority_and_missing_input(self):
        self.assertEqual(json.loads(transfer('plan',self.plan,'missing.json',True)[0]),self.plan)
        with self.assertRaises(ValueError):transfer('plan')

    def test_creators_isolate_globals_and_add_new_document(self):
        for filename,mode in [('CREATE_LAYOUT_GRASSHOPPER.py','layout'),('CREATE_STRUCTURE_GRASSHOPPER.py','structure'),('CREATE_DETAILING_GRASSHOPPER.py','detailing'),('CREATE_ROOM_CONFIGURATOR.py','combined')]:
            source=(ROOT/filename).read_text()
            self.assertIn("init_globals={'CANVAS_MODE':%r}"%mode,source)
            self.assertIn('runpy.run_path',source)
            ast.parse(source)
        source=(ROOT/'room_canvas.py').read_text()
        ast.parse(source)
        self.assertIn('doc=GH_Document()',source)
        self.assertIn('DocumentServer.AddDocument(doc)',source)
        self.assertNotIn('RemoveDocument',source)
        self.assertNotIn('SetSource(',source)
        self.assertIn('%f',source)

if __name__=='__main__':unittest.main()
