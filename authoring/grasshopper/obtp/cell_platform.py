"""Repetitive building/terrace platform; member envelopes are not engineered."""
from .cells import X,Y


def bounds(p,L,W,annex):
    return (-2*X,L) if p['program_type']==1 else (0,L+annex+X)


def terrace(p,parts,L,W,F,annex):
    parts[:]=[a for a in parts if a['family']!='terrace' and not a['id'].startswith('firewood-niche/joist-')]
    lo,hi=bounds(p,L,W,annex);end=L+annex
    def add(id,o,s,mat='deck-wood'):
        parts.append(dict(id=id,origin=o,size=s,material=mat,family='terrace',assembly=id.split('/')[0]))
    # Submembers repeat at half-cell increments; they do not add foundation nodes.
    for i,x in enumerate(range(lo,hi,450)):
        add('terrace/joist-'+str(i),[x,-Y,F-173],[45,Y,145],'timber')
    for i,y in enumerate(range(-Y,-104,100)):
        add('terrace/board-'+str(i),[lo,y,F-28],[hi-lo,min(95,-104-y),28])
    side0,side1=(lo,-704) if p['program_type']==1 else (end+104,hi)
    frame0,frame1=(lo,0) if p['program_type']==1 else (end,hi)
    for i,y in enumerate(range(0,W,600)):
        add('terrace-side/joist-'+str(i),[frame0,y,F-173],[frame1-frame0,45,145],'timber')
    for i,x in enumerate(range(side0,side1,100)):
        add('terrace-side/board-'+str(i),[x,0,F-28],[min(95,side1-x),W,28])
    return ((hi-lo)*(Y-104)+(side1-side0)*W)/1e6


def foundation(p,parts,interfaces,L,W,F,annex):
    lo,hi=bounds(p,L,W,annex)
    parts[:]=[a for a in parts if a['family']!='foundation']
    xs=list(range(lo,hi+1,X));ys=list(range(-Y,W+1,Y));nodes=[]
    def add(id,o,s,mat):
        parts.append(dict(id=id,origin=o,size=s,material=mat,family='foundation',assembly='foundation-platform',engineering_status='coordination-only'))
    concrete=p['foundation_type']==1;dz=300 if concrete else 145
    material='concrete-study' if concrete else 'timber'
    if p['include_foundation']:
        for j,y in enumerate(ys):
            for i,x in enumerate(xs):
                nodes.append([x,y]);add(f'foundation-grid-{j}/pile-{i}',[x-45,y-45,-800],[90,90,800-dz],'concrete-study')
            # Supported stock breaks, never interpolate or redistribute support nodes.
            cuts=[lo-45]
            while hi+45-cuts[-1]>6000:
                cuts.append(max(x for x in xs if cuts[-1]<x<=cuts[-1]+6000))
            cuts.append(hi+45)
            for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
                add(f'foundation-grid-{j}/beam-{i}',[a,y-45,-dz],[b-a,90,dz],material)
        for i,x in enumerate(xs):
            for j,(a,b) in enumerate(zip(ys,ys[1:])):
                add(f'foundation-tie-{i}/member-{j}',[x-45,a+45,-dz],[90,b-a-90,dz],material)
        # Deck framing sits 65 mm above floor datum. Separate packing avoids
        # extending a packing member through the building floor.
        for i,x in enumerate(range(lo,hi,450)):
            for j,(y,h) in enumerate([(-Y,45),(-45,45)]):
                add(f'foundation-deck-front-{i}/packing-{j}',[x,y,0],[45,h,F-173],'timber')
        frame0,frame1=(lo,0) if p['program_type']==1 else (L+annex,hi)
        for i,y in enumerate(range(0,W,600)):
            for j,x in enumerate(range(frame0,frame1+1,X)):
                a=max(frame0,x-45);b=min(frame1,x+45)
                if b>a:add(f'foundation-deck-side-{i}/packing-{j}',[a,y,0],[b-a,45,F-173],'timber')
        interfaces.append(dict(id='cell-platform/bearings',type='900 x 1200 uniform support lattice',capacity=None,fasteners=None,status='soil, member spans, anchors and joint stiffness require engineering'))
    for label,y in [('front',-22),('back',W)]:
        parts.append(dict(id='floor-edge-'+label+'/board',origin=[0,y,0],size=[L+annex,22,220],material='cladding-wood',family='floor',assembly='floor-edge-'+label))
    for label,x in [('left',-22),('right',L+annex)]:
        parts.append(dict(id='floor-edge-'+label+'/board',origin=[x,0,0],size=[22,W,220],material='cladding-wood',family='floor',assembly='floor-edge-'+label))
    return dict(type=p['foundation_type'],label='Poliai ir medinės sijos' if not concrete else 'Poliai ir gelžbetoninis rostverkas',assembly_id='foundation-platform',connected_platform=True,status='geometry-study-not-engineered',grid_origin_mm=[0,0],coordination_pitch_mm=[X,Y],support_pitch_mm=[X,Y],support_nodes_mm=nodes,rows_mm=ys,provisional_dimensions=True,holds=['Repeated positions do not establish pile capacity, embedment, settlement or connection adequacy.'])
