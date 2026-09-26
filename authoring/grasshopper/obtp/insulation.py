"""Cavity-fill study. Subtract actual framing/void boxes; never cover openings.
Membranes are zero-thickness layer specifications, not counterfeit structural solids.
"""
def subtract(a,b):
    o,s=a;v,t=b;lo=[max(o[k],v[k]) for k in range(3)];hi=[min(o[k]+s[k],v[k]+t[k]) for k in range(3)]
    if any(hi[k]<=lo[k] for k in range(3)):return [a]
    result=[];mn=list(o);mx=[o[k]+s[k] for k in range(3)]
    for k in range(3):
        if mn[k]<lo[k]:
            top=list(mx);top[k]=lo[k];result.append((list(mn),[top[j]-mn[j] for j in range(3)]));mn[k]=lo[k]
        if mx[k]>hi[k]:
            bot=list(mn);bot[k]=hi[k];result.append((bot,[mx[j]-bot[j] for j in range(3)]));mx[k]=hi[k]
    return result

def enrich(parts,voids,L,W,F,H,annex,px,p):
    wall=195;end=L+annex
    zones=[('front',[wall,0,F],[L-2*wall,wall,H]),('back',[wall,W-wall,F],[L-2*wall,wall,H]),('hot',[0,0,F],[wall,W,H]),('hall',[L-wall,0,F],[wall,W,H]),('partition',[px,wall,F],[p['partition_depth'],W-2*wall,H]),('ceiling',[0,0,F+H],[end,W,220]),('floor',[0,0,0],[end,W,220])]
    if annex:zones.append(('storage',[end-wall,0,F],[wall,W,H]))
    if p.get('program_type',0)==1:
        z=p['studio_zones'];zones=[]
        for name,a,b in [('left',0,z['bridge_start']),('right',z['bridge_end'],L)]:
            zones += [(name+'-front',[a+wall,0,F],[b-a-2*wall,wall,H]),(name+'-back',[a+wall,W-wall,F],[b-a-2*wall,wall,H]),(name+'-end-a',[a,0,F],[wall,W,H]),(name+'-end-b',[b-wall,0,F],[wall,W,H]),('ceiling-'+name,[a,0,F+H],[b-a,W,220]),('floor-'+name,[a,0,0],[b-a,W,220])]
        zones += [('ceiling-centre',[z['bridge_start'],0,F+H],[z['bridge_end']-z['bridge_start'],W,220]),('floor-centre',[z['bridge_start'],0,0],[z['bridge_end']-z['bridge_start'],W,220])]
    original=list(parts)
    for name,o,s in zones:
        boxes=[(o,s)]
        for a in original:
            if a['material'] not in ['timber','plywood']:continue
            if a.get('slope_y') or a.get('top_slope_y'):continue
            boxes=[q for b in boxes for q in subtract(b,(a['origin'],a['size']))]
        for v in voids:boxes=[q for b in boxes for q in subtract(b,(v['origin'],v['size']))]
        for i,(origin,size) in enumerate(boxes):
            parts.append(dict(id='insulation-'+name+'/'+str(i),origin=origin,size=size,material='mineral-wool',family='insulation',assembly='insulation-'+name))
    result=dict(status='assembly-study',use='intermittently heated year-round sauna',
      wall_cavity_mm=195,ceiling_cavity_mm=220,floor_cavity_mm=220,
      inside_to_outside=['16 mm timber lining','20 mm ventilated batten cavity','sealed sauna-rated aluminium vapour control layer; tape laps and penetrations','195 mm framed mineral-wool cavity','12 mm structural sheathing; drying assessment required','vapour-open wind barrier','25 mm vertical drainage cavity + 25 mm cross battens','22 mm vertical timber cladding'],
      membrane_geometry='zero-thickness specification; not included in wood quantities',
      holds=['Hygrothermal assessment of exterior sheathing and intermittently heated hall remains required.','Heater model, ventilation, fire distances, drying cycle and frost-drainable outdoor shower remain to be specified.','No U-value or energy class is claimed.'])

    if p.get('program_type',0)==1:
        result['use']='heated non-residential studio including central room; summer sliding ventilation'
        result['heated_centre']=True
        result['floor_layers']=['18mm structural plywood','220mm framed mineral-wool cavity','underside wind/moisture protection: product and detail required']
        result['ceiling_layers']=['16mm lining','20mm service battens','continuous airtight vapour-control layer: product required','220mm framed mineral-wool cavity','18mm roof cassette sheathing','ventilated weather roof']
        result['junction_requirements']=['airtight floor-to-slider sill joint','insulated load-bearing sill support: unresolved','external drained sill pan and deck separation','head/jamb air barrier continuity','thermal bridge assessment at all slider interfaces']
        result['inside_to_outside'][2]='vapour-control product and hygrothermal design required; no sauna foil selected'
        result['holds']=['Occupied studio ventilation, heating, material products and moisture design remain unresolved.','No U-value or energy class is claimed.']
    return result
