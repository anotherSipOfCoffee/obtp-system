"""RhinoCommon conversion kept separate from the deterministic authoring core."""
import Rhino
from .export import brep

class Api:
    File3dm=Rhino.FileIO.File3dm
    UnitSystem=Rhino.UnitSystem
    Layer=Rhino.DocObjects.Layer
    ObjectAttributes=Rhino.DocObjects.ObjectAttributes
    Box=Rhino.Geometry.Box
    Brep=Rhino.Geometry.Brep
    BoundingBox=Rhino.Geometry.BoundingBox
    Point3d=Rhino.Geometry.Point3d


def preview(scene, panels=True, cut=False, explode=0):
    if not 0<=explode<=100:raise ValueError('Explosion must be 0–100')
    geometry=[];ids=[]
    cut_z=scene['dimensions']['floor_top_mm']+1100
    for p in scene['parts']:
        if not panels and p['material']=='plywood':continue
        if cut and p['family']=='roof':continue
        q=dict(p);q['origin']=list(p['origin']);q['size']=list(p['size'])
        if cut and p['family'] in ['walls','partitions']:
            q['size'][2]=min(q['size'][2],cut_z-q['origin'][2])
            if q['size'][2]<=0:continue
        g=brep(q,Api)
        family=p['family']
        dx,dy,dz={'floor':(0,0,-250),'roof':(0,0,450),'walls':(0,200,0),
                  'partitions':(200,0,0),'furniture':(0,0,0),'foundation':(0,0,-450)}[family]
        g.Transform(Rhino.Geometry.Transform.Translation(dx*explode/100,dy*explode/100,dz*explode/100))
        geometry.append(g);ids.append(p['id'])
    return geometry,ids


def audit(scene):
    total={'timber':0.0,'plywood':0.0};solid_count=0
    for p in scene['parts']:
        g=brep(p,Api);solid_count+=1
        mass=Rhino.Geometry.VolumeMassProperties.Compute(g)
        if mass is None:raise ValueError('No volume for '+p['id'])
        if p['material'] in total:total[p['material']]+=mass.Volume/1e9
        mass.Dispose()
    for key,value in total.items():
        if abs(value-scene['metrics']['wood_m3'][key])>1e-7:
            raise ValueError('Solid/recipe volume mismatch: '+key)
    return dict(runtime=str(Rhino.RhinoApp.Version),solid_count=solid_count,wood_m3=total,status='Rhino geometry checks passed; engineering holds remain')
