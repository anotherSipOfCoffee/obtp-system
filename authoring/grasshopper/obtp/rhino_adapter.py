"""RhinoCommon conversion kept separate from the deterministic authoring core."""
import Rhino
from .export import brep
from .preview_filter import visible
from .cut_view import clipped_part, stationary

class Api:
    File3dm=Rhino.FileIO.File3dm
    UnitSystem=Rhino.UnitSystem
    Layer=Rhino.DocObjects.Layer
    ObjectAttributes=Rhino.DocObjects.ObjectAttributes
    PolylineCurve=Rhino.Geometry.PolylineCurve
    Extrusion=Rhino.Geometry.Extrusion
    Mesh=Rhino.Geometry.Mesh
    Transform=Rhino.Geometry.Transform
    Box=Rhino.Geometry.Box
    Brep=Rhino.Geometry.Brep
    BoundingBox=Rhino.Geometry.BoundingBox
    Point3d=Rhino.Geometry.Point3d


def preview(scene, panels=True, cut=False, explode=0, visibility=None, only=0):
    if not 0<=explode<=100:raise ValueError('Explosion must be 0–100')
    geometry=[];ids=[]
    cut_z=scene['dimensions']['floor_top_mm']+1100
    for p in scene['parts']:
        if not visible(p,visibility,only) or cut and not stationary(p):continue
        if not panels and p['material'] in ['plywood','lining-wood','cladding-wood']:continue
        q=clipped_part(p,cut_z) if cut else dict(p)
        if q is None:continue
        g=brep(q,Api)
        family=p['family']
        dx,dy,dz={'insulation':(0,0,0),'interior':(0,0,0),'facade':(0,200,0),'ceiling':(0,0,250),'terrace':(0,0,0),'canopy':(0,0,0),'floor':(0,0,-250),'roof':(0,0,450),'walls':(0,200,0),
                  'partitions':(200,0,0),'furniture':(0,0,0),'foundation':(0,0,-450)}[family]
        g.Transform(Rhino.Geometry.Transform.Translation(dx*explode/100,dy*explode/100,dz*explode/100))
        geometry.append(g);ids.append(p['id'])
    return geometry,ids


def audit(scene):
    total={key:0.0 for key in scene['metrics']['wood_m3']};solid_count=0
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


