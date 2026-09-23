"""Restore the byte-exact historical package from committed binary parts."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def restore(output=None):
 source=ROOT/'project/archive/v74';manifest=json.loads((source/'ARCHIVE_PARTS.json').read_text());chunks=[]
 for part in manifest['parts']:
  data=(source/part['name']).read_bytes()
  if len(data)!=part['bytes'] or hashlib.sha256(data).hexdigest()!=part['sha256']:raise ValueError('Archive part mismatch: '+part['name'])
  chunks.append(data)
 data=b''.join(chunks)
 if len(data)!=manifest['bytes'] or hashlib.sha256(data).hexdigest()!=manifest['sha256']:raise ValueError('Restored archive mismatch')
 output=Path(output) if output else ROOT/'restored'/manifest['original_name'];output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(data);return output
if __name__=='__main__':print(restore())
