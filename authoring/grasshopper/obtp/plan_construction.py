"""Room-boundary adapter using the canonical wall, envelope and platform recipes.
Rectangular strip layouts only; geometry is not an engineered construction release.
"""
from . import cells

def annex_objects(p,wall_run,add,L,W,F,H,annex):
    wall=195;skin=12;depth=W-390
    if annex:
        # Exterior access only. Three unequal source zones are retained nominally:
        # front shower, middle storage, rear seat. Parametric depth divides proportionally.
        split_a=p.get('annex_split_a_mm',depth*600//1800);split_b=p.get('annex_split_b_mm',depth*1500//1800)
        wall_run('annex-end',[L+annex-wall,0],'y',W,door=(wall+split_a+p['partition_depth']+skin,600))
        for j,y in enumerate([wall+split_a,wall+split_b]):
            wall_run('annex-divider-'+str(j),[L+skin,y],'x',annex-wall-skin,d=p['partition_depth'],family='partitions')
        # Door-height soffits over the two open exterior niches. Not roof columns.
        for label,y in [('shower',0),('seat',W-wall)]:
            add('niche-'+label+'/head',[L+12,y,F+p['door_height']+59],[annex-wall-12,wall,H-p['door_height']-59],'timber','walls')
        # Review side bay has open shower/seat ends; its whole bounding area is counted.
        add('outside-seat/seat',[L+84,wall+split_b+p['partition_depth']+84,F+420],[annex-wall-168,W-(wall+split_b+p['partition_depth']+84),35],'object','furniture')

def sauna_furniture(p,add,wall,hot,depth,F):
    # Slatted furniture retains the reference's long upper and shorter lower benches.
    for name,bx,by,bw,bh,level in [('upper',wall+46,wall+depth-p['bench_depth']-46,hot-92,p['bench_depth'],p['bench_height']),
                                 ('lower',wall+46,wall+depth-2*p['bench_depth']-58,min(1200,hot-92),p['bench_depth'],p['foot_bench_height'])]:
        slats=5;slat=(bh-4*10)//5
        for j in range(slats):add('bench-'+name+'/slat-'+str(j),[bx,by+j*(slat+10),F+level-38],[bw,slat,38],'object','furniture')
        for j,(xx,yy) in enumerate([(bx+45,by+45),(bx+bw-90,by+45),(bx+45,by+bh-90),(bx+bw-90,by+bh-90)]):
            add('bench-'+name+'/leg-'+str(j),[xx,yy,F],[45,45,level-38],'object','furniture')
        # Removable slatted end cover on the exposed short end, with cleaning gap.
        for j,zz in enumerate(range(80,level-38,100)):
            add('bench-'+name+'/end-cover-'+str(j),[bx+bw-20,by,F+zz],[20,bh,min(90,level-38-zz)],'object','furniture')
        # Removable slatted fronts and the second end, with an 80 mm cleaning gap.
        for j,zz in enumerate(range(80,level-38,100)):
            h=min(90,level-38-zz)
            add('bench-'+name+'/front-cover-'+str(j),[bx+20,by,F+zz],[bw-40,20,h],'object','furniture')
            add('bench-'+name+'/other-end-cover-'+str(j),[bx,by,F+zz],[20,bh,h],'object','furniture')
    add('heater/envelope',[wall+hot-500,wall+60,F],[260,430,700],'object','furniture')

def shower_objects(p,add,L,wall,F):
    # Room-graph programme may omit the whole outdoor function, not just storage.
    if p.get('include_outdoor_shower',True):
        shower_x=L+96;shower_y=wall+250
        add('shower/riser',[shower_x,shower_y,F],[30,30,1800],'object','furniture')
        add('shower/arm',[shower_x,shower_y,F+1770],[350,30,30],'object','furniture')
        add('shower/head',[shower_x+300,shower_y-40,F+1730],[80,110,40],'object','furniture')


def specification(plan):
    """Resolve room clear faces and openings once, in an annex-right local frame."""
    import copy
    rooms=copy.deepcopy(plan['rooms']);total=plan['bounds_mm'][2]
    mirror=rooms[0]['id']=='outdoor' and len(rooms)>1
    if mirror:
        for r in rooms:r['bounds_mm'][0]=total-r['bounds_mm'][0]-r['bounds_mm'][2]
        rooms.reverse()
    indoors=[r for r in rooms if r['id']!='outdoor']
    if not indoors:raise ValueError('Outdoor-only requires a standalone storage/niche enclosure recipe; add sauna or entrance.')
    main=sum(r['bounds_mm'][2] for r in indoors);width=plan['bounds_mm'][3]
    connected=any(e['kind']=='passage' for e in plan['graph']['edges'])
    openings=[]
    for i,r in enumerate(indoors):
        x,_,w,_=r['bounds_mm'];left=x+(195 if i==0 else 102);right=x+w-(195 if i==len(indoors)-1 else 0)
        r['structural_clear_x_mm']=[left,right]
        r['clear_bounds_mm']=[left+36,231,right-left-72,width-462]
        if r['clear_bounds_mm'][2]<900:raise ValueError(r['id']+' finished width is below 900 mm')
        # Every disconnected interior component receives its own external entrance.
        exterior=(r['id']=='entrance' or len(indoors)==1 or not connected)
        if exterior:
            # Front doors; stand-alone sauna window goes on the back wall.
            a=x+(195 if i==0 else 0);b=x+w-(195 if i==len(indoors)-1 else 0)
            fit=cells.opening(a,b,cells.X,900,(a+b-900)/2)
            openings.append(dict(id='entry-'+r['id']+'/opening',kind='entrance',origin_mm=[a+fit['start'],0],axis='x',width_mm=900,room=r['id']))
    if len(indoors)==2 and connected:
        fit=cells.opening(195,width-195,cells.Y,900,(width-900)/2)
        openings.append(dict(id='sauna-partition/opening',kind='passage',origin_mm=[indoors[1]['bounds_mm'][0],195+fit['start']],axis='y',width_mm=900))
    return dict(rooms=indoors,main=main,mirror=mirror,total=total,openings=openings)


def walls_and_objects(p,parts,wall_run,add,W,F,H):
    rooms=p['layout_rooms'];L=p['layout_main_length_mm'];wall=195
    for i,r in enumerate(rooms):
        x,_,w,_=r['bounds_mm'];a=x+(wall if i==0 else 0);b=x+w-(wall if i==len(rooms)-1 else 0)
        entry=next((o for o in p['layout_openings'] if o.get('room')==r['id']),None)
        host='entry-'+r['id'] if entry else 'room-'+r['id']+'-front'
        wall_run(host,[a,0],'x',b-a,door=(entry['origin_mm'][0]-a,900) if entry else None,side_skin=-1)
    # Back window is deliberately separate from front entrances, avoiding conflicts.
    window_room=next((r for r in rooms if r['id']=='sauna'),rooms[0])
    wx0,wx1=window_room['structural_clear_x_mm'];rough=p['window_width']+20
    
    try:fit=cells.opening(wx0,wx1,cells.X,rough,(wx0+wx1-rough)/2)
    except ValueError as error:raise ValueError(str(error)+': selected window in '+window_room['id']+'; enlarge this room or select a smaller offered window') from error
    wx=wx0+fit['start']
    # Split the back at room boundaries, using corner deductions only at terminals.
    for i,r in enumerate(rooms):
        x,_,w,_=r['bounds_mm'];a=x+(wall if i==0 else 0);b=x+w-(wall if i==len(rooms)-1 else 0)
        is_window=r['id']==window_room['id']
        wall_run('back-window' if is_window else 'room-'+r['id']+'-back',[a,W-wall],'x',b-a,door=(wx-a,rough) if is_window else None)
    parts[:]=[a for a in parts if not a['id'].startswith('back-window/door-')]
    fw=p['window_width'];fh=p['door_height']-20;fz=F+10;fx=wx+10;fy=W-wall+12.5
    for label,xx,zz,a,c in [('left',fx,fz,51,fh),('right',fx+fw-51,fz,51,fh),('bottom',fx+51,fz,fw-102,51),('top',fx+51,fz+fh-51,fw-102,51)]:
        add('window/'+label,[xx,fy,zz],[a,170,c],'object','walls')
    for i,gy in enumerate([50,72,94]):add('window/glazing-'+str(i),[fx+51,W-wall+gy,fz+51],[fw-102,4,fh-102],'glass','walls')
    wall_run('hot-end',[0,0],'y',W,side_skin=-1)
    wall_run('hall-end',[L-wall,0],'y',W)
    for r in rooms[1:]:
        opening=next((o for o in p['layout_openings'] if o['kind']=='passage'),None)
        wall_run('sauna-partition',[r['bounds_mm'][0],wall],'y',W-390,d=p['partition_depth'],door=(opening['origin_mm'][1]-wall,900) if opening else None,family='partitions')
    annex=p['storage_length_steps']*cells.X if p['storage'] else 0
    annex_objects(p,wall_run,add,L,W,F,H,annex)
    sauna=next((r for r in rooms if r['id']=='sauna'),None)
    if sauna:
        a,b=sauna['structural_clear_x_mm'];length=b-a
        if length<1800 or W-390<2*p['bench_depth']+600:raise ValueError('Sauna benches and circulation do not fit finished room')
        def moved_add(id,origin,size,*args,**kwargs):
            origin=list(origin);origin[0]+=a-wall
            add(id,origin,size,*args,**kwargs)
        sauna_furniture(p,moved_add,wall,length,W-390,F)
    shower_objects(p,add,L,wall,F)

def reflect_scene(scene):
    """Reflect the complete physical assembly, then let derived outputs regenerate."""
    import hashlib,json
    end=scene['dimensions']['length_mm']+scene['dimensions']['annex_length_mm']
    for item in scene['parts']+scene['opening_voids']:
        item['origin'][0]=end-item['origin'][0]-item['size'][0]
    for item in scene['wall_regions']:
        item['base'][0]=end-item['base'][0]-(item['length'] if item['axis']=='x' else item['depth'])
    for item in scene.get('cell_spec',{}).get('wall_assemblies',[]):
        if item['axis']=='x':item['bounds_mm']=[end-item['bounds_mm'][1],end-item['bounds_mm'][0]]
    for item in scene['rooms']:
        x,y,w,h=item['bounds_mm'];item['bounds_mm']=[end-x-w,y,w,h]
    for item in scene['config']['layout_rooms']:
        for key in ('bounds_mm','clear_bounds_mm'):
            x,y,w,h=item[key];item[key]=[end-x-w,y,w,h]
        a,b=item['structural_clear_x_mm'];item['structural_clear_x_mm']=[end-b,end-a]
    for item in scene['config']['layout_openings']:
        item['origin_mm'][0]=end-item['origin_mm'][0]-(item['width_mm'] if item['axis']=='x' else 90)
    spec=scene['foundation_spec']
    spec['support_nodes_mm']=[[end-x,y] for x,y in spec.get('support_nodes_mm',[])]
    spec['grid_origin_mm']=[end,0];spec['x_direction']=-1
    scene['dimensions']['main_origin_x_mm']=scene['dimensions']['annex_length_mm']
    scene['geometry_sha256']=hashlib.sha256(json.dumps(scene['parts'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    scene['holds'].append('Mirrored layout: asymmetric connection machining and product handing require review; no interchangeability is inferred from equal member sizes.')
