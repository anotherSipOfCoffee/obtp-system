"""Protect actual joint support and cross-category geometry, not just counts."""
import itertools,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from test_r02 import collide

class RepeatedCuts(unittest.TestCase):
    def test_all_wood_categories_are_collision_free(self):
        for program,preset,roof in itertools.product(range(2),range(6),range(2)):
            scene=build(parameters(preset,program_type=program,roof_type=roof))
            parts=sorted([a for a in scene['parts'] if a['material'] in scene['metrics']['wood_m3']],key=lambda a:a['origin'][0])
            for i,a in enumerate(parts):
                for b in parts[i+1:]:
                    if b['origin'][0]>=a['origin'][0]+a['size'][0]-1e-6:break
                    self.assertFalse(collide(a,b),(scene['config']['id'],roof,a['id'],b['id']))

    def test_new_lining_joints_have_full_width_seats(self):
        for program,window,preset in itertools.product(range(2),(580,880,1180),(2,3)):
            scene=build(parameters(preset,program_type=program,window_width=window))
            for a in scene['parts']:
                if a['material']!='lining-wood' or '/board-' not in a['id'] or '-cut-' not in a['id']:continue
                if int(a['id'].rsplit('-cut-',1)[1])==0:continue
                axis=0 if a['family']=='ceiling' or a['size'][1]==16 else 1
                joint=a['origin'][axis]
                seats=[b for b in scene['parts'] if b['assembly']==a['assembly'] and '/batten-' in b['id'] and b['size'][axis]>=45 and b['origin'][axis]<=joint-20 and b['origin'][axis]+b['size'][axis]>=joint+20]
                if a['family']=='interior':seats=[b for b in seats if b['origin'][2]<=a['origin'][2] and b['origin'][2]+b['size'][2]>=a['origin'][2]+a['size'][2]]
                self.assertTrue(seats,a['id'])

    def test_facade_batten_joints_have_counterbatten_seats(self):
        for program in range(2):
            scene=build(parameters(2,program_type=program))
            rails=[a for a in scene['parts'] if a['family']=='facade' and '/batten-' in a['id']]
            for a,b in itertools.combinations(rails,2):
                if a['assembly']!=b['assembly'] or a['origin'][2]!=b['origin'][2]:continue
                axis=0 if a['size'][1]==25 else 1
                if abs(a['origin'][axis]+a['size'][axis]-b['origin'][axis])>1e-6:continue
                joint=b['origin'][axis]
                self.assertTrue(any(c['assembly']==a['assembly'] and '/counter-' in c['id'] and c['size'][axis]>=45 and c['origin'][axis]<=joint-20 and c['origin'][axis]+c['size'][axis]>=joint+20 and c['origin'][2]<=a['origin'][2] and c['origin'][2]+c['size'][2]>=a['origin'][2]+a['size'][2] for c in scene['parts']),(a['id'],b['id']))

    def test_roof_rail_splices_bear_on_studs(self):
        for program,roof in itertools.product(range(2),range(2)):
            scene=build(parameters(2,program_type=program,roof_type=roof))
            for a in scene['parts']:
                if not a['id'].startswith('weather-bearing-') or '/top-cut-' not in a['id'] or a['id'].endswith('-cut-0'):continue
                joint=a['origin'][0]
                seats=[b for b in scene['parts'] if b['assembly']==a['assembly'] and '/stud-' in b['id'] and b['origin'][0]<=joint-1 and b['origin'][0]+b['size'][0]>=joint+1]
                self.assertTrue(seats,a['id'])
                self.assertTrue(any(abs(b['origin'][2]+b['size'][2]-a['origin'][2])<1e-6 for b in seats))

    def test_deck_clears_trim_and_retains_geometric_bearing(self):
        for program in range(2):
            scene=build(parameters(2,program_type=program))
            end=scene['dimensions']['length_mm']+scene['dimensions']['annex_length_mm']
            for a in scene['parts']:
                if not a['id'].startswith('terrace/joist-') or not 0<=a['origin'][0]<end:continue
                self.assertEqual(a['origin'][1]+a['size'][1],-22)
                self.assertTrue(any(b['id'].startswith('foundation-deck-') and b['origin'][0]==a['origin'][0] and b['origin'][1]+b['size'][1]==-22 and b['size'][1]>=45 for b in scene['parts']))

    def test_studio_headers_and_ceiling_clear_glazing(self):
        for closed in (True,False):
            scene=build(parameters(2,program_type=1,studio_winter_closed=closed))
            glazing=[a for a in scene['parts'] if a['id'].startswith('studio-slider-')]
            structure=[a for a in scene['parts'] if a['id'].startswith(('studio-bridge/header-','ceiling-centre/'))]
            for a,b in itertools.product(structure,glazing):self.assertFalse(collide(a,b),(a['id'],b['id']))

if __name__=='__main__':unittest.main()
