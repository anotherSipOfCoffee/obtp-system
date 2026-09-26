"""Traceable analysis preparation. No engineering defaults and no simulated results.
Coordinates are exported in metres from canonical detailed solids, never web meshes.
"""
import copy
import hashlib
import json
import math
from collections import Counter
from .export import vertices


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def inputs():
    return {
      'scope': {'wind':'paused_by_owner','snow':'paused_by_owner'},
      'site': {'country':'Lithuania','location_scope':'general, no site-specific design values','topography':'ideally flat (owner brief; survey pending)',
               'coordinates':None,'altitude_m':None,'north_degrees':None,
               'terrain_by_direction':None,'wind_na_edition':None,'snow_na_edition':None},
      'thermal':{'design_external_temperature_C':None,'surface_resistances':None,
                 'materials':{},'window_Uw_W_m2K':None,'ventilation_schedule':None},
      'structure':{'materials':{},'member_local_axes':{},'connections':{},'supports':{},
                   'permanent_actions':None,'imposed_actions':None,'snow_actions':None,
                   'wind_actions':None,'combinations':None},
      'stages':[
        {'id':'before','heater_power_W':0,'duration_s':None,'initial_temperature_C':None,'relative_humidity':None},
        {'id':'during','heater_rated_power_W':9000,'duty_schedule':None,'duration_s':None,'temperature_setpoint_C':None,'moisture_generation_kg_s':None},
        {'id':'after','heater_power_W':0,'duration_s':None,'ventilation_schedule':None,'initial_state':'from completed during-stage solution'}],
      'heater':{'candidate':'Harvia Spirit SP90E / HSPE904M','rated_power_W':9000,
                'body_mm':[385,334,687],'room_range_m3':[8,14],
                'status':'candidate only; mounting, clearances and adjusted room volume not accepted',
                'source':'https://www.harvia.com/en/products/HSPE904M/spirit-sp90e-90-kw-black'}}


def prepare(scene,settings=None):
    cfg=copy.deepcopy(inputs() if settings is None else settings)
    parts=scene['parts']; ids=[p['id'] for p in parts]
    if len(set(ids))!=len(ids):raise ValueError('Duplicate source part IDs')
    if scene['units']!='mm':raise ValueError('Expected canonical millimetre model')
    solids=[]
    for p in parts:
        vs=vertices(p)
        if not all(math.isfinite(x) for v in vs for x in v):raise ValueError('Nonfinite part '+p['id'])
        if any(x<=0 for x in p['size']):raise ValueError('Nonpositive size '+p['id'])
        if any(vs[i+4][2]<=vs[i][2] for i in range(4)):raise ValueError('Inverted prism '+p['id'])
        solids.append({'id':p['id'],'assembly':p['assembly'],'family':p['family'],
                       'material':p['material'],'vertices_m':[[x/1000 for x in v] for v in vs],
                       'size_m':[x/1000 for x in p['size']]})
    # Independent content hash includes joints/specs, not just visual geometry.
    source=digest({'parts':parts,'interfaces':scene['interfaces'],
                   'envelope':scene['envelope_spec'],'window':scene['window_spec'],'suppliers':scene.get('supplier_spec')})
    sections={}
    for name in ['plan','section-a','section-b','window-head','window-sill']:
        v=scene['drawings']['views'][name]
        sections[name]={'axis':v['axis'],'level_m':v['level_mm']/1000,
          'polygons':[{'source_id':p['id'],'material':p['material'],
                       'points_m':[[x/1000 for x in q] for q in p['points']]}
                      for p in v['polygons'] if p.get('cut') and p.get('points')]}
    bearing=[p['id'] for p in parts if p['material'] in ('timber','plywood') and p['family'] in ('walls','floor','roof','partitions','canopy')]
    required={
      'thermal':['Design weather/location','Conductivity vs temperature and moisture for each material',
                 'Surface boundary coefficients, cavities and emissivity','Window/door certified data',
                 'Zone temperatures, humidity, ventilation and time schedules','Closed thermal domains and mesh convergence'],
      'structure':['Timber grade, plywood lay-up and orthotropy','Member local axes and beam/shell classification',
                   'Joint topology, stiffness/releases and fastener schedules','Foundation soil, supports and anchor specification',
                   'G, Q, S, W actions and Lithuanian National Annex combinations','Equilibrium and mesh/member convergence'],
      'wind':['Site coordinates, altitude, terrain by direction and orientation','Applicable LT National Annex values and edition',
              'Pressure zones, loaded areas, internal pressure and dominant openings','Validated structural load path and anchors']}
    return {'schema':'obtp-analysis-preflight/1','configuration':scene['config']['id'],
      'geometry_sha256':scene['geometry_sha256'],'source_sha256':source,'inputs_sha256':digest(cfg),
      'units':{'length':'m','force':'N','temperature':'degC','time':'s'},'inputs':cfg,
      'solids':solids,'sections':sections,'structural_candidate_ids':bearing,
      'interfaces':copy.deepcopy(scene['interfaces']),
      'junction_review':[
        {'id':'junction/'+kind,'kind':kind,'status':'requires domain and boundary assignment','psi_W_mK':None}
        for kind in ['wall-floor','wall-roof','corner','opening','cassette-joint','penetration']],
      'actions':{'snow':{'status':'paused_by_owner','values':None},'wind':{'status':'paused_by_owner','values':None}},
      'point_bridges':{'status':'requires separate 3D model','chi_W_K':None},
      'audit':{'source_parts':len(parts),'structural_candidates':len(bearing),
               'unresolved_interfaces':sum(x.get('capacity') is None for x in scene['interfaces']),
               'materials':dict(Counter(p['material'] for p in parts)),
               'finite_positive_prisms':True,'unique_ids':True,
               'overlap_mesh_connectivity_check':'not completed'},
      'workflows':{k:{'status':'paused_by_owner' if k=='wind' else 'not_run','required':v,'results':None} for k,v in required.items()}}


def validate_result_identity(preflight,receipt):
    """Reject stale solver receipts even when the geometry alone is unchanged."""
    for key in ('source_sha256','inputs_sha256'):
        if receipt.get(key)!=preflight[key]:raise ValueError('Stale analysis '+key)
    if receipt.get('status')!='completed':raise ValueError('Solver run not completed')
    for key in ('solver','version','input_file_sha256','output_file_sha256','checks'):
        if not receipt.get(key):raise ValueError('Missing solver evidence: '+key)
    if not all(v is True for v in receipt['checks'].values()):raise ValueError('Solver checks not passed')
    return True


def write_bundle(scene,directory,settings=None):
    from pathlib import Path
    from .drawings import svg
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    result=prepare(scene,settings)
    (directory/'preflight.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (directory/'inputs.json').write_text(json.dumps(result['inputs'],indent=2),encoding='utf-8')
    for name in result['sections']:
        (directory/(name+'.svg')).write_text(svg(scene['drawings']['views'][name]),encoding='utf-8')
    return result
