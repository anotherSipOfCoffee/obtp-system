"""R02 researched finish/roof/terrace geometry studies, not engineered details.
Sloped members are affine prisms; slope_y shears Z along Y and preserves volume.
"""
import math


def enrich(p,parts,voids,interfaces,L,W,F,H,annex,wall_regions):
    wall=195; skin=12; end=L+annex; hot=p['sauna_length_steps']*600; px=wall+hot
    depth=W-390; D=p['terrace_steps']*600; outer=84 # 12 sheathing + 25 + 25 battens + 22 boards
    def add(id,o,s,mat='timber',family='roof',slope=0):
        if min(s)<=0:raise ValueError('Nonpositive envelope part '+id)
        a=dict(id=id,origin=list(o),size=list(s),material=mat,family=family,assembly=id.split('/')[0])
        if slope:a['slope_y']=slope
        parts.append(a)
    def subtract(rect,hole):
        u,z,a,h=rect;v,w,b,k=hole
        x0=max(u,v);x1=min(u+a,v+b);z0=max(z,w);z1=min(z+h,w+k)
        if x1<=x0 or z1<=z0:return [rect]
        return [q for q in [(u,z,x0-u,h),(x1,z,u+a-x1,h),(x0,z,x1-x0,z0-z),(x0,z1,x1-x0,z+h-z1)] if q[2]>0 and q[3]>0]
    def surface(name,axis,base,u0,length,inward,interior=True,holes=()):
        # base is the structural face. u is longitudinal, v is perpendicular.
        # Continuous cavity; boards shown with a small joint reveal, not a certified profile.
        cuts=list(holes)
        for v in voids:
            k=0 if axis=='x' else 1;other=1-k
            if v['origin'][other]-1 <= base <= v['origin'][other]+v['size'][other]+1:
                cuts.append((v['origin'][k],F,v['size'][k],p['door_height']))
        # Record the filled finish zone from the same surface dimensions, including
        # ventilated cavities; no repeated cladding strips in a conceptual plan.
        for u,z,a,h in __import__('functools').reduce(lambda rs,c:[t for rr in rs for t in subtract(rr,c)],cuts,[(u0,F,length,H)]):
            if z <= F+1100 < z+h:
                thick=36 if interior else 84
                v=base if inward>0 else base-thick
                wall_regions.append(dict(id=name,axis=axis,base=[u,v] if axis=='x' else [v,u],length=a,depth=thick))
        def put(label,u,z,a,h,offset,thick,material):
            for j,(uu,zz,aa,hh) in enumerate(__import__('functools').reduce(lambda rs,c:[t for r in rs for t in subtract(r,c)],cuts,[(u,z,a,h)])):
                v=base+inward*offset-(thick if inward<0 else 0)
                o=[uu,v,zz] if axis=='x' else [v,uu,zz]
                size=[aa,thick,hh] if axis=='x' else [thick,aa,hh]
                add(name+'/'+label+'-'+str(j),o,size,material,'interior' if interior else 'facade')
        if interior:
            # 20 x 45 support battens, nominal 400 mm spacing (Thermory).
            for i,u in enumerate(range(int(u0),int(u0+length),400)):
                put('batten-'+str(i),u,F+20,min(45,u0+length-u),H-40,0,20,'lining-wood')
            for i,z in enumerate(range(F+20,F+H-20,95)):
                put('board-'+str(i),u0,z,length,min(93,F+H-20-z),20,16,'lining-wood')
        else:
            for i,u in enumerate(range(int(u0),int(u0+length),600)):
                put('counter-'+str(i),u,F,min(45,u0+length-u),H,12,25,'cladding-wood')
            for i,z in enumerate(range(F,F+H,600)):
                put('batten-'+str(i),u0,z,length,min(45,F+H-z),37,25,'cladding-wood')
            for i,u in enumerate(range(int(u0),int(u0+length),80)):
                put('board-'+str(i),u,F,min(78,u0+length-u),H,62,22,'cladding-wood')
    if p.get('program_type',0)==1:
        z=p['studio_zones'];bs=z['bridge_start'];be=z['bridge_end'];rs=z['right_start']
        for name,a,b in [('left',0,bs),('right',be,L)]:
            for label,y,sgn in [('front',wall,1),('back',W-wall,-1)]:surface('lining-'+name+'-'+label,'x',y,a+wall+36,b-a-2*wall-72,sgn)
            surface('lining-'+name+'-end-a','y',a+wall,wall,depth,1)
            surface('lining-'+name+'-end-b','y',b-wall,wall,depth,-1)
            for label,y,sgn in [('front',0,-1),('back',W,1)]:surface('facade-'+name+'-'+label,'x',y,a-outer,b-a+2*outer,sgn,False)
            surface('facade-'+name+'-end-a','y',a,0,W,-1,False)
            surface('facade-'+name+'-end-b','y',b,0,W,1,False)
            for i,y in enumerate(range(wall+36,W-wall-36,95)):
                add('ceiling-'+name+'/board-'+str(i),[a+wall+36,y,F+H-36],[b-a-2*wall-72,min(93,W-wall-36-y),16],'lining-wood','ceiling')
            for i,x in enumerate(range(a+wall+36,b-wall-36,400)):
                add('ceiling-'+name+'/batten-'+str(i),[x,wall+36,F+H-20],[min(45,b-wall-36-x),depth-72,20],'lining-wood','ceiling')
        for side,y in [('front',0),('back',W)]:
            surface('log-niche-'+side,'x',y,-600,600,-1 if side=='front' else 1,False)
        for side,y in [('front',wall),('back',W-wall)]:
            surface('log-niche-inner-'+side,'x',y,-600,516,1 if side=='front' else -1,False)
        for j,x in enumerate([-600,-129]):
            add('firewood-niche/joist-'+str(j),[x,wall,F-173],[45,W-2*wall,145],'timber','floor')
            add('firewood-niche/pad-'+str(j),[x,wall,-200],[90,W-2*wall,265],'concrete-study','foundation')
        # Heated centre retains continuous structural floor sheathing.
        # Ceiling finish follows the same 16mm lining +20mm service-batten recipe.
        for i,y in enumerate(range(0,W,95)):
            add('ceiling-centre/board-'+str(i),[bs,y,F+H-36],[be-bs,min(93,W-y),16],'lining-wood','ceiling')
        for i,x in enumerate(range(bs,be,400)):
            add('ceiling-centre/batten-'+str(i),[x,0,F+H-20],[min(45,be-x),W,20],'lining-wood','ceiling')
    else:
        # Interior lining stays within each room, preserving framing geometry.
        partition_hole=[(px-36,F,p['partition_depth']+84,H)]
        for label,y,sgn in [('front',wall,1),('back',W-wall,-1)]:
            surface('lining-'+label,'x',y,wall+36,L-2*wall-72,sgn,holes=partition_hole)
        surface('lining-hot-end','y',wall,wall,depth,1)
        surface('lining-hall-end','y',L-wall,wall,depth,-1)
        surface('lining-partition-hot','y',px,wall+36,depth-72,-1)
        surface('lining-partition-hall','y',px+p['partition_depth']+12,wall+36,depth-72,1)
        # Ceiling lining and battens, independent from floor/roof structural skin.
        for name,x0,x1 in [('hot',wall+36,px-36),('hall',px+p['partition_depth']+48,L-wall-36)]:
            for i,x in enumerate(range(int(x0),int(x1),400)):
                add('ceiling-'+name+'/batten-'+str(i),[x,wall+36,F+H-20],[min(45,x1-x),depth-72,20],'lining-wood','ceiling')
            for i,y in enumerate(range(wall+36,W-wall-36,95)):
                add('ceiling-'+name+'/board-'+str(i),[x0,y,F+H-36],[x1-x0,min(93,W-wall-36-y),16],'lining-wood','ceiling')
        for label,y,sgn in [('front',0,-1),('back',W,1)]:surface('facade-'+label,'x',y,-outer,L+2*outer,sgn,False)
        surface('facade-hot-end','y',0,0,W,-1,False)
        if not annex:surface('facade-hall-end','y',L,0,W,1,False)
        else:
            surface('facade-annex-end','y',end,0,W,1,False)
            # Short return walls are open at shower/seat ends; finish their exterior faces.
            for j,y in enumerate([wall+depth*600//1800,wall+depth*1500//1800]):
                for side,base,sgn in [('a',y,-1),('b',y+p['partition_depth']+12,1)]:
                    surface('annex-lining-'+str(j)+side,'x',base,L+12,annex-wall-12,sgn,True)
        if annex:
            ya=wall+depth*600//1800+p['partition_depth']+48
            yb=wall+depth*1500//1800-36
            surface('lining-storage-end','y',end-wall,ya,yb-ya,-1)
            surface('lining-storage-back','y',L+12,ya,yb-ya,1)
    # Independently supported deck: no implied cantilever or unverified ledger attachment.
    deck_y=-outer-20-D; deck_end=-outer-20
    if D:
        for i,x in enumerate(range(0,end,600)):
            add('terrace/joist-'+str(i),[x,deck_y,F-28-145],[45,D,145],'deck-wood','terrace')
        for i,y in enumerate(range(deck_y,deck_end,100)):
            add('terrace/board-'+str(i),[0,y,F-28],[end,min(95,deck_end-y),28],'deck-wood','terrace')
        for j,y in enumerate([deck_y,deck_end-90]):
            add('terrace/bearer-'+str(j),[0,y,F-28-145-90],[end,90,90],'deck-wood','terrace')
            for i,x in enumerate(range(0,end,1800)):
                add('terrace/pad-'+str(j)+'-'+str(i),[x,y-60,-200],[150,150,175],'concrete-study','foundation')
    side_area=0
    if p['program_type']==0:
        # Full shower-side return, in 600mm coordination steps; starts at facade edge.
        sx=end+outer+20; sy=deck_end; run=W+outer+20-sy
        for i,x in enumerate(range(sx,sx+D,100)):
            add('terrace-side/board-'+str(i),[x,sy,F-28],[min(95,sx+D-x),run,28],'deck-wood','terrace')
        for i,y in enumerate(range(sy,sy+run,600)):
            add('terrace-side/joist-'+str(i),[sx,y,F-173],[D,45,145],'deck-wood','terrace')
        for j,x in enumerate([sx,sx+D-90]):
            add('terrace-side/bearer-'+str(j),[x,sy,F-263],[90,run,90],'deck-wood','terrace')
            for i,y in enumerate(range(sy,sy+run,1800)):
                add('terrace-side/pad-'+str(j)+'-'+str(i),[x-30,y,-200],[150,150,175],'concrete-study','foundation')
        # Fill corner connecting front deck and side return, outside both existing strips.
        for i,y in enumerate(range(deck_y,deck_end,100)):
            add('terrace-corner/board-'+str(i),[end,y,F-28],[outer+20+D,min(95,deck_end-y),28],'deck-wood','terrace')
        for i,x in enumerate(range(end,sx+D,600)):
            add('terrace-corner/joist-'+str(i),[x,deck_y,F-173],[45,D,145],'deck-wood','terrace')
        for j,y in enumerate([deck_y,deck_end-90]):
            add('terrace-corner/bearer-'+str(j),[end,y,F-263],[outer+20+D,90,90],'deck-wood','terrace')
            add('terrace-corner/pad-'+str(j),[sx+D-150,y,-200],[150,150,175],'concrete-study','foundation')
        side_area=(D*run+(outer+20+D)*D)/1e6
    # Retain main horizontal ceiling cassette. Weather roof is a separate supported study.
    base=F+H+238; cover=D if p['roof_type']!=2 else 0
    overhang=0 if p['roof_type']==2 else 150
    y0=-outer-overhang-cover; y1=W+outer+overhang; x0=-outer-overhang; length=end+2*(outer+overhang)
    extension=600 if p.get('program_type')==1 else 0
    x0-=extension;length+=extension
    slope=1/40 if p['roof_type']==0 else math.tan(math.radians(8))
    if p['roof_type']==2:
        # MyCabin S30 overall height reference: 4480 mm from model datum.
        # Retain System walls and solve rise from actual cover/seam top.
        slope=(4480-base-100-197)/((y1-y0)/2)
        if slope<=0:raise ValueError('Gable height target is below the roof build-up')
    # Metal roof: minimum 7° per Ruukki LT; choose 8° study. Flat: membrane at design 1:40.
    if p['roof_type']==2:
        mid=W/2; planes=[(y0,mid,slope),(mid,y1,-slope)]
        zfun=lambda y:base+100+slope*min(y-y0,y1-y)
    else:
        planes=[(y0,y1,-slope)] # High entrance eave; drain toward rear, away from deck.
        zfun=lambda y:base+100+slope*(y1-y)
    for k,(a,b,m) in enumerate(planes):
        for i,x in enumerate(range(int(x0),int(x0+length),600)):
            add('weather-roof-'+str(k)+'/rafter-'+str(i),[x,a,zfun(a)],[45,b-a,145],'timber','roof',m)
        for i,x in enumerate(range(int(x0),int(x0+length),600)):
            for j,y in enumerate(range(math.ceil(a),math.ceil(b),1200)):
                # Split sheet stock; exact plane start is retained below for noninteger ridge.
                yy=max(a,y);dy=min(1200,b-yy)
                if dy>0:add('weather-roof-'+str(k)+'/deck-'+str(i)+'-'+str(j),[x,yy,zfun(yy)+145],[min(600,x0+length-x),dy,18],'plywood','roof',m)
        add('weather-roof-'+str(k)+'/cover',[x0,a,zfun(a)+163],[length,b-a,2],'roof-membrane' if p['roof_type']==0 else 'roof-metal','roof',m)
        if p['roof_type']!=0:
            for i,x in enumerate(range(int(x0),int(x0+length),475)):
                add('weather-roof-'+str(k)+'/seam-'+str(i),[x,a,zfun(a)+165],[3,b-a,32],'roof-metal','roof',m)
    if p['roof_type']==2:
        for label,a,m in [('front',W/2-100,slope),('back',W/2,-slope)]:
            add('ridge-cap/'+label,[x0,a,zfun(a)+195],[length,100,2],'roof-metal','roof',m)
    # Close the weather-roof perimeter above the retained level ceiling cassette.
    # The attic/roof build-up remains a ventilated construction-detail study.
    for side,y in [('front',-outer),('back',W+outer-22)]:
        for i,x in enumerate(range(-outer-extension,int(end+outer),80)):
            add('roof-fascia-'+side+'/'+str(i),[x,y,F+H],[min(78,end+outer-x),22,zfun(y)-F-H],'cladding-wood','roof')
            parts[-1]['top_slope_y']=(zfun(y+22)-zfun(y))/22
    for side,x in [('hot',-outer-extension),('end',end+outer-22)]:
        for k,(a,b,m) in enumerate(planes):
            low=max(a,0);high=min(b,W)
            for i,y in enumerate(range(math.ceil(low),math.ceil(high),80)):
                dy=min(78,high-y)
                if dy>0:
                    add('roof-fascia-'+side+'/'+str(k)+'-'+str(i),[x,y,F+H],[22,dy,zfun(y)-F-H],'cladding-wood','roof')
                    parts[-1]['top_slope_y']=m
    # Roof reaction lines over perimeter walls; gable ridge needs its own support study.
    supports=[0,W-90]+([W/2-45] if p['roof_type']==2 else [])
    for j,y in enumerate(supports):
        spans=[(y,45),(y+45,45)] if p['roof_type']==2 and j==2 else [(y,90)]
        for k,(yy,dy) in enumerate(spans):
            h=zfun(yy)-base;m=(zfun(yy+dy)-zfun(yy))/dy
            group='weather-bearing-'+str(j)+'-'+str(k)
            if min(h,h+m*dy)<135:
                add(group+'/packing-study',[-extension,yy,base],[end+extension,dy,h],'timber','roof')
                parts[-1]['top_slope_y']=m
            else:
                add(group+'/bottom',[-extension,yy,base],[end+extension,dy,45],'timber','roof')
                add(group+'/top',[-extension,yy,base+h-45],[end+extension,dy,45],'timber','roof',m)
                positions=sorted(set([-extension,end-45]+[x for x in range(int(x0),int(x0+length),600) if 45-extension<=x<=end-90]))
                for n,x in enumerate(positions):
                    add(group+'/stud-'+str(n),[x,yy,base+45],[45,dy,h-90],'timber','roof')
                    parts[-1]['top_slope_y']=m
    post_spacing=0
    if cover:
        interfaces.append(dict(id='canopy/cantilever',type='post-free roof extension study',projection_mm=cover+outer+overhang,capacity=None,fasteners=None,status='unresolved structural design'))
    # Conservative envelope includes cladding, terrace and all roof projection; no exemption inference.
    minx=min(x0,min(a['origin'][0] for a in parts));maxx=max(x0+length,max(a['origin'][0]+a['size'][0] for a in parts))
    miny=min(y0,deck_y if D else y0);maxy=max(y1,max(a['origin'][1]+a['size'][1] for a in parts))
    area=(maxx-minx)*(maxy-miny)/1e6
    height=max(a['origin'][2]+a['size'][2]+max(0,(a.get('slope_y',0)+a.get('top_slope_y',0))*a['size'][1]) for a in parts)
    support_span=max(post_spacing,D)
    if area>50:raise ValueError('Finished roof/terrace projection bound exceeds 50.00 m²')
    if height>5000:raise ValueError('Actual roof geometry exceeds 5000 mm height')
    if max(W,support_span)>6000:raise ValueError('Generated support spacing exceeds 6000 mm')
    interfaces.append(dict(id='wall-floor/platform',type='bottom plate -> floor skin -> perimeter blocking/bearing',capacity=None,fasteners=None))
    return dict(area=area,height=height,support_span=support_span,terrace_area=end*D/1e6+side_area,enclosed_area=(L+2*outer)*(W+2*outer)/1e6)
