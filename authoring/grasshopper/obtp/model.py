"""Original OBTP Cassette 01 authoring core, millimetres.

Source section sizes: System 13e7d109386b270a5eab91f9461868a99d1e48bc.
Room arrangement is a comparison candidate, not an approved replacement of DXF.
No Rhino import here: the same recipes can be tested without a Rhino licence.
"""
import hashlib
import json
import math

VERSION = 'GH-R01'
SPEC = dict(pitch=600, wall_depth=195, stud=45, joist_depth=220,
            floor_skin=18, wall_skin=12, roof_skin=18, wall_height=2100)
PRESETS = [dict(id='sauna-'+size+('-storage' if storage else '-open'),
                size=size.upper(), storage=storage, room_depth_steps=3,
                sauna_length_steps=4, hall_length_steps=hall)
           for size, hall in [('s', 2), ('m', 3), ('l', 4)]
           for storage in [False, True]]
DEFAULTS = dict(room_depth_steps=3, sauna_length_steps=4, hall_length_steps=3,
                storage=False, storage_length_steps=2, wall_height=2100,
                partition_depth=90, door_width=900, door_height=1900,
                sauna_door_offset=150, bench_depth=600, bench_height=900,
                foot_bench_height=450, include_foundation=True)
HOLDS = [
 'Owner-plan fit not accepted: 1800 mm structural inside-face depth is a proposal.',
 'Source door offsets are retained in reference drawings; generated doors use explicit candidate parameters.',
 'Cassette end pieces, off-grid partitions and opening framing need connection review.',
 'No engineered lintel, fastener schedule, racking, foundation or roof-weathering design.',
 'Sauna lining, finished clearances, ventilation and heater installation are unverified.',
 'Grasshopper/Rhino 8 execution acceptance is pending.']


def parameters(preset_index=2, custom=False, **overrides):
    if isinstance(preset_index, bool) or preset_index not in range(6):
        raise ValueError('Preset index must be 0–5')
    p = dict(DEFAULTS)
    p.update(PRESETS[preset_index])
    if custom:
        unknown = set(overrides) - set(DEFAULTS)
        if unknown:
            raise ValueError('Unknown parameters: ' + ', '.join(sorted(unknown)))
        p.update({k: v for k, v in overrides.items() if v is not None})
        p['id'] = 'sauna-custom'
    for k in DEFAULTS:
        if isinstance(DEFAULTS[k], bool):
            if not isinstance(p[k], bool):
                raise ValueError(k + ' must be boolean')
        elif isinstance(p[k], bool) or not isinstance(p[k], (int, float)) or not math.isfinite(p[k]) or int(p[k]) != p[k]:
            raise ValueError(k + ' must be a whole number')
        else:
            p[k] = int(p[k])
    return p


def build(p):
    p = dict(p)
    for k in ['room_depth_steps', 'sauna_length_steps', 'hall_length_steps', 'storage_length_steps']:
        if not 1 <= p[k] <= 18:
            raise ValueError(k + ' must be 1–18 steps')
    if p['wall_height'] not in (2100, 2700):
        raise ValueError('Wall height must use System 2100 or 2700 mm study')
    if p['partition_depth'] not in (90, 120):
        raise ValueError('Partition framing study: choose 90 or 120 mm')
    if not 600 <= p['door_width'] <= 1200 or not 1600 <= p['door_height'] <= p['wall_height']-200:
        raise ValueError('Door dimensions do not leave the reserved header zone')
    if not 400 <= p['bench_depth'] <= 800 or not 650 <= p['bench_height'] <= 1100 or not 250 <= p['foot_bench_height'] < p['bench_height']-150:
        raise ValueError('Bench study dimensions are outside supported ranges')
    wall, skin, pitch = SPEC['wall_depth'], SPEC['wall_skin'], SPEC['pitch']
    depth = p['room_depth_steps'] * pitch
    hot = p['sauna_length_steps'] * pitch
    nominal_hall = p['hall_length_steps'] * pitch
    inside_length = hot + nominal_hall
    W, L = depth + 2*wall, inside_length + 2*wall
    annex = p['storage_length_steps'] * pitch if p['storage'] else 0
    H, F = p['wall_height'], SPEC['joist_depth'] + SPEC['floor_skin']
    hall_clear = nominal_hall-p['partition_depth']
    if hall_clear < p['door_width']+180:
        raise ValueError('Hall does not accommodate the entrance opening and jamb zones')
    if p['sauna_door_offset'] < 90 or p['sauna_door_offset']+p['door_width']+90 > depth:
        raise ValueError('Sauna door and its jamb zones do not fit the partition')
    if depth < 2*p['bench_depth']+600 or hot < 1800:
        raise ValueError('Bench and circulation reservation does not fit this study')
    # Conservative bound includes sheathing and the entire optional side bay.
    area = (L+annex+2*skin)*(W+2*skin)/1e6
    height = F+H+SPEC['joist_depth']+SPEC['roof_skin']
    if area > 50 or area <= 0:
        raise ValueError('Building-area bound exceeds 50.00 m²')
    if height > 5000:
        raise ValueError('Generated height exceeds 5000 mm')
    if W > 6000:
        raise ValueError('Floor/roof bearing-line span exceeds 6000 mm')
    parts, interfaces, opening_voids = [], [], []

    def add(id, origin, size, material='timber', family='walls', assembly=None):
        if any(not math.isfinite(v) for v in origin+size) or any(v <= 0 for v in size):
            raise ValueError('Invalid part ' + id)
        parts.append(dict(id=id, origin=list(origin), size=list(size), material=material,
                          family=family, assembly=assembly or id.rsplit('/', 1)[0]))

    def line_box(id, base, axis, u, v, z, a, b, c, material, family, assembly):
        if axis == 'x':
            origin, size = [base[0]+u, base[1]+v, z], [a,b,c]
        else:
            origin, size = [base[0]+v, base[1]+u, z], [b,a,c]
        add(id, origin, size, material, family, assembly)

    # Main and optional side bay share continuous transverse floor joist logic.
    # Last, shorter bay is explicitly retained as an end cassette, not stretched.
    partition_x = wall+hot
    for stage, z, thickness in [('floor', 0, SPEC['floor_skin']), ('roof', F+H, SPEC['roof_skin'])]:
        for i, x in enumerate(range(0, L+annex, pitch)):
            a = min(pitch, L+annex-x)
            if a < 90:
                raise ValueError('Residual cassette is too short for two boundary joists')
            group = stage+'-'+str(i)
            add(group+'/edge-a',[x,0,z],[45,W,220],family=stage,assembly=group)
            add(group+'/edge-b',[x+a-45,0,z],[45,W,220],family=stage,assembly=group)
            bands = [(0,45),(W//2-22,W//2+23),(W-45,W)]
            for j,(y0,y1) in enumerate(bands):
                add(group+'/blocking-'+str(j),[x+45,y0,z],[a-90,y1-y0,220],family=stage,assembly=group)
            # Add trimmers below parallel partition axes, excluding existing joists/blocking.
            if stage == 'floor':
                for k, ax in enumerate([partition_x] + ([L-wall] if annex else [])):
                    lo, hi = max(x+45,ax), min(x+a-45,ax+p['partition_depth'])
                    if hi > lo:
                        for j, (y0,y1) in enumerate([(45,bands[1][0]),(bands[1][1],W-45)]):
                            add(group+'/partition-trimmer-'+str(k)+'-'+str(j),[lo,y0,z],[hi-lo,y1-y0,220],family=stage,assembly=group)
            # Split transverse sheets to respect the System sheet stock envelope.
            for j,y in enumerate(range(0,W,2400)):
                add(group+'/skin-'+str(j),[x,y,z+220],[a,min(2400,W-y),thickness],'plywood',stage,group)
            interfaces.append(dict(id=group+'/bearing',type='slab-bearing',span_mm=W,capacity=None,fasteners=None))

    def wall_run(name, base, axis, length, d=wall, door=None, family='walls', side_skin=1):
        """Independent framed cassettes and explicit rough-opening frame; no booleans."""
        def put(label,u,v,z,a,b,c,mat='timber',group=None):
            if mat=='plywood' and c>2440:
                for j in range(2):line_box(name+'/'+label+'-sheet-'+str(j),base,axis,u,v,F+z+j*c/2,a,b,c/2,mat,family,group or name)
            else:line_box(name+'/'+label,base,axis,u,v,F+z,a,b,c,mat,family,group or name)
        def panel(start, end, index):
            width=end-start
            if width < 90:
                raise ValueError('Wall residual below 90 mm: '+name)
            group=name+'/cassette-'+str(index)
            put('plate-bottom-'+str(index),start,0,0,width,d,45,group=group)
            put('plate-top-'+str(index),start,0,H-45,width,d,45,group=group)
            put('stud-left-'+str(index),start,0,45,45,d,H-90,group=group)
            put('stud-right-'+str(index),end-45,0,45,45,d,H-90,group=group)
            if H>2440 and width>90:
                put('sheet-backing-'+str(index),start+45,0,H/2-22.5,width-90,d,45,group=group)
            sheets=[(0,H)] if H<=2440 else [(0,H/2),(H/2,H/2)]
            for j,(z,sh) in enumerate(sheets):
                put('skin-'+str(index)+'-'+str(j),start,-skin if side_skin<0 else d,z,width,skin,sh,'plywood',group)
            interfaces.append(dict(id=group+'/joint',type='wall-cassette',capacity=None,fasteners=None))
        intervals=[(0,length)]
        if door:
            start, width=door
            lo,hi=start-90,start+width+90
            if lo<0 or hi>length:
                raise ValueError('Door jamb/end cassette conflict: '+name)
            if lo<90:lo=0
            if length-hi<90:hi=length
            intervals=[(0,lo),(hi,length)]
            head=p['door_height'];group=name+'/opening'
            for side,u,a in [('left',lo,start-45-lo),('right',start+width+45,hi-start-width-45)]:
                put('king-'+side,u,0,0,a,d,H-45,group=group)
            for side,u in [('left',start-45),('right',start+width)]:
                put('jack-'+side,u,0,0,45,d,head,group=group)
            put('lintel',start-45,0,head,width+90,d,H-head-45,group=group)
            put('opening-top',lo,0,H-45,hi-lo,d,45,group=group)
            for label,u,a,z,c in [('left',lo,start-lo,0,H),('right',start+width,hi-start-width,0,H),('head',start,width,head,H-head)]:
                put('opening-skin-'+label,u,-skin if side_skin<0 else d,z,a,skin,c,'plywood',group)
            if axis=='x':vo=[base[0]+start,base[1]-skin,F];vs=[width,d+2*skin,head]
            else:vo=[base[0]-skin,base[1]+start,F];vs=[d+2*skin,width,head]
            opening_voids.append(dict(id=group,origin=vo,size=vs))
            # Gray joinery is independent from the structural aperture.
            put('door-jamb-left',start,d//2,0,30,40,head,'object',group)
            put('door-jamb-right',start+width-30,d//2,0,30,40,head,'object',group)
            put('door-head',start+30,d//2,head-30,width-60,40,30,'object',group)
            put('door-leaf',start+35,d//2+45,5,width-70,35,head-40,'object',group)
            interfaces.append(dict(id=group,type='opening',capacity=None,fasteners=None))
        n=0
        for begin,end in intervals:
            x=begin
            while x<end:
                width=min(pitch,end-x)
                if 0<end-(x+width)<90:width=end-x
                panel(x,x+width,n);x+=width;n+=1

    entry=hot+p['partition_depth']+(hall_clear-p['door_width'])//2
    wall_run('front',[wall,0],'x',inside_length,door=(entry,p['door_width']),side_skin=-1)
    wall_run('back',[wall,W-wall],'x',inside_length)
    wall_run('hot-end',[0,0],'y',W,side_skin=-1)
    wall_run('hall-end',[L-wall,0],'y',W)
    wall_run('sauna-partition',[partition_x,wall],'y',depth,d=p['partition_depth'],
             door=(p['sauna_door_offset'],p['door_width']),family='partitions')
    if annex:
        # Exterior access only. Three unequal source zones are retained nominally:
        # front shower, middle storage, rear seat. Parametric depth divides proportionally.
        split_a=depth*600//1800;split_b=depth*1500//1800
        wall_run('annex-end',[L+annex-wall,0],'y',W,door=(wall+split_a+p['partition_depth']+skin,600))
        for j,y in enumerate([wall+split_a,wall+split_b]):
            wall_run('annex-divider-'+str(j),[L+skin,y],'x',annex-wall-skin,d=p['partition_depth'],family='partitions')
        # Review side bay has open shower/seat ends; its whole bounding area is counted.
        add('outside-seat/seat',[L+45,wall+split_b+90,F+420],[annex-wall-90,max(150,depth-split_b-90),35],'object','furniture')
    # Slatted furniture retains the reference's long upper and shorter lower benches.
    for name,bx,by,bw,bh,level in [('upper',wall,wall+depth-p['bench_depth'],hot,p['bench_depth'],p['bench_height']),
                                 ('lower',wall,wall+depth-2*p['bench_depth']-12,min(1200,hot),p['bench_depth'],p['foot_bench_height'])]:
        slats=5;slat=(bh-4*10)//5
        for j in range(slats):add('bench-'+name+'/slat-'+str(j),[bx,by+j*(slat+10),F+level-38],[bw,slat,38],'object','furniture')
        for j,(xx,yy) in enumerate([(bx+45,by+45),(bx+bw-90,by+45),(bx+45,by+bh-90),(bx+bw-90,by+bh-90)]):
            add('bench-'+name+'/leg-'+str(j),[xx,yy,F],[45,45,level-38],'object','furniture')
    add('heater/envelope',[wall+60,wall+60,F],[260,430,700],'object','furniture')
    shower_x=L+25;shower_y=wall+250
    add('shower/riser',[shower_x,shower_y,F],[30,30,2100],'object','furniture')
    add('shower/arm',[shower_x,shower_y,F+2070],[350,30,30],'object','furniture')
    add('shower/head',[shower_x+300,shower_y-40,F+2030],[80,110,40],'object','furniture')
    if p['include_foundation']:
        for j,y in enumerate([-100,W-200]):add('foundation/strip-'+str(j),[0,y,-200],[L+annex,300,200],'concrete-study','foundation')
    ids=[a['id'] for a in parts]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate part identity')
    wood={mat:sum(math.prod(a['size'])/1e9 for a in parts if a['material']==mat) for mat in ['timber','plywood']}
    geometry_hash=hashlib.sha256(json.dumps(parts,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(schema='obtp-parametric-release/1',version=VERSION,units='mm',config=p,
                system_spec=SPEC,parts=parts,interfaces=interfaces,opening_voids=opening_voids,
                metrics=dict(building_area_bound_m2=area,internal_clear_rectangle_m2=inside_length*depth/1e6,
                             main_clear_floor_less_partition_m2=(inside_length-p['partition_depth'])*depth/1e6,
                             height_mm=height,max_bearing_line_span_mm=W,
                             wood_m3=wood,total_wood_m3=sum(wood.values())),
                dimensions=dict(length_mm=L,width_mm=W,annex_length_mm=annex,floor_top_mm=F),
                checks=dict(area=area<=50,height=height<=5000,span=W<=6000),
                status='review-candidate',website_ready=False,manufacturing_release=False,
                holds=list(HOLDS),geometry_sha256=geometry_hash)
