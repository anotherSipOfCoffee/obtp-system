"""Data-driven cassette blueprint adapter. No preset lookup or selection checks."""
import copy,math
from . import model,cells,room_config as rc,room_structure as rs

def validate(plan):
 p=rc.require(plan,'plan');b=p['construction']
 if b.get('schema')!='obtp-cassette-blueprint/1':raise ValueError('Unsupported construction blueprint')
 c=copy.deepcopy(b['context']);commands=copy.deepcopy(b['commands'])
 if [c['L']+c['annex'],c['W']]!=p['bounds_mm'][2:]:raise ValueError('Blueprint footprint differs from plan')
 if c['W']!=2400 or c['L']<=0 or c['L']+c['annex']>12600:raise ValueError('Unsupported blueprint dimensions')
 for cmd in commands:
  if cmd['kind'] not in ('wall','part','interface'):raise ValueError('Unsupported construction command')
  if cmd['kind']=='wall':
   name,base,axis,length=cmd['args']
   if axis not in ('x','y') or length<=0 or not all(math.isfinite(v) for v in base+[length]):raise ValueError('Invalid wall run')
 if runs_from_commands(commands)!=p['wall_runs']:raise ValueError('Wall runs do not match blueprint commands')
 return p,c,commands

def skeleton(plan,system,roof_type,foundation_type):
 p,c,commands=validate(plan);rc.integer(system,0,0,'Cassette');rc.integer(roof_type,0,1,'Roof');rc.integer(foundation_type,0,1,'Foundation')
 c['p'].update(roof_type=roof_type,foundation_type=foundation_type)
 state=model.merge_branches(c,[model.walls(c,commands),model.slabs(c)])
 windowhosts=[cmd['args'][0] for cmd in commands if cmd['kind']=='wall' and 'window' in cmd['args'][0]]
 state['parts']=[v for v in state['parts'] if not (v['material']=='object' and any(v['id'].startswith(n+'/') for n in windowhosts))]
 weather=[];rs.weather(weather,c['L']+c['annex'],c['W'],c['F'],c['H'],roof_type)
 parts=[v for v in state['parts']+weather if v['material']=='timber']
 nodes=rs.foundation(parts,[0,0,c['L']+c['annex'],c['W']],foundation_type)
 return rc.seal('skeleton',plan=p,runs=p['wall_runs'],parts=parts,panel_parts=[v for v in state['parts']+weather if v['material']=='plywood'],roof_cover_parts=[v for v in weather if v['material'] in ('roof-metal','roof-membrane')],opening_voids=state['opening_voids'],wall_regions=state['wall_regions'],interfaces=state['interfaces'],dimensions=dict(length_mm=c['L']+c['annex'],width_mm=c['W'],annex_length_mm=c['annex'],floor_top_mm=c['F'],wall_height_mm=c['H']),roof_type=roof_type,foundation_type=foundation_type,foundation_nodes=nodes,blueprint_state=state,blueprint_context=c,holds=rc.HOLDS)

def detail(skeleton,terrace=1,paneling=1):
 s=rc.require(skeleton,'skeleton');c=s['blueprint_context'];state=s['blueprint_state']
 objects=[v for v in state['parts'] if v['material'] not in ('timber','plywood')]
 state['parts']=[v for v in s['parts'] if v['family']!='foundation']+s['panel_parts']+s['roof_cover_parts']+objects
 model.enrich_stage(c,state,'surfaces')
 if terrace:model.enrich_stage(c,state,'terrace')
 else:state['terrace_spec']=dict(terrace_area=0)
 if paneling>=1:model.enrich_stage(c,state,'insulation')
 if paneling<2:state['parts']=[v for v in state['parts'] if v['material']!='lining-wood']
 # Shared supports follow the actual platform footprint, including any canonical return.
 parts=state['parts'];support=[v for v in parts if v['family'] in ('floor','terrace')]
 rect=[min(v['origin'][0] for v in support),min(v['origin'][1] for v in support),max(v['origin'][0]+v['size'][0] for v in support),max(v['origin'][1]+v['size'][1] for v in support)]
 nodes=rs.foundation(parts,rect,s['foundation_type'])
 scene=rs.scene(skeleton,parts,dict(terrace_enabled=bool(terrace),paneling=paneling,facade=True,foundation_nodes=nodes))
 scene['config']['size']=s['plan'].get('preset_label','Imported plan').split()[-1]
 scene['holds'].append('Preset blueprint preserves architectural niche recipes; the new weather roof and support layout remain engineering studies.')
 return scene

def runs_from_commands(commands):
 runs=[]
 for c in commands:
  if c['kind']!='wall':continue
  name,base,axis,length=c['args'];kw=c['kwargs'];depth=kw.get('d',195);k=0 if axis=='x' else 1
  r=dict(id=name,base=base,axis=axis,length=length,depth=depth,side='front' if axis=='x' and base[1]==0 else 'back' if axis=='x' else 'west' if base[0]==0 else 'east',external=kw.get('family','walls')!='partitions')
  if kw.get('door'):
   u,w=kw['door'];fit=dict(start=u) if name=='annex-end' else cells.opening(base[k],base[k]+length,cells.X if k==0 else cells.Y,w,base[k]+u)
   o=list(base);o[k]+=fit['start'];r.update(door_width=w,opening_start=fit['start'],opening_origin=o,kind='window' if 'window' in name else 'door')
  runs.append(r)
 return runs
