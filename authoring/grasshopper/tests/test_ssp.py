import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.ssp_sheets import prepare,bounds

class SSPTests(unittest.TestCase):
    def test_supported_presets_fit_fixed_scales_without_mutation(self):
        for program in (0,1):
            for i in range(6):
                scene=build(parameters(i,program_type=program))
                before=copy.deepcopy(scene)
                r=prepare(scene)
                self.assertEqual(scene,before)
                self.assertEqual(len(r['sheets']),9)
                self.assertEqual(r['geometry_sha256'],scene['geometry_sha256'])
                self.assertEqual(r['omitted_required'],['site-plan-and-site-specific-data'])
                for p in r['sheets']:
                    self.assertEqual(p['total'],9)
                    for q in p['details']:
                        self.assertIn(q['scale'],(10,25,50,100))
                        b=bounds(q['view']);box=q['box']
                        self.assertLessEqual((b[2]-b[0])/q['scale'],box[2]-box[0])
                        self.assertLessEqual((b[3]-b[1])/q['scale'],box[3]-box[1])
                        for a in q['view']['polygons']:
                            self.assertIn(a['id'],{x['id'] for x in scene['parts']})
    def test_roofs_and_core_scope(self):
        for roof in range(3):
            r=prepare(build(parameters(5,roof_type=roof)))
            self.assertEqual([p['code'] for p in r['sheets']],['BD-01','BD-02','BD-03','BD-04','SA-01','SA-02','SA-03','SA-04','SA-05'])
            self.assertFalse(any('Analizė' in p['name'] or 'Gamintojai' in p['name'] or 'mazgai' in p['name'] for p in r['sheets']))

if __name__=='__main__':unittest.main()
