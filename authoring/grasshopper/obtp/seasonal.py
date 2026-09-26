"""Seasonal court and open log rack: coordination objects, not thermal approval."""
def enrich(p,parts,L,W,F,H,interfaces):
    if p['program_type']!=1:return None
    z=p['studio_zones'];left=z['bridge_start']+84;right=z['bridge_end']-84
    width=right-left;closed=p['studio_winter_closed'];panel=(width+100)/3
    def add(id,o,s,mat='object'):
        parts.append(dict(id=id,origin=o,size=s,material=mat,family='furniture',assembly=id.split('/')[0]))
    for side,y in [('front',0),('rear',W-150)]:
        group='studio-slider-'+side
        for label,zz in [('sill',F),('head',F+H-50)]:add(group+'/'+label,[left,y,zz],[width,150,50])
        for j in range(3):
            x=left+j*(panel-50) if closed else left
            yy=y+j*45
            add(group+'/glass-'+str(j),[x+35,yy+15,F+50],[panel-70,12,H-100],'glass')
            for edge,xx in [('left',x),('right',x+panel-35)]:add(group+'/'+edge+'-'+str(j),[xx,yy,F+50],[35,40,H-100])
            for edge,zz in [('bottom',F+50),('top',F+H-85)]:add(group+'/'+edge+'-'+str(j),[x+35,yy,zz],[panel-70,40,35])
    # Documented body envelope only; deliberately no fabricated flue installation.
    add('studio-stove/body',[left+400,W-950,F],[388,368,715])
    # Open-front rack on left short end, separated from cladding by a 100mm gap.
    for j,y in enumerate([195,W-240]):add('firewood-rack/upright-'+str(j),[-784,y,F],[45,45,1500])
    add('firewood-rack/base',[-784,195,F],[600,W-390,45])
    add('firewood-rack/top',[-784,195,F+1500],[600,W-390,45])
    for j,zz in enumerate([F+300,F+750,F+1200]):add('firewood-rack/back-rail-'+str(j),[-229,195,zz],[45,W-390,45])
    interfaces.append(dict(id='studio-slider/host',type='sliding enclosure threshold/head coordination',capacity=None,fasteners=None))
    return dict(state='closed' if closed else 'open',thermal_status='unheated seasonal buffer; no energy saving calculated',
        clear_opening_study_mm=width-panel,
        heater=dict(manufacturer='Morso',model='1442',body_mm=[388,368,715],status='body-envelope-only; not installation-ready',
          source='https://morsoe.com/other/product/indoor/wood-burning-stove/p1442_int',
          unresolved=['heater sizing','combustible clearances','hearth','combustion air','flue route and roof penetration','door operation and escape route']),
        firewood=dict(side='left short end',depth_mm=600,status='open rack; no enclosing doors'))
