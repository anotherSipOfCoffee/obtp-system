"""Plan-only adapter to shared cassette member recipes; no preset building build."""
import copy,hashlib,json,math
from . import room_config as rc,model,cells
from .manufacturing import analyse

def add(parts,id,o,s,material='timber',family='walls',assembly=None,**extra):
 if any(not math.isfinite(v) for v in o+s) or min(s)<=0:raise ValueError('Invalid member '+id)
 parts.append(dict(id=id,origin=list(o),size=list(s),material=material,family=family,assembly=assembly or id.split('/')[0],**extra))

def foundation(parts,rect,kind):
 x0,y0,x1,y1=rect
 xs=cells.boundaries(x0,x1,1800);ys=cells.boundaries(y0,y1,1200);depth=145 if kind==0 else 300;mat='timber' if kind==0 else 'concrete-study'
 for j,y in enumerate(ys):
  for i,x in enumerate(xs):add(parts,'support-%d/pile-%d'%(j,i),[x-45,y-45,-800],[90,90,800-depth],'concrete-study','foundation','foundation')
  for i,(a,b) in enumerate(zip(xs,xs[1:])):add(parts,'support-%d/beam-%d'%(j,i),[a-45 if i==0 else a,y-72.5,-depth],[b-a+(45 if i==0 else 0)+(45 if i==len(xs)-2 else 0),145,depth],mat,'foundation','foundation')
 return [[x,y] for y in ys for x in xs]

def skeleton(plan,system=0,roof_type=0,foundation_type=0):
 if isinstance(plan,dict) and 'construction' in plan:
  from .room_blueprint import skeleton as generate
  return generate(plan,system,roof_type,foundation_type)
 p=rc.require(plan,'plan');rc.integer(system,0,0,'Cassette system');roof_type=rc.integer(roof_type,0,1,'Roof');foundation_type=rc.integer(foundation_type,0,1,'Foundation');L,W=p['bounds_mm'][2:]
 runs=rc.wall_runs(p)
 # Only reusable section/dimension preparation and member generators are called.
 params=dict(model.DEFAULTS,room_depth_steps=W//1200,sauna_length_steps=3,hall_length_steps=2,storage=False,layout_main_length_mm=L,layout_rooms=[dict(bounds_mm=r['bounds_mm']) for i,r in enumerate(p['rooms']) if i==0 or p['edges'][i-1]['boundary']!='open'],roof_type=roof_type)
 ctx=model.prepare(params);commands=[]
 for r in runs:
  kw=dict(d=r['depth'],family='walls' if r['external'] else 'partitions',side_skin=-1 if r['side'] in ('front','west') else 1)
  if r.get('door_width'):kw['door']=(r['opening_start'],r['door_width'])
  commands.append(dict(kind='wall',args=[r['id'],r['base'],r['axis'],r['length']],kwargs=kw))
 wall=model.walls(ctx,commands);slabs=model.slabs(ctx);allparts=wall['parts']+slabs['parts']
 weather(allparts,L,W,ctx['F'],ctx['H'],roof_type)
 parts=[v for v in allparts if v['material']=='timber'];panels=[v for v in allparts if v['material']=='plywood']
 nodes=foundation(parts,[0,0,L,W],foundation_type)
 # Both insulated ceiling cassettes and the sloped weather framing are visible here.
 return rc.seal('skeleton',plan=p,runs=runs,parts=parts,panel_parts=panels,roof_cover_parts=[v for v in allparts if v['material'] in ('roof-metal','roof-membrane')],opening_voids=wall['opening_voids'],wall_regions=wall['wall_regions'],interfaces=wall['interfaces']+slabs['interfaces'],dimensions=dict(length_mm=L,width_mm=W,annex_length_mm=0,floor_top_mm=ctx['F'],wall_height_mm=ctx['H']),roof_type=roof_type,foundation_type=foundation_type,foundation_nodes=nodes,holds=rc.HOLDS)

def weather(parts,L,W,F,H,kind):
 base=F+H+238;slope=1/40 if kind==0 else math.tan(math.radians(8));height=lambda y:100+slope*(W+150-y)
 # Bearing rails bear directly on the roof cassette; rafters on those rails.
 for j,y in enumerate(cells.boundaries(0,W-90,1200)):
  for i,x in enumerate(range(0,L,1800)):add(parts,'weather-seat-%d/rail-%d'%(j,i),[x,y,base],[min(1800,L-x),90,height(y)],family='roof',top_slope_y=-slope)
 xs=sorted(set([0,L-45]+list(range(900,L-45,900))))
 for i,x in enumerate(xs):add(parts,'weather/rafter-'+str(i),[x,-150,base+height(-150)],[45,W+300,145],family='roof',slope_y=-slope)
 cuts=[-150]+[x+22.5 for x in xs[1:-1]]+[L+150]
 ys=[-150]+list(range(1200,W+150,1200))+[W+150]
 for j,y in enumerate(ys[1:-1]):
  for i,(a,b) in enumerate(zip(xs,xs[1:])):add(parts,'weather-block-%d/member-%d'%(j,i),[a+45,y-22.5,base+height(y-22.5)],[b-a-45,45,145],family='roof',slope_y=-slope)
 for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
  for j,(y,z) in enumerate(zip(ys,ys[1:])):add(parts,'weather-deck-%d/panel-%d'%(i,j),[a,y,base+height(y)+145],[b-a,z-y,18],'plywood','roof',slope_y=-slope)
 # Cover is a schematic layer; compatible substrate/battens/fasteners require design.
 add(parts,'weather/cover',[-150,-150,base+height(-150)+163],[L+300,W+300,2 if kind==0 else .5],'roof-membrane' if kind==0 else 'roof-metal','roof',slope_y=-slope)

def scene(skeleton,parts,detail):
 s=rc.require(skeleton,'skeleton');p=s['plan'];h=hashlib.sha256(json.dumps(parts,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 ids=[v['id'] for v in parts]
 if len(set(ids))!=len(ids):raise ValueError('Duplicate generated part ID')
 from .documentation import axon,volume
 result=dict(schema='obtp-room-scene/1',version='GH-R30-ROOM-CONFIG',display_revision='GH-R30',status='geometry-study-not-engineered',document_date='2026-09-28',config=dict(id='rooms-'+p['sha256'][:10],program_type=p['building_type'],size='CUSTOM'),plan=p,dimensions=s['dimensions'],wall_regions=s['wall_regions'],opening_voids=s['opening_voids'],interfaces=s['interfaces'],parts=parts,detail=detail,holds=rc.HOLDS+['No automatically selected windows, equipment or services. This is a layout/construction study, not a habitable building specification.','Weather-cover attachment and ventilation, waterproofing and vapour layers require design; sheet/lining choices are geometry studies.'],checks=dict(unique_ids=True,positive_dimensions=all(min(v['size'])>0 for v in parts)),geometry_sha256=h)
 result['manufacturing']=analyse(result,True)
 wood={m:sum(volume(v) for v in parts if v['material']==m) for m in ('timber','plywood','cladding-wood','lining-wood','deck-wood')};result['metrics']=dict(wood_m3=wood,total_wood_m3=sum(wood.values()))
 result['drawings']=dict(source_geometry_sha256=h,views={'room-plan':rc.plan_view(p),'axon':axon(parts)})
 return result
