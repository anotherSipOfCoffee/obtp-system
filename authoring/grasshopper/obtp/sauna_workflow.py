"""R27 bounded room-control sequence: preset -> resolved plan -> cassette -> scene.
No building is generated while choosing or resolving a preset.
"""
import copy
from . import layout
from .model import parameters
PRESETS=tuple('Sauna '+n for n in ('S / no storage','S / storage','M / no storage','M / storage','L / no storage','L / storage'))+('Custom Sauna',)+tuple('Studio '+n for n in ('S / no storage','S / storage','M / no storage','M / storage','L / no storage','L / storage'))+('Custom Studio',)

def select(preset_index=2,**inputs):
 index=layout.integer(preset_index,0,13,'Building preset')
 if index<6:
  p=parameters(index,program_type=0)
  programme=layout.programme(sauna=True,entrance=True,outdoor=p['storage'],sauna_cells=p['sauna_length_steps'],entrance_cells=p['hall_length_steps'],outdoor_cells=p['storage_length_steps'],depth_cells=p['room_depth_steps'])
  graph=layout.relationships(programme);arrangement=0
 elif index==6:
  base=layout.integer(inputs.get('base_preset',2),0,5,'Sauna base preset')
  defaults=parameters(base,program_type=0)
  enabled=inputs.get('use_overrides',True)
  if type(enabled) is not bool:raise ValueError('Use overrides must be Boolean')
  inputs=dict(inputs)
  limits={}
  for key,param,minimum in [('sauna_cells','sauna_length_steps',3),('entrance_cells','hall_length_steps',2),('outdoor_cells','storage_length_steps',1)]:
   default=defaults[param];lo=max(minimum,default-1);hi=default+1
   limits[key]=[lo,hi]
   if enabled:
    delta=layout.integer(inputs.get(key+'_delta',0),-1,1,key+' change')
    inputs[key]=layout.integer(inputs.get(key,default+delta),lo,hi,key+' near selected preset')
   else:inputs[key]=default
  if enabled and 'depth_cells' in inputs and inputs['depth_cells']!=defaults['room_depth_steps']:raise ValueError('Custom width is fixed to selected preset (2400 mm)')
  inputs['depth_cells']=defaults['room_depth_steps']
  if not enabled:inputs.update(sauna=True,entrance=True,outdoor=defaults['storage'],sauna_entrance=2,entrance_outdoor=3,sauna_outdoor=0,arrangement=0)
  programme=layout.programme(**{k:inputs.get(k,d) for k,d in [('sauna',True),('entrance',True),('outdoor',defaults['storage']),('sauna_cells',3),('entrance_cells',3),('outdoor_cells',1),('depth_cells',2)]})
  graph=layout.relationships(programme,**{k:inputs.get(k,d) for k,d in [('sauna_entrance',2),('entrance_outdoor',3),('sauna_outdoor',0)]})
  arrangement=layout.integer(inputs.get('arrangement',0),0,5,'arrangement')
 else:
  graph=None;arrangement=0
 settings={k:inputs.get(k,d) for k,d in [('roof_type',1),('window_width',1180),('wall_height',2100),('foundation_type',0),('include_foundation',True),('window_shift',0)]}
 for k,allowed in [('roof_type',(0,1)),('window_width',(580,880,1180)),('wall_height',(2100,2700)),('foundation_type',(0,1)),('window_shift',(-1,0,1))]:
  if type(settings[k]) not in (int,float) or settings[k] not in allowed:raise ValueError('Unsupported '+k)
  settings[k]=int(settings[k])
 if type(settings['include_foundation']) is not bool:raise ValueError('Foundation inclusion must be Boolean')
 result=dict(schema='obtp-sauna-selection/1',preset_index=index,preset_name=PRESETS[index],custom=index in (6,13),graph=graph,arrangement=arrangement,cassette_settings=settings,preserve_legacy_shower=index<6)
 if index==6:result.update(base_preset=base,use_overrides=enabled,dimension_limits=limits)
 if index==13:
  base=layout.integer(inputs.get('base_preset',2),0,5,'Studio base preset')
  enabled=inputs.get('use_overrides',False)
  if type(enabled) is not bool:raise ValueError('Use overrides must be Boolean; False resets to selected preset')
  defaults=parameters(base,program_type=1)
  if enabled and 'depth_cells' in inputs and inputs['depth_cells']!=defaults['room_depth_steps']:raise ValueError('Custom width is fixed to selected preset (2400 mm)')
  changes={}
  for key,name,lo,hi in [('sauna_length_steps','work_cells',3,6),('hall_length_steps','centre_cells',2,3),('storage_length_steps','preparation_cells',2,3)]:
   default=defaults[key]
   delta=layout.integer(inputs.get(name+'_delta',0),-1,1,name+' change') if enabled else 0
   value=layout.integer(inputs.get(name,default+delta),max(lo,default-1),min(hi,default+1),name+' (within one 900 mm cell of selected preset)') if enabled else default
   changes[key]=value
  result.update(base_preset=base,use_overrides=enabled,studio_dimensions=changes,reset='Set Use overrides False to restore the selected preset dimensions')
 result['selection_sha256']=layout.digest(result)
 return result

def resolve(selection):
 source=copy.deepcopy(selection);claimed=source.pop('selection_sha256',None)
 if claimed!=layout.digest(source):raise ValueError('Preset selection changed without validation')
 if source.get('schema')!='obtp-sauna-selection/1':raise ValueError('Unsupported preset input')
 plan=studio_plan(source) if source['preset_index']>=7 else layout.solve(source['graph'],source['arrangement'])
 return dict(schema='obtp-sauna-layout/1',selection=copy.deepcopy(selection),plan=plan,system='cassette',status='construction-compatible' if plan['construction_compatible'] else 'plan-only')

def construct(document):
 from .plan_pipeline import construct as generate
 return generate(document)


def studio_config(selection):
 p=parameters(selection.get('base_preset',selection['preset_index']-7),program_type=1)
 if selection['preset_index']==13:
  p.update(selection['studio_dimensions'])
  p['id']='studio-plan-'+layout.digest(selection)[:10]
  p['size']='CUSTOM'
 p.update(selection['cassette_settings'])
 return p

def studio_plan(selection):
 """Resolve saved Studio zoning without constructing a hidden 3D building."""
 from . import cells
 p=studio_config(selection);W,L,hot,hall,annex=cells.resolve(p);z=p['studio_zones']
 bs,be=z['bridge_start'],z['bridge_end']
 rooms=[dict(id=name,bounds_mm=[a,0,b-a,W],zone='interior') for name,a,b in [('work',0,bs),('centre',bs,be),('preparation',be,L)]]
 programme=dict(active={r['id']:True for r in rooms},holds=[])
 graph=dict(programme=programme,edges=[dict(a='work',b='centre',kind='passage'),dict(a='centre',b='preparation',kind='passage')])
 openings=[]
 for name,base,axis,length,width in [('studio-left-entry',[bs-195,0],'y',W,p['door_width']),('studio-right-entry',[be,0],'y',W,p['door_width']),('front',[z['right_start'],0],'x',z['right_clear'],p['door_width']),('front-window',[195,0],'x',hot,p['window_width']+20)]:
  k=0 if axis=='x' else 1;fit=cells.opening(base[k],base[k]+length,cells.X if k==0 else cells.Y,width,base[k]+(length-width)//2)
  if name=='front-window':fit=cells.shifted_opening(base[k],base[k]+length,cells.X,width,base[k]+(length-width)//2,p.get('window_shift',0))
  o=list(base);o[k]+=fit['start'];openings.append(dict(id=name+'/opening',kind='window' if name=='front-window' else 'entrance',origin_mm=o,axis=axis,width_mm=width))
 plan=dict(schema='obtp-resolved-plan/1',programme=programme,graph=graph,arrangement=0,candidate_count=1,candidate_orders=[['work','centre','preparation']],rooms=rooms,finished_room_rectangles=[],openings=openings,bounds_mm=[0,0,L,W],construction_compatible=True,holds=['Studio strip topology: work -> heated centre -> preparation; dimensions are plan inputs. Arbitrary room topology is unsupported.','Storage changes the existing Studio equipment programme; it does not remove the preparation room.','Supplier, structural and lifting acceptance remain unresolved.'])
 plan['plan_sha256']=layout.digest(plan)
 return plan
