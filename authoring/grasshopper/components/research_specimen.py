#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
core=importlib.import_module(name+'.research_specimens')
def value(key,default):
    v=globals().get(key,default)
    if hasattr(v,'Value'):v=v.Value
    return default if v is None else v
geometry=[];materials=[];report='';catalogue=[];schedule=[]
try:
    from System.Drawing import Color
    import Rhino
    from Grasshopper.Kernel.Types import GH_Material
    kw={k:value(k,v) for k,v in dict(system=1,specimen=0,bays=3,span=2400,height=2100,sheet=12,depth=195,pitch=900,thickness=45,mode=0,object_index=0,explode=0,insulation=False,core=False).items()}
    kw['depth']=value('cassette_depth',195) if kw['system']==1 else value('b_depth',240)
    result=core.compare(**kw)
    for m in result['meshes']:
        mesh=Rhino.Geometry.Mesh()
        for v in m['vertices']:mesh.Vertices.Add(*v)
        for f in m['faces']:mesh.Faces.AddFace(*f)
        mesh.Normals.ComputeNormals();geometry.append(mesh)
        rgba=m['rgba'];materials.append(GH_Material(Rhino.Display.DisplayMaterial(Color.FromArgb(rgba[3],rgba[0],rgba[1],rgba[2]))))
    report=result['report'];catalogue=result['catalogue'];schedule=[json.dumps(r,sort_keys=True) for r in result['schedule']]
except Exception as error:
    geometry=[];materials=[];report=str(error);catalogue=[];schedule=[]
    import Grasshopper
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,report)
