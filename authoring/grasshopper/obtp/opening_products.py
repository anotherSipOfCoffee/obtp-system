"""Pinned supplier identities and price evidence; unknown quotations are never zero."""
DATE='2026-09-26'
HARVIA=dict(supplier='Harvia',product='Glass door grey / pine',manufacturer_code='D91902M',ean='6417659010030',frame_mm=[890,1890,92],
 source='https://www.harvia.com/en/products/D91902M/glass-door-gray-9x19-pine-frame',price_eur=344.0,
 price_source='https://saunabee.com/product/quick_view?product_id=1561',price_basis='Retail listing; VAT basis and Lithuania delivery need confirmation',
 status='documented product envelope; profile/hardware omitted',checked=DATE)

def record(scene,item):
    ids=item['part_ids'];p=scene['config'];is_sauna=p['program_type']==0
    if item['id']=='sauna-partition/door' and is_sauna and p['door_width']==900 and p['door_height']==1900:
        return dict(HARVIA,project_id='D-HARVIA-D91902M')
    if any(id.startswith('window/') for id in ids):
        return dict(supplier='Pihla',product='Saunan ikkuna / fixed' if is_sauna else 'Varma Kiinteä / fixed candidate',manufacturer_code='24201' if is_sauna else None,
          project_id=f"L-PIHLA-{p['window_width']}-1880",frame_mm=[p['window_width'],p['door_height']-20,170],price_eur=None,price_basis='Dimension-specific quotation required',
          source='https://www.pihla.fi/product/saunan-ikkuna/' if is_sauna else 'https://www.pihla.fi/ikkunat/kiinteat-ikkunat/',checked=DATE,
          status='dimensional candidate; exact glazing, size acceptance and price not confirmed')
    if any(id.startswith('studio-slider-') for id in ids):
        return dict(supplier='Doleta',product='Lift-and-slide / custom candidate',manufacturer_code=None,project_id='SD-DOLETA-'+item['id'].split('/')[0],
          frame_mm=None,price_eur=None,price_basis='Supplier quotation required',source='https://www.doleta.lt/lt/produktai/slankiojancios-sistemos/prasilenkiancios-sistemos-lift-and-slide/',checked=DATE,
          status='Supplier candidate only; model remains generic. Triple-track feasibility and profiles unverified.')
    return dict(supplier='Doleta',product='Timber exterior door / custom candidate',manufacturer_code=None,project_id='D-DOLETA-'+item['id'].split('/')[0],
      frame_mm=None,price_eur=None,price_basis='Supplier quotation required',source='https://www.doleta.lt/lt/produktai/lauko-durys/medines-lauko-durys/',checked=DATE,
      status='Supplier candidate only; current envelope is project-required size, not an approved supplier model')

def apply_sauna_door(parts,name,width,height,d):
    # Called before geometry generation. Published external dimensions only.
    if name!='sauna-partition' or width!=900 or height!=1900:return None
    # Simplified boundary profiles are explicitly NOT a manufacturer CAD reconstruction.
    return [('door-jamb-left',5,(d-92)/2,0,30,92,1890),('door-jamb-right',865,(d-92)/2,0,30,92,1890),
      ('door-head',35,(d-92)/2,1860,830,92,30),('door-leaf',35,(d-8)/2,10,830,8,1850)]
