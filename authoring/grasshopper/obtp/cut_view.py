"""Display-only horizontal cut shared by browser exports and Rhino preview."""
from .export import vertices

def clipped_part(part, level):
    points=vertices(part);lo=min(v[2] for v in points);hi=max(v[2] for v in points)
    if lo>=level:return None
    if hi<=level:return dict(part)
    if part.get('slope_y') or part.get('top_slope_y'):
        raise ValueError('Partial inclined solid needs explicit mesh clipping: '+part['id'])
    q=dict(part);q['origin']=list(part['origin']);q['size']=list(part['size'])
    q['size'][2]=level-q['origin'][2]
    return q

def parts_below(scene):
    level=scene['dimensions']['floor_top_mm']+1100
    return [q for p in scene['parts'] if (q:=clipped_part(p,level)) is not None]
