import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.manufacturing import identity,cladding,analyse
from obtp.model import build,parameters

class ManufacturingTests(unittest.TestCase):
    def test_identity_ignores_display_category_but_not_manufacturing_details(self):
        a=dict(id='floor-0/edge-a',family='floor',material='timber',size=[45,2400,220])
        b=dict(a,id='roof-2/edge-b',family='roof',size=[2400.0,45.0,220.0])
        self.assertEqual(identity(a),identity(b))
        b['manufacturing']={'handedness':'left','machining':'drilled-4','connection_detail':'A'}
        self.assertNotEqual(identity(a),identity(b))
        c=copy.deepcopy(b);c['manufacturing']['connection_detail']='B'
        self.assertNotEqual(identity(b),identity(c))
        c=copy.deepcopy(b);c['manufacturing']['handedness']='right'
        self.assertNotEqual(identity(b),identity(c))

    def test_only_facade_finish_is_excluded(self):
        for ident,family,expected in [('facade-front/board-1','facade',True),('roof-fascia-hot/0-1','roof',True),('facade-front/batten-1','facade',False),('facade-front/counter-1','facade',False),('weather-edge-front/fascia','roof',False),('floor-edge-front/board','floor',False)]:
            self.assertEqual(cladding(dict(id=ident,family=family)),expected)
        s=build(parameters(2,roof_type=0));a=analyse(s)
        self.assertEqual(a['physical_pieces']+a['cladding']['physical_pieces'],len(s['parts']))
        self.assertEqual(a['unique_types_including_cladding']-a['cladding_exclusion_type_effect'],a['unique_manufactured_part_candidates'])

    def test_terrace_direction_and_supported_board_joints(self):
        for program in range(2):
            s=build(parameters(2,program_type=program,roof_type=0))
            deck=[a for a in s['parts'] if a['family']=='terrace']
            joists=[a for a in deck if a['material']=='timber']
            boards=[a for a in deck if '/board-' in a['id']]
            front=[a for a in boards if a['id'].startswith('terrace/')]
            side=[a for a in boards if a['id'].startswith('terrace-side/')]
            self.assertEqual(min(a['origin'][1] for a in side)-max(a['origin'][1]+a['size'][1] for a in front),5)
            for a in boards:
                self.assertLessEqual(a['size'][0],1800)
                self.assertLessEqual(a['size'][1],95)
                self.assertEqual(a['size'][2],28)
                for x in [a['origin'][0]+1,a['origin'][0]+a['size'][0]-1]:
                    self.assertTrue(any(j['origin'][0]<=x<=j['origin'][0]+j['size'][0] and j['origin'][1]<=a['origin'][1]<j['origin'][1]+j['size'][1] for j in joists),a['id'])

    def test_studio_niche_floor_has_supported_joists(self):
        s=build(parameters(2,program_type=1))
        joists=[a for a in s['parts'] if a['id'].startswith('firewood-niche/joist-')]
        self.assertEqual(len(joists),2)
        for j in joists:
            self.assertEqual(j['origin'][1],0)
            self.assertEqual(j['size'][1],s['dimensions']['width_mm'])
            self.assertEqual(j['origin'][2],0)
            self.assertEqual(j['size'][2],s['dimensions']['floor_top_mm']-28)
            self.assertFalse(any(a['id'].startswith('foundation-deck-') and '/packing-' in a['id'] for a in s['parts']))


    def test_opening_jacks_retain_direct_bearing_and_repeat_side_plates(self):
        for program in range(2):
            for window in (580,880,1180):
                for preset in (2,3):
                    scene=build(parameters(preset,program_type=program,window_width=window))
                    for group in scene['cell_spec']['wall_assemblies']:
                        parts=[a for a in scene['parts'] if a['assembly']==group['id'] and a['material'] in ('timber','plywood')]
                        if group['kind'] in ('solid','terminal'):
                            self.assertEqual(len(parts),5)
                            self.assertEqual(len({identity(a) for a in parts}),3)
                            continue
                        lintel=next(a for a in parts if a['id'].endswith('/lintel'))
                        for side in ('left','right'):
                            jack=next(a for a in parts if a['id'].endswith('/jack-'+side))
                            bottom=next(a for a in parts if a['id'].endswith('/plate-bottom-'+side))
                            top=next(a for a in parts if a['id'].endswith('/plate-top-'+side))
                            self.assertEqual(identity(bottom),identity(top))
                            self.assertEqual(jack['origin'][2],bottom['origin'][2]+bottom['size'][2])
                            self.assertEqual(jack['origin'][2]+jack['size'][2],lintel['origin'][2])
                            for axis in (0,1):
                                self.assertGreaterEqual(jack['origin'][axis],lintel['origin'][axis])
                                self.assertLessEqual(jack['origin'][axis]+jack['size'][axis],lintel['origin'][axis]+lintel['size'][axis])

    def test_lean_storage_opening_remains_in_storage_zone(self):
        for i in [1,3,5]:
            s=build(parameters(i,roof_type=0));p=s['config']
            self.assertEqual(s['dimensions']['width_mm'],2400)
            door=next(v for v in s['opening_voids'] if v['id']=='annex-end/opening')
            self.assertGreaterEqual(door['origin'][1],195+p['annex_split_a_mm']+p['partition_depth'])
            self.assertLessEqual(door['origin'][1]+door['size'][1],195+p['annex_split_b_mm'])

    def test_gh_has_normal_preview_and_no_obsolete_controls(self):
        root=Path(__file__).resolve().parents[1]
        setup=(root/'CREATE_GRASSHOPPER.py').read_text()
        for text in ['Show only','part_controls','Gable / metal','controls[\'facade_type\']','controls[\'terrace_steps\']']:
            self.assertNotIn(text,setup)
        self.assertIn('3D model',setup)
        self.assertNotIn('drawings.bake',(root/'components/export.py').read_text())

if __name__=='__main__':unittest.main()
