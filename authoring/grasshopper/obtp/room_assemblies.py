"""Independent geometry-driven box, foundation and detailed roof assemblies.
No preset selection, blueprint context or stored manufactured member commands.
"""
import copy,math
from . import room_config as rc,room_structure as rs,model,cells

def dimensions(plan):
 p=rc.require(plan,'plan')
 if 'construction' in p:raise ValueError('Legacy R30 blueprint plan: regenerate Layout in R31 to export geometry-only structural inputs')
 x,y,L,W=p['bounds_mm']
 if x!=0 or y!=0 or L<=0 or W<=0 or not all(math.isfinite(v) for v in (L,W)):raise ValueError('Expected positive rectangular plan at local origin')
 F=p.get('levels',{}).get('floor_top_mm',238);H=p.get('levels',{}).get('wall_height_mm',2100)
 if F!=238 or H not in (2100,2700):raise ValueError('Supported floor datum 238; wall height 2100 or 2700 mm')
 return p,dict(length_mm=L,width_mm=W,annex_length_mm=0,floor_top_mm=F,wall_height_mm=H)

def box(plan,system=0):
 rc.integer(system,0,0,'Cassette');p,dim=dimensions(plan);L=dim['length_mm'];W=dim['width_mm'];H=dim['wall_height_mm'];runs=rc.wall_runs(p)
 # Only geometric room bounds and physical wall/opening attributes drive framing.
 rooms=[dict(bounds_mm=r['bounds_mm']) for i,r in enumerate(p['rooms']) if i==0 or p['edges'][i-1]['boundary']!='open']
 context=model.prepare(dict(model.DEFAULTS,room_depth_steps=int(W/1200),wall_height=H,sauna_length_steps=3,hall_length_steps=2,storage=False,layout_main_length_mm=L,layout_rooms=rooms))
 if context['W']!=W:raise ValueError('Width must align with supported 1200 mm grid')
 context['p']['structural_partition_axes']=[r['base'][0] for r in runs if r['axis']=='y' and 0<r['base'][0]<L]
 commands=[]
 for r in runs:
  base=r['base'];axis=r['axis'];length=r['length'];depth=r['depth']
  if axis not in ('x','y') or length<=0 or depth not in (90,120,195):raise ValueError('Invalid wall geometry: '+r['id'])
  kw=dict(d=depth,family=r.get('family','walls' if r['external'] else 'partitions'),side_skin=r.get('skin_side',-1 if r['side'] in ('front','west') else 1))
  if r.get('door_width'):kw['door']=[r['opening_start'],r['door_width']]
  commands.append(dict(kind='wall',args=[r['id'],base,axis,length],kwargs=kw))
 state=model.merge_branches(context,[model.walls(context,commands),model.slabs(context)])
 # Door/product studies are deferred to detailing. Window kind is explicit.
 windowhosts=[r['id'] for r in runs if r.get('kind')=='window']
 state['parts']=[v for v in state['parts'] if not (v['material']=='object' and any(v['id'].startswith(n+'/') for n in windowhosts))]
 # Roof support over genuine open long-edge spans, derived from occupied wall intervals.
 for side,y in [('front',0),('back',W-195)]:
  intervals=sorted((r['base'][0],r['base'][0]+r['length']) for r in runs if r['axis']=='x' and r['base'][1]==y)
  cursor=0
  for a,b in intervals+[(L,L)]:
   if a-cursor>=900:
    id='open-edge-'+side+'/header-'+str(int(cursor))
    rs.add(state['parts'],id,[cursor,y,dim['floor_top_mm']+H],[a-cursor,195,220],'timber','walls')
    state['interfaces'].append(dict(id=id,type='open-edge header; bearing/connection engineering unresolved',capacity=None,fasteners=None))
   cursor=max(cursor,b)
 from .plate_ribs import subtract
 headers=[v for v in state['parts'] if v['id'].startswith('open-edge-')]
 trimmed=[]
 for part in state['parts']:
  if part['family']=='roof' and part['material']=='timber':
   boxes=[(part['origin'],part['size'])]
   for header in headers:boxes=[q for b in boxes for q in subtract(b,header)]
   for i,(o,size) in enumerate(boxes):trimmed.append(dict(part,origin=o,size=size,id=part['id'] if len(boxes)==1 else part['id']+'-cut-'+str(i)))
  else:trimmed.append(part)
 state['parts']=trimmed
 timber=[v for v in state['parts'] if v['material']=='timber'];panels=[v for v in state['parts'] if v['material']=='plywood'];products=[v for v in state['parts'] if v['material'] not in ('timber','plywood')]
 return rc.seal('box',source=p['sha256'],plan=p,parts=timber,panel_parts=panels,product_parts=products,runs=runs,dimensions=dim,opening_voids=state['opening_voids'],wall_regions=state['wall_regions'],interfaces=state['interfaces'])

def foundation(plan,foundation_type=0,terrace=True):
 p,dim=dimensions(plan);kind=rc.integer(foundation_type,0,1,'Foundation')
 if type(terrace) is not bool:raise ValueError('Terrace must be Boolean')
 L,W=dim['length_mm'],dim['width_mm']
 bounds=p.get('platform_bounds_mm',[0,-1200,L,W]) if terrace else p.get('floor_bounds_mm',[0,0,L,W])
 parts=[];nodes=rs.foundation(parts,bounds,kind)
 return rc.seal('foundation',source=p['sha256'],parts=parts,dimensions=dim,foundation_type=kind,terrace=terrace,nodes=nodes,bounds_mm=bounds)

def roof(plan,roof_type=0,terrace=True):
 from .envelope import enrich
 p,dim=dimensions(plan);kind=rc.integer(roof_type,0,1,'Roof')
 if type(terrace) is not bool:raise ValueError('Terrace must be Boolean')
 L,W,F,H=[dim[k] for k in ('length_mm','width_mm','floor_top_mm','wall_height_mm')]
 settings=dict(model.DEFAULTS,program_type=0,roof_type=kind,wall_height=H,terrace_steps=2 if terrace else 0,roof_west_extension_mm=p.get('roof_west_extension_mm',0))
 parts=[];interfaces=[]
 info=enrich(settings,parts,[],interfaces,L,W,F,H,0,[],phase='roof',terrace_area=0)
 return rc.seal('roof',source=p['sha256'],parts=parts,interfaces=interfaces,dimensions=dim,roof_type=kind,terrace=terrace,roof_info=info)

def assemble(box_data,foundation_data,roof_data):
 b=rc.require(box_data,'box');f=rc.require(foundation_data,'foundation');r=rc.require(roof_data,'roof')
 if len({x['source'] for x in (b,f,r)})!=1:raise ValueError('Assembly inputs belong to different plans')
 if f['terrace']!=r['terrace']:raise ValueError('Roof and foundation terrace settings disagree')
 if not b['dimensions']==f['dimensions']==r['dimensions']:raise ValueError('Assembly dimensions disagree')
 structural=[p for p in r['parts'] if p['material']=='timber']
 roofpanels=[p for p in r['parts'] if p['material']=='plywood']
 finish=[p for p in r['parts'] if p['material'] not in ('timber','plywood')]
 return rc.seal('skeleton',plan=b['plan'],runs=b['runs'],parts=b['parts']+f['parts']+structural,panel_parts=b['panel_parts']+roofpanels,roof_cover_parts=finish,product_parts=b['product_parts'],opening_voids=b['opening_voids'],wall_regions=b['wall_regions'],interfaces=b['interfaces']+r['interfaces'],dimensions=b['dimensions'],roof_type=r['roof_type'],foundation_type=f['foundation_type'],foundation_nodes=f['nodes'],foundation_bounds_mm=f['bounds_mm'],terrace_enabled=f['terrace'],assembly_sources={k:x['sha256'] for k,x in [('box',b),('foundation',f),('roof',r)]},holds=rc.HOLDS)
