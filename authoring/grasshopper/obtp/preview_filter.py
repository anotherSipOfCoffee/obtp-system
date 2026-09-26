"""Display-only semantic groups. Never modifies the canonical scene."""
GROUPS = (
 ('roof_beams', 'Roof beams / rafters / bearing'),
 ('roof_panels', 'Roof cassette panels / decking'),
 ('roof_cover', 'Roof covering / seams'),
 ('roof_fascia', 'Roof fascia'),
 ('facade', 'Facade boards'),
 ('facade_battens', 'Facade battens'),
 ('window_frames', 'Window frames'),
 ('glazing', 'Window and sliding glazing'),
 ('door_frames', 'Door frames / sliding tracks'),
 ('door_leaves', 'Door leaves'),
 ('wall_frame', 'Wall framing'),
 ('wall_panels', 'Wall sheathing'),
 ('partitions', 'Partition framing / panels'),
 ('floor_frame', 'Floor beams / blocking'),
 ('floor_panels', 'Floor panels'),
 ('insulation', 'Insulation'),
 ('interior', 'Interior lining / battens'),
 ('ceiling', 'Ceiling lining / battens'),
 ('terrace_frame', 'Terrace joists / bearers'),
 ('terrace_boards', 'Terrace boards'),
 ('foundation', 'Foundation study'),
 ('furniture', 'Furniture / heater / firewood rack'),
 ('other', 'Other parts'),
)

def category(part):
    id=part['id']; family=part['family']; material=part['material']
    if material=='glass':return 'glazing'
    if id.startswith('window/'):return 'window_frames'
    if '/door-leaf' in id:return 'door_leaves'
    if '/door-' in id or id.startswith('studio-slider-'):return 'door_frames'
    if family=='roof':
        if material=='timber':return 'roof_beams'
        if material=='plywood':return 'roof_panels'
        if material=='cladding-wood':return 'roof_fascia'
        return 'roof_cover'
    if family=='facade':return 'facade' if '/board-' in id else 'facade_battens'
    if family=='walls':return 'wall_panels' if material=='plywood' else 'wall_frame'
    if family=='floor':return 'floor_panels' if material=='plywood' else 'floor_frame'
    if family=='terrace':return 'terrace_boards' if '/board-' in id else 'terrace_frame'
    if family in ('partitions','insulation','interior','ceiling','foundation','furniture'):return family
    return 'other'

def visible(part, visibility=None, only=0):
    only=int(only or 0)
    if not 0<=only<=len(GROUPS):raise ValueError('Unknown preview isolation group')
    key=category(part)
    # Solo overrides switches; switching back restores their previous state.
    if only:return key==GROUPS[only-1][0]
    return (visibility or {}).get(key,True)

