"""Compile the finite buyer catalogue from the SAME Python core used by GH.
No Rhino runtime required to export these exact mesh recipes. No browser generator.
"""
import argparse,copy,hashlib,itertools,json,sys,zipfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from obtp.model import build,parameters,VERSION
from obtp.export import browser_scene,COLORS,file3dm
from obtp.drawings import svg
from obtp.sheets import pdf
from obtp.suppliers import catalogue as supplier_catalogue

def compile_catalogue(destination,revision):
    target=Path(destination);target.mkdir(parents=True,exist_ok=True)
    shutil.copytree(ROOT/"suppliers"/"assets",target/"supplier-assets",dirs_exist_ok=True)
    (target/"suppliers.json").write_text(json.dumps(supplier_catalogue(),ensure_ascii=False,indent=2))
    entries=[]
    for program,i,roof,terrace,window in itertools.product(range(2),range(6),range(3),[2],[580,880,1180]):
        scene=build(parameters(i,program_type=program,roof_type=roof,terrace_steps=terrace,window_width=window,facade_type=0))
        if not all(scene['checks'].values()):raise ValueError('Invalid catalogue member')
        key=scene['config']['id']+f'-r{roof}-t{terrace}-w{window}-f0'
        web=browser_scene(scene)
        web.update(config=scene['config'],dimensions=scene['dimensions'],checks=scene['checks'],source_revision=revision,authoring_version=VERSION)
        cut=copy.deepcopy(scene);cut['parts']=[]
        for part in scene['parts']:
            if part['family'] in ['roof','ceiling','canopy']:continue
            p=copy.deepcopy(part)
            if p['family'] in ['walls','partitions','interior','facade','insulation']:
                p['size'][2]=min(p['size'][2],scene['dimensions']['floor_top_mm']+1100-p['origin'][2])
                if p['size'][2]<=0:continue
            cut['parts'].append(p)
        clipped=browser_scene(cut)
        web['cut']=dict(models=clipped['models'],items=clipped['items'])
        for chunk in [web,web['cut']]:
            for m in chunk['models']:
                for asset in m['assets']:
                    mat=asset['material'];asset['color']=[v/255 for v in COLORS.get(mat,COLORS['object'])[:3]]
        web['drawings']=scene['drawings']
        web['envelope_spec']=scene['envelope_spec']
        web['window_spec']=scene['window_spec']
        web['supplier_spec']=scene['supplier_spec']
        (target/(key+'-plan.svg')).write_text(svg(scene['drawings']['views']['concept-plan']))
        pdf(scene,target/(key+'.pdf'))
        data=json.dumps(web,separators=(',',':')).encode();(target/(key+'.json')).write_bytes(data)
        entries.append(dict(key=key,file=key+'.json',sha256=hashlib.sha256(data).hexdigest(),geometry_sha256=scene['geometry_sha256']))
    (target/'manifest.json').write_text(json.dumps(dict(version=VERSION,source_revision=revision,defaults=dict(size='m',storage=False,roof=1,terrace=2,window=1180,facade=0),entries=entries),indent=2))
    with zipfile.ZipFile(target/'OBTP_Grasshopper_Source.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.rglob('*'):
            if p.is_file() and p.suffix in ['.py','.md','.json','.png','.svg'] and not any(x in p.parts for x in ['exports','roof-studies','references','previews','__pycache__']):z.write(p,p.relative_to(ROOT))
    # Offline package contains the same core plus the six default Rhino models/PDFs.
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        with zipfile.ZipFile(target/'OBTP_Grasshopper_R07.zip','w',zipfile.ZIP_DEFLATED) as z:
            with zipfile.ZipFile(target/'OBTP_Grasshopper_Source.zip') as source:
                for name in source.namelist():z.writestr(name,source.read(name))
            for program,i in itertools.product(range(2),range(6)):
                scene=build(parameters(i,program_type=program));stem=scene['config']['id'];path=Path(temp)/(stem+'.3dm');file3dm([scene],path);z.write(path,'exports/'+path.name)
                key=stem+'-r1-t2-w1180-f0';z.write(target/(key+'.pdf'),'exports/'+stem+'.pdf')
    print('Compiled',len(entries),'script-authored website configurations')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination');ap.add_argument('--revision',required=True);args=ap.parse_args();compile_catalogue(args.destination,args.revision)
