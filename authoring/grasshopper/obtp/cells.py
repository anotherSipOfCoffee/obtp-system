"""Shared 900 x 1200 coordination rules; capacities remain unresolved."""
import math

X, Y = 900, 1200


def enabled(p):
    return p.get('grid_system', 0) == 1


def resolve(p, wall=195):
    """Keep boundary frame faces on the envelope, internal wall starts on nodes.

    This avoids silently treating nominal cells as finished room dimensions.
    Corner/end deductions remain explicit terminal assemblies.
    """
    nx=p['sauna_length_steps']; nh=p['hall_length_steps']; ny=p['room_depth_steps']
    W=ny*Y; hot=nx*X-wall
    if p['program_type']==1:
        bs=nx*X; be=(nx+nh)*X; L=(nx+nh+p['storage_length_steps'])*X
        p['studio_zones']=dict(left_end=bs,bridge_start=bs,bridge_end=be,right_start=be+wall,right_clear=L-be-2*wall)
        hot=bs-2*wall; hall=be-bs; annex=0
    else:
        L=(nx+nh)*X;hall=nh*X-wall;annex=p['storage_length_steps']*X if p['storage'] else 0
    p['resolved_hot_mm']=hot
    p['resolved_hall_mm']=hall
    p['resolved_partition_x_mm']=wall+hot
    p['resolved_depth_mm']=W-2*wall
    p['annex_split_a_mm']=(650 if W==2400 else Y-wall)
    p['annex_split_b_mm']=(1650 if W==2400 else 2*Y-wall)
    return W,L,hot,hall,annex


def boundaries(start,end,step):
    return sorted(set([start,end]+[v for v in range(math.ceil(start/step)*step,math.floor(end/step)*step+1,step) if start<v<end]))


def opening(start,end,step,width,preferred):
    """Select a whole-bay opening envelope, including explicit terminal deductions."""
    axes=boundaries(start,end,step);choices=[]
    for i,a in enumerate(axes):
        for b in axes[i+1:]:
            if b-a < width+180:continue
            u=(a+b-width)/2
            if u-start<195 or end-(u+width)<195:continue
            choices.append((b-a,abs(u-preferred),a,b,u))
    if not choices:raise ValueError('Opening and framing do not fit whole cell bays')
    _,_,a,b,u=min(choices)
    return dict(start=u-start,lo=a-start,hi=b-start,nominal_bounds_mm=[a,b],rough_width_mm=width)


def wall_segments(base,axis,length,opening_envelope=None,forced=()):
    step=X if axis=='x' else Y;start=base[0 if axis=='x' else 1];end=start+length
    axes=sorted(set(boundaries(start,end,step)+[v for v in forced if start<v<end]))
    intervals=[]
    for a,b in zip(axes,axes[1:]):
        if opening_envelope and a<opening_envelope[1]-1e-6 and b>opening_envelope[0]+1e-6:continue
        if b-a<90:raise ValueError('Cell terminal too short for framing')
        intervals.append((a-start,b-start))
    return intervals


def record(p,L,W,annex,assemblies):
    return dict(schema='obtp-cell-system/1',id='shared-900x1200-r15',cell_mm=[X,Y],origin_mm=[0,0],
      reference='outer structural frame faces; internal wall near faces; explicit corner deductions',
      building_cells=[round(L/X),round(W/Y)],annex_cells=round(annex/X),
      wall_joint_policy='cell seams; openings replace whole adjoining bays',wall_assemblies=assemblies,
      engineering_status='coordination-study',holds=['Panel widths are coordination envelopes, not universal cut lengths.',
      'Terminal, opening and node connections require engineering; capacities and fasteners remain unset.'])
