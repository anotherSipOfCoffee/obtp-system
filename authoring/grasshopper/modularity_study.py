"""Bounded, reproducible GH-only modularity experiments; never a production pipeline.
All candidates use the current canonical recipes; only seam/opening rules vary.
Run small screen first. --full validates only the retained production finalist.
"""
import argparse, contextlib, json, math, subprocess, sys, hashlib, tempfile, tarfile, io, importlib.util
from pathlib import Path
from obtp import model, cells
from obtp.manufacturing import analyse, identity, cladding
from obtp.optimisation import analyse as stock
BASELINE_COMMIT='d02d8322bb1f456e4b005d5f6a023f236eddc220'
ORIGINAL_SEGMENTS=cells.wall_segments
ORIGINAL_OPENING=cells.opening


def kit_segments(kit):
    def split(base,axis,length,opening_envelope=None,forced=()):
        start=base[0 if axis=='x' else 1];end=start+length
        spans=[(start,end)] if not opening_envelope else [(start,opening_envelope[0]),(opening_envelope[1],end)]
        result=[]
        for a,b in spans:
            length=round(b-a,6)
            if length<=0:continue
            options=[]
            for n in range(int(length//min(kit))+1):
                for m in range(int(length//max(kit))+1):
                    rem=round(length-n*min(kit)-m*max(kit),6)
                    if rem<0 or 0<rem<90:continue
                    widths=[max(kit)]*m+[min(kit)]*n+([rem] if rem else [])
                    if any(w>max(kit) for w in widths):continue
                    # Prefer exact kit solutions, then fewer cassette interfaces.
                    options.append(((bool(rem),len(widths),-rem),widths))
            if not options:raise ValueError('No supported terminal partition')
            u=a
            for width in min(options)[1]:
                result.append((u-start,u+width-start));u+=width
        return result
    return split


def host_opening(window_host,move):
    def choose(start,end,step,width,preferred):
        current=ORIGINAL_OPENING(start,end,step,width,preferred)
        u=start+current['start']
        host=window_host if width==1200 else (900 if width<=600 else 1200)
        axes=cells.boundaries(start,end,300);choices=[]
        for a in axes:
            b=a+host
            if b>end or (0<a-start<90) or (0<end-b<90):continue
            low=max(a+90,start+195);high=min(b-width-90,end-width-195)
            if low>high:continue
            v=min(max(u,low),high)
            if abs(v-u)>move:continue
            choices.append((abs(v-u),abs((a+b)/2-(u+width/2)),a,b,v))
        if not choices:raise ValueError('Host {} cannot fit without >{} mm opening relocation'.format(host,move))
        _,_,a,b,v=min(choices)
        return dict(start=v-start,lo=a-start,hi=b-start,nominal_bounds_mm=[a,b],rough_width_mm=width)
    return choose

MODES={
 'baseline':(None,None,0),
 'A-solids':((900,1200),None,0),
 'B-solids':((600,1200),None,0),
 'A-fixed-1500':((900,1200),1500,0),
 'A-move-1500':((900,1200),1500,150),
 'A-move-1800':((900,1200),1800,150),
 'B-move-1500':((600,1200),1500,150),
 'B-move-1800':((600,1200),1800,150),
}
@contextlib.contextmanager
def candidate(mode):
    kit,host,move=MODES[mode]
    cells.wall_segments=kit_segments(kit) if kit else ORIGINAL_SEGMENTS
    cells.opening=host_opening(host,move) if host else ORIGINAL_OPENING
    try:yield
    finally:cells.wall_segments=ORIGINAL_SEGMENTS;cells.opening=ORIGINAL_OPENING


def configurations(full=False):
    if full:
        for program in range(2):
            for preset in range(6):
                for roof in range(2):
                    for window in (580,880,1180):
                        for foundation in range(2):
                            for winter in ([True,False] if program else [True]):
                                yield preset,dict(program_type=program,roof_type=roof,window_width=window,foundation_type=foundation,studio_winter_closed=winter)
    else:
        for program in range(2):
            for preset in range(6):
                for trial in range(2):
                    yield preset,dict(program_type=program,roof_type=trial,window_width=1180 if trial==0 else (580,880,1180)[preset%3],foundation_type=trial,studio_winter_closed=bool(trial))


def metrics(scene,detail=False):
    from obtp.modularity import procurement
    a=analyse(scene);proc=procurement(scene)
    primary=[p for p in scene['parts'] if not cladding(p)]
    purchased=set(proc['purchased_representation_ids'])
    fabricated=[p for p in primary if p['id'] not in purchased]
    # Remaining generic furniture/equipment must not be called fabricated.
    unresolved=[p for p in fabricated if p['material'] in ('object','glass')]
    fabricated=[p for p in fabricated if p['material'] not in ('object','glass')]
    mats={m:sum(p['size'][0]*p['size'][1]*(p['size'][2]+p.get('top_slope_y',0)*p['size'][1]/2)/1e9 for p in primary if p['material']==m) for m in sorted({p['material'] for p in primary})}
    assemblies=scene.get('cell_spec',{}).get('wall_assemblies',[])
    joints=0
    for i,x in enumerate(assemblies):
        for y in assemblies[i+1:]:
            if x['id'].split('/')[0]!=y['id'].split('/')[0]:continue
            if abs(x['bounds_mm'][1]-y['bounds_mm'][0])<1e-6 or abs(y['bounds_mm'][1]-x['bounds_mm'][0])<1e-6:joints+=1
    result=dict(types=a['unique_manufactured_part_candidates'],pieces=a['physical_pieces'],
        fabricated_types=len({identity(p) for p in fabricated}),fabricated_pieces=len(fabricated),
        purchased_units=proc['purchased_units'],purchased_representation_pieces=len(purchased),
        unresolved_object_pieces=len(unresolved),assembly_types=a['unique_assembly_candidates'],assemblies=a['assemblies_installed'],
        modeled_interfaces=len(scene['interfaces']),within_run_cassette_seams=joints,
        actual_fasteners=None,material_m3=mats,usable_area_m2=scene['metrics']['main_clear_floor_less_partition_m2'],
        dimensions=scene['dimensions'],rooms=scene.get('rooms',[]),geometry_sha256=scene['geometry_sha256'],
        cladding=a['cladding'],type_keys=a['type_keys'],fabricated_keys=sorted({identity(p) for p in fabricated}),assembly_keys=a['assembly_keys'])
    assert result['pieces']==result['fabricated_pieces']+result['purchased_representation_pieces']+result['unresolved_object_pieces']
    if detail:
        result['stock_study']=stock(scene)
        result['opening_dimensions']=scene['modularity']['openings']
    return result


def run(destination,full=False):
    out=Path(destination);out.mkdir(parents=True,exist_ok=True);result={}
    frozen=None;temp=None
    if full:
        temp=tempfile.TemporaryDirectory()
        repo=Path(__file__).resolve().parents[2]
        data=subprocess.check_output(['git','-C',str(repo),'archive',BASELINE_COMMIT,'authoring/grasshopper'])
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(temp.name,filter='data')
        root=Path(temp.name)/'authoring/grasshopper/obtp'
        spec=importlib.util.spec_from_file_location('frozen_r20',root/'__init__.py',submodule_search_locations=[str(root)])
        package=importlib.util.module_from_spec(spec);sys.modules['frozen_r20']=package;spec.loader.exec_module(package)
        frozen=__import__('frozen_r20.model',fromlist=['build'])
    modes=['baseline'] if full else list(MODES)
    for mode in modes:
        rows=[];errors=[];keys=set();fab=set();assembly=set()
        with candidate(mode):
            for i,opts in configurations(full):
                key=str(i)+'-'+json.dumps(opts,sort_keys=True)
                try:
                    s=model.build(model.parameters(i,**opts));a=metrics(s,detail=(i==2 and opts['roof_type']==0 and opts['window_width']==1180 and opts['foundation_type']==0))
                    assert all(s['checks'].values())
                    if frozen:
                        previous=frozen.build(frozen.parameters(i,**opts))
                        assert s['geometry_sha256']==previous['geometry_sha256'], 'R20 geometry changed'
                        assert s['drawings']==previous['drawings'], 'R20 drawings changed'
                        a['baseline_geometry_exact_match']=True
                    if full and (len(rows)+1)%36==0:print('Verified frozen R20',len(rows)+1,flush=True)
                    keys.update(a.pop('type_keys'));fab.update(a.pop('fabricated_keys'));assembly.update(a.pop('assembly_keys'))
                    rows.append(dict(key=key,program=opts['program_type'],preset=i,options=opts,metrics=a))
                except ValueError as e:errors.append(dict(key=key,error=str(e)))
        result[mode]=dict(rows=rows,errors=errors,catalogue_types=len(keys),catalogue_fabricated_types=len(fab),catalogue_assembly_types=len(assembly),pieces=sum(r['metrics']['pieces'] for r in rows))
        print(mode,'configurations',len(rows),'errors',len(errors),'types',len(keys),'fabricated',len(fab),'pieces',result[mode]['pieces'],flush=True)
    payload=dict(schema='obtp-modularity-study/1',baseline_commit=BASELINE_COMMIT,full=full,versions=result,
        method='Same footprints and room programmes. No quantities excluded except facade finish boards. Purchased representations reconciled separately. Incomplete candidates cannot win.',
        unknowns=['Actual fastening counts and labour times unknown','Stock study: hypothetical 6000 mm timber and 3 mm kerf, no sheet nesting','Connection, grain, grade and machining definitions incomplete; all types provisional'])
    (out/('full.json' if full else 'screen.json')).write_text(json.dumps(payload,indent=2))
    if temp:temp.cleanup()
    return payload
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('destination');p.add_argument('--full',action='store_true');a=p.parse_args();run(a.destination,a.full)
