"""Versioned, validated file handoffs between independent room canvases."""
import hashlib
import json
import os
import tempfile
from pathlib import Path
from .room_config import require
from .layout import digest


def validate(data, stage):
    if stage in ('plan', 'skeleton', 'box', 'foundation', 'roof'):
        return require(data, stage)
    if stage != 'scene' or not isinstance(data, dict) or data.get('schema') != 'obtp-room-scene/1':
        raise ValueError('Expected a complete room configuration scene')
    if not data.get('parts') or not data.get('geometry_sha256'):
        raise ValueError('Scene has no complete geometry')
    actual=hashlib.sha256(json.dumps(data['parts'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if actual != data['geometry_sha256']:raise ValueError('Scene geometry checksum mismatch')
    return data


def transfer(stage, upstream=None, file_path='', read_file=False, write_file=False):
    """Live input wins. Bad live data must never fall back to an old file."""
    live = upstream is not None and upstream != ''
    if live:
        data = validate(json.loads(upstream) if isinstance(upstream, str) else upstream, stage)
    elif read_file:
        envelope = json.loads(Path(file_path).expanduser().read_text(encoding='utf-8'))
        if envelope.get('schema') != 'obtp-handoff/1' or envelope.get('stage') != stage:
            raise ValueError('Wrong handoff type; expected '+stage)
        if envelope.get('sha256') != digest(envelope.get('data')):
            raise ValueError('Handoff checksum mismatch')
        data = validate(envelope['data'], stage)
    else:
        raise ValueError('Connect live '+stage+' data or enable Read saved with a valid file path')
    message = 'Live '+stage if live else 'Imported '+stage
    if write_file:
        if not live:
            raise ValueError('Export requires live input; imported files are not rewritten')
        if not str(file_path).strip():raise ValueError('Choose an export file path')
        path = Path(file_path).expanduser()
        if path.suffix.lower() != '.json':raise ValueError('Handoff path must end in .json')
        path.parent.mkdir(parents=True, exist_ok=True)
        envelope = dict(schema='obtp-handoff/1',stage=stage,units='mm',data=data,sha256=digest(data))
        fd, temporary = tempfile.mkstemp(dir=str(path.parent),prefix='.obtp-',suffix='.json')
        try:
            with os.fdopen(fd,'w',encoding='utf-8') as stream:
                json.dump(envelope,stream,ensure_ascii=False,indent=2)
            os.replace(temporary,path)
        finally:
            if os.path.exists(temporary):os.unlink(temporary)
        message += ' / saved '+str(path)
    return json.dumps(data), message
