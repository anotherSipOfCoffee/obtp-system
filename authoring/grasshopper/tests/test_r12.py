import sys,unittest,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.optimisation import analyse
from obtp.documentation import documents
from obtp.export import vertices

class R12(unittest.TestCase):
 def test_platform_connected(self):
  for pr in (0,1):
   for idx in range(6):
    s=build(parameters(idx,program_type=pr));ps=[a for a in s['parts'] if a['family']=='foundation' and ('/beam-' in a['id'] or a['id'].startswith('foundation-tie-'))]
    self.assertEqual({a['assembly'] for a in ps},{'foundation-platform'})
    seen={0};pending=[0]
    while pending:
     a=ps[pending.pop()]
     for j,b in enumerate(ps):
      if j not in seen and all(min(a['origin'][k]+a['size'][k],b['origin'][k]+b['size'][k])-max(a['origin'][k],b['origin'][k])>=-1e-6 for k in range(3)):
       seen.add(j);pending.append(j)
    self.assertEqual(len(seen),len(ps),(pr,idx,[p['id'] for j,p in enumerate(ps) if j not in seen]))
    self.assertTrue(all(a['capacity'] is None for a in s['interfaces'] if a['id'].startswith('foundation-')))
 def test_supplier_and_types(self):
  s=build(parameters());item=next(x for x in s['object_library']['instances'] if x['id']=='sauna-partition/door');r=item['product']
  self.assertEqual(r['manufacturer_code'],'D91902M');self.assertEqual(r['frame_mm'],[890,1890,92]);self.assertEqual(r['price_eur'],344)
  parts=[a for a in s['parts'] if a['id'] in item['part_ids']];vs=[v for a in parts for v in vertices(a)]
  sizes=[max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3)]
  self.assertEqual(sorted(sizes),sorted(r['frame_mm']))
  o=analyse(s);self.assertLessEqual(o['normalised_types'],o['orientation_specific_types'])
  self.assertTrue(all(b['used_mm']<=6000 for b in o['cutting_plan']))
  self.assertTrue(any(x.get('product',{}).get('price_eur') is None for x in s['object_library']['instances']))
 def test_roof_support_layers(self):
  for roof in range(3):
   s=build(parameters(roof_type=roof));ids=[a['id'] for a in s['parts']]
   if roof!=2:self.assertTrue(any('/sheet-block-' in id for id in ids))
   if roof:self.assertTrue(any('/counter-' in id and id.startswith('weather-roof-') for id in ids));self.assertTrue(any('/batten-' in id and id.startswith('weather-roof-') for id in ids))
   if roof==2:self.assertAlmostEqual(s['metrics']['height_mm'],4480)
   self.assertTrue(all(s['checks'].values()))
if __name__=='__main__':unittest.main()
