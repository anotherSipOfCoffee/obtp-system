"""Bundle the complete GH source plus optional locally regenerated review exports."""
import hashlib,json,sys,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'authoring/grasshopper'
out=Path(sys.argv[1] if len(sys.argv)>1 else 'OBTP_Grasshopper_R26.zip').resolve()
files=[]
for folder in ['obtp','components','analysis','comparison_data','tests']:
 files += [p for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix in ('.py','.json','.md','.gz')]
files += [p for p in root.iterdir() if p.is_file() and p.suffix in ('.py','.md')]
for folder in ['review-r22','review-r23','review-r24','review-r25','gh-documents']:
 files += [p for p in (root/folder).glob('*') if p.is_file() and (p.suffix in ('.html','.svg','.png','.3dm','.csv','.pdf','.md') or (folder in ('review-r23','review-r24','review-r25') and p.suffix=='.json'))]
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(set(files)):z.write(p,p.relative_to(root))
 z.writestr('PACKAGE_MANIFEST.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for required in ['GH_R26.md','obtp/checkpoints.py','components/assembly_checkpoint.py','components/final_preview.py','components/inspect_checkpoints.py','GH_R25.md','obtp/plan_construction.py','CREATE_GRASSHOPPER.py','components/comparison.py','obtp/plate_ribs.py','comparison_data/wikihouse.json.gz','GH_R24.md','obtp/sauna_workflow.py','components/sauna_preset.py','components/sauna_cassette.py','CREATE_RESEARCH_GRASSHOPPER.py','obtp/layout.py','components/room_programme.py','components/room_relationships.py','components/room_layout.py','components/layout_bridge.py']:
  assert required in z.namelist(),required
print(str(out),out.stat().st_size,'bytes;',len(files),'files')
