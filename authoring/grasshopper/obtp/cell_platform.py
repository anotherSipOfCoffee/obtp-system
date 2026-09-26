"""Repetitive building/terrace platform; member envelopes are not engineered."""
from .cells import X,Y


def bounds(p,L,W,annex):
    return (-2*X,L) if p['program_type']==1 else (0,L+annex+X)


def terrace(p,parts,L,W,F,annex):
    parts[:]=[a for a in parts if a['family']!='terrace']
    lo,hi=bounds(p,L,W,annex);end=L+annex
    def add(id,o,s,mat='deck-wood'):
        parts.append(dict(id=id,origin=o,size=s,material=mat,family='terrace',assembly=id.split('/')[0]))
    # One X-directed board family throughout front and return. Butt joints land
    # on joists; no rotated return and no boards longer than 1800 mm.
    side0,side1=(lo,-704) if p['program_type']==1 else (end+104,hi)
    def strip(name,x0,x1,y0,y1):
        cuts=[x0]+[x for x in range(lo,hi+1,1800) if x0<x<x1]+[x1]
        supports=sorted(set([x0,x1-45]+[x-22.5 for x in cuts[1:-1]]))
        for x in range(lo,hi,450):
            if x0<=x<=x1-45 and all(abs(x-seat)>=45 for seat in supports):supports.append(x)
        supports.sort()
        # Remove a redundant near-end support, retaining every board-joint seat.
        for i,x in enumerate(supports):
            # Return joists continue through the front terrace, closing the
            # corner without overlapping a separate front joist.
            if name=='terrace-side':
                parts[:]=[a for a in parts if not (a['id'].startswith('terrace/joist-') and abs(a['origin'][0]-x)<0.01)]
            frame_start=-Y if name=='terrace-side' else y0
            frame_end=(-22 if x<end and x+45>0 else 0) if y1==-104 else y1
            add(name+'/joist-'+str(i),[x,frame_start,F-173],[45,frame_end-frame_start,145],'timber')
        for i,y in enumerate(range(y0,y1,100)):
            for j,(a,b) in enumerate(zip(cuts,cuts[1:])):
                add(name+'/board-'+str(i)+'-'+str(j),[a,y,F-28],[b-a,min(95,y1-y),28])
        return supports
    strip('terrace',lo,hi,-Y,-104)
    strip('terrace-side',side0,side1,-100,W)
    return ((hi-lo)*(Y-104)+(side1-side0)*(W+100))/1e6


def foundation(p,parts,interfaces,L,W,F,annex):
    lo,hi=bounds(p,L,W,annex)
    bearing_width=145 # shared study rail; clears floor trim with a >=45 mm deck seat
    parts[:]=[a for a in parts if a['family']!='foundation']
    xs=sorted(set(list(range(lo,hi+1,2*X))+[hi]));ys=list(range(-Y,W+1,Y));nodes=[]
    def add(id,o,s,mat):
        parts.append(dict(id=id,origin=o,size=s,material=mat,family='foundation',assembly='foundation-platform',engineering_status='coordination-only'))
    concrete=p['foundation_type']==1;dz=300 if concrete else 145
    material='concrete-study' if concrete else 'timber'
    if p['include_foundation']:
        for j,y in enumerate(ys):
            for i,x in enumerate(xs):
                nodes.append([x,y]);add(f'foundation-grid-{j}/pile-{i}',[x-45,y-45,-800],[90,90,800-dz],'concrete-study')
            # Short beam segments end at actual bearings. The planning pitch
            # remains 900; supports normally span two cells, with a terminal bay.
            cuts=[lo-45]+xs[1:-1]+[hi+45]
            for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
                add(f'foundation-grid-{j}/beam-{i}',[a,y-bearing_width/2,-dz],[b-a,bearing_width,dz],material)
        for i,x in enumerate(xs):
            for j,(a,b) in enumerate(zip(ys,ys[1:])):
                add(f'foundation-tie-{i}/member-{j}',[x-45,a+bearing_width/2,-dz],[90,b-a-bearing_width,dz],material)
        # Pack each actual deck joist at each crossed platform bearing row.
        deck=[a for a in parts if a['material']=='timber' and (a['family']=='terrace' or a['id'].startswith('firewood-niche/joist-'))]
        for i,a in enumerate(deck):
            x,y,_=a['origin'];dx,dy,_=a['size']
            for j,row in enumerate(ys):
                low=max(y,row-bearing_width/2);high=min(y+dy,row+bearing_width/2)
                if high>low:add(f'foundation-deck-{i}/packing-{j}',[x,low,0],[dx,high-low,F-173],'timber')
        interfaces.append(dict(id='cell-platform/bearings',type='1800 x 1200 support rhythm with explicit terminal bays',capacity=None,fasteners=None,status='soil, member spans, anchors and joint stiffness require engineering'))
    for label,y in [('front',-22),('back',W)]:
        parts.append(dict(id='floor-edge-'+label+'/board',origin=[0,y,0],size=[L+annex,22,220],material='cladding-wood',family='floor',assembly='floor-edge-'+label))
    for label,x in [('left',-22),('right',L+annex)]:
        parts.append(dict(id='floor-edge-'+label+'/board',origin=[x,0,0],size=[22,W,220],material='cladding-wood',family='floor',assembly='floor-edge-'+label))
    return dict(type=p['foundation_type'],label='Poliai ir medinės sijos' if not concrete else 'Poliai ir gelžbetoninis rostverkas',assembly_id='foundation-platform',connected_platform=True,status='geometry-study-not-engineered',grid_origin_mm=[0,0],coordination_pitch_mm=[X,Y],support_pitch_mm=[2*X,Y],support_nodes_mm=nodes,rows_mm=ys,provisional_dimensions=True,bearing_width_mm=bearing_width,holds=['Repeated positions do not establish pile capacity, embedment, settlement or connection adequacy.'])
