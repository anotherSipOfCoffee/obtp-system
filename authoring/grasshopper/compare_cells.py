"""Measured comparison of preserved legacy and new canonical geometry."""
import argparse,json
from pathlib import Path
from obtp.model import build,parameters,legacy_parameters,VERSION
from obtp.optimisation import analyse
from obtp.drawings import svg


def summarize(s):
    opt=analyse(s);d=s['dimensions'];p=s['config']
    walls=[a for a in s['parts'] if a['family'] in ('walls','partitions') and a['material'] in ('timber','plywood')]
    return dict(geometry_sha256=s['geometry_sha256'],length_mm=d['length_mm']+d['annex_length_mm'],width_mm=d['width_mm'],
      footprint_m2=(d['length_mm']+d['annex_length_mm'])*d['width_mm']/1e6,
      physical_wood_parts=opt['physical_wood_parts'],geometric_wood_types=opt['normalised_types'],
      wall_assemblies=len({a['assembly'] for a in walls}),structural_wall_parts=len(walls),
      foundation_supports=len(s['foundation_spec']['support_nodes_mm']),wood_m3=s['metrics']['total_wood_m3'],
      terrace_area_m2=s['metrics']['terrace_area_m2'])


def compare(destination):
    target=Path(destination);target.mkdir(parents=True,exist_ok=True);rows=[]
    for program in range(2):
        for i in range(6):
            options=dict(program_type=program,roof_type=0,studio_winter_closed=False if program else True)
            old=build(legacy_parameters(i,**options));new=build(parameters(i,**options))
            name=new['config']['id'];rows.append(dict(id=name,previous=summarize(old),cells=summarize(new)))
            if i==2:
                for label,s in [('previous',old),('cells',new)]:
                    (target/(name+'-'+label+'-plan.svg')).write_text(svg(s['drawings']['views']['concept-plan']),encoding='utf-8')
    result=dict(version=VERSION,baseline_commit='1ad71826acfcc7d6d5df9a06167c5fcfea20b516',
      scope='Same named programme/size/storage choices, flat roof, foundation type 0, window 1180. Dimensions change; this is not an equal-area cost comparison. Geometric types are not certified interchangeable manufactured products.',configurations=rows)
    (target/'cell-comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    lines=['# Integrated cell system versus previous system','','Measured from both canonical geometry paths. All dimensions are structural frame bounds. Same named configurations, different areas; no price or assembly-time savings inferred.','','| Configuration | Previous → new footprint (mm) | Wall assemblies | Wood parts | Geometric wood types | Foundation supports |','|---|---|---:|---:|---:|---:|']
    for r in rows:
        a,b=r['previous'],r['cells'];lines.append(f"| {r['id']} | {a['length_mm']} × {a['width_mm']} → {b['length_mm']} × {b['width_mm']} | {a['wall_assemblies']} → {b['wall_assemblies']} | {a['physical_wood_parts']} → {b['physical_wood_parts']} | {a['geometric_wood_types']} → {b['geometric_wood_types']} | {a['foundation_supports']} → {b['foundation_supports']} |")
    lines+=['','New geometry uses 900 × 1200 planning cells and a full rectangular support lattice with that pitch. Wall opening envelopes replace whole adjacent bays; terminal deductions are explicit. Existing material sections remain provisional so the dimensional integration does not imply newly engineered construction.','', 'The former 600 mm placement remains callable through legacy_parameters for regression and comparison. PDFs remain disabled. Native Rhino/GH acceptance and structural/connection design remain outstanding.']
    (target/'cell-comparison.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('destination');args=parser.parse_args();compare(args.destination)
