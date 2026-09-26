"""Conceptual wall silhouettes derived from the model's authored wall envelopes.
No browser reconstruction, no third-party geometry dependency (native GH compatible).
"""
import copy

def subtract(r,h):
    x,y,X,Y=r;a,b,A,B=h;u,v=max(x,a),max(y,b);U,V=min(X,A),min(Y,B)
    if U<=u or V<=v:return [r]
    return [q for q in [(x,y,u,Y),(U,y,X,Y),(u,y,U,v),(u,V,U,Y)] if q[2]>q[0] and q[3]>q[1]]

def union_loops(rects):
    xs=sorted(set(round(v,5) for r in rects for v in [r[0],r[2]]));ys=sorted(set(round(v,5) for r in rects for v in [r[1],r[3]]))
    cells=set()
    for i in range(len(xs)-1):
        x=(xs[i]+xs[i+1])/2
        for j in range(len(ys)-1):
            y=(ys[j]+ys[j+1])/2
            if any(a<x<A and b<y<B for a,b,A,B in rects):cells.add((i,j))
    edges=set()
    for i,j in cells:
        for neighbor,a,b in [((i,j-1),(xs[i],ys[j]),(xs[i+1],ys[j])),((i+1,j),(xs[i+1],ys[j]),(xs[i+1],ys[j+1])),((i,j+1),(xs[i+1],ys[j+1]),(xs[i],ys[j+1])),((i-1,j),(xs[i],ys[j+1]),(xs[i],ys[j]))]:
            if neighbor not in cells:edges.add((a,b))
    loops=[]
    while edges:
        a,b=min(edges);edges.remove((a,b));loop=[a,b]
        while b!=a:
            choices=sorted(e for e in edges if e[0]==b)
            if not choices:raise ValueError('Open conceptual wall boundary')
            e=choices[0];edges.remove(e);b=e[1];loop.append(b)
        pts=loop[:-1];clean=[]
        for i,p in enumerate(pts):
            prev,nxt=pts[i-1],pts[(i+1)%len(pts)]
            if (p[0]-prev[0])*(nxt[1]-p[1])!=(p[1]-prev[1])*(nxt[0]-p[0]):clean.append(list(p))
        if len(clean)>2:loops.append(clean)
    return loops

def conceptual(scene,detailed):
    rects=[]
    for a in scene['wall_regions']:
        x,y=a['base'];w,h=(a['length'],a['depth']) if a['axis']=='x' else (a['depth'],a['length'])
        rs=[(x,y,x+w,y+h)]
        for v in scene['opening_voids']:
            vx,vy,_=v['origin'];vw,vh,_=v['size']
            rs=[q for r in rs for q in subtract(r,(vx,vy,vx+vw,vy+vh))]
        rects+=rs
    v=copy.deepcopy(detailed)
    v['polygons']=[p for p in v['polygons'] if p['family'] in ['furniture','terrace'] or p['id'].startswith('window/')]
    for p in v['polygons']:p['fill']='#ffffff';p['cut']=False
    v['wall_loops']=union_loops(rects)
    v['style']='conceptual';v['source_geometry_sha256']=scene['geometry_sha256']
    return v
