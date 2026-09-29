"""Connected wall-run display poses. Canonical parts and assembly IDs stay intact."""
import math
from .export import vertices

def groups(scene, classifier):
    parts=[p for p in scene['parts'] if classifier(p)==4]
    roots={p['id'].split('/')[0] for p in parts if p['material']=='timber'}
    runs=[]
    for r in scene['wall_regions']:
        if r['id'] not in roots:continue
        k=0 if r['axis']=='x' else 1;n=1-k
        runs.append(dict(axis=k,normal=r['base'][n],depth=r['depth'],lo=r['base'][k],hi=r['base'][k]+r['length'],roots=[r['id']],parts=[]))
    runs.sort(key=lambda r:(r['axis'],r['normal'],r['depth'],r['lo']))
    merged=[]
    for r in runs:
        if merged and all(r[k]==merged[-1][k] for k in ('axis','normal','depth')) and r['lo']<=merged[-1]['hi']+.01:
            merged[-1]['hi']=max(merged[-1]['hi'],r['hi']);merged[-1]['roots']+=r['roots']
        else:merged.append(r)
    extra=[]
    for p in parts:
        root=p['id'].split('/')[0]
        candidates=[r for r in merged if root in r['roots']]
        if not candidates and p['family']=='insulation':
            c=[p['origin'][i]+p['size'][i]/2 for i in range(3)]
            candidates=[r for r in merged if r['lo']-.01<=c[r['axis']]<=r['hi']+.01 and r['normal']-.01<=c[1-r['axis']]<=r['normal']+r['depth']+.01]
        if candidates:candidates[0]['parts'].append(p)
        else:extra.append(dict(name=p['id'],parts=[p],auxiliary=True))
    result=[]
    for r in merged:
        if not r['parts']:continue
        vs=[v for p in r['parts'] for v in vertices(p)];n=1-r['axis']
        low=min(v[n] for v in vs);high=max(v[n] for v in vs)
        centre=(scene['dimensions']['width_mm'] if n==1 else scene['dimensions']['length_mm'])/2
        direction=-1 if (low+high)/2<centre else 1
        r.update(name=' + '.join(r['roots']),pivot=low if direction<0 else high,direction=direction,z=scene['dimensions']['floor_top_mm'])
        result.append(r)
    # Transverse walls raise before the long sides, leaving their laydown
    # sweep clear of already-standing side-wall bottom plates.
    return sorted(result,key=lambda r:(-r['axis'],r['normal'],r['lo']))+extra

def pose(group, angle):
    """Angle from upright. Bottom-edge pivot stays fixed at the floor datum."""
    if not angle:return group['parts']
    if group.get('auxiliary'):
        z=min(p['origin'][2] for p in group['parts']);m=[[1,0,0,0],[0,1,0,0],[0,0,1,-z]]
    else:
        k=group['axis'];n=1-k;b=group['pivot'];z=group['z'];d=group['direction']
        c=math.cos(math.radians(angle));s=math.sin(math.radians(angle))
        # Right-handed quarter-turn; project wall height to the outward side.
        m=[[float(i==j) for j in range(3)]+[0.] for i in range(3)]
        m[n][n]=c;m[n][2]=d*s;m[n][3]=b*(1-c)-d*s*z
        m[2][n]=-d*s;m[2][2]=c;m[2][3]=z*(1-c)+d*s*b
    return [dict(p,display_transform=m,display_wall_group=group['name']) for p in group['parts']]

_CACHE={}

def sequence(scene, classifier, legacy_stage_parts):
    """Raise one wall at a time: simultaneous flat walls may occupy the same area."""
    key=scene['geometry_sha256']
    if key in _CACHE:return _CACHE[key]
    steps=[]
    def add(label,parts,note,active):steps.append(dict(label=label,parts=parts,note=note,active=active))
    for phase,label in [(0,'Foundation'),(1,'Floor preparation'),(2,'Floor placement')]:
        shown=legacy_stage_parts(scene,phase);add(label,shown,'Follow the engineered support and connection details.',[p['id'] for p in shown if classifier(p)==(2 if phase else 0)])
    standing=[p for p in scene['parts'] if classifier(p)<4]
    for group in groups(scene,classifier):
        ids=[p['id'] for p in group['parts']]
        for angle,label in ([(90,'Prepare'),(0,'Place')] if group.get('auxiliary') else [(90,'Lay flat'),(45,'Raise 45 degrees'),(0,'Upright')]):
            note='Handling and connections unverified; this is a geometry study.' if group.get('auxiliary') else 'Same connected wall and openings; fixed bottom-edge pivot. Flat work height is the floor datum, on temporary supports. Lifting/bracing unverified.'
            add(group['name']+' / '+label,standing+pose(group,angle),note,ids)
        standing+=group['parts']
    for phase,label in [(5,'Roof preparation'),(6,'Roof placement'),(7,'Window and door preparation'),(8,'Opening insertion'),(9,'Interior'),(10,'Terrace decking'),(11,'Cladding last')]:
        shown=legacy_stage_parts(scene,phase);target={5:6,7:8}.get(phase,phase)
        add(label,shown,'Follow the separate supplier, connection and handling details.',[p['id'] for p in shown if classifier(p)==target])
    _CACHE.clear();_CACHE[key]=steps
    return steps
