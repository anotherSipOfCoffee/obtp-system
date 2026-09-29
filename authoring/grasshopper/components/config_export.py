#! python 3
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')]);package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
receipt='Export off'
try:
 enabled=globals().get('run_export',False);enabled=getattr(enabled,'Value',enabled)
 if enabled:
  v=globals().get('scene_json');v=getattr(v,'Value',v);scene=json.loads(v)
  if not scene or scene.get('schema')!='obtp-room-scene/1':raise ValueError('Connect a complete room-config scene')
  code=importlib.import_module(name+'.export');adapter=importlib.import_module(name+'.rhino_adapter')
  folder=root/'exports-room-config'/scene['geometry_sha256'][:12]
  outputs=code.export_one(scene,folder,adapter.Api)
  (folder/'manufacturing-schedules.json').write_text(json.dumps(scene['manufacturing'],indent=2))
  receipt='Saved model, drawings, parts CSV and separate primary/cladding schedules: '+str(folder)
except Exception as error:
 receipt=str(error)
 import Grasshopper
 ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,receipt)
