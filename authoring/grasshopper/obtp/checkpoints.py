"""Inspectable stage contracts. Display filtering never changes source quantities."""
import hashlib
from collections import Counter
from .manufacturing import identity,cladding
from .preview_stages import prepare
from .documentation import stage,stage_parts
from .wall_erection import sequence

def inspect(scene):
 if scene['drawings']['source_geometry_sha256']!=scene['geometry_sha256']:raise ValueError('Drawing checkpoint is stale')
 parts=scene['parts'];counts=Counter(p['assembly'] for p in parts)
 return dict(report='CP3 / '+scene['config']['id']+'\n'+str(len(parts))+' complete-model pieces; '+str(len(counts))+' assemblies.\n'+str(sum(cladding(p) for p in parts))+' separately counted facade boards.\nGeometry / drawings hash agrees. Checks are geometric, not engineering approval.',
  rooms=[str(r) for r in scene.get('layout_contract',{}).get('rooms',scene.get('rooms',[]))],
  openings=[v['id']+' | '+str(v['size'])+' mm | '+str(v['origin']) for v in scene['opening_voids']],
  assemblies=[k+' | '+str(counts[k])+' pcs' for k in sorted(counts)],
  assembly_ids=sorted(counts),
  parts=[p['id']+' | '+p['assembly']+' | '+p['material']+' | '+str(p['size']) for p in parts],
  checks=[k+': '+('PASS' if v else 'FAIL') for k,v in scene['checks'].items()]+scene['holds'])

def assembly(scene,progress=100):
 d=prepare(scene,progress,0);palette={};used=set()
 for key in sorted({identity(p) for p in scene['parts']}):
  salt=0
  while True:
   h=hashlib.sha256((key+':'+str(salt)).encode()).digest();color=tuple(64+x*160//256 for x in h[:3])
   if color not in used:break
   salt+=1
  palette[key]=color+(255,);used.add(color)
 d['type_rgba']=[palette[identity(p)] for p in d['parts']]
 steps=sequence(scene,stage,stage_parts)
 d.update(dimensions=scene['dimensions'],schema='obtp-display-checkpoint/1',source_geometry_sha256=scene['geometry_sha256'],assembly_ids=sorted({p['assembly'] for p in scene['parts']}),steps=[str(i+1)+' / '+s['label'] for i,s in enumerate(steps)],source_piece_count=len(scene['parts']))
 return d

def structure(p):
 return p['family'] in ('floor','walls','partitions','roof','terrace','foundation') and p['material'] in ('timber','plywood','concrete-study')

def view(display,scope=2,type_colours=False,assembly_filter=''):
 if display.get('schema')!='obtp-display-checkpoint/1':raise ValueError('Connect the assembly checkpoint')
 if scope not in (0,1,2):raise ValueError('Preview scope: 0 structure, 1 building without facade boards, 2 complete')
 scope=int(scope)
 assembly_filter=assembly_filter.strip()
 if assembly_filter and assembly_filter not in display['assembly_ids']:raise ValueError('Unknown assembly ID; copy an exact ID from CP3, or clear the filter')
 select=[i for i,p in enumerate(display['parts']) if (scope==2 or scope==1 and not cladding(p) or scope==0 and structure(p)) and (not assembly_filter or p['assembly']==assembly_filter)]
 result={k:[display[k][i] for i in select] for k in ('parts','type_ids')}
 result['rgba']=[display['type_rgba' if type_colours else 'rgba'][i] for i in select]
 result['legend']=sorted(set(t+' | RGB '+','.join(str(x) for x in c[:3]) for t,c in zip(result['type_ids'],result['rgba']))) if type_colours else []
 result['status']=display['status']+'\nScope: '+('Structure + panels','Building without facade boards','Complete with cladding')[scope]+' | '+str(len(select))+' visible / '+str(display['source_piece_count'])+' canonical pieces.\nDisplay-only; quantities and exports stay complete.'
 return result
