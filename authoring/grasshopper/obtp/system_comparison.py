"""One additional GH comparison component; original building pipeline stays intact."""
import copy,gzip,hashlib,json
from functools import lru_cache
from pathlib import Path
from .export import vertices,FACES,COLORS
from .manufacturing import identity,analyse
from . import plate_ribs
DATA=Path(__file__).resolve().parents[1]/'comparison_data'

@lru_cache(maxsize=1)
def source():
    data=json.loads(gzip.decompress((DATA/'wikihouse.json.gz').read_bytes()))
    data['models']=[json.loads((DATA/(p['id']+'.json')).read_text()) for p in data['objects']]
    return data

def display_faces(vertices,faces):
    # Original source assets remain unchanged. Omit zero-area tessellation faces only.
    result=[]
    for face in faces:
        a,b,c=[vertices[i] for i in face[:3]]
        u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
        cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
        if sum(x*x for x in cross)>1e-16:result.append(face)
    return result

def _value(value,choices,name):
    if isinstance(value,bool) or value not in choices:raise ValueError('Invalid '+name)
    return value

def _box_mesh(p,offset):
    return dict(id=p['id'],material=p['material'],vertices=[[v[k]+offset[k] for k in range(3)] for v in vertices(p)],faces=FACES,
      type_id='P-'+hashlib.sha256(identity(p).encode()).hexdigest()[:16],assembly=p['assembly'])

def preview(system=2,scene=None,bays=4,layer=3,panels=True,insulation=False,foundation=True,mode=0,object_index=0,explode=0,
            pitch=900,span=3600,height=2100,thickness=45,depth=240,offset=(18000,0,0),core=False):
    system=_value(system,(0,1,2),'system');layer=_value(layer,(0,1,2,3),'layer');mode=_value(mode,(0,1,2),'inspection')
    plate_ribs._integer('bays',bays,1,8);plate_ribs._integer('object_index',object_index,0,100000);plate_ribs._integer('explode',explode,0,100)
    meshes=[];report=[];catalogue=[];schedule=[];payload=None
    if system==0:
        data=source();layer_name=['floor','walls','roof','all'][layer]
        catalogue=[p['id']+' | '+p['role'] for p in data['objects']] if mode!=2 else [j['id']+' | '+j['name'] for j in data['connections']]
        if mode==0:items=data['assemblies'][str(int(bays))+'/'+layer_name]
        elif mode==1:
            if object_index>=len(data['objects']):raise ValueError('WikiHouse object index 0..'+str(len(data['objects'])-1))
            items=[dict(block=data['objects'][int(object_index)]['id'],translation=[0,0,0])]
        else:
            if object_index>=len(data['connections']):raise ValueError('WikiHouse connection index 0..'+str(len(data['connections'])-1))
            joint=data['connections'][int(object_index)];items=joint['items'];report.extend([joint['rule'],joint['evidence']])
        lookup={m['id']:m for m in data['models']}
        for i,item in enumerate(items):
            r=item.get('rotation',[1,0,0,0,1,0,0,0,1]);t=item['translation'];e=item.get('explode',[0,0,0])
            for a in lookup[item['block']]['assets']:
                vs=[[sum(r[k*3+j]*v[j] for j in range(3))+t[k]+offset[k]+e[k]*explode/100 for k in range(3)] for v in a['vertices']]
                faces=display_faces(vs,a['faces'])
                meshes.append(dict(id=item.get('instanceId',str(i))+'/'+a['id'],vertices=vs,faces=faces,source_faces_omitted=len(a['faces'])-len(faces),material=a.get('material','plywood'),type_id=item['block']+'/'+a['id'],assembly=item.get('instanceId',str(i))))
        report.append('Zero-area source tessellation faces omitted from display copies: '+str(sum(m.get('source_faces_omitted',0) for m in meshes)))
        report+=['SYSTEM 1: WikiHouse Skylark 150; source '+data['pin'],'Rigid source mesh placement; no resizing. Module pitch 600 mm; source span 4572 mm.','Height/span/panel/insulation/foundation controls do not alter source parts.','One source roof Brep remains open. Source-asset IDs are not a verified manufacturing equivalence classification.','CC BY-SA 4.0; see WIKIHOUSE_NOTICE.md. End walls and project engineering unresolved.']
        payload=dict(source_pin=data['pin'],items=copy.deepcopy(items),scope='source mesh inspection')
    else:
        if system==1:
            if scene is None:raise ValueError('Connect the original Shared module scene_json for the Studio cassette system')
            payload=scene;report+=['SYSTEM 2: Studio-pinned canonical cassette model '+scene['version'],scene['config']['id'],
              'Building parameters come from Shared module. Modules/pitch/span/rib dimensions are B-only; no old 600 mm cassette geometry.']
        else:
            payload=plate_ribs.build(bays,pitch,span,height,thickness,depth);report+=['SYSTEM 3: B / repeated LVL plate ribs with insulation infill',json.dumps(payload['config'],sort_keys=True)]
        allparts=payload['parts'];groups={}
        for p in allparts:groups.setdefault(p['assembly'],[]).append(p)
        keys=list(groups);catalogue=['%d | %s | %d constituent pieces'%(i,k,len(groups[k])) for i,k in enumerate(keys)]
        selected=allparts
        if mode==1:
            if object_index>=len(keys):raise ValueError('Assembly-object index 0..'+str(len(keys)-1))
            selected=groups[keys[int(object_index)]]
        elif mode==2:
            if system==1:
                # Existing connected wall assemblies retain actual openings and all their constituents.
                from .wall_erection import groups as walls
                from .documentation import stage
                runs=walls(payload,stage);catalogue=['%d | %s'%(i,r['name']) for i,r in enumerate(runs)]
                if object_index>=len(runs):raise ValueError('Wall-run index 0..'+str(len(runs)-1))
                selected=runs[int(object_index)]['parts'];report.append('Connected wall interface context; no new or certified fastening geometry.')
            else:
                joints=payload['joints'];catalogue=['%d | %s | %s'%(i,j['id'],j['type']) for i,j in enumerate(joints)]
                if object_index>=len(joints):raise ValueError('Joint index 0..'+str(len(joints)-1))
                j=joints[int(object_index)];ids=set(j['parts']);selected=[p for p in allparts if p['id'] in ids];report.append(json.dumps(j,sort_keys=True))
        allowed=[{'foundation','floor'},{'foundation','floor','walls','partitions'},{'foundation','floor','walls','partitions','roof','ceiling'},None][layer]
        for p in selected:
            if allowed is not None and p['family'] not in allowed:continue
            if not panels and p['material']=='plywood':continue
            if not insulation and p['material']=='mineral-wool':continue
            if not foundation and p['family']=='foundation':continue
            if core and p['material'] not in ('timber','plywood','mineral-wool','concrete-study'):continue
            m=_box_mesh(p,offset)
            delta={'roof':(0,0,600),'walls':(0,-300 if p['origin'][1]<1000 else 300,0),'floor':(0,0,-250)}.get(p['family'],(0,0,0))
            if explode:m['vertices']=[[v[k]+delta[k]*explode/100 for k in range(3)] for v in m['vertices']]
            meshes.append(m)
        counts=analyse(payload,True);schedule=counts['primary_schedule']
        report+=['Full source (not filtered preview): %d candidate types / %d non-cladding pieces; %d assemblies. Facade separately: %d pieces.'%(counts['unique_manufactured_part_candidates'],counts['physical_pieces'],counts['assemblies_installed'],counts['cladding']['physical_pieces'])]
        report+=payload['holds']
    for m in meshes:
        rgb=COLORS.get(m['material'],(190,177,146,255))
        if core:
            digest=hashlib.sha256(m['type_id'].encode()).digest();rgb=tuple(65+v%160 for v in digest[:3])+(255,)
        m['rgba']=rgb
    report+=['Visible mesh pieces: '+str(len(meshes)),'Preview separation is not an erection simulation. Native Rhino/GH execution and structural capacity unverified.',
             'System scopes differ; no percentage part-reduction comparison is claimed.']
    return dict(schema='obtp-system-comparison/1',system=system,meshes=meshes,report='\n'.join(report),catalogue=catalogue,schedule=schedule,source=payload)
