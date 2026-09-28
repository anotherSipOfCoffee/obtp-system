#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
# Set by the third creator; each component owns one transformation.
STAGE='programme'
core=importlib.import_module(name+'.room_config')
def val(k,default=None):
 v=globals().get(k,default)
 if hasattr(v,'Value'):v=v.Value
 return default if v is None else v
def seq(k):
 v=val(k,[])
 if isinstance(v,str):return [v]
 return [getattr(x,'Value',x) for x in v]
def read(k):return json.loads(val(k,'null'))
data_json=None;report='';rows=[]
try:
 if STAGE=='programme':
  data=core.programme(val('building_type',0),seq('functions'))
 elif STAGE=='adjacency':data=core.rules(read('upstream'),seq('rules'))
 elif STAGE=='boundaries':data=core.rules(read('upstream'),seq('rules'),kind='boundary')
 elif STAGE=='plan':data=core.solve(read('upstream'),val('length_cells',8),val('width_cells',2),val('arrangement',0),val('entrance_side',0),val('summer_passage',False))
 elif STAGE=='skeleton':
  code=importlib.import_module(name+'.room_structure');data=code.skeleton(read('upstream'),val('system',0),val('roof_type',0),val('foundation_type',0))
 elif STAGE=='detail':
  code=importlib.import_module(name+'.room_detail');data=code.build(read('upstream'),val('terrace',1),val('return_end',0),val('outdoor_shower',False),val('outdoor_bench',False),val('paneling',1),val('facade',True))
 else:raise ValueError('Unknown stage')
 data_json=json.dumps(data)
 rows=[r['id']+' | '+r['label'] for r in data.get('rooms',[]) ]
 report=STAGE.upper()+' / valid geometry input. Millimetres.'
 if STAGE in ('adjacency','boundaries'):report+='\nRules: '+str(data.get(STAGE,{}))+'\nUnspecified pairs: may share edge; if neighbours, partition with opening.'
 if STAGE=='plan':
  report+='\n'+str(data['bounds_mm'][2])+' x '+str(data['bounds_mm'][3])+' mm | '+str(data['area_m2'])+' m². This does not establish SLD exemption.\nArrangement '+str(data['arrangement'])+' / '+str(len(data['candidate_orders'])-1)+'\nOrder: '+' → '.join(r['id'] for r in data['rooms'])
  rows += [r['id']+' | '+str(r['bounds_mm'][2])+' x '+str(r['bounds_mm'][3])+' coordination mm' for r in data['rooms']]
 if STAGE=='skeleton':report+='\n'+str(len(data['parts']))+' frame/support members. Structural panels are reserved for detailing. Capacity unverified.'
 if STAGE=='detail':
  q=data['manufacturing'];report+='\n'+str(q['physical_pieces'])+' primary pieces; '+str(q['unique_manufactured_part_candidates'])+' provisional types; '+str(q['cladding']['physical_pieces'])+' separate cladding boards.\nOpenings and room minima are studies; windows/equipment/services are not automatically specified.'
except Exception as error:
 data_json=None;rows=[];report=STAGE+': '+str(error)
 import Grasshopper
 ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,report)
