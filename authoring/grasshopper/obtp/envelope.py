"""R02 researched finish/roof/terrace geometry studies, not engineered details.
Sloped members are affine prisms; slope_y shears Z along Y and preserves volume.
"""
import math


def enrich(p,parts,voids,interfaces,L,W,F,H,annex):
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
    # Retain main horizontal ceiling cassette. Weather roof is a separate supported study.
    base=F+H+238; cover=D if p['roof_type']!=2 else 0
    y0=-outer-150-cover; y1=W+outer+150; x0=-outer-150; length=end+2*(outer+150)
    slope=1/40 if p['roof_type']==0 else math.tan(math.radians(8 if p['roof_type']==1 else 25))
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
    # Close the weather-roof perimeter above the retained level ceiling cassette.
    # The attic/roof build-up remains a ventilated construction-detail study.
    for side,y in [('front',-outer),('back',W+outer-22)]:
        for i,x in enumerate(range(-outer,int(end+outer),80)):
            add('roof-fascia-'+side+'/'+str(i),[x,y,F+H],[min(78,end+outer-x),22,zfun(y)-F-H],'cladding-wood','roof')
            parts[-1]['top_slope_y']=(zfun(y+22)-zfun(y))/22
    for side,x in [('hot',-outer),('end',end+outer-22)]:
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
                add(group+'/packing-study',[0,yy,base],[end,dy,h],'timber','roof')
                parts[-1]['top_slope_y']=m
            else:
                add(group+'/bottom',[0,yy,base],[end,dy,45],'timber','roof')
                add(group+'/top',[0,yy,base+h-45],[end,dy,45],'timber','roof',m)
                positions=sorted(set([0,end-45]+[x for x in range(int(x0),int(x0+length),600) if 45<=x<=end-90]))
                for n,x in enumerate(positions):
                    add(group+'/stud-'+str(n),[x,yy,base+45],[45,dy,h-90],'timber','roof')
                    parts[-1]['top_slope_y']=m
    post_spacing=0
    if cover:
        # Independent outer beam/posts support canopy; never stretch a cassette cantilever.
        yy=deck_y+60;n=max(1,math.ceil((end-120)/3000));post_spacing=(end-120)/n
        beamtop=zfun(yy)
        add('canopy/beam',[0,yy,beamtop-195],[end,90,195],'timber','canopy')
        parts[-1]['top_slope_y']=-slope
        door=next(v for v in voids if v['id']=='front/opening')
        forbidden=(door['origin'][0]-150-120,door['origin'][0]+door['size'][0]+150)
        positions=[]
        for i in range(n+1):
            x=round(i*post_spacing)
            if forbidden[0]<x<forbidden[1]:x=round(min(forbidden,key=lambda edge:abs(edge-x)))
            positions.append(x)
        positions=sorted(set(positions))
        post_spacing=max(b-a for a,b in zip(positions,positions[1:]))
        if post_spacing>3000:raise ValueError('Canopy supports cannot keep door approach clear within 3000 mm post spacing')
        for i,x in enumerate(positions):
            add('canopy/post-'+str(i),[x,yy,F],[120,90,beamtop-195-F],'timber','canopy')
    # Conservative envelope includes cladding, terrace and all roof projection; no exemption inference.
    area=length*(y1-min(y0,deck_y if D else y0))/1e6
    height=max(a['origin'][2]+a['size'][2]+max(0,(a.get('slope_y',0)+a.get('top_slope_y',0))*a['size'][1]) for a in parts)
    support_span=max(post_spacing,D)
    if area>50:raise ValueError('Finished roof/terrace projection bound exceeds 50.00 m²')
    if height>5000:raise ValueError('Actual roof geometry exceeds 5000 mm height')
    if max(W,support_span)>6000:raise ValueError('Generated support spacing exceeds 6000 mm')
    interfaces.append(dict(id='wall-floor/platform',type='bottom plate -> floor skin -> perimeter blocking/bearing',capacity=None,fasteners=None))
    return dict(area=area,height=height,support_span=support_span,terrace_area=end*D/1e6,enclosed_area=(L+2*outer)*(W+2*outer)/1e6)
