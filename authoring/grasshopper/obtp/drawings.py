"""Deterministic intersections, dimensions and symbol anchors from canonical 3D.
All coordinates are mm. Browser/PDF only present this authored drawing data.
"""
import json,math
from pathlib import Path
from .export import vertices
EDGES=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
def hull(points):
    pts=sorted(set(tuple(round(v,6) for v in p) for p in points))
    if len(pts)<3:return []
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];hi=[]
    for p in pts:
        while len(lo)>1 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi)>1 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
        hi.append(p)
    return lo[:-1]+hi[:-1]
def section(part,axis,level):
    vs=vertices(part);pts=[];axes=[k for k in range(3) if k!=axis]
    for a,b in EDGES:
        u,v=vs[a],vs[b];d=v[axis]-u[axis]
        if abs(u[axis]-level)<1e-7:pts.append([u[k] for k in axes])
        if abs(d)>1e-9 and 0<=(t:=(level-u[axis])/d)<=1:pts.append([u[k]+t*(v[k]-u[k]) for k in axes])
    return hull(pts)
def dimension(a,b,offset=300,label=None):
    axis=0 if abs(a[0]-b[0])>=abs(a[1]-b[1]) else 1
    return dict(a=a,b=b,axis=axis,offset=offset,value_mm=abs(b[axis]-a[axis]),label=label)
def derive(scene):
    d=scene['dimensions'];p=scene['config'];L=d['length_mm'];W=d['width_mm'];F=d['floor_top_mm'];end=L+d['annex_length_mm']
    views={};rafters=[a for a in scene['parts'] if '/rafter-' in a['id']]
    section_x=min((a['origin'][0]+a['size'][0]/2 for a in rafters),key=lambda x:abs(x-(195+p['sauna_length_steps']*600/2)))
    cuts=[('plan',2,F+1100),('section-a',0,section_x),('section-b',1,W*.35)]
    for name,axis,level in cuts:
        polygons=[]
        for part in scene['parts']:
            poly=section(part,axis,level)
            cut=bool(poly)
            if name=='plan' and not cut and part['family'] in ['floor','terrace','furniture'] and max(v[2] for v in vertices(part))<level:
                poly=hull([v[:2] for v in vertices(part)])
            if name!='plan' and not cut and part['family']=='furniture':
                axes=[k for k in range(3) if k!=axis];poly=hull([[v[k] for k in axes] for v in vertices(part)])
            if not poly:continue
            wall=part['family'] in ['walls','partitions','interior','facade'] or part['id'].startswith('insulation-') and not part['id'].startswith(('insulation-ceiling','insulation-floor'))
            fill='#111111' if cut and wall and part['material'] not in ['object','glass'] else '#eeeeee' if cut else '#ffffff'
            polygons.append(dict(id=part['id'],points=poly,fill=fill,cut=cut,material=part['material'],family=part['family']))
        # Put black sectioned walls above projected furniture/floor.
        polygons.sort(key=lambda a:a['cut'])
        if name=='plan':
            dims=[dimension([0,0],[end,0],-550),dimension([0,0],[0,W],-500),dimension([195,W],[195+p['sauna_length_steps']*600,W],400),dimension([195+p['sauna_length_steps']*600+p['partition_depth'],W],[L-195,W],400)]
            for v in scene['opening_voids']:
                x,y,z=v['origin'];a,b,h=v['size'];dims.append(dimension([x,y],[x+a,y] if a>b else [x,y+b],400 if v['id']=='annex-end/opening' else -220))
            dims.append(dimension([end,-104-p['terrace_steps']*600],[end,-104],450))
        else:
            width=W if axis==0 else end
            dims=[dimension([0,0],[width,0],-300),dimension([width,F],[width,F+p['wall_height']],400),dimension([0,0],[0,scene['metrics']['height_mm']],-450)]
        views[name]=dict(axis=axis,level_mm=level,polygons=polygons,dimensions=dims,polylines=[])
    if p['roof_type']==2:
        ridge=[v for a in scene['parts'] if a['id'].startswith('ridge-cap/') for v in vertices(a)]
        views['section-b']['guides']=[dict(points=[[min(v[0] for v in ridge),max(v[2] for v in ridge)],[max(v[0] for v in ridge),max(v[2] for v in ridge)]],label='Kraigo projekcija')]
    views['plan']['labels']=[dict(at=[195+p['sauna_length_steps']*600-600,W*.40],text='Pirtis'),dict(at=[195+p['sauna_length_steps']*600+p['partition_depth']+(p['hall_length_steps']*600-p['partition_depth'])/2,W*.75],text='Prieangis')]
    if p['storage']:views['plan']['labels'].append(dict(at=[L+d['annex_length_mm']/2,195+(W-390)*.58],text='Sandėliukas'))
    # Window schedule is projected from actual joinery parts, never guessed from UI width.
    window=[a for a in scene['parts'] if a['id'].startswith('window/')]
    x0=min(a['origin'][0] for a in window);z0=min(a['origin'][2] for a in window)
    polys=[]
    for a in window:
        polys.append(dict(id=a['id'],points=hull([[v[0]-x0,v[2]-z0] for v in vertices(a)]),fill='#eeeeee' if a['material']=='glass' else '#ffffff',cut=False,material=a['material']))
    views['window']=dict(axis=1,level_mm=98,polygons=polys,polylines=[],dimensions=[dimension([0,0],[p['window_width'],0],-180),dimension([p['window_width'],0],[p['window_width'],p['door_height']-20],180)])
    views['window-plan']=dict(axis=2,level_mm=F+1100,polygons=[dict(id=a['id'],points=[[v[0]-x0,v[1]] for v in section(a,2,F+1100)],fill='#eeeeee',cut=True,material=a['material']) for a in window],polylines=[],dimensions=[])
    # Source DXF blocks provide optional plan symbols. Interior benches remain true 3D projections:
    # source file contains Outdoor Bench, not a vetted interior sauna-bench symbol.
    source=Path(__file__).with_name('symbols.json')
    if source.exists():
        symbols=json.loads(source.read_text())
        def place(name,origin,sx=1,sy=1,angle=0):
            c,s=math.cos(angle),math.sin(angle)
            for line in symbols['blocks'][name]['lines']:
                views['plan']['polylines'].append([[origin[0]+c*x*sx-s*y*sy,origin[1]+s*x*sx+c*y*sy] for x,y in line])
        for v in scene['opening_voids']:
            if 'window' in v['id']:continue
            x,y,z=v['origin'];a,b,h=v['size'];axis=0 if a>b else 1;size=a if axis==0 else b
            # Door source X runs -450..450 and opens toward positive Y.
            origin=[x+a/2,y+b/2];place('Door Lining',origin,size/900,size/900,math.pi if axis==0 else -math.pi/2)
        seat=next((a for a in scene['parts'] if a['id']=='outside-seat/seat'),None)
        if seat:place('Outdoor Bench',[seat['origin'][0],seat['origin'][1]+seat['size'][1]],seat['size'][0]/1100,seat['size'][1]/333.776002644)
        views['plan']['symbol_source_sha256']=symbols['source_sha256']
    from .plan_styles import conceptual
    views['concept-plan']=conceptual(scene,views['plan'])
    # Jamb detail at the same cut as plan, cropped around the actual window edge.
    wx=min(a['origin'][0] for a in window);detail=[]
    for a in views['plan']['polygons']:
        pts=a['points']
        if pts and min(q[0] for q in pts)<wx+140 and max(q[0] for q in pts)>wx-300 and min(q[1] for q in pts)<270 and max(q[1] for q in pts)>-90:detail.append(a)
    views['window-jamb']=dict(axis=2,level_mm=F+1100,polygons=detail,polylines=[],dimensions=[dimension([wx,12.5],[wx,182.5],-180),dimension([wx,12.5],[wx+51,12.5],-70)],crop=[wx-260,-110,wx+140,250])
    return dict(schema='obtp-drawings/2',source_geometry_sha256=scene['geometry_sha256'],units='mm',views=views,
      cut_markers=[dict(name='A-A',axis=0,position=cuts[1][2]),dict(name='B-B',axis=1,position=cuts[2][2])])

def dimension_lines(dim):
    a,b=dim['a'],dim['b'];k=dim['axis'];j=1-k;o=dim['offset'];u=list(a);v=list(b);u[j]+=o;v[j]+=o
    return [(a,u),(b,v),(u,v)],[(u[0]+v[0])/2,(u[1]+v[1])/2],dim.get('label') or str(round(dim['value_mm']))

def svg(view):
    from html import escape
    pts=[p for a in view['polygons'] for p in a['points']]+[p for a in view['polylines'] for p in a]
    pts += [p for loop in view.get('wall_loops',[]) for p in loop]
    for d in view['dimensions']:
        ls,_,_=dimension_lines(d);pts += [p for l in ls for p in l]
    lo=[min(p[k] for p in pts)-250 for k in (0,1)];hi=[max(p[k] for p in pts)+250 for k in (0,1)]
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{lo[0]} {-hi[1]} {hi[0]-lo[0]} {hi[1]-lo[1]}"><rect x="{lo[0]}" y="{-hi[1]}" width="{hi[0]-lo[0]}" height="{hi[1]-lo[1]}" fill="white"/>']
    if view.get('wall_loops'):
        path=' '.join('M'+' L'.join(f'{x},{-y}' for x,y in loop)+' Z' for loop in view['wall_loops'])
        out.append(f'<path d="{path}" fill="#111" fill-rule="evenodd"/>')
    for a in view['polygons']:out.append('<polygon points="'+' '.join(f'{x},{-y}' for x,y in a['points'])+f'" fill="{a["fill"]}" stroke="#222" stroke-width="6"/>')
    for a in view['polylines']:out.append('<polyline points="'+' '.join(f'{x},{-y}' for x,y in a)+'" fill="none" stroke="#222" stroke-width="8"/>')
    for a in view.get('labels',[]):out.append(f'<text x="{a["at"][0]}" y="{-a["at"][1]}" font-family="Arial" font-size="90" text-anchor="middle">{escape(a["text"])}</text>')
    for d in view['dimensions']:
        lines,pt,label=dimension_lines(d)
        for a,b in lines:out.append(f'<path d="M{a[0]},{-a[1]} L{b[0]},{-b[1]}" stroke="#555" stroke-width="5"/>')
        out.append(f'<text x="{pt[0]}" y="{-pt[1]-30}" font-family="Arial" font-size="90" text-anchor="middle">{escape(label)}</text>')
    return ''.join(out)+'</svg>'
