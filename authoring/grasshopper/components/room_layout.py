#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
core=importlib.import_module(name+'.layout')
def value(key,default):
    v=globals().get(key,default)
    if hasattr(v,'Value'):v=v.Value
    return default if v is None else v
def fail(error):
    import Grasshopper
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,str(error))
plan_json=None;geometry=[];materials=[];labels=[];label_points=[];report=''
try:
    import Rhino
    from System.Drawing import Color
    from Grasshopper.Kernel.Types import GH_Material
    selection=value('workflow_json',None)
    if selection is not None:
        workflow=importlib.import_module(name+'.sauna_workflow')
        document=workflow.resolve(json.loads(selection));plan=document['plan'];graph=plan['graph'];plan_json=json.dumps(document)
    else:
        graph=json.loads(value('graph_json','null'))
        if graph is None:raise ValueError('Connect a valid relationship graph')
        plan=core.solve(graph,int(value('arrangement',0)));plan_json=json.dumps(plan)
    palette={'sauna':(203,153,117),'entrance':(137,169,188),'outdoor':(163,184,137)}
    def add(g,rgb):geometry.append(g);materials.append(GH_Material(Rhino.Display.DisplayMaterial(Color.FromArgb(*rgb))))
    ox,oy=0,-7500
    for r in plan['rooms']:
        x,y,w,h=r['bounds_mm'];x+=ox;y+=oy
        mesh=Rhino.Geometry.Mesh()
        for xx,yy in [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]:mesh.Vertices.Add(xx,yy,0)
        mesh.Faces.AddFace(0,1,2,3);mesh.Normals.ComputeNormals();add(mesh,palette[r['id']])
        labels.append(r['id']+' / '+str(w)+' x '+str(h)+' mm');label_points.append(Rhino.Geometry.Point3d(x+w/2,y+h/2,20))
    for r in plan['finished_room_rectangles']:
        x,y,w,h=r['bounds_mm'];pts=[Rhino.Geometry.Point3d(ox+xx,oy+yy,10) for xx,yy in [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]]
        add(Rhino.Geometry.PolylineCurve(pts),(60,60,60))
    for o in plan['openings']:
        x,y=o['origin_mm'];w=o['width_mm'];add(Rhino.Geometry.LineCurve(Rhino.Geometry.Point3d(ox+x,oy+y,15),Rhino.Geometry.Point3d(ox+x+(w if o['axis']=='x' else 0),oy+y+(w if o['axis']=='y' else 0),15)),(220,65,50))
    # Explicit graph diagram next to the room plan, independent of room inclusion.
    positions={r:Rhino.Geometry.Point3d(ox+i*1600,oy-1500,0) for i,r in enumerate(core.ROOM_IDS) if plan['programme']['active'][r]}
    for r,point in positions.items():
        add(Rhino.Geometry.Circle(point,160).ToNurbsCurve(),palette[r]);labels.append('GRAPH: '+r);label_points.append(point)
    for e in graph['edges']:add(Rhino.Geometry.LineCurve(positions[e['a']],positions[e['b']]),(220,65,50) if e['kind']=='passage' else (65,80,90))
    report=('Preset: '+document['selection']['preset_name']+'\n' if selection is not None else '')+'Arrangement %d / %d: %s\nConstruction adapter: %s\n%s'%(plan['arrangement'],plan['candidate_count']-1,' -> '.join(r['id'] for r in plan['rooms']),'AVAILABLE' if plan['construction_compatible'] else 'PLAN ONLY','\n'.join(plan['holds']))
except Exception as error:
    plan_json=None;geometry=[];materials=[];labels=[];label_points=[];report=str(error);fail(error)
