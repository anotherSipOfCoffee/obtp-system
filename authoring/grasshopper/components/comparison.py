#! python 3
"""Third-system research comparison. All imports are bundled beside the GH file."""
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
geometry=[];materials=[];part_ids=[];type_ids=[];catalogue=[];report='Comparison disabled';comparison_json=None
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
def value(key,default):
    v=globals().get(key,default)
    if hasattr(v,'Value'):v=v.Value
    return default if v is None else v
try:
    if bool(value('enabled',True)):
        import Rhino
        from System.Drawing import Color
        from Grasshopper.Kernel.Types import GH_Material
        core=importlib.import_module(name+'.system_comparison')
        text=value('scene_json',None)
        result=core.preview(system=int(value('system',2)),scene=json.loads(text) if text else None,
          bays=int(value('bays',4)),layer=int(value('layer',3)),panels=bool(value('panels',True)),insulation=bool(value('insulation',False)),foundation=bool(value('foundation',True)),
          mode=int(value('inspection',0)),object_index=int(value('object_index',0)),explode=int(value('explode',0)),
          pitch=int(value('rib_pitch',900)),span=int(value('rib_span',3600)),height=int(value('rib_height',2100)),thickness=int(value('rib_thickness',45)),depth=int(value('rib_depth',240)),core=bool(value('core_frame',False)))
        report=result['report'];catalogue=result['catalogue'];cache={}
        for p in result['meshes']:
            mesh=Rhino.Geometry.Mesh()
            for v in p['vertices']:mesh.Vertices.Add(*v)
            for f in p['faces']:mesh.Faces.AddFace(*f)
            mesh.Normals.ComputeNormals();mesh.Compact()
            if not mesh.IsValid:raise ValueError('Invalid display mesh '+p['id'])
            geometry.append(mesh);part_ids.append(p['id']);type_ids.append(p['type_id'])
            rgba=tuple(p['rgba'])
            if rgba not in cache:cache[rgba]=GH_Material(Rhino.Display.DisplayMaterial(Color.FromArgb(*rgba[:3]),1-rgba[3]/255.0))
            materials.append(cache[rgba])
        comparison_json=json.dumps({k:v for k,v in result.items() if k!='meshes'})
except Exception as error:
    geometry=[];materials=[];part_ids=[];type_ids=[];comparison_json=None;report='INVALID COMPARISON: '+str(error)
    import Grasshopper
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,report)
