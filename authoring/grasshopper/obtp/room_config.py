"""R28 independent bounded strip planning. Millimetres; no building preset lookup."""
import copy,itertools
from .layout import digest,integer
TYPES=('Sauna','Studio','Living studio')
# Minimums are study recipe reservations, not statutory or ergonomic standards.
FUNCTIONS=[('Entrance / vestibule',2,2),('Hall / circulation',2,2),('Storage / cupboard',1,1),('Technical / services',1,1),('WC',2,1),('Shower / washroom',2,1),('Bathroom / shower + WC',2,2),('Sauna / steam room',3,3),('Changing room',2,2),('Rest / lounge',2,3),('Workspace / creative studio',3,4),('Workshop / making',3,4),('Preparation / cleanup',2,2),('Kitchenette',2,2),('Kitchen / dining',3,3),('Living room',3,4),('Living / sleeping',3,4),('Bedroom',3,3),('Wardrobe / dressing',1,1)]
ADJ=('may','must','cannot');BOUNDARY=('open','opening','partition');SIDES=('front','back','west','east')
HOLDS=['Geometric candidate only: member capacities, bracing, joints, soil and lifting remain unverified.','Room minima are study reservations, not verified usable-space, fire, accessibility or equipment clearances.','Area/height bounds do not establish SLD or permit exemption.','Open connections do not certify a post-free load path. Door products and installation details are unselected.']

def seal(kind,**data):
 v=dict(schema='obtp-room-config/1',stage=kind,**data);v['sha256']=digest(v);return v

def require(v,kind):
 if not isinstance(v,dict):raise ValueError(kind+': missing upstream result')
 q=copy.deepcopy(v);h=q.pop('sha256',None)
 if q.get('schema')!='obtp-room-config/1' or q.get('stage')!=kind or digest(q)!=h:raise ValueError(kind+': stale or edited input; recompute upstream')
 return copy.deepcopy(v)

def programme(building_type=0,functions=(7,0,2)):
 t=integer(building_type,0,2,'Building type');functions=list(functions)
 if not 1<=len(functions)<=6:raise ValueError('Connect 1–6 function Value Lists; every list is one room')
 rooms=[];counts={}
 for i,f in enumerate(functions):
  f=integer(f,0,len(FUNCTIONS)-1,'Room function');name,minimum,weight=FUNCTIONS[f];counts[f]=counts.get(f,0)+1
  rooms.append(dict(id='R%02d'%(i+1),function=f,label=name+' '+str(counts[f]),minimum_cells=minimum,weight=weight))
 return seal('programme',building_type=t,rooms=rooms,holds=HOLDS)

def pair_rule(a,b,value,kind='adjacency'):
 a=integer(a,1,6,'Room A');b=integer(b,1,6,'Room B')
 if a==b:raise ValueError('Choose two different rooms')
 labels=ADJ if kind=='adjacency' else BOUNDARY
 value=integer(value,0,2,'Rule')
 return 'R%02d R%02d %s'%(min(a,b),max(a,b),labels[value])

def rules(program,rules=(),kind='adjacency'):
 p=require(program,'programme' if kind=='adjacency' else 'adjacency')
 valid={r['id'] for r in p['rooms']};rows={};labels=ADJ if kind=='adjacency' else BOUNDARY
 for text in rules:
  for row in str(text).splitlines():
   if not row.strip():continue
   words=row.split()
   if len(words)!=3:raise ValueError('Rule format: R01 R02 '+labels[0])
   a,b,value=words
   if a not in valid or b not in valid or a==b:raise ValueError('Rule references absent or identical rooms: '+row)
   if value not in labels:raise ValueError('Unsupported rule: '+value)
   key='|'.join(sorted((a,b)))
   if key in rows and rows[key]!=value:raise ValueError('Conflicting rules for '+key)
   rows[key]=value
 if kind=='adjacency':return seal('adjacency',building_type=p['building_type'],rooms=p['rooms'],adjacency=rows,holds=HOLDS)
 return seal('boundaries',building_type=p['building_type'],rooms=p['rooms'],adjacency=p['adjacency'],boundaries=rows,holds=HOLDS)

def solve(contract,length_cells=8,width_cells=2,arrangement=0,entrance_side=0,summer_passage=False):
 c=require(contract,'boundaries');nx=integer(length_cells,3,14,'Overall length cells');ny=integer(width_cells,2,3,'Overall width cells');side=SIDES[integer(entrance_side,0,3,'Entrance side')]
 if type(summer_passage) is not bool:raise ValueError('Summer passage must be Boolean')
 if summer_passage and c['building_type']!=1:raise ValueError('Summer passage is Studio-only')
 rooms=copy.deepcopy(c['rooms']);entry=next((r['id'] for r in rooms if r['function']==0),rooms[0]['id'])
 passage=(next((r['id'] for r in rooms if r['function']==1),None) or next((r['id'] for r in rooms if r['function']==0),None)) if summer_passage else None
 if summer_passage and passage is None:raise ValueError('Add Entrance or Hall for the Studio through-passage')
 if summer_passage and len(rooms)<3:raise ValueError('Central summer passage needs at least three rooms, with a room on each side')
 if passage:next(r for r in rooms if r['id']==passage)['minimum_cells']=max(3,next(r for r in rooms if r['id']==passage)['minimum_cells'])
 minimum=sum(r['minimum_cells'] for r in rooms)
 if nx<minimum:raise ValueError('Programme needs at least %d length cells; current %d. Enlarge the overall grid or remove a room.'%(minimum,nx))
 if (nx*900+24)*(ny*1200+24)>50e6:raise ValueError('Envelope exceeds the 50 m² study cap; this cap does not establish permit exemption')
 sizes={r['id']:r['minimum_cells'] for r in rooms}
 for _ in range(nx-minimum):
  r=max(rooms,key=lambda r:r['weight']/sizes[r['id']]);sizes[r['id']]+=1
 candidates=[];original={r['id']:i for i,r in enumerate(rooms)}
 for order in itertools.permutations(rooms):
  ids=[r['id'] for r in order]
  if passage and passage in (ids[0],ids[-1]):continue
  edges={'|'.join(sorted((a,b))) for a,b in zip(ids,ids[1:])}
  if any((v=='must' and k not in edges) or (v=='cannot' and k in edges) for k,v in c['adjacency'].items()):continue
  # A boundary instruction requests actual neighbours, rather than being ignored.
  if any(k not in edges for k in c['boundaries']):continue
  if side=='west' and ids[0]!=entry or side=='east' and ids[-1]!=entry:continue
  candidates.append((sum(abs(i-original[v]) for i,v in enumerate(ids)),ids))
 candidates.sort(key=lambda v:(v[0],v[1]));candidates=candidates[:8]
 if not candidates:raise ValueError('No single-row order satisfies neighbour rules and entrance location')
 index=integer(arrangement,0,len(candidates)-1,'Arrangement');order=candidates[index][1];byid={r['id']:r for r in rooms};placed=[];x=0;W=ny*1200;L=nx*900
 for i,key in enumerate(order):
  r=copy.deepcopy(byid[key]);width=sizes[key]*900
  edge_kind=c['boundaries'].get('|'.join(sorted((order[i-1],key))),'opening') if i else None
  left=195 if i==0 else (0 if edge_kind=='open' else 90);right=195 if i==len(order)-1 else 0
  r.update(bounds_mm=[x,0,width,W],clear_bounds_mm=[x+left,195,width-left-right,W-390]);placed.append(r);x+=width
 edges=[]
 for a,b in zip(order,order[1:]):
  key='|'.join(sorted((a,b)));edges.append(dict(a=a,b=b,adjacency=c['adjacency'].get(key,'may'),boundary=c['boundaries'].get(key,'opening')))
 # Each connected interior group has an outside entry. Closed partitions cannot trap rooms.
 groups=[[order[0]]]
 for e in edges:
  if e['boundary']=='partition':groups.append([e['b']])
  else:groups[-1].append(e['b'])
 entries=[]
 for group in groups:
  room=entry if entry in group else max(group,key=lambda k:sizes[k]);entries.append(dict(room=room,side=side if entry in group else 'front',width=900,kind='door'))
 if passage:
  entries=[e for e in entries if e['room']!=passage or e['side'] not in ('front','back')]+[dict(room=passage,side=s,width=1800,kind='double-door') for s in ('front','back')]
 result=seal('plan',building_type=c['building_type'],rooms=placed,edges=edges,bounds_mm=[0,0,L,W],grid_mm=[900,1200],candidate_orders=[v[1] for v in candidates],arrangement=index,entry_room=entry,entrance_side=side,entries=entries,summer_passage=passage,area_m2=L*W/1e6,holds=HOLDS)
 wall_runs(result) # Opening fit is checked before any 3D generation.
 return result

def plan_view(plan):
 p=require(plan,'plan');polys=[];labels=[]
 for r in p['rooms']:
  x,y,w,h=r['bounds_mm'];polys.append(dict(id=r['id'],points=[[x,y],[x+w,y],[x+w,y+h],[x,y+h]],fill=('#e4cfb5' if r['function']==7 else '#dae3d7'),material='plywood',cut=False))
  labels.append(dict(at=[x+w/2,y+h/2],text=r['id']+' '+r['label'].split('/')[0].strip(),size=85))
 lines=[]
 from .plate_ribs import subtract
 for run in wall_runs(p):
  k=0 if run['axis']=='x' else 1;size=[run['length'],run['depth'],1] if k==0 else [run['depth'],run['length'],1]
  boxes=[(run['base']+[0],size)]
  if run.get('door_width'):
   a=run['opening_origin'];b=list(a);b[k]+=run['door_width']
   cut=[run['depth'],run['depth'],1];cut[k]=run['door_width']
   boxes=[piece for box in boxes for piece in subtract(box,dict(origin=a+[0],size=cut))]
   # Opening line is offset into its host to distinguish it from the room outline.
   lines.append([a,b])
  for j,(o,z) in enumerate(boxes):
   x,y=o[:2];w,h=z[:2];polys.append(dict(id=run['id']+'-'+str(j),points=[[x,y],[x+w,y],[x+w,y+h],[x,y+h]],fill='#333333',material='timber',cut=True))

 return dict(polygons=polys,polylines=lines,labels=labels,dimensions=[])

def wall_runs(plan):
 from . import cells
 p=require(plan,'plan')
 if 'wall_runs' in p:return __import__('copy').deepcopy(p['wall_runs'])
 L,W=p['bounds_mm'][2:];runs=[]
 for r in p['rooms']:
  x,_,w,_=r['bounds_mm'];a=max(195,x);b=min(L-195,x+w)
  for side,y in [('front',0),('back',W-195)]:runs.append(dict(id=r['id']+'-'+side,room=r['id'],side=side,base=[a,y],axis='x',length=b-a,depth=195,external=True))
 for side,x in [('west',0),('east',L-195)]:runs.append(dict(id='end-'+side,room=p['rooms'][0 if side=='west' else -1]['id'],side=side,base=[x,0],axis='y',length=W,depth=195,external=True))
 for i,e in enumerate(p['edges']):
  if e['boundary']=='open':continue
  x=p['rooms'][i+1]['bounds_mm'][0]
  runs.append(dict(id='partition-'+e['a']+'-'+e['b'],room=e['b'],side='internal',base=[x,195],axis='y',length=W-390,depth=90,external=False,door_width=900 if e['boundary']=='opening' else 0,kind='passage'))
 for e in p['entries']:
  matches=[r for r in runs if r['external'] and r['side']==e['side'] and r['room']==e['room']]
  if not matches:raise ValueError('Entrance room must meet chosen outer edge')
  matches[0].update(door_width=e['width'],kind=e['kind'])
 for r in runs:
  if not r.get('door_width'):continue
  k=0 if r['axis']=='x' else 1;base=r['base'][k];width=r['door_width']
  try:fit=cells.opening(base,base+r['length'],cells.X if k==0 else cells.Y,width,base+(r['length']-width)/2)
  except ValueError:raise ValueError(r['id']+': opening and jambs do not fit; enlarge the overall length or change the room programme')
  r['opening_start']=fit['start'];r['opening_origin']=list(r['base']);r['opening_origin'][k]+=fit['start']
 return runs
