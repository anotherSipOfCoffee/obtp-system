"""Geometric standardisation and one-dimensional stock study, not structural optimisation."""
from collections import defaultdict

def signature(a,normalised=True):
    dims=tuple(round(x,6) for x in a['size'])
    if normalised and a['material']=='timber' and not a.get('slope_y') and not a.get('top_slope_y'):
        dims=tuple(sorted(dims))
    return (a['family'],a['material'],dims,round(a.get('slope_y',0),8),round(a.get('top_slope_y',0),8))

def analyse(scene):
    wood=[a for a in scene['parts'] if a['material'] in ('timber','plywood','lining-wood','cladding-wood','deck-wood')]
    raw=len({signature(a,False) for a in wood});normal=len({signature(a) for a in wood})
    sections=defaultdict(list);excluded=[]
    for a in wood:
        if a['material']!='timber' or a.get('slope_y') or a.get('top_slope_y'):continue
        w,h,l=sorted(a['size'])
        if l>6000 or l<3*h:excluded.append(a['id']);continue
        sections[(w,h)].append((l,a['id']))
    stock=[]
    for section,items in sorted(sections.items()):
        bins=[]
        for length,id in sorted(items,reverse=True):
            target=next((b for b in bins if b['used_mm']+length+3<=6000),None)
            if target is None:target={'section_mm':list(section),'used_mm':0,'cuts':[]};bins.append(target)
            target['cuts'].append({'id':id,'length_mm':length});target['used_mm']+=length+3
        stock.extend(bins)
    used=sum(b['used_mm'] for b in stock)
    return dict(schema='obtp-component-rationalisation/1',physical_wood_parts=len(wood),orientation_specific_types=raw,normalised_types=normal,
      fewer_geometric_types=raw-normal,stock_length_mm=6000,assumed_kerf_mm=3,stock_bars=len(stock),
      stock_utilisation_percent=round(100*used/(6000*len(stock)),2) if stock else None,cutting_plan=stock,excluded_ids=excluded,
      method='orientation-normalised rectangular timber types; first-fit-decreasing 1D cutting-stock heuristic',
      scope='No member deletion, reduced sections or new structural splices. Rotation does not certify grain, grade, machining or connection equivalence.',
      holds=['6000mm stock and 3mm kerf are explicit study inputs; confirm availability and end trim.','No 2D plywood nesting, defects, grading, toolpaths or assembly-time calculation.','Fractal hierarchy retained as module > cassette > part; recursive subdivision is not an optimisation objective.'])
