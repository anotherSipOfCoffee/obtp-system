"""Linked object definitions; portable Python, millimetres, no GDL runtime.

Door R1 deliberately preserves the existing coordination geometry. Supplier
selection is unresolved. Structural apertures stay with the host wall recipe.
"""
import hashlib
import json
import math
from pathlib import Path

DEFINITIONS = {
    'obtp.door.study': dict(revision=1, status='generic-placeholder',
        geometry='door_recipe', plan='source-dxf-door-lining',
        section='actual-model-intersection', supplier=None,
        omissions=['hardware', 'installation joint', 'certified clear opening']),
    'obtp.object.placeholder': dict(revision=1, status='generic-placeholder',
        geometry='existing-model-parts', plan='actual-model-projection',
        section='actual-model-intersection', supplier=None),
}

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def definition(key, revision=1):
    if key not in DEFINITIONS or DEFINITIONS[key]['revision'] != revision:
        raise ValueError('Unsupported object definition/revision: '+str(key))
    return dict(DEFINITIONS[key])


def door_recipe(width, height, wall_depth):
    """Local u along opening, v into wall; inherited study sizes, not product data."""
    if not all(math.isfinite(v) for v in (width,height,wall_depth)) or min(width-70,height-40,wall_depth)<=0:
        raise ValueError('Invalid door dimensions')
    v=wall_depth//2
    return [('door-jamb-left',0,v,0,30,40,height),
            ('door-jamb-right',width-30,v,0,30,40,height),
            ('door-head',30,v,height-30,width-60,40,30),
            ('door-leaf',35,v+45,5,width-70,35,height-40)]


def attach(scene):
    """Resolve placement slots to pinned definitions without mutating physical parts."""
    instances=[];claimed=set()
    for opening in scene['opening_voids']:
        if 'window' in opening['id']:continue
        prefix=opening['id'].rsplit('/',1)[0]
        ids=[p['id'] for p in scene['parts'] if p['id'].startswith(prefix+'/door-')]
        if len(ids)!=4:raise ValueError('Incomplete door instance '+prefix)
        x,y,z=opening['origin'];a,b,h=opening['size'];axis=0 if a>b else 1
        angle=math.pi if axis==0 else -math.pi/2
        if prefix=='studio-left-entry':angle=math.pi/2
        instances.append(dict(id=prefix+'/door',definition='obtp.door.study',revision=1,
            host_opening_id=opening['id'],part_ids=ids,
            parameters=dict(rough_width_mm=a if axis==0 else b,height_mm=h,
                            state_3d='closed',symbol_state='swing-diagram'),
            placement=dict(origin_mm=[x+a/2,y+b/2,z],plan_angle_rad=angle),
            status='generic-placeholder'))
        claimed.update(ids)
    groups={}
    for part in scene['parts']:
        if part['id'] not in claimed and (part['material'] in ('object','glass') or part['family']=='furniture'):
            # Window frame and glazing form a single replaceable slot.
            key='window' if part['id'].startswith('window/') else part['assembly']
            groups.setdefault(key,[]).append(part)
    for key,parts in sorted(groups.items()):
        lo=[min(p['origin'][k] for p in parts) for k in range(3)]
        hi=[max(p['origin'][k]+p['size'][k] for p in parts) for k in range(3)]
        instances.append(dict(id=key+'/object',definition='obtp.object.placeholder',revision=1,
            part_ids=[p['id'] for p in parts],placement=dict(origin_mm=lo),
            parameters=dict(bounds_mm=[hi[k]-lo[k] for k in range(3)]),status='generic-placeholder'))
    if len({i['id'] for i in instances})!=len(instances):raise ValueError('Duplicate object slot')
    from .opening_products import record
    for item in instances:
        if item['definition']=='obtp.door.study' or any(id.startswith(('window/','studio-slider-')) for id in item['part_ids']):item['product']=record(scene,item)
    symbols=json.loads(Path(__file__).with_name('symbols.json').read_text())
    record=dict(schema='obtp-object-library/1',units='mm',definitions=DEFINITIONS,
                instances=instances,symbol_source_sha256=symbols['source_sha256'])
    record['sha256']=digest(record)
    return record


def plan_symbols(library):
    source=json.loads(Path(__file__).with_name('symbols.json').read_text())
    if source['source_sha256']!=library['symbol_source_sha256']:
        raise ValueError('Object symbol source changed; regenerate model')
    result=[]
    for item in library['instances']:
        definition(item['definition'],item['revision'])
        if item['definition']!='obtp.door.study':continue
        x,y,z=item['placement']['origin_mm'];angle=item['placement']['plan_angle_rad']
        c,s=math.cos(angle),math.sin(angle);scale=item['parameters']['rough_width_mm']/900
        lines=[[[x+c*u*scale-s*v*scale,y+s*u*scale+c*v*scale] for u,v in line]
               for line in source['blocks']['Door Lining']['lines']]
        result.append(dict(instance_id=item['id'],part_ids=item['part_ids'],polylines=lines,
                           definition=item['definition'],revision=item['revision']))
    return result
