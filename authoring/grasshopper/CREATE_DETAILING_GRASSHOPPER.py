#! python 3
"""Create a separate native GH document. Safe with other definitions already open."""
from pathlib import Path
import runpy
# Fresh globals on every run: another creator cannot change this mode or ROOT.
runpy.run_path(str(Path(__file__).resolve().parent/'room_canvas.py'),
               init_globals={'CANVAS_MODE':'detailing'})
