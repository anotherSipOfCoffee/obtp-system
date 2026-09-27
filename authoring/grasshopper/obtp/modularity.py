"""Dimensional coordination and opening contracts, independent of display groups.
R21 retains R20 geometry after bounded kit screening. None of these records
certifies capacity, supplier compatibility, clear passage or a lifting unit.
"""
from .manufacturing import cladding
COORDINATION_MM=300
SOURCE_DATE='2026-09-27'
SUPPLIER_REFERENCES={
 'harvia-D91902M':dict(source='https://www.harvia.com/en/products/D91902M/glass-door-gray-9x19-pine-frame',frame_outside_mm=[890,1890,92],required_installation_opening_mm=None,clear_passage_mm=None,leaf_mm=None,verified='published product envelope only'),
 'swedoor-9x19':dict(source='https://www.swedoor.fi/ohjeet/mitoitus/ulko-ovien-mitat',frame_outside_mm=[888,1880,105],required_installation_opening_mm=[910,1900],clear_passage_mm=None,leaf_mm=None,verified='manufacturer size table; approximate installation opening; model availability unresolved'),
 'swedoor-10x21':dict(source='https://www.swedoor.fi/ohjeet/mitoitus/ulko-ovien-mitat',frame_outside_mm=[988,2080,105],required_installation_opening_mm=[1010,2100],clear_passage_mm=None,leaf_mm=None,verified='manufacturer size table; approximate installation opening; model availability unresolved'),
}


def procurement(scene):
    """Separate units without turning their display subparts into a saving."""
    ids=set();units=[]
    primary={p['id'] for p in scene['parts'] if not cladding(p)}
    for item in scene.get('object_library',{}).get('instances',[]):
        if not item.get('product'):continue
        selected=sorted(set(item['part_ids']) & primary)
        if not selected:continue
        if ids.intersection(selected):raise ValueError('Product representation claimed twice')
        ids.update(selected)
        units.append(dict(id=item['id'],supplier=item['product'].get('supplier'),manufacturer_code=item['product'].get('manufacturer_code'),
            representation_part_ids=selected,status=item['product']['status']))
    return dict(purchased_units=len(units),purchased_representation_ids=sorted(ids),units=units,
        counting_note='Purchased units replace no model pieces in the legacy total. Unknown equipment/furniture stays an explicit unresolved-object category. Supplier constituent BOMs unknown.')


def attach(scene):
    parts=scene['parts'];p=scene['config'];F=scene['dimensions']['floor_top_mm']
    assembly={a['id']:a for a in scene.get('cell_spec',{}).get('wall_assemblies',[])}
    records=[]
    for void in scene['opening_voids']:
        root=void['id'].rsplit('/',1)[0];is_window='window' in root
        host=assembly.get(void['id']);axis=0 if (host and host['axis']=='x') or (not host and void['size'][0]>void['size'][1]) else 1
        rough=[void['size'][axis],void['size'][2]];u=void['origin'][axis]
        members=[a for a in parts if a['assembly']==void['id'] and a['material'] in ('timber','plywood')]
        bounds=host['bounds_mm'] if host else [min(a['origin'][axis] for a in members),max(a['origin'][axis]+a['size'][axis] for a in members)]
        zones=[u-bounds[0],bounds[1]-u-rough[0]]
        prefix='window/' if is_window else root+'/door-'
        joinery=[a for a in parts if a['id'].startswith(prefix)]
        low=[min(a['origin'][k] for a in joinery) for k in range(3)]
        high=[max(a['origin'][k]+a['size'][k] for a in joinery) for k in range(3)]
        frame=[high[axis]-low[axis],high[2]-low[2]]
        leaf=next((a for a in joinery if a['id'].endswith('door-leaf')),None)
        supplier='harvia-D91902M' if root=='sauna-partition' and not p['program_type'] and rough==[900,1900] else None
        reference=SUPPLIER_REFERENCES.get(supplier)
        gaps=[low[axis]-u,u+rough[0]-high[axis],low[2]-void['origin'][2],void['origin'][2]+rough[1]-high[2]]
        candidates=[]
        if not is_window and not supplier:
            for code in ('swedoor-9x19','swedoor-10x21'):
                spec=SUPPLIER_REFERENCES[code];required=spec['required_installation_opening_mm']
                candidates.append(dict(reference=code,required_installation_opening_mm=required,
                    shortfall_mm=[max(0,required[i]-rough[i]) for i in range(2)],
                    geometric_rough_fit=all(required[i]<=rough[i] for i in range(2)),adopted=False))
        records.append(dict(id=void['id'],axis='xy'[axis],host_bounds_mm=bounds,host_width_mm=bounds[1]-bounds[0],
            installation_opening_mm=rough,installation_opening_origin_mm=void['origin'],
            modeled_frame_outside_mm=frame,verified_frame_outside_mm=reference['frame_outside_mm'] if reference else None,
            modeled_leaf_mm=[leaf['size'][axis],leaf['size'][2]] if leaf else None,verified_leaf_mm=None,
            clear_usable_passage_mm=None,passage_status='Not certified; hinges, leaf swing, seals and hardware unresolved',
            structural_side_zones_mm=zones,king_stud_width_mm=45,jack_stud_width_mm=45,header_bearing_mm=45,
            supported_infill_beyond_two_studs_mm=[max(0,z-90) for z in zones],
            adapter_detail='Existing full-width top/bottom plates, king and jack studs, counted side plywood and cavity fill; no loose thin filler assumed',
            component_ids=[a['id'] for a in members],
            modeled_installation_gaps_left_right_bottom_top_mm=gaps,
            manufacturer_installation_tolerances_mm=None,
            levels_mm=dict(structural_floor_top=F,modeled_finished_floor=F,finish_build_up_allowance=None,
                rough_sill=void['origin'][2],rough_head=void['origin'][2]+rough[1],frame_bottom=low[2],frame_head=high[2],threshold=None),
            source_reference=supplier,alternative_product_checks=candidates,
            status='Envelope verified; installation and usable passage unresolved' if supplier else 'Project geometry only; exact supplier product not verified'))
    return dict(schema='obtp-modularity/1',coordination_increment_mm=COORDINATION_MM,
        planning=dict(cell_mm=[900,1200] if p.get('grid_system') else [600,600],reference='Outer structural faces and internal near faces; not finished clear dimensions'),
        structural_assemblies=dict(policy='Retained R20 wall/floor/roof recipes; geometry is not forced onto 300 mm cut lengths',wall_assemblies=scene.get('cell_spec',{}).get('wall_assemblies',[])),
        manufactured_parts=dict(identity='obtp.manufacturing.identity',status='Provisional: unresolved grain, grade, machining, handedness and connection patterns'),
        purchased_products=procurement(scene),openings=records,
        connection_details=dict(records=scene['interfaces'],fastener_count=None,capacity_verified=False),
        supplier_references=SUPPLIER_REFERENCES,source_checked=SOURCE_DATE,
        selection='Retain baseline geometry: screened A/B alternatives do not improve the complete tradeoff',
        holds=['300 mm is a coordination reference, not a new physical bay or customer control.',
            'All opening clear passage, threshold and installation requirements require product-specific confirmation.',
            'Connected erection groups are display groups, not certified lifting units.'])
