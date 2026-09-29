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

def skeleton(plan,system=0,roof_type=0,foundation_type=0,terrace=True):
 from .room_assemblies import box,foundation,roof,assemble
 return assemble(box(plan,system),foundation(plan,foundation_type,terrace),roof(plan,roof_type,terrace))


def scene(skeleton,parts,detail):
 s=rc.require(skeleton,'skeleton');p=s['plan'];h=hashlib.sha256(json.dumps(parts,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 ids=[v['id'] for v in parts]
 if len(set(ids))!=len(ids):raise ValueError('Duplicate generated part ID')
 from .documentation import axon,volume
 result=dict(schema='obtp-room-scene/1',version='GH-R31-ROOM-CONFIG',display_revision='GH-R31',status='geometry-study-not-engineered',document_date='2026-09-28',config=dict(id='rooms-'+p['sha256'][:10],program_type=p['building_type'],size='CUSTOM'),plan=p,dimensions=s['dimensions'],wall_regions=s['wall_regions'],opening_voids=s['opening_voids'],interfaces=s['interfaces'],parts=parts,detail=detail,holds=rc.HOLDS+['No automatically selected windows, equipment or services. This is a layout/construction study, not a habitable building specification.','Weather-cover attachment and ventilation, waterproofing and vapour layers require design; sheet/lining choices are geometry studies.'],checks=dict(unique_ids=True,positive_dimensions=all(min(v['size'])>0 for v in parts)),geometry_sha256=h)
 result['manufacturing']=analyse(result,True)
 wood={m:sum(volume(v) for v in parts if v['material']==m) for m in ('timber','plywood','cladding-wood','lining-wood','deck-wood')};result['metrics']=dict(wood_m3=wood,total_wood_m3=sum(wood.values()))
 result['drawings']=dict(source_geometry_sha256=h,views={'room-plan':rc.plan_view(p),'axon':axon(parts)})
 return result
