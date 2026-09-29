"""Construction-only specimens. No rooms, equipment or building programmes.
WikiHouse remains rigid pinned source geometry; research controls never stretch it.
"""
import copy
from . import model,cells,plate_ribs,system_comparison
from .manufacturing import analyse
KINDS=('wall','floor','roof','opening','corner','interface')

def cassette(kind=0,bays=3,span=2400,height=2100,sheet=12,depth=195):
 kind=plate_ribs._integer('specimen',kind,0,5)
 bays=plate_ribs._integer('bays',bays,2,6)
 span=plate_ribs._integer('span',span,2400,4800)
 if span%1200:raise ValueError('Cassette span must increment by 1200 mm')
 if height not in (2100,2700):raise ValueError('Cassette height must be 2100 or 2700 mm')
 if sheet not in (12,18):raise ValueError('Research sheet thickness must be 12 or 18 mm')
 if depth not in (145,195,220):raise ValueError('Research frame depth must be 145, 195 or 220 mm')
 # Prepare dimensions only; no building is generated. Individual specimen recipes
 # use the same wall-run and slab transformations as the canonical cassette model.
 p=model.parameters();context=model.prepare(p);context.update(L=bays*900,W=span,H=height,annex=0,skin=sheet,wall=depth,studio=False,plan_rooms=[dict(bounds_mm=[0,0,bays*900,span])])
 context['p'].update(wall_height=height,door_width=900)
 commands=[]
 def wall(name,base,axis,length,opening=False):
  kw=dict(d=depth)
  if opening:kw['door']=((length-900)/2,900)
  commands.append(dict(kind='wall',args=[name,base,axis,length],kwargs=kw))
 if kind in (0,3,4,5):wall('specimen-wall',[0,0],'x',bays*900,kind==3)
 if kind==4:wall('specimen-return',[bays*900,0],'y',span)
 result=model.slabs(context,('floor' if kind in (1,5) else 'roof',)) if kind in (1,2,5) else dict(parts=[],interfaces=[],opening_voids=[],wall_regions=[],cell_assemblies=[])
 if commands:
  wall_result=model.walls(context,commands)
  for key in result:result[key]+=wall_result[key]
 # Remove purchased joinery placeholders: this is a rough-opening framing specimen.
 parts=[p for p in result['parts'] if p['material']!='object']
 for part in parts:
  if part['family'] in ('floor','roof') and part['material']=='plywood':part['size'][2]=sheet
 # Cavity volumes are explicit candidate infill blanks, cut around actual framing.
 if kind in (0,3,4,5):
  for name,base,axis,length in [cmd['args'] for cmd in commands]:
   domain=(base+[context['F']], [length,depth,height] if axis=='x' else [depth,length,height])
   boxes=[domain]
   for solid in parts+result['opening_voids']:
    boxes=[piece for box in boxes for piece in plate_ribs.subtract(box,solid)]
   for i,(origin,size) in enumerate(plate_ribs.merge_boxes(boxes)):
    parts.append(dict(id=name+'/insulation-'+str(i),origin=origin,size=size,material='mineral-wool',family='walls',assembly=name))
 if kind in (1,2,5):
  family='floor' if kind in (1,5) else 'roof';z=0 if family=='floor' else context['F']+height
  boxes=[([0,0,z],[bays*900,span,220])]
  for solid in parts:
   if solid['family']==family:boxes=[piece for box in boxes for piece in plate_ribs.subtract(box,solid)]
  for i,(origin,size) in enumerate(plate_ribs.merge_boxes(boxes)):
   parts.append(dict(id='specimen-'+family+'/insulation-'+str(i),origin=origin,size=size,material='mineral-wool',family=family,assembly='specimen-'+family))
 scene=dict(schema='obtp-research-specimen/1',version='R27-CASSETTE-SPECIMEN',units='mm',config=dict(id='cassette-'+KINDS[kind],bays=bays,span_mm=span,height_mm=height,sheet_mm=sheet,frame_depth_mm=depth,stud_mm=45,grid_mm=[900,1200]),parts=parts,interfaces=result['interfaces'],holds=['Implemented rectangular specimen geometry; measured counts and dimensions only.','145/195/220 mm depth and 12/18 mm sheets are research choices, not approved products or structural capacities.','Opening bearing, corners, fasteners, floor-wall ties, racking and diaphragm action require engineering.','Insulation is geometric infill; thermal/moisture performance unresolved.'])
 return scene

def compare(system=1,specimen=0,bays=3,span=2400,height=2100,sheet=12,depth=195,pitch=900,thickness=45,mode=0,object_index=0,explode=0,insulation=False,core=False):
 if system==0:
  result=system_comparison.preview(0,bays=bays,mode=mode,object_index=object_index,explode=explode,offset=(0,0,0),core=core)
  result['report']+='\nCassette/B dimensions are inactive for pinned WikiHouse. Source object/connection choice is authoritative.'
  return result
 if system==1:
  scene=cassette(specimen,bays,span,height,sheet,depth)
  result=system_comparison.preview(1,scene=scene,mode=0,panels=True,insulation=insulation,explode=explode,offset=(0,0,0),core=core)
  result['report']=result['report'].replace('SYSTEM 2: Studio-pinned canonical cassette model','SYSTEM 2: canonical cassette construction specimen').replace('Building parameters come from Shared module. Modules/pitch/span/rib dimensions are B-only; no old 600 mm cassette geometry.','Research-only cassette specimen. No building, room programme or furniture is generated.')
  return result
 if system!=2:raise ValueError('System must be WikiHouse, cassette or experimental B')
 result=system_comparison.preview(2,bays=bays,pitch=pitch,span=span,height=height,thickness=thickness,depth=depth,mode=mode,object_index=object_index,explode=explode,insulation=insulation,offset=(0,0,0),core=core)
 result['report']+='\nB has wall/floor/roof ribs and knee/base interfaces. An opening/end-corner recipe is not implemented; do not infer one from the cassette specimen selector.'
 return result
