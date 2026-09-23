"""Build a self-contained snapshot from three pinned local checkouts. No network writes."""
import hashlib,json,os,shutil,subprocess,zipfile
from pathlib import Path
from restore_v74 import restore
ROOT=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
 cfg=json.loads((ROOT/'project/SNAPSHOT_REQUEST.json').read_text());out=Path.cwd()/'snapshot-output';stage=Path.cwd()/'snapshot-stage'/cfg['name'];stage.mkdir(parents=True,exist_ok=False);out.mkdir(exist_ok=True);commits={}
 for name,expected in cfg['repositories'].items():
  repo=ROOT.parent/name;actual=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip();expected=os.environ.get('GITHUB_SHA') if expected=='$self'else expected
  if actual!=expected:raise ValueError('Checkout mismatch '+name)
  commits[name]=actual
  for p in sorted(repo.rglob('*')):
   rel=p.relative_to(repo)
   if '.git' in rel.parts or '__pycache__' in rel.parts or not p.is_file():continue
   dest=stage/'05_REPOSITORIES'/name/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 # Verify permanent committed binary payloads before extraction.
 for entry in json.loads((ROOT/'sources/PERMANENT_FILE_MANIFEST.json').read_text()):
  data=(ROOT/entry['path']).read_bytes()
  if len(data)!=entry['bytes']or sha(data)!=entry['sha256']:raise ValueError('Permanent file mismatch '+entry['path'])
 archive=restore(stage/'90_ARCHIVE/OBTP_Project_System_v74.zip')
 with zipfile.ZipFile(archive)as z:
  for entry in json.loads((ROOT/'project/archive/v74/FILE_INVENTORY.json').read_text()):
   data=z.read('OBTP_Project_System_v74/'+entry['path'])
   if len(data)!=entry['bytes']or sha(data)!=entry['sha256']:raise ValueError('v74 content mismatch '+entry['path'])
 cad=stage/'04_SOURCE_CAD';cad.mkdir()
 for bundle in sorted((ROOT/'sources/skylark150').glob('*.zip')):
  with zipfile.ZipFile(bundle)as z:
   for name in z.namelist():
    rel=Path(name)
    if rel.is_absolute()or '..'in rel.parts:raise ValueError('Unsafe archive path')
    if name.endswith('/'):continue
    data=z.read(name);p=cad/rel
    if p.exists()and p.read_bytes()!=data:raise ValueError('Conflicting source copies '+name)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 source_checks=[]
 for entry in json.loads((ROOT/'docs/CATALOGUE_SOURCE_LOCK.json').read_text()):
  data=(cad/entry['path']).read_bytes();blob=hashlib.sha1(('blob %d\0'%len(data)).encode()+data).hexdigest()
  if blob!=entry['sha']:raise ValueError('Original CAD blob mismatch '+entry['path'])
  source_checks.append(dict(path=entry['path'],git_blob_sha=blob))
 agent=stage/'01_AGENT';agent.mkdir();shutil.copyfile(ROOT/'project/AGENT_GUIDE.md',agent/'AGENT_GUIDE.md');shutil.copyfile(ROOT/'project/CURRENT_STATE.md',agent/'CURRENT_STATE.md');shutil.copyfile(ROOT/'project/AGENT_GUIDE.md',stage/'AGENTS.md')
 (stage/'00_START_HERE.md').write_text(f'''# OBTP {cfg['version']} — complete GitHub snapshot / {cfg['date']}
GitHub is the editable source of truth. This Drive package is a dated snapshot, not a second master.

## Read order
1. AGENTS.md and 01_AGENT/AGENT_GUIDE.md.
2. 01_AGENT/CURRENT_STATE.md and SNAPSHOT_MANIFEST.json.
3. 05_REPOSITORIES/<target-project>/AGENTS.md and relevant current docs.

Before changing a project, inspect the latest GitHub main branch and compare it with the exact commits recorded here. Never overwrite newer GitHub work with this snapshot wholesale. Historical v74 instructions are not current instructions.

## Contents
05_REPOSITORIES contains all three pinned repository exports. System's project/ directory contains shared guides, original pilot files and historical evidence. 04_SOURCE_CAD contains the actual original CAD/DXF, not LFS pointers. 90_ARCHIVE preserves the complete, byte-exact original v74 package. FILE_INVENTORY.json and SHA256SUMS.txt verify the contents.

## Authoritative repositories
https://github.com/anotherSipOfCoffee/obtp-studio
https://github.com/anotherSipOfCoffee/obtp-architecture
https://github.com/anotherSipOfCoffee/obtp-system

## Already-selected next deliverable
Full illustrated technical PDF report from current GitHub evidence. The owner asked to consolidate storage first. That report remains pending; old archived reports are not its replacement.
''')
 (stage/'WEBSITE_LINKS.md').write_text('# Published outputs\n'+''.join('- '+name+': https://anothersipofcoffee.github.io/'+name+'/\n'for name in commits))
 manifest=dict(schema='obtp-project-snapshot/1',version=cfg['version'],date=cfg['date'],source_of_truth='GitHub',role='dated full snapshot; no continuous two-way sync',repositories=commits,original_cad=source_checks,v74_original_sha256=sha(archive.read_bytes()),pending_deliverable='Full illustrated technical PDF report',includes_actual_cad=True,git_lfs_pointers_used=False)
 (stage/'SNAPSHOT_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
 inventory=[dict(path=str(p.relative_to(stage)),bytes=p.stat().st_size,sha256=sha(p.read_bytes()))for p in sorted(stage.rglob('*'))if p.is_file()]
 (stage/'FILE_INVENTORY.json').write_text(json.dumps(inventory,indent=2));(stage/'SHA256SUMS.txt').write_text(''.join(f"{i['sha256']}  {i['path']}\n"for i in inventory))
 package=out/(cfg['name']+'.zip')
 with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for p in sorted(stage.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(stage.parent)))
 with zipfile.ZipFile(package)as z:
  if z.testzip()is not None:raise ValueError('ZIP CRC check failed')
  for entry in inventory:
   if sha(z.read(cfg['name']+'/'+entry['path']))!=entry['sha256']:raise ValueError('Snapshot checksum mismatch')
 report=dict(passed=True,package=package.name,package_bytes=package.stat().st_size,sha256=sha(package.read_bytes()),included_commits=commits,files_verified=len(inventory),original_cad_files_verified=len(source_checks),v74_files_verified=196,checks=['three exact GitHub commits','permanent bundle hashes','byte-exact restored v74 archive','196 v74 file hashes','original CAD Git blob hashes','all snapshot file hashes','ZIP CRC'])
 (out/'VERIFICATION.json').write_text(json.dumps(report,indent=2));(out/(package.name+'.sha256')).write_text(report['sha256']+'  '+package.name+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
