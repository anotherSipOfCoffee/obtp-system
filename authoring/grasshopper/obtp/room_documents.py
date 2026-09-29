"""Scene-driven document recipes, CNC review outlines and material-only estimates."""
import copy,csv,json,math
from pathlib import Path
from . import documentation as d
from .manufacturing import schedule,cladding
from .schedule_pdf import included
from .drawings import section,dimension
from .ssp_sheets import elevation
from .room_exchange import validate

DEFAULT_RATES={
 'schema':'obtp-material-rates/1','currency':'EUR','basis':'Indicative ex-VAT proxies; retail prices divided by assumed 1.21. Not quotations.',
 'checked':'2026-09-28','waste_fraction':0.10,
 'rates':{
  'timber':{'eur_m3':475.14,'source':'https://mtmediena.lt/c24-mediena/','note':'Impregnated 45x70 C24 benchmark; proxy only for other sections and treatments.'},
  'plywood':{'eur_m3':round(70.99/1.21/(2.44*1.22*.018),2),'source':'https://www.senukai.lt/p/fanera-e-e-244-cm-x-122-cm-x-18-mm/msqd','note':'Regular retail 70.99 EUR / 2440x1220x18 E/E sheet. VAT division and transfer to other thicknesses are assumptions; structural grade unverified.'},
  'mineral-wool':{'eur_m3':round(25.90/1.21/(2.44*.2),2),'source':'https://www.senukai.lt/p/akmens-vata-rockwool-100-cm-x-61-cm-x-20-cm/100v4','note':'Regular retail 25.90 EUR / 2.44 m2 x 200 mm. Assumed retail VAT division; applicability unverified.'}}}

def estimate(scene,rates):
 if rates.get('schema')!='obtp-material-rates/1' or rates.get('currency')!='EUR':raise ValueError('Expected EUR material rates file')
 waste=rates.get('waste_fraction',0)
 if not isinstance(waste,(int,float)) or not math.isfinite(waste) or not 0<=waste<=1:raise ValueError('Waste fraction must be 0..1')
 rows=[]
 for mat in sorted(set(v['material'] for v in scene['parts'])):
  for separate in (False,True):
   parts=[v for v in scene['parts'] if v['material']==mat and cladding(v)==separate]
   if not parts:continue
   rate=rates['rates'].get(mat,{}).get('eur_m3')
   if rate is not None and (not isinstance(rate,(int,float)) or not math.isfinite(rate) or rate<0):raise ValueError('Invalid rate for '+mat)
   volume=sum(d.volume(v) for v in parts);qty=volume*(1+waste)
   rows.append(dict(material=mat,separate_cladding=separate,pieces=len(parts),net_m3=volume,allowance_m3=qty,eur_m3=rate,eur=None if rate is None else qty*rate))
 return dict(geometry_sha256=scene['geometry_sha256'],basis=rates['basis'],waste_fraction=waste,rows=rows,priced_subtotal_eur=sum(r['eur'] or 0 for r in rows),unpriced_materials=sorted(set(r['material'] for r in rows if r['eur'] is None)),excludes=['labour','machining','transport','fasteners and other unmodelled items'],rates=rates)

def part_sheets(scene,cnc=False):
 selected=[v for v in scene['parts'] if v['material']=='plywood'] if cnc else [v for v in scene['parts'] if included(v)]
 rows=schedule(selected);byid={v['id']:v for v in selected};pages=[]
 if cnc:
  p=d.page('CNC supplier instructions / REVIEW ONLY','CNC-00');pages.append(p)
  for i,note in enumerate(['1. IDs match the model and quantities. Millimetres; DXF profiles are 1:1.',
   '2. Profiles represent modelled sheet faces only. No toolpaths, offsets or nesting.',
   '3. Confirm plywood grade, stock format, grain direction and face orientation.',
   '4. Confirm joints, holes, pockets, kerf, tolerances, edge finish and tooling.',
   '5. Sloped/sheared panels remain in this schedule but are excluded from DXF.',
   '6. Do not cut before supplier and designer approve the unresolved machining.',
   '7. Quantities are constituent pieces; grouping does not certify interchangeability.']):d.text(p,25,240-i*22,note,3)
 for i,row in enumerate(rows):
  if i%6==0:pages.append(d.page('CNC sheet parts / review' if cnc else 'Parts / core, panels and insulation',('CNC-' if cnc else 'P-')+str(len(pages)+1).zfill(2)))
  p=pages[-1];x=25+(i%2)*190;y=248-(i%6//2)*64;part=byid[row['instances'][0]]
  d.text(p,x,y,row['type_id']+' | '+row['definition']['material']+' | qty '+str(row['pieces']),2.5)
  dims=' x '.join('%g'%v for v in part['size']);d.text(p,x,y-7,dims+' mm',2.4)
  view=d.axon([part])
  if cnc:
   thick,w,h=sorted(part['size']);view=dict(polygons=[dict(id=part['id'],points=[[0,0],[w,0],[w,h],[0,h]],material='plywood',cut=False)],polylines=[],labels=[],dimensions=[dimension([0,0],[w,0],-120,label='%g'%w),dimension([w,0],[w,h],120,label='%g'%h)])
  d.slot(p,row['type_id'],view,[x,y-51,x+90,y-13],(1,2,5,10,20,25,50,75,100,200))
  d.text(p,x+95,y-22,'Machining: unresolved',2.2);d.text(p,x+95,y-30,'Grain/handing: confirm',2.2)
  if part.get('slope_y') or part.get('top_slope_y'):d.text(p,x+95,y-38,'SLOPED / no cut DXF',2.2)
  d.text(p,x,y-59,'Instance: '+part['id'][:80],1.9)
 return d.finish(scene,pages,'cnc-review' if cnc else 'parts')

def project(scene):
 pages=[];p=d.page('Supaprastintas projektas / review drawings','SP-00');pages.append(p)
 lines=['Model-linked architectural review; not a complete statutory project.',
 'Site, orientation, survey, utilities and responsible designers are not supplied.',
 'Structural capacities, connection design and product compatibility are unresolved.',
 'Living Studio is a study; dwelling, fire and accessibility compliance is not verified.',
 'Plan, sections and elevations below are derived from the selected model.',
 'Only current modelled materials and geometry are represented.']
 for i,line in enumerate(lines):d.text(p,25,240-i*22,line,3)
 L=scene['dimensions']['length_mm'];W=scene['dimensions']['width_mm'];F=scene['dimensions']['floor_top_mm']
 for name,axis,level in [('Plan',2,F+1100),('Section A',0,L*.35),('Section B',1,W*.5)]:
  v=dict(polygons=[],polylines=[],dimensions=[],labels=[])
  for part in scene['parts']:
   pts=section(part,axis,level)
   if pts:v['polygons'].append(dict(id=part['id'],points=pts,material=part['material'],cut=True))
  if axis==2:
   for room in scene['plan']['rooms']:
    x,y,w,h=room['bounds_mm'];v['labels'].append(dict(at=[x+w/2,y+h/2],text=room['label'].split('/')[0]))
   v['dimensions']=[dimension([0,0],[L,0],-300),dimension([0,0],[0,W],-300)]
  p=d.page(name,'SP-'+str(len(pages)).zfill(2));pages.append(p);d.slot(p,name,v,[25,60,400,250],(25,50,75,100,150))
 for axis,positive,label in [(1,False,'Front'),(1,True,'Back'),(0,False,'West'),(0,True,'East')]:
  p=d.page(label+' elevation','SP-'+str(len(pages)).zfill(2));pages.append(p);d.slot(p,label,elevation(scene,axis,positive),[25,60,400,250],(25,50,75,100,150))
 return d.finish(scene,pages,'project-review')

def cost_sheets(scene,estimate):
 p=d.page('Approximate materials / partial priced subtotal','COST-01')
 for x,label in zip([25,135,190,255,325],['Material','Net m3','With allowance m3','EUR/m3','Amount EUR']):d.text(p,x,248,label,2.7)
 for i,r in enumerate(estimate['rows']):
  values=[r['material']+(' / CLADDING' if r['separate_cladding'] else ''),'%.3f'%r['net_m3'],'%.3f'%r['allowance_m3'],'UNPRICED' if r['eur_m3'] is None else '%.2f'%r['eur_m3'],'-' if r['eur'] is None else '%.2f'%r['eur']]
  for x,value in zip([25,135,190,255,325],values):d.text(p,x,233-i*11,value,2.7)
 d.text(p,25,75,'Priced subtotal only: %.2f EUR (indicative ex-VAT proxies)'%estimate['priced_subtotal_eur'],3)
 d.text(p,25,64,'Waste allowance: %.0f%%; not a nesting result. Unpriced items are NOT zero cost.'%(estimate['waste_fraction']*100),2.5)
 p2=d.page('Materials / assumptions and sources','COST-02')
 import textwrap
 y=248
 for line in [estimate['basis'],'Excluded: '+', '.join(estimate['excludes'])]+[m+': '+str(v.get('eur_m3'))+' EUR/m3. '+v.get('note','')+' '+v.get('source','') for m,v in estimate['rates']['rates'].items()]:
  for wrapped in textwrap.wrap(line,110):d.text(p2,25,y,wrapped,2.5);y-=8
  y-=10
 return d.finish(scene,[p,p2],'material-costs')

def cutting_files(scene,folder):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);rows=[]
 for row in schedule([v for v in scene['parts'] if v['material']=='plywood']):
  part=next(v for v in scene['parts'] if v['id']==row['instances'][0]);sizes=sorted(part['size']);status='review-outline';filename=''
  if part.get('slope_y') or part.get('top_slope_y'):status='hold-sloped-panel'
  else:
   w,h=sizes[-2:];filename=row['type_id']+'.dxf'
   pairs=[(0,'SECTION'),(2,'HEADER'),(9,'$ACADVER'),(1,'AC1015'),(9,'$INSUNITS'),(70,4),(0,'ENDSEC'),(0,'SECTION'),(2,'ENTITIES'),(0,'LWPOLYLINE'),(100,'AcDbEntity'),(8,'REVIEW_OUTLINE'),(100,'AcDbPolyline'),(90,4),(70,1)]
   for x,y in [(0,0),(w,0),(w,h),(0,h)]:pairs.extend([(10,x),(20,y)])
   pairs.extend([(0,'ENDSEC'),(0,'EOF')]);(folder/filename).write_text(''.join(str(k)+'\n'+str(v)+'\n' for k,v in pairs),encoding='utf-8')
  rows.append(dict(type_id=row['type_id'],pieces=row['pieces'],thickness_mm=sizes[0],dimensions_mm=part['size'],instances=row['instances'],profile=filename,status=status,grain='unresolved',machining='unresolved'))
 (folder/'cutting-register.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 return rows

def recipes(scene,rates):
 validate(scene,'scene');cost=estimate(scene,rates)
 return {'parts':part_sheets(scene),'assembly':d.assembly(scene,False),'parts-layout':d.parts_layout(scene,False),'project-review':project(scene),'cnc-review':part_sheets(scene,True),'material-costs':cost_sheets(scene,cost)},cost

def export(scene,destination,rates_path,native=False):
 if not str(destination).strip():raise ValueError('Select a destination folder')
 folder=Path(destination).expanduser()/('OBTP-'+scene['geometry_sha256'][:12]);folder.mkdir(parents=True,exist_ok=True)
 rates=json.loads(Path(rates_path).read_text(encoding='utf-8-sig'))
 docs,cost=recipes(scene,rates);receipts=[]
 for name,recipe in docs.items():
  (folder/(name+'-layouts.json')).write_text(json.dumps(recipe,ensure_ascii=False),encoding='utf-8')
  if native:
   from .native_drawings import bake
   receipts.append(bake(scene,folder,recipe))
  else:
   from .ssp_preview import pdf
   pdf(recipe,folder/(name+'.pdf'))
 cutting_files(scene,folder/'cnc-review');(folder/'material-costs.json').write_text(json.dumps(cost,indent=2),encoding='utf-8');(folder/'cladding-schedule.json').write_text(json.dumps(schedule([p for p in scene['parts'] if cladding(p)]),indent=2),encoding='utf-8')
 receipt=dict(folder=str(folder),geometry_sha256=scene['geometry_sha256'],documents=list(docs),native=native,native_receipts=receipts)
 (folder/'receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');return receipt

def selected_recipe(scene,kind=3,rates=None):
 """Generate only the selected preview set, rather than all document sets."""
 if kind==0:return part_sheets(scene)
 if kind==1:return d.assembly(scene,False)
 if kind==2:return d.parts_layout(scene,False)
 if kind==3:return project(scene)
 if kind==4:return part_sheets(scene,True)
 if kind==5:return cost_sheets(scene,estimate(scene,rates or DEFAULT_RATES))
 raise ValueError('Document set must be 0..5')

def modelspace(recipe,start=0,scale=10):
 """Paper-space recipe mapped to readable, tiled model-space sheet geometry."""
 from .drawings import dimension_lines
 lines=[];texts=[]
 for i,sheet in enumerate(recipe['sheets'],start):
  ox=(i%3)*460*scale;oy=-6500-(i//3+1)*330*scale
  def paper(q):return [ox+q[0]*scale,oy+q[1]*scale,0]
  for a,b in sheet['lines']:lines.append([paper(a),paper(b)])
  for t in sheet['texts']:texts.append(dict(at=paper(t['at']),text=t['text'],height=t['size']*scale))
  for detail in sheet['details']:
   v=detail['view'];x,y,X,Y=detail['box'];cx,cy=detail['center'];ratio=detail['scale']
   def point(q):return paper([(x+X)/2+(q[0]-cx)/ratio,(y+Y)/2+(q[1]-cy)/ratio])
   for polygon in v['polygons']:lines.append([point(q) for q in polygon['points']+[polygon['points'][0]]])
   for line in v['polylines']:lines.append([point(q) for q in line])
   for t in v.get('labels',[]):texts.append(dict(at=point(t['at']),text=t['text'],height=2.5*scale))
   for dim in v['dimensions']:
    strokes,at,label=dimension_lines(dim)
    for a,b in strokes:lines.append([point(a),point(b)])
    texts.append(dict(at=point(at),text=label,height=2.5*scale))
 return dict(lines=lines,texts=texts,sheets=len(recipe['sheets']),scale=scale)
