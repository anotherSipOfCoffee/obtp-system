"""R28 detailing driven by the resolved plan, with explicit geometric reservations."""
import copy
from . import room_config as rc,room_structure as rs,cells
from .plate_ribs import subtract,merge_boxes
TERRACES=('None','Entrance side','Two opposite sides','L / entrance and one return','U / both long sides and one short side')

def terrace_rects(plan,mode,end):
 mode=rc.integer(mode,0,4,'Terrace');end=rc.integer(end,0,1,'Short return end');side=plan['entrance_side'];L,W=plan['bounds_mm'][2:]
 sides=[]
 if mode==1:sides=[side]
 if mode==2:sides=[side,{'front':'back','back':'front','west':'east','east':'west'}[side]]
 if mode==3:sides=[side,('west' if end==0 else 'east') if side in ('front','back') else ('front' if end==0 else 'back')]
 if mode==4:sides=['front','back',side if side in ('west','east') else ('west' if end==0 else 'east')]
 rects=[]
 if 'front' in sides:rects.append(('front',[0,-1200,L,0]))
 if 'back' in sides:rects.append(('back',[0,W,L,W+1200]))
 for label,a,b in [('west',-1200,0),('east',L,L+1200)]:
  if label in sides:rects.append((label,[a,-1200 if 'front' in sides else 0,b,W+1200 if 'back' in sides else W]))
 return rects

def deck(parts,rects,F,L,W):
 for name,(a,b,c,d) in rects:
  joists=cells.transverse_members(a,c);joints=[a]+[x for x in joists if a+100<x<c-100 and abs(x%1800)<1e-6]+[c]
  # Boundary and grid seam members all share the canonical 45 mm floor faces.
  for i,x in enumerate(joists):rs.add(parts,'deck-'+name+'/joist-'+str(i),[x,b,0],[45,d-b,F-28],family='terrace')
  for j,y in enumerate(range(b,d,100)):
   for i,(x,z) in enumerate(zip(joints,joints[1:])):rs.add(parts,'deck-'+name+'/board-%d-%d'%(j,i),[x,y,F-28],[z-x,min(95,d-y),28],'deck-wood','terrace')
 # Edge covers only on exposed boundaries; shared seams and building interfaces stay clear.
 solids=[v for _,v in rects]+[[0,0,L,W]]
 for name,rect in rects:
  a,b,c,d=rect
  for label,k,coord,lo,hi,sign in [('front',0,b,a,c,-1),('back',0,d,a,c,1),('west',1,a,b,d,-1),('east',1,c,b,d,1)]:
   intervals=[(lo,hi)]
   for other in solids:
    if other is rect:continue
    opposite=other[3 if k==0 else 2] if sign<0 else other[1 if k==0 else 0]
    if opposite!=coord:continue
    u,v=(other[0],other[2]) if k==0 else (other[1],other[3]);next_intervals=[]
    for x,z in intervals:
     if v<=x or u>=z:next_intervals.append((x,z));continue
     if x<u:next_intervals.append((x,u))
     if v<z:next_intervals.append((v,z))
    intervals=next_intervals
   for j,(u,v) in enumerate(intervals):
    for i,x in enumerate(range(int(u),int(v),1800)):
     normal=coord-22 if sign<0 else coord
     o=[x,normal,0] if k==0 else [normal,x,0];size=[min(1800,v-x),22,F-28] if k==0 else [22,min(1800,v-x),F-28]
     rs.add(parts,'deck-edge-'+name+'-'+label+'/trim-%d-%d'%(j,i),o,size,'deck-wood','terrace')

def cut_openings(box,run,F,H):
 boxes=[box]
 if run.get('door_width'):
  k=0 if run['axis']=='x' else 1;o=[-10000,-10000,F];size=[20000,20000,1900]
  o[k]=run['opening_origin'][k];size[k]=run['door_width']
  boxes=[piece for b in boxes for piece in subtract(b,dict(origin=o,size=size))]
 return boxes

def layer(parts,run,F,H,offset,thickness,material,family,prefix,vertical=True):
 k=0 if run['axis']=='x' else 1;n=1-k
 if vertical:
  count=int((run['length']+99)//100);rows=[(i*100,0,min(95,run['length']-i*100),H) for i in range(count)]
 else:rows=[(0,z,run['length'],min(45,H-z)) for z in sorted(set([0,H-45]+list(range(900,H-45,900))))]
 for i,(u,z,w,h) in enumerate(rows):
  o=run['base']+[F+z];o[k]+=u;o[n]+=offset;size=[0,0,h];size[k]=w;size[n]=thickness
  for j,(a,b) in enumerate(cut_openings((o,size),run,F,H)):rs.add(parts,prefix+'/'+('board-' if family=='facade' and material=='cladding-wood' else 'member-')+str(i)+'-'+str(j),a,b,material,family,prefix)

def overlaps(a,b):return min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1])

def features(parts,plan,rects,F,shower,bench):
 if not shower and not bench:return []
 if plan['building_type']!=0:raise ValueError('Outdoor shower and bench are Sauna-only')
 if not rects:raise ValueError('Enable a terrace before outdoor features')
 L,W=plan['bounds_mm'][2:];reservations=[];features=[]
 for run in rc.wall_runs(plan):
  if not run['external'] or not run.get('door_width'):continue
  x,y=run['opening_origin'];w=run['door_width'];side=run['side']
  reservations.append([x,-1200,x+w,0] if side=='front' else [x,W,x+w,W+1200] if side=='back' else [-1200,y,0,y+w] if side=='west' else [L,y,L+1200,y+w])
 for kind,enabled,dx,dy in [('shower',shower,990,990),('bench',bench,900,450)]:
  if not enabled:continue
  choice=None
  for side,(a,b,c,d) in rects:
   for x in range(a+75,c-dx+1,75):
    for y in (b+75,d-dy-75):
     box=[x,y,x+dx,y+dy]
     if y<b or y+dy>d or any(overlaps(box,q) for q in reservations):continue
     choice=(side,box);break
    if choice:break
   if choice:break
  if not choice:raise ValueError(kind+': no terrace reservation clear of door approaches; enlarge/change terrace or room plan')
  side,(x,y,X,Y)=choice;reservations.append([x,y,X,Y]);features.append(dict(kind=kind,bounds_mm=[x,y,X-x,Y-y],side=side))
  if kind=='bench':
   for i,xx in enumerate([x,X-45]):rs.add(parts,'outdoor-bench/leg-'+str(i),[xx,y,F],[45,dy,400],'timber','furniture')
   for i,yy in enumerate(range(int(y),int(Y),100)):rs.add(parts,'outdoor-bench/seat-'+str(i),[x,yy,F+400],[dx,min(95,Y-yy),28],'deck-wood','furniture')
   for i,z in enumerate(range(0,400,100)):
    rs.add(parts,'outdoor-bench/front-'+str(i),[x,y-22,F+z],[dx,22,95],'lining-wood','furniture')
    for label,xx in [('a',x-22),('b',X)]:rs.add(parts,'outdoor-bench/end-'+label+'-'+str(i),[xx,y,F+z],[22,dy,95],'lining-wood','furniture')
  else:
   # Three-sided screen with open approach; no invented plumbing or waterproof tray.
   for i,(xx,yy) in enumerate([(x,y),(X-45,y),(x,Y-45),(X-45,Y-45)]):rs.add(parts,'outdoor-shower/post-'+str(i),[xx,yy,F],[45,45,1900],'timber','furniture')
   for i,z in enumerate(range(0,1900,100)):rs.add(parts,'outdoor-shower/screen-'+str(i),[x,y,F+z],[dx,22,95],'lining-wood','furniture')
   for i,z in enumerate(range(0,1900,100)):
    for label,xx in [('a',x-22),('b',X)]:rs.add(parts,'outdoor-shower/side-'+label+'-'+str(i),[xx,y,F+z],[22,dy,95],'lining-wood','furniture')
   rs.add(parts,'outdoor-shower/fixture',[x+dx/2,y+45,F+100],[25,25,1700],'object','furniture')
 return features

def architectural_detail(skeleton,paneling):
 from . import model
 s=rc.require(skeleton,'skeleton');p=s['plan'];c=copy.deepcopy(p.get('detailing_context',p.get('construction',{}).get('context')))
 if [c['L']+c['annex'],c['W']]!=p['bounds_mm'][2:]:raise ValueError('Architectural finish zones no longer match the plan; supply updated zones or remove detailing_context')
 parts=s['parts']+s['panel_parts']+s['roof_cover_parts']+s.get('product_parts',[])+copy.deepcopy(p.get('fixtures',[]))
 state=dict(parts=parts,interfaces=s['interfaces'],opening_voids=s['opening_voids'],wall_regions=s['wall_regions'],cell_assemblies=[])
 model.enrich_stage(c,state,'surfaces')
 if s['terrace_enabled']:model.enrich_stage(c,state,'terrace')
 if paneling>=1:model.enrich_stage(c,state,'insulation')
 if paneling<2:state['parts']=[v for v in state['parts'] if v['material']!='lining-wood']
 scene=rs.scene(skeleton,state['parts'],dict(terrace_enabled=s['terrace_enabled'],paneling=paneling,facade=True,foundation_nodes=s['foundation_nodes']))
 scene['config']['size']=p.get('preset_label','Imported plan').split()[-1]
 return scene

def build(skeleton,terrace=None,return_end=0,outdoor_shower=False,outdoor_bench=False,paneling=1,facade=True):
 s=rc.require(skeleton,'skeleton')
 if terrace is None:terrace=int(s.get('terrace_enabled',True))
 if 'assembly_sources' in s and bool(terrace)!=s['terrace_enabled']:raise ValueError('Terrace changes belong upstream in Foundation and Roof; regenerate both branches')
 if s['plan'].get('detailing_context') or s['plan'].get('construction'):
  return architectural_detail(skeleton,rc.integer(paneling,0,2,'Panel build-up'))
 s=rc.require(skeleton,'skeleton');paneling=rc.integer(paneling,0,2,'Panel build-up')
 for name,v in [('Facade',facade),('Outdoor shower',outdoor_shower),('Outdoor bench',outdoor_bench)]:
  if type(v) is not bool:raise ValueError(name+' must be Boolean')
 p=s['plan'];L,W=p['bounds_mm'][2:];F=s['dimensions']['floor_top_mm'];H=s['dimensions']['wall_height_mm']
 parts=copy.deepcopy(s['parts'])+copy.deepcopy(s['panel_parts'])+copy.deepcopy(s['roof_cover_parts']);rects=terrace_rects(p,terrace,return_end);deck(parts,rects,F,L,W)
 limits=[r for _,r in rects]+[[0,0,L,W]];bbox=[min(r[0] for r in limits),min(r[1] for r in limits),max(r[2] for r in limits),max(r[3] for r in limits)]
 if 'assembly_sources' in s:
  b=s['foundation_bounds_mm']
  if any(bbox[i]<b[i] for i in (0,1)) or any(bbox[i]>b[i] for i in (2,3)):raise ValueError('Terrace exceeds supplied foundation footprint')
  nodes=s['foundation_nodes']
 else:
  parts[:]=[v for v in parts if v['family']!='foundation'];nodes=rs.foundation(parts,bbox,s['foundation_type'])
 if paneling>=1:
  domains=[]
  for r in s['runs']:
   size=[r['length'],r['depth'],H] if r['axis']=='x' else [r['depth'],r['length'],H]
   domains.append((r['id'],r['base']+[F],size))
  domains += [('floor',[0,0,0],[L,W,220]),('roof',[0,0,F+H],[L,W,220])]
  solids=copy.deepcopy(parts)+s['opening_voids']
  for name,o,size in domains:
   boxes=[(o,size)]
   for v in solids:boxes=[q for b in boxes for q in subtract(b,v)]
   for i,(a,b) in enumerate(merge_boxes(boxes)):rs.add(parts,'infill-'+name+'/blank-'+str(i),a,b,'mineral-wool','insulation',name)
 for r in s['runs']:
  if r['external'] and facade:
   outward=-1 if r['side'] in ('front','west') else 1
   bat=-37 if outward<0 else r['depth']+12;board=-59 if outward<0 else r['depth']+37
   layer(parts,r,F,H,bat,25,'timber','facade','facade-backing-'+r['id'],False)
   layer(parts,r,F,H,board,22,'cladding-wood','facade','facade-'+r['id'])
  if paneling==2:
   inward=r['depth'] if r['side'] in ('front','west') else -14
   layer(parts,r,F,H,inward,14,'lining-wood','interior','lining-'+r['id'])
 # Purchased door envelopes are separate from fabricated opening frames.
 products=[]
 for r in s['runs']:
  if not r.get('door_width'):continue
  width=r['door_width'];k=0 if r['axis']=='x' else 1;n=1-k;o=r['opening_origin']+[F+10];o[k]+=10;o[n]+=r['depth']/2-22
  if r.get('kind')=='window':
   w=width-20
   for label,u,z,a,h in [('left',0,0,51,1880),('right',w-51,0,51,1880),('bottom',51,0,w-102,51),('top',51,1829,w-102,51),('glass',51,51,w-102,1778)]:
    pos=o[:];pos[k]+=u;pos[2]+=z;size=[0,0,h];size[k]=a;size[n]=4 if label=='glass' else 44
    rs.add(parts,'window-'+r['id']+'/'+label,pos,size,'glass' if label=='glass' else 'object','walls','window-'+r['id'])
   products.append(dict(id='window-'+r['id'],rough_opening_mm=[width,1900],frame_outside_mm=[w,1880],status='geometric placeholder; supplier compatibility unverified'))
   continue
  double=r.get('kind')=='double-door';leaf=(width-20-(10 if double else 0))/(2 if double else 1)
  for i in range(2 if double else 1):
   a=o[:];a[k]+=i*(leaf+10);size=[0,0,1880];size[k]=leaf;size[n]=44
   rs.add(parts,'door-'+r['id']+'/leaf-'+str(i),a,size,'object','walls','door-'+r['id'])
  products.append(dict(id='door-'+r['id'],rough_opening_mm=[width,1900],frame_outside_mm=None,leaf_count=2 if double else 1,clear_passage_mm=None,status='schematic placeholder; actual product, frame, threshold and tolerances unselected'))
 if not facade:
  from .checkpoints import facade_layer
  parts[:]=[v for v in parts if not facade_layer(v)]
 extras=features(parts,p,rects,F,outdoor_shower,outdoor_bench)
 return rs.scene(s,parts,dict(terraces=[dict(side=n,bounds_mm=r) for n,r in rects],features=extras,foundation_nodes=nodes,paneling=paneling,facade=facade,products=products))
