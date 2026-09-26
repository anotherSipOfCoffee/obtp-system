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
    # Recess framed by extensions of the long walls; no freestanding rack.
    for i,y in enumerate(range(195,W-195,100)):
        add('firewood-niche/board-'+str(i),[-600,y,F-28],[516,min(95,W-195-y),28],'deck-wood')
    interfaces.append(dict(id='studio-slider/host',type='sliding enclosure threshold/head coordination',capacity=None,fasteners=None))
    return dict(state='closed' if closed else 'open',thermal_status='heated winter room design intent; U-values and energy use not calculated',
        glazing_requirement=dict(type='thermally broken insulated sliding system',candidate='Schuco ASE60 triple-track',status='candidate only; minimum sash size and threshold installation require supplier confirmation',Uw_W_m2K=None,source='https://www.schueco.com/lt/architektams/gaminiai/slankiosios-sistemos/sliding-and-lift-sliding-systems-/ase60'),
        operating_modes=dict(winter='closed glazing; heated envelope',summer='stacked sliding panels; heating off'),
        physical_profiles_status='generic coordination placeholders, not manufacturer profiles',
        clear_opening_study_mm=width-panel,
        heater=dict(manufacturer='Morso',model='1442',body_mm=[388,368,715],status='body-envelope-only; not installation-ready',
          source='https://morsoe.com/other/product/indoor/wood-burning-stove/p1442_int',
          unresolved=['heater sizing','combustible clearances','hearth','combustion air','flue route and roof penetration','door operation and escape route']),
        firewood=dict(side='left short end',depth_mm=600,status='recess between extended long walls; open short end'))
