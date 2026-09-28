"""R23 constrained room graph -> rectangular plan -> guarded legacy adapter.
The planning contract is independent of Rhino and of manufactured part geometry.
"""
import copy,hashlib,json
from . import cells
ROOM_IDS=('sauna','entrance','outdoor')
PAIRS=(('sauna','entrance'),('entrance','outdoor'),('sauna','outdoor'))
KINDS=('none','adjacency','passage','external_access')

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def integer(v,lo,hi,name):
 if isinstance(v,bool) or not isinstance(v,(int,float)) or int(v)!=v or not lo<=v<=hi:raise ValueError('%s must be %d..%d'%(name,lo,hi))
 return int(v)
def programme(sauna=True,entrance=True,outdoor=True,sauna_cells=3,entrance_cells=3,outdoor_cells=1,depth_cells=2):
 active={k:v for k,v in zip(ROOM_IDS,(sauna,entrance,outdoor))}
 if any(type(v) is not bool for v in active.values()):raise ValueError('Room activation must be Boolean')
 if not any(active.values()):raise ValueError('Activate at least one room')
 sizes={k:integer(v,lo,hi,k+' cells') for k,v,lo,hi in [('sauna',sauna_cells,3,8),('entrance',entrance_cells,2,8),('outdoor',outdoor_cells,1,4)]}
 return dict(schema='obtp-room-programme/1',active=active,length_cells=sizes,depth_cells=integer(depth_cells,2,4,'depth cells'),grid_mm=[cells.X,cells.Y],outdoor_functions=['shower','storage','seating'],holds=['Outdoor zone is mixed: open shower/seating and enclosed storage. Functions retained together in this first solver.'])

def relationships(program,sauna_entrance=2,entrance_outdoor=3,sauna_outdoor=0):
 edges=[];ignored=[]
 for (a,b),kind in zip(PAIRS,(sauna_entrance,entrance_outdoor,sauna_outdoor)):
  kind=KINDS[integer(kind,0,3,'relationship')]
  if kind=='none':continue
  if not program['active'][a] or not program['active'][b]:ignored.append(a+' / '+b+' ignored because a room is inactive');continue
  if 'outdoor' in (a,b) and kind=='passage':raise ValueError('Outdoor zone uses external access, not an invented internal doorway')
  edges.append(dict(a=a,b=b,kind=kind))
 return dict(schema='obtp-room-graph/1',programme=copy.deepcopy(program),edges=edges,notes=ignored)

def _rect(x,y,w,h):return [x,y,w,h]
def _touch(a,b):
 x,y,w,h=a;u,v,s,t=b
 return ((abs(x+w-u)<1e-6 or abs(u+s-x)<1e-6) and min(y+h,v+t)>max(y,v)) or ((abs(y+h-v)<1e-6 or abs(v+t-y)<1e-6) and min(x+w,u+s)>max(x,u))
def solve(graph,arrangement=0):
 """Enumerate six bounded strip orders. Explicit adjacency must be satisfied.
 Default order reproduces existing Sauna cell envelopes. Reversing is plan-only.
 """
 from itertools import permutations
 p=copy.deepcopy(graph['programme']);active=[r for r in ROOM_IDS if p['active'][r]]
 orders=list(permutations(active));arrangement=integer(arrangement,0,5,'arrangement')
 candidates=[];width=p['depth_cells']*cells.Y
 for order in orders:
  x=0;rooms=[]
  for r in order:
   n=p['length_cells'][r]*cells.X;rooms.append(dict(id=r,bounds_mm=_rect(x,0,n,width),zone='mixed outdoor/storage' if r=='outdoor' else 'interior'));x+=n
  lookup={r['id']:r for r in rooms}
  if any(e['kind'] in ('adjacency','passage') and not _touch(lookup[e['a']]['bounds_mm'],lookup[e['b']]['bounds_mm']) for e in graph['edges']):continue
  # Keep a single outdoor zone at a terminal, never through the indoor circulation.
  if 'outdoor' in order and len(order)>2 and order.index('outdoor')==1:continue
  candidates.append(rooms)
 if not candidates:raise ValueError('No strip layout satisfies these adjacency requirements; remove a conflicting edge')
 if arrangement>=len(candidates):raise ValueError('Available arrangement indices: 0..'+str(len(candidates)-1))
 rooms=candidates[arrangement];order=[r['id'] for r in rooms];total=sum(r['bounds_mm'][2] for r in rooms)
 warnings=list(p['holds'])+list(graph['notes']);openings=[];wall=195;partition=90
 normal=order in (['sauna','entrance'],['sauna','entrance','outdoor'])
 connected=any(e['kind']=='passage' and {e['a'],e['b']}=={'sauna','entrance'} for e in graph['edges'])
 # This first construction bridge accepts only the proven legacy topology.
 compatible=normal and connected
 clear=[]
 if normal:
  hot=p['length_cells']['sauna']*cells.X;main=hot+p['length_cells']['entrance']*cells.X
  clear=[dict(id='sauna',bounds_mm=[wall+36,wall+36,hot-wall-72,width-2*wall-72]),dict(id='entrance',bounds_mm=[hot+partition+48,wall+36,main-hot-wall-partition-84,width-2*wall-72])]
  # Match the original aperture resolver exactly, not a generic centred symbol.
  door_y=wall+int((width-2*wall-900)/2)
  internal=cells.opening(wall,width-wall,cells.Y,900,door_y)
  if connected:openings.append(dict(id='sauna-partition/opening',kind='passage',origin_mm=[hot,wall+internal['start']],axis='y',width_mm=900,status='existing canonical rough opening'))
  hall=main-hot-wall;entry=cells.opening(hot,main-wall,cells.X,900,hot+partition+(hall-partition-900)//2)
  openings.append(dict(id='front/opening',kind='entrance',origin_mm=[hot+entry['start'],0],axis='x',width_mm=900,status='existing canonical rough opening'))
 else:
  for room in rooms:
   x,y,w,h=room['bounds_mm'];clear.append(dict(id=room['id'],bounds_mm=[x+wall+36,y+wall+36,w-2*wall-72,h-2*wall-72],status='provisional perimeter deduction; partition build-up unresolved'))
  for e in graph['edges']:
   if e['kind']=='passage':
    a=next(r for r in rooms if r['id']==e['a']);b=next(r for r in rooms if r['id']==e['b']);x=max(a['bounds_mm'][0],b['bounds_mm'][0]);openings.append(dict(id=e['a']+'-'+e['b'],kind='passage',origin_mm=[x,(width-900)/2],axis='y',width_mm=900,status='planning reservation only; host framing unresolved'))
 if not compatible:warnings.append('PLAN ONLY: construction adapter currently accepts sauna + entrance, optional terminal outdoor zone, original order and internal passage. No fabricated scene or exports are generated for this alternative.')
 if 'outdoor' in active:warnings.append('Retained default shower niche is narrow; useful clearances, waterproofing and separate outdoor function resizing remain unresolved.')
 if 'sauna' in active and 'entrance' not in active:warnings.append('Standalone sauna requires a separate exterior door, glazing and heater/circulation study; this plan is not construction-ready.')
 # An external edge is an outdoor route requirement, not proof of a door or shared wall.
 warnings.append('External access edges reserve relationships only; site paths, thresholds and clear passage remain unresolved.')
 result=dict(schema='obtp-resolved-plan/1',programme=p,graph=copy.deepcopy(graph),arrangement=arrangement,candidate_count=len(candidates),candidate_orders=[[r['id'] for r in rs] for rs in candidates],rooms=rooms,finished_room_rectangles=clear,openings=openings,bounds_mm=[0,0,total,width],construction_compatible=compatible,holds=warnings)
 result['plan_sha256']=digest(result)
 return result

def build_from_plan(plan,base_config=None,preserve_legacy_shower=False):
 """Validated bridge; never silently export a stale or unsupported room plan."""
 from .model import build,parameters
 fresh=solve(plan['graph'],plan['arrangement'])
 if digest(plan)!=digest(fresh):raise ValueError('Resolved plan was edited or is stale; regenerate from programme/graph')
 if not fresh['construction_compatible']:raise ValueError('Plan-only arrangement: construction bridge is unavailable')
 p=fresh['programme'];standard=p['length_cells']['sauna']==3 and p['depth_cells']==2 and p['length_cells']['outdoor']==1 and p['length_cells']['entrance'] in (2,3,4)
 preset={2:0,3:2,4:4}.get(p['length_cells']['entrance'],2)+int(p['active']['outdoor'])
 baseline=parameters(preset,program_type=0)
 if not standard:baseline.update(id='sauna-plan-'+fresh['plan_sha256'][:10],size='CUSTOM')
 if base_config:
  for key in ('roof_type','window_width','foundation_type','include_foundation','wall_height'):
   if key in base_config:baseline[key]=base_config[key]
 baseline.update(sauna_length_steps=p['length_cells']['sauna'],hall_length_steps=p['length_cells']['entrance'],storage_length_steps=p['length_cells']['outdoor'],room_depth_steps=p['depth_cells'],storage=p['active']['outdoor'])
 if not p['active']['outdoor'] and not preserve_legacy_shower:baseline['include_outdoor_shower']=False
 scene=build(baseline)
 if scene['dimensions']['length_mm']+scene['dimensions']['annex_length_mm']!=fresh['bounds_mm'][2] or scene['dimensions']['width_mm']!=fresh['bounds_mm'][3]:raise ValueError('Plan-to-construction footprint mismatch')
 for r in fresh['finished_room_rectangles']:
  actual=next(x for x in scene['rooms'] if x['id']==('hall' if r['id']=='entrance' else r['id']))
  if actual['clear_width_mm']!=r['bounds_mm'][2] or actual['clear_depth_mm']!=r['bounds_mm'][3]:raise ValueError('Finished room mismatch')
 for opening in fresh['openings']:
  actual=next(x for x in scene['opening_voids'] if x['id']==opening['id'])
  axis=0 if opening['axis']=='x' else 1
  if abs(actual['origin'][axis]-opening['origin_mm'][axis])>1e-6 or actual['size'][axis]!=opening['width_mm']:raise ValueError('Plan-to-construction opening mismatch')
 scene['layout_contract']=dict(plan_sha256=fresh['plan_sha256'],rooms=fresh['rooms'],source='constrained room graph',engineering_status='unchanged canonical engineering holds')
 return scene
