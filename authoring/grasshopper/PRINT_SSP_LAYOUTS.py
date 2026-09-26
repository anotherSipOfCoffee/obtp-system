#! python 3
"""Reprint the latest generated SSP layouts after editing them in Rhino."""
import Rhino
import json
import sys
import importlib.util
import hashlib
from pathlib import Path
import rhinoscriptsyntax as rs
root=Path(__file__).resolve().parent
name='obtp_'+hashlib.sha1(str(root).encode()).hexdigest()[:12]
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,root/'obtp'/'__init__.py',submodule_search_locations=[str(root/'obtp')])
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
from importlib import import_module
names=json.loads(Rhino.RhinoDoc.ActiveDoc.Strings.GetValue('OBTP/SSP/latest_pages') or '[]')
lookup={p.PageName:p for p in Rhino.RhinoDoc.ActiveDoc.Views.GetPageViews()}
if not names or any(n not in lookup for n in names):raise RuntimeError('Export SSP layouts from GH first; one or more layouts are missing')
path=rs.SaveFileName('Print SSP Rhino layouts','PDF (*.pdf)|*.pdf||',filename='OBTP-SSP-R02.pdf')
if path:print(import_module(name+'.native_drawings').print_layouts([lookup[n] for n in names],path))
