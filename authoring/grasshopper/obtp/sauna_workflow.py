"""Single R24 sequence: preset -> resolved plan -> cassette -> scene.
No building is generated while choosing or resolving a preset.
"""
import copy
from . import layout
from .model import parameters
PRESETS=('S / no storage','S / storage','M / no storage','M / storage','L / no storage','L / storage','Custom')

def select(preset_index=2,**inputs):
 index=layout.integer(preset_index,0,6,'Sauna preset')
 if index<6:
  p=parameters(index,program_type=0)
  programme=layout.programme(sauna=True,entrance=True,outdoor=p['storage'],sauna_cells=p['sauna_length_steps'],entrance_cells=p['hall_length_steps'],outdoor_cells=p['storage_length_steps'],depth_cells=p['room_depth_steps'])
  graph=layout.relationships(programme);arrangement=0
 else:
  programme=layout.programme(**{k:inputs.get(k,d) for k,d in [('sauna',True),('entrance',True),('outdoor',True),('sauna_cells',3),('entrance_cells',3),('outdoor_cells',1),('depth_cells',2)]})
  graph=layout.relationships(programme,**{k:inputs.get(k,d) for k,d in [('sauna_entrance',2),('entrance_outdoor',3),('sauna_outdoor',0)]})
  arrangement=layout.integer(inputs.get('arrangement',0),0,5,'arrangement')
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
 plan=layout.solve(source['graph'],source['arrangement'])
 return dict(schema='obtp-sauna-layout/1',selection=copy.deepcopy(selection),plan=plan,system='cassette',status='construction-compatible' if plan['construction_compatible'] else 'plan-only')

def construct(document):
 if document!=resolve(document['selection']):raise ValueError('Layout changed or is stale; resolve it before construction')
 selection=document['selection'];plan=document['plan']
 scene=layout.build_from_plan(plan,selection['cassette_settings'],preserve_legacy_shower=selection['preserve_legacy_shower'])
 scene['display_revision']='GH-R24-SAUNA-CASSETTE-WORKFLOW'
 scene['layout_contract'].update(workflow='preset -> layout -> cassette -> 3D',preset_index=selection['preset_index'],preset_name=selection['preset_name'],selection_sha256=selection['selection_sha256'])
 return scene
