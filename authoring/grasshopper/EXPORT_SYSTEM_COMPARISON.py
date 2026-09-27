"""Portable R22 review exports. No website writes; no Rhino license required.
Run: python EXPORT_SYSTEM_COMPARISON.py [output-directory]
Requires rhino3dm==8.35.0, numpy and pillow. HTML/PNG/JSON/CSV and 3DM share the same comparison meshes.
"""
import csv,html,json,math,sys
from pathlib import Path
from obtp.model import build,parameters
from obtp.system_comparison import preview
from obtp.review_raster import render

def write3dm(result,path):
    import rhino3dm as r
    doc=r.File3dm();doc.Settings.ModelUnitSystem=r.UnitSystem.Millimeters;layers={}
    for p in result['meshes']:
        mesh=r.Mesh()
        for v in p['vertices']:mesh.Vertices.Add(*v)
        for f in p['faces']:mesh.Faces.AddFace(*f)
        mesh.Normals.ComputeNormals();mesh.Compact()
        if not mesh.IsValid:raise ValueError('Invalid mesh '+p['id'])
        material=p['material']
        if material not in layers:
            layer=r.Layer();layer.Name=material;layer.Color=tuple(p['rgba']);layers[material]=doc.Layers.Add(layer)
        a=r.ObjectAttributes();a.Name=p['id'];a.LayerIndex=layers[material];a.SetUserString('type_id',p['type_id']);a.SetUserString('assembly',p['assembly']);a.SetUserString('status','RESEARCH GEOMETRY; NOT ENGINEERED')
        doc.Objects.AddMesh(mesh,a)
    if not doc.Write(str(path),8):raise IOError(path)
    reopened=r.File3dm.Read(str(path))
    if len(reopened.Objects)!=len(result['meshes']):raise ValueError('3DM object reconciliation failed')

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    studio=build(parameters(3,program_type=1,roof_type=0,studio_winter_closed=False))
    jobs=[('01_WikiHouse',dict(system=0,bays=4)),('02_Studio_Cassette',dict(system=1,scene=studio)),
          ('03_B_Ribs',dict(system=2,panels=False)),('04_B_Insulated',dict(system=2,insulation=True)),('05_B_Knee',dict(system=2,mode=2))]
    cards=[];manifest=[]
    for name,args in jobs:
        result=preview(**args,offset=(0,0,0));(out/(name+'.json')).write_text(json.dumps(result,separators=(',',':')))
        write3dm(result,out/(name+'.3dm'))
        illustration=preview(system=0,mode=1,object_index=0,offset=(0,0,0)) if args['system']==0 else result
        render(illustration,out/(name+'.png'))
        if result['schedule']:
            with (out/(name+'-schedule.csv')).open('w',newline='') as stream:
                writer=csv.writer(stream);writer.writerow(['type_id','pieces','definition','instance_ids'])
                for row in result['schedule']:writer.writerow([row['type_id'],row['pieces'],json.dumps(row['definition']),';'.join(row['instances'])])
        cards.append('<article><h2>'+name.replace('_',' ')+(' — W-S source detail; full chassis in 3DM' if args['system']==0 else '')+'</h2><img src="'+name+'.png"><details><summary>Scope and design holds</summary><pre>'+html.escape(result['report'])+'</pre></details></article>')
        manifest.append(dict(name=name,visible_meshes=len(result['meshes']),source_hash=result['source'].get('geometry_sha256'),metrics=result['source'].get('metrics')))
    (out/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>OBTP R22 System comparison</title><style>body{font:16px system-ui;background:#f4f1e9;color:#282b26;max-width:1400px;margin:30px auto;padding:20px}main{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{border:1px solid #bcb6a8;padding:16px;background:white}img{width:100%;height:420px;object-fit:contain}pre{white-space:pre-wrap;font-size:12px}@media(max-width:800px){main{display:block}}</style><h1>OBTP R22: three systems</h1><p>Actual generated geometry. Different scopes and footprints: not a cost or performance ranking. B is an open-ended research chassis, not a construction-ready building.</p><main>'+''.join(cards)+'</main>')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(manifest,indent=2))
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'review-r22')
