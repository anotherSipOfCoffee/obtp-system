#! python 3
"""Reposition only named OBTP stage groups in the active GH document."""
from pathlib import Path
import runpy
import Grasshopper
ns=runpy.run_path(str(Path(__file__).resolve().parent/'obtp'/'canvas_tidy.py'))
doc=Grasshopper.Instances.ActiveCanvas.Document
if doc is None:raise RuntimeError('Open an OBTP definition first')
print('Tidied %s OBTP groups; wiring unchanged'%ns['tidy'](doc))
Grasshopper.Instances.ActiveCanvas.Refresh()
