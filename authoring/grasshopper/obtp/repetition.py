"""Shared cut stations and physical bearing positions; no capacity assumptions."""
import math


def spans(start,end,pitch):
    cuts=[start]+[start+i*pitch for i in range(1,math.ceil((end-start)/pitch))]+[end]
    return list(zip(cuts,cuts[1:]))


def supports(start,end,pitch,width=45):
    """Full-width end seats and centred interior seats, without overlaps."""
    if end-start<=width:return [start]
    positions=[start]+[start+i*pitch-width/2 for i in range(1,math.ceil((end-start)/pitch)) if start+i*pitch-width/2<=end-width]
    while len(positions)>1 and end-width-positions[-1]<width:positions.pop()
    if end-width-positions[-1]>=width:positions.append(end-width)
    return positions


def finish_spans(start,end,wall=195,partition=90,lining_depth=36,sheathing=12):
    """Reuse 900/1800 extensions plus the recurring room-end cut.

    The terminal lengths follow the existing layer stack, not a second grid.
    Preserve short/constant runs instead of subdividing every finish board.
    """
    length=end-start
    for terminal in (1800-2*wall-2*lining_depth,1800-wall-partition-2*lining_depth-sheathing):
        steps=round((length-terminal)/900)
        if steps>0 and abs(length-terminal-steps*900)<1e-6:
            cuts=[];x=start
            while steps:
                count=min(2,steps);cuts.append((x,x+count*900));x+=count*900;steps-=count
            return cuts+[(x,end)]
    return [(start,end)]


def support_joints(start,end,joints,pitch=400,width=45):
    required=sorted(set([start,end-min(width,end-start)]+[x-width/2 for x in joints]))
    positions=list(required)
    for x in range(int(start),int(end-width)+1,pitch):
        if all(abs(x-y)>=width-1e-6 for y in positions):positions.append(x)
    return sorted(positions)
