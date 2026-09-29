"""Versioned, hash-checked stage contracts; millimetres. No native dependencies.

The supported domain is a single level, axis-aligned contiguous strip of programme
rooms. Layout supplies boundaries; arrangement derives candidate walls, apertures
and slab bays. Each branch manufactures only its own parts. No complete scene is
created until completion. Capacity is never inferred from geometric acceptance.
"""
import copy
from . import model, layout, cells

SCHEMA='obtp-construction-stage/1'

def seal(stage,source,**data):
 result=dict(schema=SCHEMA,stage=stage,units='mm',source=source,**data)
 result['sha256']=layout.digest(result)
 return result

def require(value,stage):
 if not isinstance(value,dict):raise ValueError(stage+': missing upstream result; downstream cleared')
 value=copy.deepcopy(value);claim=value.pop('sha256',None)
 if value.get('schema')!=SCHEMA or value.get('stage')!=stage or claim!=layout.digest(value):
  raise ValueError(stage+': invalid or stale stage contract; recompute upstream')
 value['sha256']=claim
 return value

def structure(document):
 from . import sauna_workflow as flow
 if document!=flow.resolve(document['selection']):raise ValueError('03 Structure: stale plan; recompute Layout')
 selection=document['selection'];plan=document['plan']
 if selection['preset_index']>=7:
  p=flow.studio_config(selection)
  # The plan, not the saved preset, supplies all downstream dimensions.
  rooms=plan['rooms'];p.update(sauna_length_steps=rooms[0]['bounds_mm'][2]//cells.X,hall_length_steps=rooms[1]['bounds_mm'][2]//cells.X,storage_length_steps=rooms[2]['bounds_mm'][2]//cells.X,room_depth_steps=plan['bounds_mm'][3]//cells.Y)
 else:p=layout.config_from_plan(plan,selection['cassette_settings'],selection['preserve_legacy_shower'])
 context=model.prepare(p)
 commands=model.arrange(context)
 runs=[];openings=[];nodes={}
 for command in commands:
  if command['kind']!='wall':continue
  args=command['args'];kw=command['kwargs'];name,base,axis,length=args[:4];depth=kw.get('d',195)
  end=list(base);end[0 if axis=='x' else 1]+=length
  run=dict(id=name,base_mm=list(base),end_mm=end,axis=axis,length_mm=length,depth_mm=depth,level='L0',assembly_rule='900 X / 1200 Y grid; terminals >=90; opening bays replace solid bays',capacity=None)
  runs.append(run)
  for point in (base,end):nodes.setdefault(tuple(point),[]).append(name)
  if kw.get('door'):
   start,width=kw['door'];i=0 if axis=='x' else 1
   fit=cells.opening(base[i],base[i]+length,cells.X if axis=='x' else cells.Y,width,base[i]+start) if name!='annex-end' else dict(start=start)
   origin=list(base);origin[i]+=fit['start']
   openings.append(dict(id=name+'/opening',host=name,origin_mm=origin,axis=axis,width_mm=width,height_mm=p['door_height'],level='L0',kind='window' if 'window' in name else 'door',installation_gap_mm=10 if 'window' in name else None))
 total=context['L']+context['annex'];width=context['W']
 if [total,width]!=plan['bounds_mm'][2:]:raise ValueError('03 Structure: plan footprint disagrees with assembly boundaries')
 from .cell_platform import bounds as platform_bounds
 lo,hi=platform_bounds(p,context['L'],width,context['annex'])
 xs=sorted(set(list(range(lo,hi+1,1800))+[hi]));ys=list(range(-1200,width+1,1200))
 supports=[[x,y] for y in ys for x in xs] if p['include_foundation'] else []
 if p.get('layout_mirror'):
  for run in runs:
   for key in ('base_mm','end_mm'):run[key][0]=total-run[key][0]-(run['depth_mm'] if run['axis']=='y' else 0)
  for run in runs:
   if run['axis']=='x':run['base_mm'],run['end_mm']=run['end_mm'],run['base_mm']
  depths={run['id']:run['depth_mm'] for run in runs}
  for opening in openings:opening['origin_mm'][0]=total-opening['origin_mm'][0]-(opening['width_mm'] if opening['axis']=='x' else depths[opening['host']])
  supports=[[total-x,y] for x,y in supports]
 contacts=[]
 def rectangle(run):
  x,y=run['base_mm'];xx,yy=run['end_mm'];d=run['depth_mm']
  return [min(x,xx),min(y,yy),max(x,xx)+(d if run['axis']=='y' else 0),max(y,yy)+(d if run['axis']=='x' else 0)]
 for i,a in enumerate(runs):
  aa=rectangle(a)
  for b in runs[i+1:]:
   bb=rectangle(b)
   if min(aa[2],bb[2])>=max(aa[0],bb[0]) and min(aa[3],bb[3])>=max(aa[1],bb[1]):
    contacts.append(dict(id=a['id']+'|'+b['id'],runs=[a['id'],b['id']],type='orthogonal contact' if a['axis']!=b['axis'] else 'collinear terminal',status='geometric contact; corner/junction fastening unresolved',capacity=None))
 resolved=copy.deepcopy(plan)
 resolved.update(units='mm',boundary_mm=[[0,0],[total,0],[total,width],[0,width]],levels=[dict(id='L0',floor_top_mm=context['F'],wall_height_mm=context['H'])],opening_hosts=openings,wall_runs=runs,junctions=contacts,foundation_nodes_mm=supports,platform_bounds_mm=([total-hi,-1200,total-lo,width] if p.get('layout_mirror') else [lo,-1200,hi,width]),slab_boundary_mm=[0,0,total,width],terrace_rule='1200 mm front coordination strip; programme-specific side return',unsupported=['curves','arbitrary angles','holes','branching room graph','multiple levels'])
 return seal('structure',plan['plan_sha256'],document=document,context=context,commands=commands,resolved_plan=resolved,report='Candidate structural arrangement: %d wall runs, %d hosted openings. Geometric coordination only; lintels, spans, junctions, bracing, canopy, soil and lifting remain engineering holds.'%(len(runs),len(openings)))

def generate(structural,stage):
 s=require(structural,'structure')
 if stage not in ('floor','roof','walls'):raise ValueError('Unknown construction branch '+str(stage))
 c=copy.deepcopy(s['context'])
 result=model.walls(c,s['commands']) if stage=='walls' else model.slabs(c,(stage,))
 return seal(stage,s['sha256'],result=result,display_context=display_context(s),report='%s: %d parts generated; dimensions in mm. Capacities and fasteners unresolved.'%(stage,len(result['parts'])))

ENRICHMENT=('surfaces','terrace','weather','foundation','insulation')

def merge(structural,floor,roof,walls):
 s=require(structural,'structure');branches=[]
 for name,value in [('floor',floor),('roof',roof),('walls',walls)]:
  value=require(value,name)
  if value['source']!=s['sha256']:raise ValueError('Assembly merge: '+name+' belongs to a different plan')
  branches.append(value['result'])
 return seal('framing',s['sha256'],state=model.merge_branches(s['context'],branches),display_context=display_context(s),report='Floor, roof and wall branch identities verified and combined.')

def enrich(structural,previous,phase):
 s=require(structural,'structure')
 if phase not in ENRICHMENT:raise ValueError('Unknown stage '+phase)
 index=ENRICHMENT.index(phase);expected='framing' if index==0 else ENRICHMENT[index-1]
 previous=require(previous,expected)
 if previous['source']!=s['sha256']:raise ValueError(phase+': stale upstream plan')
 state=previous['state'];before=len(state['parts'])
 model.enrich_stage(s['context'],state,phase)
 return seal(phase,s['sha256'],state=state,display_context=display_context(s),added_ids=[p['id'] for p in state['parts'][before:]],report=phase+': generated '+str(len(state['parts'])-before)+' constituent parts; connection design unresolved.')

def finish(structural,insulation):
 s=require(structural,'structure');value=require(insulation,'insulation')
 if value['source']!=s['sha256']:raise ValueError('Quantities: stale upstream plan')
 scene=model.finalize(s['context'],value['state'])
 document=s['document'];selection=document['selection'];plan=document['plan']
 if selection['preset_index']<7:layout.validate_scene(plan,scene)
 scene['layout_contract']=dict(plan_sha256=plan['plan_sha256'],rooms=plan['rooms'],source='shared bounded plan pipeline',engineering_status='candidate geometry, capacities unresolved',workflow='preset -> plan -> arrangement -> assembly branches -> finishes -> scene',preset_index=selection['preset_index'],preset_name=selection['preset_name'],selection_sha256=selection['selection_sha256'])
 scene['resolved_plan']=s['resolved_plan'];scene['display_revision']='GH-R27-PLAN-STAGES'
 return scene

def construct(document):
 s=structure(document)
 state=merge(s,generate(s,'floor'),generate(s,'roof'),generate(s,'walls'))
 for phase in ENRICHMENT:state=enrich(s,state,phase)
 return finish(s,state)


def display_context(structural):
 c=structural['context']
 return dict(floor_top_mm=c['F'],mirror=bool(c['p'].get('layout_mirror')),total_mm=c['L']+c['annex'])

def preview_parts(data):
 """One display coordinate convention; intermediate canonical branches stay intact."""
 if data.get('schema')!=SCHEMA:
  return copy.deepcopy(data.get('parts',[])),data['dimensions']['floor_top_mm']
 require(data,data['stage'])
 if data['stage']=='structure':
  f=data['context']['F'];parts=[]
  for r in data['resolved_plan']['wall_runs']:
   size=[r['length_mm'],r['depth_mm'],data['context']['H']] if r['axis']=='x' else [r['depth_mm'],r['length_mm'],data['context']['H']]
   parts.append(dict(id=r['id'],origin=r['base_mm']+[f],size=size,material='timber',family='walls',assembly=r['id']))
  return parts,f
 parts=copy.deepcopy(data.get('result',data.get('state',{})).get('parts',[]))
 if 'added_ids' in data:
  ids=set(data['added_ids']);parts=[p for p in parts if p['id'] in ids]
 c=data['display_context']
 if c['mirror']:
  for p in parts:p['origin'][0]=c['total_mm']-p['origin'][0]-p['size'][0]
 return parts,c['floor_top_mm']
