"""Explicit THERM handoff using its documented Fairyfly public API.
Returned file is unverified until parsed and independently checked. Never marks completed.
"""
import argparse,hashlib,json,importlib.metadata
from pathlib import Path

def run(source,preflight_path,output):
    from fairyfly_therm.run import run_thmz
    source=Path(source).resolve()
    if source.suffix.lower()!='.thmz' or not source.is_file():raise ValueError('Provide a checked THMZ input')
    preflight=json.loads(Path(preflight_path).read_text())
    # THERM modifies the archive; preserve original and run a local copy.
    import shutil
    out=Path(output).resolve();out.mkdir(parents=True,exist_ok=True)
    target=out/source.name
    if target==source:raise ValueError('Output folder must differ from source folder')
    shutil.copy2(source,target)
    receipt={'status':'running','source_sha256':preflight['source_sha256'],
      'inputs_sha256':preflight['inputs_sha256'],'solver':'THERM via Fairyfly',
      'version':{'fairyfly-therm':importlib.metadata.version('fairyfly-therm'),'THERM':None},
      'input_file_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
    receipt_path=out/'solver-receipt.json'
    try:
        result=Path(run_thmz(str(target),silent=False))
        receipt.update(status='executed_unverified',output_file=str(result),
            output_file_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
            checks={'boundary_conditions':False,'mesh_convergence':False,'result_parse':False})
    except Exception as exc:
        receipt.update(status='failed',error=str(exc));raise
    finally:receipt_path.write_text(json.dumps(receipt,indent=2))
    return receipt
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('thmz');p.add_argument('preflight');p.add_argument('output')
    a=p.parse_args();print(json.dumps(run(a.thmz,a.preflight,a.output),indent=2))
