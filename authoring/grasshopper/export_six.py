"""Run in Rhino 8 Python 3 for an accepted runtime export, or CPython + rhino3dm for a portable preview.
Neither mode changes the websites. Outputs remain review candidates.
"""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from obtp.model import PRESETS, build, parameters
from obtp.export import export_one, file3dm


def main(output=None):
    directory=Path(output or Path(__file__).parent/'exports')
    try:
        import Rhino
        # Adapter exposes both geometry and FileIO types consumed by our writer.
        from obtp.rhino_adapter import Api
        api=Api
        runtime='Rhino '+str(Rhino.RhinoApp.Version)
    except ImportError:
        api=None;runtime='Portable CPython/rhino3dm preview; not a Grasshopper solve'
    scenes=[];manifest=[]
    for i,preset in enumerate(PRESETS):
        scene=build(parameters(i));scenes.append(scene)
        manifest.append(dict(id=preset['id'],parameters=scene['config'],metrics=scene['metrics'],
                             geometry_sha256=scene['geometry_sha256'],files=export_one(scene,directory,api)))
    file3dm(scenes,directory/'OBTP_Sauna_All_Six_R04.3dm',api)
    (directory/'manifest.json').write_text(json.dumps(dict(schema='obtp-catalogue/1',runtime=runtime,
        website_ready=False,configurations=manifest),indent=2),encoding='utf-8')
    print('Exported six review configurations to '+str(directory))
    return directory

if __name__=='__main__':main()
