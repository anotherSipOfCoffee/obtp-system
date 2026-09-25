#! python 3
"""Run in Rhino 8 Python 3. Exercises the real Rhino geometry/export pipeline.
Writes only a new diagnostics folder; does not change the active Rhino model.
"""
import sys
import json
import traceback
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
out=ROOT/'diagnostics'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
out.mkdir(parents=True)
report={'status':'running','checks':[],'native_grasshopper_solve_tested':False}
try:
    import Rhino
    from obtp.model import parameters,build
    from obtp.rhino_adapter import Api,audit
    from obtp.export import export_one
    report['rhino_version']=str(Rhino.RhinoApp.Version)
    cases=[(i,{}) for i in range(6)]+[(2,dict(roof_type=r,terrace_steps=2)) for r in range(3)]
    for case,(index,options) in enumerate(cases):
        scene=build(parameters(index,**options))
        check=audit(scene)
        destination=out/('case-'+str(case))
        files=export_one(scene,destination,Api)
        path=destination/(scene['config']['id']+'.3dm')
        reopened=Rhino.FileIO.File3dm.Read(str(path))
        if reopened is None:raise ValueError('Cannot reopen '+str(path))
        try:
            if reopened.Objects.Count != len(scene['parts']):raise ValueError('Part count changed')
            if any(not obj.Geometry.IsValid or not obj.Geometry.IsSolid for obj in reopened.Objects):
                raise ValueError('Invalid or open Brep after export')
        finally:reopened.Dispose()
        report['checks'].append({'configuration':scene['config']['id'],'audit':check,'files':files})
    report['status']='PASS: nine native Rhino geometry and export checks; GH canvas still needs inspection'
except Exception:
    report['status']='FAIL'
    report['traceback']=traceback.format_exc()
finally:
    path=out/'rhino-check.json'
    path.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(report['status'])
    print('Diagnostic report: '+str(path))
    if 'traceback' in report:print(report['traceback'])
