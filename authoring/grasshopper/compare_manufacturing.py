"""Reproduce all baselines from immutable Git history; only one production core.
Usage: python compare_manufacturing.py destination [--full-catalogue]
"""
import argparse, importlib.util, itertools, json, subprocess, sys, tempfile, gzip
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
PINS={'original':'1ad71826acfcc7d6d5df9a06167c5fcfea20b516','cells':'a11e613ac923fd5de6a3d3f1368e6c6eebc57745'}
from obtp.manufacturing import analyse
from obtp.drawings import svg


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path/'obtp/__init__.py',submodule_search_locations=[str(path/'obtp')])
    package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
    return __import__(name+'.model',fromlist=['build'])


def summary(scene):
    a=analyse(scene);a.update(dimensions=scene['dimensions'],geometry_sha256=scene['geometry_sha256'],
      usable_area_m2=scene['metrics']['main_clear_floor_less_partition_m2'],wood_m3=scene['metrics']['total_wood_m3'])
    return a


def run(destination,full=False):
    out=Path(destination);out.mkdir(parents=True,exist_ok=True)
    rows=[];models={}
    with tempfile.TemporaryDirectory() as temp:
        for name,sha in PINS.items():
            target=Path(temp)/name;target.mkdir()
            import tarfile,io
            data=subprocess.check_output(['git','-C',str(REPO),'archive',sha,'authoring/grasshopper'])
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(target,filter='data')
            models[name]=module(target/'authoring/grasshopper','baseline_'+name)
        models['revised']=module(ROOT,'revised_core')
        configs=itertools.product(range(2),range(6),range(2) if full else [0], [580,880,1180] if full else [1180],range(2) if full else [0],[True,False] if full else [True])
        for program,i,roof,window,foundation,winter in configs:
            if not program and not winter:continue
            opts=dict(program_type=program,roof_type=roof,window_width=window,foundation_type=foundation,studio_winter_closed=winter)
            records={};scenes={}
            for name,m in models.items():
                s=m.build(m.parameters(i,**opts));scenes[name]=s;records[name]=summary(s)
            # Revised recipes at the first cell system's EXACT footprint/program dimensions.
            p=models['revised'].parameters(i,**opts)
            for k in ('room_depth_steps','sauna_length_steps','hall_length_steps','storage_length_steps'):
                p[k]=scenes['cells']['config'][k]
            same=models['revised'].build(p);records['revised_same_footprint']=summary(same)
            key=scenes['revised']['config']['id']+f'-r{roof}-w{window}-b{foundation}-'+('winter' if winter else 'summer')
            rows.append(dict(key=key,program='studio' if program else 'sauna',versions=records))
            if i==2 and roof==0 and window==1180 and foundation==0 and winter:
                for name,s in list(scenes.items())+[('revised_same_footprint',same)]:
                    (out/(('studio' if program else 'sauna')+'-'+name+'-plan.svg')).write_text(svg(s['drawings']['views']['concept-plan']))
                (out/(('studio' if program else 'sauna')+'-revised-schedule.json.gz')).write_bytes(gzip.compress(json.dumps(analyse(scenes['revised'],True),separators=(',',':')).encode(),mtime=0))
        catalogue={}
        for name in ['original','cells','revised_same_footprint','revised']:
            catalogue[name]={}
            for program in ['sauna','studio','combined']:
                subset=[r['versions'][name] for r in rows if program=='combined' or r['program']==program]
                catalogue[name][program]=dict(unique_manufactured_part_candidates=len({k for r in subset for k in r['type_keys']}),
                   physical_pieces=sum(r['physical_pieces'] for r in subset),unique_assembly_candidates=len({k for r in subset for k in r['assembly_keys']}),
                   assemblies_installed=sum(r['assemblies_installed'] for r in subset),configuration_count=len(subset))
        for row in rows:
            for a in row['versions'].values():
                a.pop('type_keys');a.pop('assembly_keys')
                for key in ('uncertainty','schema','status'):a.pop(key,None)
        result=dict(schema='obtp-three-version-comparison/1',baseline_commits=PINS,
           revised_source='current checkout; commit recorded by consuming source pin',full_catalogue=full,
           scope='All supported configurations' if full else 'S/M/L × storage for both buildings, flat roof, 1180 mm window, timber foundation, closed Studio sliders',
           counting_rule='obtp/manufacturing.py applied unchanged to all snapshots; only facade finish boards excluded. All figures are provisional candidate counts, NOT verified manufacturing counts.',
           target_achieved=False,rows=rows,catalogue=catalogue,uncertainty=['Manufacturing grades, machining, grain, handedness and joint definitions are incomplete.','Counts are provisional candidate classes; actual manufactured types and actual site assembly counts cannot be certified.','Purchased-product subparts are geometric representations, not verified supplier BOMs.','Unmodelled fasteners, seals and tapes remain unknown in all versions.'])
        (out/'manufacturing-comparison.json.gz').write_bytes(gzip.compress(json.dumps(result,separators=(',',':')).encode(),mtime=0))
        lines=['# Three-version manufacturing comparison','','Counts are provisional: manufacturing details are incomplete. The 75% target is not achieved or certified. Facade boards alone are excluded equally in every version; battens, trims, all other materials and object representations remain counted.','','## Per-building default M / no storage','','| Building / version | Candidate types | Pieces excl. cladding | Cladding pieces | Assembly types / installed | Width mm |','|---|---:|---:|---:|---:|---:|']
        for row in rows:
            if '-m-open-r0-w1180-b0-winter' not in row['key']:continue
            for name,a in row['versions'].items():
                lines.append(f"| {row['program']} / {name} | {a['unique_manufactured_part_candidates']} | {a['physical_pieces']} | {a['cladding']['physical_pieces']} | {a['unique_assembly_candidates']} / {a['assemblies_installed']} | {a['dimensions']['width_mm']} |")
        lines+=['','## Catalogue union, not the sum of unique counts','','| Version | Sauna types | Studio types | Combined types |','|---|---:|---:|---:|']
        for name,a in catalogue.items():lines.append(f"| {name} | {a['sauna']['unique_manufactured_part_candidates']} | {a['studio']['unique_manufactured_part_candidates']} | {a['combined']['unique_manufactured_part_candidates']} |")
        lines+=['','## Measured reduction in catalogue diversity','','| Reference | Sauna | Studio | Combined |','|---|---:|---:|---:|']
        for name in ['original','cells']:
            vals=[100*(1-catalogue['revised'][p]['unique_manufactured_part_candidates']/catalogue[name][p]['unique_manufactured_part_candidates']) for p in ['sauna','studio','combined']]
            lines.append('| '+name+' → revised | '+' | '.join(f'{v:.1f}%' for v in vals)+' |')
        lines+=['','Same-footprint isolates revised construction recipes from Sauna narrowing; compare cells → revised_same_footprint, then revised_same_footprint → revised. All JSON rows retain cladding-inclusion effects, material breakdowns, usable area, wood volume and exact geometry hashes. Physical catalogue totals mean building one of every configuration; they are not a typical order quantity.','',*['- '+s for s in analyse(scenes['revised'])['uncertainty']]]
        (out/'manufacturing-comparison.md').write_text('\n'.join(lines)+'\n')
        print(json.dumps(catalogue,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('destination');p.add_argument('--full-catalogue',action='store_true');a=p.parse_args();run(a.destination,a.full_catalogue)
