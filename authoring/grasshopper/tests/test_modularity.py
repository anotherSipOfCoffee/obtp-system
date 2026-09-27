import unittest,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.modularity import procurement,SUPPLIER_REFERENCES
from obtp.manufacturing import analyse
from modularity_study import metrics,candidate

class ModularityTest(unittest.TestCase):
    def test_window_dimensional_chain(self):
        for width in (580,880,1180):
            s=build(parameters(2,window_width=width))
            w=next(o for o in s['modularity']['openings'] if 'window' in o['id'])
            self.assertEqual(w['modeled_frame_outside_mm'],[width,1880])
            self.assertEqual(w['installation_opening_mm'],[width+20,1900])
            self.assertEqual(w['modeled_installation_gaps_left_right_bottom_top_mm'],[10]*4)
            self.assertIsNone(w['manufacturer_installation_tolerances_mm'])
            self.assertIsNone(w['verified_frame_outside_mm'])
            self.assertAlmostEqual(sum(w['structural_side_zones_mm'])+width+20,w['host_width_mm'])
    def test_product_fit_is_not_invented(self):
        s=build(parameters(2));records={o['id']:o for o in s['modularity']['openings']}
        d=records['sauna-partition/opening']
        self.assertEqual(d['verified_frame_outside_mm'],[890,1890,92])
        self.assertIsNone(d['clear_usable_passage_mm'])
        self.assertIsNone(d['manufacturer_installation_tolerances_mm'])
        front=records['front/opening']
        self.assertEqual(front['alternative_product_checks'][0]['shortfall_mm'],[10,0])
        self.assertEqual(front['alternative_product_checks'][1]['shortfall_mm'],[110,200])
        self.assertFalse(any(x['adopted'] for x in front['alternative_product_checks']))
    def test_count_reconciliation_and_no_mutation(self):
        for program in (0,1):
            s=build(parameters(2,program_type=program));before=json.dumps(s['parts'],sort_keys=True)
            a=metrics(s);p=procurement(s)
            self.assertEqual(a['pieces'],a['fabricated_pieces']+a['purchased_representation_pieces']+a['unresolved_object_pieces'])
            self.assertEqual(a['pieces'],analyse(s)['physical_pieces'])
            self.assertEqual(len(p['purchased_representation_ids']),len(set(p['purchased_representation_ids'])))
            self.assertEqual(before,json.dumps(s['parts'],sort_keys=True))
    def test_experiment_does_not_leak_to_production(self):
        s=build(parameters(2));before=s['geometry_sha256']
        with candidate('B-solids'):
            b=build(parameters(2))
            self.assertNotEqual(before,b['geometry_sha256'])
            self.assertEqual(s['dimensions'],b['dimensions'])
        self.assertEqual(before,build(parameters(2))['geometry_sha256'])
    def test_legacy_contract(self):
        s=build(parameters(2,grid_system=0))
        self.assertEqual(s['modularity']['planning']['cell_mm'],[600,600])
        self.assertGreater(len(s['modularity']['openings']),0)
if __name__=='__main__':unittest.main()
