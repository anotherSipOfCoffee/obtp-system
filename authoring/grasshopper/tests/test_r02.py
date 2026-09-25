import itertools,json,math,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.export import vertices,export_one

def collide(a,b):
    # Exact interval test for these X/Y-aligned boxes and linearly sloped prisms.
    lo=[max(a['origin'][i],b['origin'][i]) for i in [0,1]]
    hi=[min(a['origin'][i]+a['size'][i],b['origin'][i]+b['size'][i]) for i in [0,1]]
    if any(hi[i]-lo[i]<=1e-6 for i in [0,1]):return False
    def z(p,top):
        m=p.get('slope_y',0)+(p.get('top_slope_y',0) if top else 0)
        return m,p['origin'][2]+(p['size'][2] if top else 0)-m*p['origin'][1]
    low,high=lo[1],hi[1]
    for first,second in [(z(a,False),z(b,True)),(z(b,False),z(a,True))]:
        m=first[0]-second[0];c=first[1]-second[1]+1e-6
        if abs(m)<1e-12:
            if c>=0:return False
        elif m>0:high=min(high,-c/m)
        else:low=max(low,-c/m)
    return high-low>1e-6

class R02(unittest.TestCase):
    def check(self,s):
        mats=set(s['metrics']['wood_m3'])
        ps=sorted([p for p in s['parts'] if p['material'] in mats],key=lambda p:p['origin'][0])
        for i,a in enumerate(ps):
            for b in ps[i+1:]:
                if b['origin'][0]>=a['origin'][0]+a['size'][0]-1e-6:break
                self.assertFalse(collide(a,b),(s['config'],a['id'],b['id']))
        self.assertTrue(all(s['checks'].values()))
        actual=max(v[2] for p in s['parts'] for v in vertices(p))
        self.assertAlmostEqual(actual,s['metrics']['height_mm'])
        window=next(v for v in s['opening_voids'] if v['id']=='front-window/opening')
        door=next(v for v in s['opening_voids'] if v['id']=='front/opening')
        self.assertEqual(window['origin'][2],door['origin'][2]);self.assertEqual(window['size'][2],door['size'][2])
        for p in s['parts']:
            if p['id'].startswith('canopy/post-'):
                self.assertTrue(p['origin'][0]+120<=door['origin'][0]-150 or p['origin'][0]>=door['origin'][0]+door['size'][0]+150)
        self.assertTrue(any(p['family']=='interior' for p in s['parts']))
        self.assertTrue(any('end-cover' in p['id'] for p in s['parts']))
        self.assertTrue(any(p['material']=='glass' for p in s['parts']))
        self.assertFalse(s['website_ready'])
    def test_roofs_terraces_six(self):
        for i,roof,terrace,window in itertools.product(range(6),range(3),[1,2],[600,900,1200]):
            self.check(build(parameters(i,roof_type=roof,terrace_steps=terrace,window_width=window)))
    def test_export(self):
        import rhino3dm
        with tempfile.TemporaryDirectory() as d:
            for roof in range(3):
                s=build(parameters(3,roof_type=roof,terrace_steps=2));export_one(s,d)
                doc=rhino3dm.File3dm.Read(str(Path(d)/(s['config']['id']+'.3dm')))
                self.assertEqual(len(doc.Objects),len(s['parts']))
                for p,o in zip(s['parts'],doc.Objects):
                    self.assertTrue(o.Geometry.IsValid and o.Geometry.IsSolid,p['id'])
                    vs=vertices(p);actual=[v.Location for v in o.Geometry.Vertices]
                    for k,attr in enumerate(['X','Y','Z']):
                        self.assertAlmostEqual(min(getattr(v,attr) for v in actual),min(x[k] for x in vs),places=4,msg=p['id'])
                        self.assertAlmostEqual(max(getattr(v,attr) for v in actual),max(x[k] for x in vs),places=4,msg=p['id'])
    def test_rejection(self):
        for kw in [dict(terrace_steps=5),dict(roof_type=3),dict(window_width=1500),dict(room_depth_steps=8,sauna_length_steps=8,hall_length_steps=8,terrace_steps=4)]:
            with self.assertRaises(ValueError):build(parameters(0,True,**kw))
if __name__=='__main__':unittest.main()
