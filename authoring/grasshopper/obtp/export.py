"""Offline review export. Production publication stays disabled until acceptance."""
import csv
import hashlib
import json
from pathlib import Path

FACES=[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]]
COLORS={'timber':(187,168,135,255),'plywood':(207,188,155,255),'object':(145,149,150,255),'concrete-study':(125,129,130,255)}


def vertices(p):
    x,y,z=p['origin'];a,b,c=p['size']
    return [[x,y,z],[x+a,y,z],[x+a,y+b,z],[x,y+b,z],
            [x,y,z+c],[x+a,y,z+c],[x+a,y+b,z+c],[x,y+b,z+c]]


def brep(p, api):
    lo=p['origin'];hi=[lo[k]+p['size'][k] for k in range(3)]
    result=api.Brep.CreateFromBox(api.Box(api.BoundingBox(api.Point3d(*lo),api.Point3d(*hi))))
    if result is None or not result.IsValid or not result.IsSolid:
        raise ValueError('Invalid solid: '+p['id'])
    return result


def file3dm(scenes, path, api=None):
    if api is None:
        import rhino3dm as api
    doc=api.File3dm();doc.Settings.ModelUnitSystem=api.UnitSystem.Millimeters
    layers={}
    for i,scene in enumerate(scenes):
        for p in scene['parts']:
            name=scene['config']['id']+' / '+p['family']+' / '+p['material']
            if name not in layers:
                layer=api.Layer();layer.Name=name
                color=COLORS[p['material']]
                try:layer.Color=color
                except TypeError:
                    from System.Drawing import Color
                    layer.Color=Color.FromArgb(color[3],color[0],color[1],color[2])
                layers[name]=doc.Layers.Add(layer)
            q=dict(p);q['origin']=[p['origin'][0]+(i%2)*9000,p['origin'][1]+(i//2)*6500,p['origin'][2]] if len(scenes)>1 else list(p['origin'])
            attr=api.ObjectAttributes() if hasattr(api,'ObjectAttributes') else None
            if attr is None:
                import Rhino
                attr=Rhino.DocObjects.ObjectAttributes()
            attr.Name=p['id'];attr.LayerIndex=layers[name]
            for k,v in dict(obtp_id=p['id'],assembly=p['assembly'],material=p['material'],family=p['family'],
                            configuration=scene['config']['id'],source_revision=scene['version'],
                            geometry_sha256=scene['geometry_sha256'],status=scene['status']).items():attr.SetUserString(k,str(v))
            doc.Objects.AddBrep(brep(q,api),attr)
    if not doc.Write(str(path),8):raise IOError('Could not save '+str(path))


def browser_scene(scene):
    # One mesh per distinct part for R01: identity is stable, no baked display offsets.
    models=[];items=[]
    for p in scene['parts']:
        id=p['id'];vs=vertices(p)
        models.append(dict(id=id,units='mm',schema='obtp-source-mesh/1',assets=[dict(
            id=id,vertices=vs,faces=FACES,dimensions=p['size'],material='furniture-study' if p['material']=='object' else p['material'],
            bounds=[p['origin'],[p['origin'][k]+p['size'][k] for k in range(3)]],explode=[0,0,0])]))
        direction={'floor':[0,0,-250],'roof':[0,0,450],'walls':[0,200,0],'partitions':[200,0,0],
                   'furniture':[0,0,0],'foundation':[0,0,-450]}[p['family']]
        items.append(dict(id=id,block=id,translation=[0,0,0],stage=p['family'],assembly=p['assembly'],explode=direction))
    return dict(models=models,items=items,units='mm',source_geometry_sha256=scene['geometry_sha256'],
                status=scene['status'],website_ready=False,metrics=scene['metrics'],holds=scene['holds'])


def export_one(scene, directory, api=None):
    if not all(scene['checks'].values()):raise ValueError('Envelope check failed')
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    stem=scene['config']['id'];outputs=[]
    for suffix,data in [('.json',scene),('.browser.json',browser_scene(scene))]:
        p=directory/(stem+suffix);p.write_text(json.dumps(data,indent=2),encoding='utf-8');outputs.append(p)
    path=directory/(stem+'.3dm');file3dm([scene],path,api);outputs.append(path)
    path=directory/(stem+'-parts.csv')
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['id','assembly','family','material','x_mm','y_mm','z_mm','a_mm','b_mm','c_mm','solid_m3'])
        for p in scene['parts']:
            a,b,c=p['size'];w.writerow([p['id'],p['assembly'],p['family'],p['material'],*p['origin'],a,b,c,a*b*c/1e9])
    outputs.append(path)
    return [dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in outputs]
