"""Auditable provisional manufacturing identities, independent of display categories.

Missing grade, machining and connection data prevent a manufacturing release.
No unknowns are silently promoted to verified interchangeability.
"""
from collections import Counter, defaultdict
import hashlib, json, re


def cladding(part):
    # Only visible facade finish boards, including the raised roof facade.
    # Battens, counterbattens, floor-edge trim and weather-edge trim stay primary.
    return (part['family']=='facade' and '/board-' in part['id']) or part['id'].startswith('roof-fascia-')


def role(a):
    name=re.sub(r'-cut-\d+$','',a['id'].split('/')[-1])
    name=re.sub(r'-(left|right|front|back|top|bottom|a|b)(?=-|$)','',name)
    name=re.sub(r'-?\d+(?:-\d+)*$','',name)
    if a['material']=='object' or a['material']=='glass':
        # Purchased-product envelopes and furniture are not interchangeable stock.
        return re.sub(r'-(left|right|front|back|hot|hall|\d+)','',a['id'].split('/')[0])+':'+name
    if name.startswith(('edge','blocking','partition-trimmer','skin')) and a['family'] in ('floor','roof'):
        return 'cassette:'+name
    if name.startswith(('stud','infill-stud')):return 'wall-stud' if a['family'] in ('walls','partitions') else 'roof-bearing-stud'
    return name


def identity(a, geometric=False):
    sloped=bool(a.get('slope_y') or a.get('top_slope_y'))
    dims=tuple(round(float(x),6) for x in a['size'])
    if not sloped:dims=tuple(sorted(dims))
    manufacturing=a.get('manufacturing',{})
    key=dict(material=manufacturing.get('material_spec',a['material']),dimensions_mm=dims,
             slope_y=round(float(a.get('slope_y',0)),9),top_slope_y=round(float(a.get('top_slope_y',0)),9))
    if not geometric:
        key.update(section_and_grain=manufacturing.get('grain_axis','unresolved'),
          machining=manufacturing.get('machining','unresolved'),handedness=manufacturing.get('handedness','unresolved'),
          connection=manufacturing.get('connection_detail','unresolved'),
          unresolved_application=role(a) if not manufacturing.get('verified') else None)
    return json.dumps(key,sort_keys=True,separators=(',',':'))


def schedule(parts):
    groups=defaultdict(list)
    for a in parts:groups[identity(a)].append(a)
    return [dict(type_id='P-'+hashlib.sha256(key.encode()).hexdigest()[:16],definition=json.loads(key),
       pieces=len(items),instances=[a['id'] for a in items],families=sorted({a['family'] for a in items}))
       for key,items in sorted(groups.items())]


def analyse(scene, details=False):
    primary=[a for a in scene['parts'] if not cladding(a)]
    excluded=[a for a in scene['parts'] if cladding(a)]
    groups=defaultdict(list)
    for a in primary:groups[a['assembly']].append(a)
    assembly_keys=[]
    for parts in groups.values():
        origin=[min(a['origin'][i] for a in parts) for i in range(3)]
        assembly_keys.append(json.dumps(sorted((identity(a),tuple(round(float(a['origin'][i]-origin[i]),6) for i in range(3))) for a in parts)))
    keys={identity(a) for a in primary};allkeys={identity(a) for a in scene['parts']}
    result=dict(schema='obtp-manufacturing-count/1',status='provisional-not-manufacturing-release',
       unique_manufactured_part_candidates=len(keys),geometric_lower_bound=len({identity(a,True) for a in primary}),
       physical_pieces=len(primary),all_physical_pieces=len(scene['parts']),
       unique_types_including_cladding=len(allkeys),cladding_exclusion_type_effect=len(allkeys)-len(keys),
       unique_assembly_candidates=len(set(assembly_keys)),assemblies_installed=len(groups),
       cladding=dict(physical_pieces=len(excluded),unique_types=len({identity(a) for a in excluded}),
          volume_m3=sum(a['size'][0]*a['size'][1]*(a['size'][2]+a.get('top_slope_y',0)*a['size'][1]/2)/1e9 for a in excluded)),
       type_keys=sorted(keys),assembly_keys=sorted(set(assembly_keys)),
       by_material={m:dict(types=len({identity(a) for a in primary if a['material']==m}),pieces=sum(a['material']==m for a in primary)) for m in sorted({a['material'] for a in primary})},
       uncertainty=['Grades, profiles, grain, machining, handedness and connection patterns are not fully specified. Counts are conservative candidate classes, not certified interchangeable parts.',
        'Unresolved application roles are retained; family/category names are not part identities. Rotated rectangular envelopes only establish geometric candidates.',
        'All modelled non-cladding solids are counted, including insulation and purchased-object representations. Purchased-product subparts are geometric placeholders; their actual constituent BOM is unknown.',
        'Air/vapour layers exist as specifications only; unmodelled fasteners, seals, tapes, flues and other required details have unknown counts in every baseline.',
        'Assembly groups are geometric installation groups, not approved prefabrication units; no diversity saving is inferred from grouping.'])
    if details:result.update(primary_schedule=schedule(primary),cladding_schedule=schedule(excluded))
    return result
