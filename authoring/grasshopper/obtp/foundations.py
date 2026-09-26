"""One setting-out lattice for building and decks. Geometry study, not sizing.
Pile depth/section and grillage are explicit provisional coordination envelopes.
"""
import math

def enrich(p,parts,interfaces,L,W,F,annex):
    # Retire independent strip/pad/bearer systems, preserving floor/terrace joists.
    parts[:]=[a for a in parts if a['family']!='foundation' and not (a['family']=='terrace' and '/bearer-' in a['id'])]
    beams=[a for a in parts if a['family']=='terrace' and '/joist-' in a['id']]
    # Common global origin: x=0. Perimeter closure lines supplement the 600 mm grid.
    segments=[(0,0,L+annex,0),(W-90,0,L+annex,0)]
    if p['program_type']==1:segments.extend([(195,-600,0,65),(W-285,-600,0,65)])
    for a in beams:
        x,y,z=a['origin'];dx,dy,_=a['size']
        if dy>dx:
            segments.extend([(y,x,x+dx,z),(y+dy-90,x,x+dx,z)])
        else:
            segments.extend([(y,x,x+dx,z)])
    # Continuous support strips on each actual joist bearing row.
    rows={}
    for y,x,X,z in segments:
        key=round(y,6);r=rows.setdefault(key,[x,X,z]);r[0]=min(r[0],x);r[1]=max(r[1],X);r[2]=max(r[2],z)
    def add(id,o,s,mat='timber',family='foundation'):
        parts.append(dict(id=id,origin=o,size=s,material=mat,family=family,assembly='foundation-platform' if family=='foundation' else id.split('/')[0],engineering_status='coordination-only'))
    nodes=[]
    if p['include_foundation']:
        for j,(y,(x,X,z)) in enumerate(sorted(rows.items())):
            # Edges and intermediate global support axes; no independent terrace datum.
            xs=sorted(set([x,X-90]+[v for v in range(math.ceil(x/1800)*1800,math.floor((X-90)/1800)*1800+1,1800)]))
            for i,xx in enumerate(xs):
                nodes.append([xx,y]);add(f'foundation-grid-{j}/pile-{i}',[xx,y,-800],[90,90,655 if p['foundation_type']==0 else 500],'concrete-study')
            material='timber' if p['foundation_type']==0 else 'concrete-study'
            dz=145 if p['foundation_type']==0 else 300
            # Reuse longer stock across intermediate supports. Splices stay over piles.
            cuts=[xs[0]]
            while X-cuts[-1]>6000:
                candidates=[v for v in xs if cuts[-1]<v<=cuts[-1]+6000]
                if not candidates:raise ValueError('No supported stock splice')
                cuts.append(max(candidates))
            cuts.append(X)
            for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
                add(f'foundation-grid-{j}/beam-{i}',[a,y,-dz],[b-a,90,dz],material)
            if z>0:add(f'foundation-grid-{j}/packing',[x,y,0],[X-x,90,z],'timber')
            interfaces.append(dict(id=f'foundation-grid-{j}/bearing',type='shared lattice bearing',capacity=None,fasteners=None,status='soil, frost, reinforcement and anchor design required'))
    # Cross ties connect bearing rows into ONE platform, not isolated terrace strips.
    # Upper insulated floor / drained decking remain distinct moisture assemblies.
    if p['include_foundation']:
        axes=[]
        for candidate in sorted(set(xx for xx,yy in nodes)):
            if not axes or candidate-axes[-1]>=90:axes.append(candidate)
        for i,a in enumerate(axes):
            bearing_rows=sorted(y for y,(x,X,z) in rows.items() if x<=a and a+90<=X)
            for j,(y,yy) in enumerate(zip(bearing_rows,bearing_rows[1:])):
                gap=yy-y-90
                if gap<=0:continue
                add(f'foundation-tie-{i}/member-{j}',[a,y+90,-dz],[90,gap,dz],material)
                interfaces.append(dict(id=f'foundation-tie-{i}/joint-{j}',type='platform cross tie end connection',capacity=None,fasteners=None,status='geometry contact; connector and stiffness design required'))
    # Removable perimeter trim conceals the cassette edge; does not seal underside ventilation.
    for label,y in [('front',-22),('back',W)]:
        add('floor-edge-'+label+'/board',[0,y,0],[L+annex,22,220],'cladding-wood','floor')
    for label,x in [('left',-22),('right',L+annex)]:
        add('floor-edge-'+label+'/board',[x,0,0],[22,W,220],'cladding-wood','floor')
    return dict(type=p['foundation_type'],label='Poliai ir medinės sijos' if p['foundation_type']==0 else 'Poliai ir gelžbetoninis rostverkas',
      assembly_id='foundation-platform',connected_platform=True,status='geometry-study-not-engineered',grid_origin_mm=[0,0],coordination_pitch_mm=600,support_pitch_mm=1800,
      support_nodes_mm=nodes,rows_mm=list(sorted(rows)),
      provisional_dimensions=True,holds=['Pile depth and section are display envelopes, not geotechnical design.',
      'Grillage section is not a construction specification; reinforcement and bearing require engineering.',
      'Unified setting-out does not imply rigid joints or verified differential settlement.'])
