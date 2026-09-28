"""R26 checkpoint sequence: preset -> resolved plan -> cassette -> scene.
No building is generated while choosing or resolving a preset.
"""
import copy
from . import layout
from .model import parameters
PRESETS=tuple('Sauna '+n for n in ('S / no storage','S / storage','M / no storage','M / storage','L / no storage','L / storage'))+('Custom Sauna',)+tuple('Studio '+n for n in ('S / no storage','S / storage','M / no storage','M / storage','L / no storage','L / storage'))

def select(preset_index=2,**inputs):
 index=layout.integer(preset_index,0,12,'Building preset')
 if index<6:
  p=parameters(index,program_type=0)
  programme=layout.programme(sauna=True,entrance=True,outdoor=p['storage'],sauna_cells=p['sauna_length_steps'],entrance_cells=p['hall_length_steps'],outdoor_cells=p['storage_length_steps'],depth_cells=p['room_depth_steps'])
  graph=layout.relationships(programme);arrangement=0
 elif index==6:
  programme=layout.programme(**{k:inputs.get(k,d) for k,d in [('sauna',True),('entrance',True),('outdoor',True),('sauna_cells',3),('entrance_cells',3),('outdoor_cells',1),('depth_cells',2)]})
  graph=layout.relationships(programme,**{k:inputs.get(k,d) for k,d in [('sauna_entrance',2),('entrance_outdoor',3),('sauna_outdoor',0)]})
  arrangement=layout.integer(inputs.get('arrangement',0),0,5,'arrangement')
 else:
  graph=None;arrangement=0
 settings={k:inputs.get(k,d) for k,d in [('roof_type',1),('window_width',1180),('wall_height',2100),('foundation_type',0),('include_foundation',True)]}
 for k,allowed in [('roof_type',(0,1)),('window_width',(580,880,1180)),('wall_height',(2100,2700)),('foundation_type',(0,1))]:
  if type(settings[k]) not in (int,float) or settings[k] not in allowed:raise ValueError('Unsupported '+k)
  settings[k]=int(settings[k])
 if type(settings['include_foundation']) is not bool:raise ValueError('Foundation inclusion must be Boolean')
 result=dict(schema='obtp-sauna-selection/1',preset_index=index,preset_name=PRESETS[index],custom=index==6,graph=graph,arrangement=arrangement,cassette_settings=settings,preserve_legacy_shower=index<6)
 result['selection_sha256']=layout.digest(result)
 return result

def resolve(selection):
 source=copy.deepcopy(selection);claimed=source.pop('selection_sha256',None)
 if claimed!=layout.digest(source):raise ValueError('Preset selection changed without validation')
 if source.get('schema')!='obtp-sauna-selection/1':raise ValueError('Unsupported preset input')
 plan=studio_plan(source) if source['preset_index']>=7 else layout.solve(source['graph'],source['arrangement'])
 return dict(schema='obtp-sauna-layout/1',selection=copy.deepcopy(selection),plan=plan,system='cassette',status='construction-compatible' if plan['construction_compatible'] else 'plan-only')

def construct(document):
 if document!=resolve(document['selection']):raise ValueError('Layout changed or is stale; resolve it before construction')
 selection=document['selection'];plan=document['plan']
 if selection['preset_index']>=7:
  from .model import build
  scene=build(studio_config(selection))
  if [scene['dimensions']['length_mm'],scene['dimensions']['width_mm']]!=plan['bounds_mm'][2:]:raise ValueError('Studio plan/construction dimensions differ')
  scene['layout_contract']=dict(plan_sha256=plan['plan_sha256'],rooms=plan['rooms'],source='saved Studio plan',engineering_status='review only')
 else:
  scene=layout.build_from_plan(plan,selection['cassette_settings'],preserve_legacy_shower=selection['preserve_legacy_shower'])
 scene['display_revision']='GH-R26-CHECKPOINTS'
 scene['layout_contract'].update(workflow='preset -> layout -> cassette -> 3D',preset_index=selection['preset_index'],preset_name=selection['preset_name'],selection_sha256=selection['selection_sha256'])
 return scene


def studio_config(selection):
 p=parameters(selection['preset_index']-7,program_type=1)
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
  o=list(base);o[k]+=fit['start'];openings.append(dict(id=name+'/opening',kind='window' if name=='front-window' else 'entrance',origin_mm=o,axis=axis,width_mm=width))
 plan=dict(schema='obtp-resolved-plan/1',programme=programme,graph=graph,arrangement=0,candidate_count=1,candidate_orders=[['work','centre','preparation']],rooms=rooms,finished_room_rectangles=[],openings=openings,bounds_mm=[0,0,L,W],construction_compatible=True,holds=['Saved Studio zoning; room graph editing is currently Sauna-only.','Storage changes the existing Studio equipment programme; it does not remove the preparation room.','Supplier, structural and lifting acceptance remain unresolved.'])
 plan['plan_sha256']=layout.digest(plan)
 return plan
