import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp import sauna_workflow as flow,plan_pipeline as pipe,research_specimens as research
from obtp.model import parameters

class R27Acceptance(unittest.TestCase):
 def test_preset_relative_limits(self):
  for base in range(6):
   p=parameters(base)
   for delta in (-1,0,1):
    if p['hall_length_steps']+delta<2:continue
    s=flow.select(6,base_preset=base,use_overrides=True,entrance_cells_delta=delta)
    d=flow.resolve(s);self.assertEqual(d['plan']['bounds_mm'][3],2400)
    entrance=next(r for r in d['plan']['rooms'] if r['id']=='entrance')
    self.assertEqual(entrance['bounds_mm'][2],(p['hall_length_steps']+delta)*900)
   for kw in (dict(sauna_cells=5),dict(depth_cells=3),dict(entrance_cells=p['hall_length_steps']+2),dict(sauna_cells_delta=0.5)):
    with self.assertRaises(ValueError):flow.select(6,base_preset=base,use_overrides=True,**kw)
   reset=flow.select(6,base_preset=base,use_overrides=False,sauna_cells_delta=99,depth_cells=99)
   self.assertEqual(flow.resolve(reset)['plan']['bounds_mm'][3],2400)
 def test_studio_width_is_not_silently_ignored(self):
  with self.assertRaisesRegex(ValueError,'width is fixed'):flow.select(13,use_overrides=True,depth_cells=3)
 def test_intermediate_and_final_coordinates(self):
  # Outdoor-first is the reflected topology; all displays must align with final.
  selection=flow.select(6,base_preset=3,use_overrides=True,outdoor=True,arrangement=1)
  document=flow.resolve(selection)
  # Select an available outdoor-first arrangement, independent of solver sorting.
  for i in range(document['plan']['candidate_count']):
   d=flow.resolve(flow.select(6,base_preset=3,use_overrides=True,outdoor=True,arrangement=i))
   if d['plan']['rooms'][0]['id']=='outdoor':document=d;break
  s=pipe.structure(document);self.assertTrue(s['context']['p']['layout_mirror'])
  branches={k:pipe.generate(s,k) for k in ('floor','roof','walls')}
  state=pipe.merge(s,**branches);stages=list(branches.values())
  for phase in pipe.ENRICHMENT:state=pipe.enrich(s,state,phase);stages.append(state)
  scene=pipe.finish(s,state);actual={p['id']:p for p in scene['parts']}
  for data in stages:
   before=copy.deepcopy(data);parts,f=pipe.preview_parts(data);self.assertEqual(data,before)
   self.assertEqual(f,scene['dimensions']['floor_top_mm'])
   for p in parts:
    if p['id'] in actual:self.assertEqual(p['origin'],actual[p['id']]['origin'],p['id'])
  self.assertEqual(sorted(s['resolved_plan']['foundation_nodes_mm']),sorted(scene['foundation_spec']['support_nodes_mm']))
  # Structural envelopes omit skin; compare actual timber extents instead.
  for run in s['resolved_plan']['wall_runs']:
   pieces=[p for p in scene['parts'] if p['id'].split('/')[0]==run['id'] and p['material']=='timber']
   self.assertTrue(pieces)
   for axis in (0,1):
    lo=run['base_mm'][axis];extent=run['length_mm'] if axis==(0 if run['axis']=='x' else 1) else run['depth_mm']
    self.assertGreaterEqual(min(p['origin'][axis] for p in pieces),lo)
    self.assertLessEqual(max(p['origin'][axis]+p['size'][axis] for p in pieces),lo+extent)
 def test_specimen_insulation_and_no_overlap(self):
  for kind in (1,2,5):
   scene=research.cassette(kind);parts=scene['parts']
   infill=[p for p in parts if p['material']=='mineral-wool'];self.assertTrue(infill)
   for a in infill:
    for b in parts:
     if a is b:continue
     overlap=[min(a['origin'][i]+a['size'][i],b['origin'][i]+b['size'][i])-max(a['origin'][i],b['origin'][i]) for i in range(3)]
     self.assertFalse(all(x>1e-6 for x in overlap),(a['id'],b['id']))
 def test_actual_stage_wrappers(self):
  import types
  from unittest.mock import patch
  root=Path(__file__).resolve().parents[1];messages=[]
  env=types.SimpleNamespace(Component=types.SimpleNamespace(OnPingDocument=lambda:types.SimpleNamespace(FilePath=str(root/'acceptance.gh')),AddRuntimeMessage=lambda *x:messages.append(x)))
  gh=types.SimpleNamespace(Kernel=types.SimpleNamespace(GH_RuntimeMessageLevel=types.SimpleNamespace(Error='error')))
  code=(root/'components/construction_stage.py').read_text()
  def execute(stage,**inputs):
   ns=dict(ghenv=env,**inputs)
   with patch.dict(sys.modules,{'Grasshopper':gh}):exec(code.replace("STAGE_NAME='structure'",'STAGE_NAME='+repr(stage)),ns)
   self.assertFalse(messages,ns['report']);self.assertIsNotNone(ns['data_json']);return ns['data_json']
  doc=flow.resolve(flow.select(13,use_overrides=True,work_cells_delta=1))
  structure=execute('structure',plan_json=json.dumps(doc))
  branches={k+'_json':execute(k,structure_json=structure) for k in ('floor','roof','walls')}
  previous=execute('framing',structure_json=structure,**branches)
  for phase in pipe.ENRICHMENT:previous=execute(phase,structure_json=structure,previous_json=previous)
  complete=json.loads(execute('complete',structure_json=structure,previous_json=previous))
  self.assertEqual(complete['parts'],flow.construct(doc)['parts'])
