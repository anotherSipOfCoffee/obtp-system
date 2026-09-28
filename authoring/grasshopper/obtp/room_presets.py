"""Preset source of plans. Downstream stages consume data, never preset selectors."""
import copy
from . import room_config as rc, model, cells
TYPES=('Sauna','Studio','Living studio / study')
SIZES=('S','M','L')
WINDOWS=((580,900),(1180,1800))

def reseal(plan,**changes):
 data=copy.deepcopy(plan);data.pop('sha256',None);data.pop('schema',None);data.pop('stage',None);data.update(changes)
 return rc.seal('plan',**data)

def window_commands(name,base,axis,length,frame,F,depth=195):
 k=0 if axis=='x' else 1;n=1-k;rough=frame+20
 fit=cells.opening(base[k],base[k]+length,cells.X if k==0 else cells.Y,rough,base[k]+(length-rough)/2)
 command=dict(kind='wall',args=[name,base,axis,length],kwargs=dict(door=[fit['start'],rough],side_skin=-1 if base[n]==0 else 1))
 parts=[];origin=base+[F+10];origin[k]+=fit['start']+10;origin[n]+=12.5
 for label,u,z,a,h in [('left',0,0,51,1880),('right',frame-51,0,51,1880),('bottom',51,0,frame-102,51),('top',51,1829,frame-102,51),('glass',51,51,frame-102,1778)]:
  o=origin[:];o[k]+=u;o[2]+=z;sz=[0,0,h];sz[k]=a;sz[n]=4 if label=='glass' else 170
  parts.append(dict(kind='part',args=[name+'-product/'+label,o,sz,'glass' if label=='glass' else 'object','walls'],kwargs={}))
 return command,parts

from .room_blueprint import runs_from_commands

def generate(building_type=0,size=1,extension=True,window=1):
 t=rc.integer(building_type,0,2,'Preset');size=rc.integer(size,0,2,'Size');wi=rc.integer(window,0,1,'Window host')
 if type(extension) is not bool:raise ValueError('Extension must be Boolean')
 frame,host=WINDOWS[wi]
 if t==2:
  # Retain the only previously generated living study; sizes are bounded variants.
  functions=[16,6,13] if extension else [16,6]
  plan=rc.solve(rc.rules(rc.rules(rc.programme(t,functions)),['R01 R03 open'] if extension else [],'boundary'),length_cells=(8+size if extension else 6+size))
  runs=rc.wall_runs(plan)
  run=next(r for r in runs if r['id']=='R01-back');base=run['base'][0];fit=cells.opening(base,base+run['length'],900,frame+20,base+(run['length']-frame-20)/2)
  run.update(door_width=frame+20,opening_start=fit['start'],opening_origin=[base+fit['start'],run['base'][1]],kind='window')
  return reseal(plan,wall_runs=runs,preset_label=TYPES[t]+' '+SIZES[size],extension=extension,window_frame_mm=frame,window_host_mm=host,study_note='Living study: equipment, accessibility and dwelling acceptance unresolved')
 p=model.parameters(size*2+int(extension),program_type=t,roof_type=0,window_width=frame,studio_winter_closed=False)
 ctx=model.prepare(p);commands=model.arrange(ctx)
 if t==0:
  lengths=[ctx['hot']+195,ctx['L']-ctx['hot']-195]+([ctx['annex']] if extension else [])
  functions=[7,0]+([2] if extension else []);labels=['Sauna','Entrance']+(['Extension / storage + shower + bench'] if extension else [])
 else:
  z=ctx['p']['studio_zones'];lengths=[z['bridge_start'],z['bridge_end']-z['bridge_start']]+([ctx['L']-z['bridge_end']] if extension else [])
  functions=[10,1]+([12] if extension else []);labels=['Workspace','Central passage' if extension else 'Central room / two windows']+(['Extension / preparation'] if extension else [])
  if not extension:
   # Retain work and centre, remove the right block at generation, not by hiding it.
   L=z['bridge_end'];W=ctx['W'];F=ctx['F']
   commands=[c for c in commands if not (c['kind']=='wall' and c['args'][0] in ('studio-right-entry','front','studio-right-back','hall-end')) and not (c['kind']=='part' and c['args'][0].startswith(('studio-preparation','studio-storage')))]
   commands.append(dict(kind='wall',args=['hall-end',[L-195,0],'y',W],kwargs={}))
   for name,y in [('front-window',0),('back-window',W-195)]:
    # The workspace already owns front-window; rename that original host first.
    if name=='front-window':
     for c in commands:
      if c['kind']=='wall' and c['args'][0]=='front-window':c['args'][0]='workspace-window'
    wall,products=window_commands(name,[z['bridge_start'],y],'x',L-z['bridge_start']-195,frame,F)
    commands.extend([wall]+products)
   ctx.update(L=L,annex=0,studio=False,inside_length=L-390,area=(L+24)*(W+24)/1e6)
   ctx['p'].update(program_type=0,storage=False,layout_main_length_mm=L)
   ctx['plan_rooms']=ctx['p']['layout_rooms']=[dict(id='workspace',bounds_mm=[0,0,lengths[0],W],clear_bounds_mm=[195,195,lengths[0]-390,W-390]),dict(id='centre',bounds_mm=[lengths[0],0,lengths[1],W],clear_bounds_mm=[lengths[0]+195,195,lengths[1]-390,W-390])]
   for room in ctx['plan_rooms']:room['structural_clear_x_mm']=[room['clear_bounds_mm'][0],room['clear_bounds_mm'][0]+room['clear_bounds_mm'][2]]
   for cmd in commands:
    if cmd['kind']=='wall' and cmd['args'][0]=='hot-end':cmd['kwargs']['door']=[(W-900)/2,900]
   # No hidden studio seasonal recipe: windows are explicit commands in this plan.
 rooms=[];x=0
 for i,(length,function,label) in enumerate(zip(lengths,functions,labels)):
  rooms.append(dict(id='R%02d'%(i+1),function=function,label=label,bounds_mm=[x,0,length,ctx['W']],clear_bounds_mm=[x+195,195,max(1,length-390),ctx['W']-390]));x+=length
 edges=[dict(a=rooms[i]['id'],b=rooms[i+1]['id'],boundary='opening') for i in range(len(rooms)-1)]
 runs=runs_from_commands(commands)
 return rc.seal('plan',building_type=t,rooms=rooms,edges=edges,entries=[],bounds_mm=[0,0,x,ctx['W']],area_m2=x*ctx['W']/1e6,entrance_side='front',arrangement=0,candidate_orders=[[r['id'] for r in rooms]],preset_label=TYPES[t]+' '+SIZES[size],extension=extension,window_frame_mm=frame,window_host_mm=host,wall_runs=runs,construction=dict(schema='obtp-cassette-blueprint/1',context=ctx,commands=commands),holds=rc.HOLDS)
