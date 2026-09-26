"""Run once against owner's batches.dxf. Keep source hash and named polylines."""
import ezdxf,json,hashlib,sys
from pathlib import Path
from ezdxf.path import make_path
p=Path(sys.argv[1]);doc=ezdxf.readfile(p);result={'source':'batches.dxf','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'blocks':{}}
for name in ['Door Lining','Outdoor Bench','Shower Kit 01']:
    lines=[]
    for e in doc.blocks[name]:
        try:lines.append([[round(v.x,6),round(v.y,6)] for v in make_path(e).flattening(2)])
        except (TypeError,ValueError,AttributeError):pass
    result['blocks'][name]={'lines':lines}
Path(__file__).resolve().parents[1].joinpath('obtp/symbols.json').write_text(json.dumps(result,separators=(',',':')))
