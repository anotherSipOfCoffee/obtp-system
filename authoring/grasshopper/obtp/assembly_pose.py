"""Rigid, display-only laydown poses; never change manufacturing dimensions."""
from collections import defaultdict
from .export import vertices

PREPARE={1:2,3:4,5:6,7:8}

def posed(parts, phase, classifier):
    """Lay out complete subassemblies in a separate ground work area."""
    target=PREPARE.get(phase)
    if target is None:return parts
    groups=defaultdict(list)
    for p in parts:
        if classifier(p)==target:groups[p['assembly']].append(p)
    matrices={};x=0;y=5000;row=0
    for name,items in sorted(groups.items()):
        vs=[v for p in items for v in vertices(p)]
        lo=[min(v[k] for v in vs) for k in range(3)]
        hi=[max(v[k] for v in vs) for k in range(3)]
        vertical=target in (4,8)
        axis=0 if hi[0]-lo[0]>=hi[1]-lo[1] else 1
        axes=(axis,2,1-axis) if vertical else (0,1,2)
        sizes=[hi[k]-lo[k] for k in axes]
        if x and x+sizes[0]>12000:x=0;y+=row+500;row=0
        # Right-handed rotation, not a reflection. Flip the normal if needed.
        sign=-1 if vertical and axis==0 else 1
        matrix=[[0.,0.,0.,0.] for _ in range(3)]
        for j,k in enumerate(axes):matrix[j][k]=sign if j==2 else 1
        matrix[0][3]=x-lo[axes[0]];matrix[1][3]=y-lo[axes[1]]
        matrix[2][3]=(-lo[axes[2]] if sign==1 else hi[axes[2]])
        matrices[name]=matrix;x+=sizes[0]+500;row=max(row,sizes[1])
    return [dict(p,display_transform=matrices[p['assembly']]) if p['assembly'] in matrices and classifier(p)==target else p for p in parts]

def display_vertices(part):
    vs=vertices(part);m=part.get('display_transform')
    return [[sum(row[k]*v[k] for k in range(3))+row[3] for row in m] for v in vs] if m else vs
