#! python 3
# Canonical source analysis preparation; solver execution is explicitly separate.
import hashlib,importlib,importlib.util,json,sys
from pathlib import Path
root=Path(ghenv.Component.OnPingDocument().FilePath).parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')])
    package=importlib.util.module_from_spec(spec);sys.modules[name]=package;spec.loader.exec_module(package)
core=importlib.reload(importlib.import_module(name+'.analysis'))
def value(x):return x.Value if hasattr(x,'Value') else x
scene=json.loads(str(value(scene_json)))
settings=json.loads(str(value(inputs_json)))
a=core.prepare(scene,settings)
preflight_json=json.dumps(a)
geometry_report=json.dumps(a['audit'],indent=2)
solver_report=json.dumps(a['workflows'],indent=2)
results_report='NOT RUN: no thermal or structural results; wind and snow paused. No numerical diagrams available.'
diagrams_report='Model-derived material sections: plan, section-a, section-b, window-head, window-sill. Export for inspection.'
receipt='Export disabled'
if bool(value(run_export)):
    out=root/'analysis-exports'/scene['config']['id']
    core.write_bundle(scene,out,settings)
    sheets=importlib.reload(importlib.import_module(name+'.sheets'))
    sheets.pdf(scene,out/'technical-product.pdf')
    receipt='Prepared geometry and diagnostic dossier: '+str(out)+'; solver workflows NOT RUN'
