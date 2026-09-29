import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from obtp import room_presets as rp,room_assemblies as a,room_detail as d,room_config as rc,checkpoints as cp
from obtp.room_documents import export,DEFAULT_RATES,project,modelspace

class AssemblyTests(unittest.TestCase):
 def test_box_is_geometry_driven_for_all_presets(self):
  for t in range(3):
   plan=rp.generate(t);self.assertNotIn('construction',plan)
   with patch('obtp.model.arrange',side_effect=AssertionError('Preset arrangement')),patch('obtp.model.parameters',side_effect=AssertionError('Preset parameters')),patch.object(rp,'generate',side_effect=AssertionError('Preset source')):
    before=a.box(plan)
    other=copy.deepcopy(plan);other.pop('detailing_context',None);other['preset_label']='Unknown external layout';other=rp.reseal(other)
    after=a.box(other)
    self.assertEqual(before['parts'],after['parts']);self.assertEqual(before['panel_parts'],after['panel_parts'])
    if 'wall_runs' in other:
     other['wall_runs'][0]['length']-=100;other=rp.reseal(other)
     self.assertNotEqual(after['parts'],a.box(other)['parts'])
 def test_roof_restores_previous_detailed_recipe(self):
  from obtp.envelope import enrich
  plan=rp.generate(0);ctx=plan['detailing_context'];p=ctx['p']
  for kind in (0,1):
   p=copy.deepcopy(p);p['roof_type']=kind;parts=[]
   enrich(p,parts,[],[],ctx['L'],ctx['W'],ctx['F'],ctx['H'],ctx['annex'],[],phase='roof',terrace_area=0)
   self.assertEqual(a.roof(plan,kind)['parts'],parts)
   self.assertTrue(any('/sheet-block-' in v['id'] for v in parts))
   if kind:self.assertTrue(any('/counter-' in v['id'] for v in parts));self.assertTrue(any('/seam-' in v['id'] for v in parts))
 def test_stale_mix_rejected_and_no_rebuilt_foundation(self):
  plan=rp.generate();b=a.box(plan);f=a.foundation(plan);r=a.roof(plan)
  with self.assertRaisesRegex(ValueError,'different plans'):a.assemble(b,a.foundation(rp.generate(size=2)),r)
  with self.assertRaisesRegex(ValueError,'terrace'):a.assemble(b,f,a.roof(plan,terrace=False))
  sk=a.assemble(b,f,r)
  with patch('obtp.room_structure.foundation',side_effect=AssertionError('Rebuilt foundation')):scene=d.build(sk)
  self.assertEqual([v for v in scene['parts'] if v['family']=='foundation'],f['parts'])
 def test_no_box_header_overlap(self):
  b=a.box(rp.generate(1));headers=[v for v in b['parts'] if v['id'].startswith('open-edge-')]
  self.assertEqual(len(headers),2)
  for h in headers:
   for v in b['parts']:
    if v['family']!='roof':continue
    overlap=[min(h['origin'][i]+h['size'][i],v['origin'][i]+v['size'][i])-max(h['origin'][i],v['origin'][i]) for i in range(3)]
    self.assertFalse(all(x>1e-6 for x in overlap))
 def test_preview_scopes_leave_quantities_unchanged(self):
  p=rp.generate();scene=d.build(a.assemble(a.box(p),a.foundation(p),a.roof(p)),paneling=2);original=copy.deepcopy(scene)
  display=cp.assembly(scene);bare=cp.view(display,1);frame=cp.view(display,3);complete=cp.view(display,2)
  self.assertTrue(any(cp.facade_layer(v) for v in complete['parts']))
  self.assertFalse(any(cp.facade_layer(v) for v in bare['parts']))
  self.assertFalse(any(v['material']=='plywood' for v in frame['parts']))
  self.assertEqual(scene,original)
 def test_windows_encoding_export_and_modelspace(self):
  plan=rp.generate();scene=d.build(a.assemble(a.box(plan),a.foundation(plan),a.roof(plan)))
  original=Path.write_text;written=[]
  def windows_write(path,text,*args,**kwargs):
   # Reproduce Windows' failure if any writer forgets an explicit Unicode encoding.
   if not kwargs.get('encoding'):text.encode('cp1252')
   written.append((str(path),kwargs.get('encoding')))
   return original(path,text,*args,**kwargs)
  with tempfile.TemporaryDirectory() as tmp:
   rates=Path(tmp)/'rates.json';rates.write_text(json.dumps(DEFAULT_RATES),encoding='utf-8')
   with patch.object(Path,'write_text',windows_write),patch('obtp.native_drawings.bake',return_value={'status':'test-only-not-native'}):
    result=export(scene,tmp,str(rates),native=True)
   self.assertTrue(written);self.assertTrue(all(enc=='utf-8' for _,enc in written))
   recipe=json.loads((Path(result['folder'])/'project-review-layouts.json').read_text(encoding='utf-8'))
   self.assertTrue(any('Ū' in t['text'] for page in recipe['sheets'] for t in page['texts']))
  drawing=modelspace(project(scene));self.assertEqual(drawing['sheets'],8)
  self.assertTrue(drawing['lines']);self.assertTrue(drawing['texts']);self.assertTrue(all(v['at'][1]<-6500 for v in drawing['texts']))
