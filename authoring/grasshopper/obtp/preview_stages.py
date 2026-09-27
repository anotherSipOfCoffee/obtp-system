"""Display-only cumulative assembly stages and canonical part-type colours."""
import hashlib
from .documentation import stage, STAGES
from .manufacturing import identity
from .export import COLORS


def core_part(part):
    return (part['family'] in ('floor','walls','partitions','roof','terrace','foundation')
            and part['material'] in ('timber','concrete-study'))


def prepare(scene, assembly_stage=8, core_frame=0):
    level=int(assembly_stage);core=int(core_frame)
    if level!=assembly_stage or not 0<=level<=8:raise ValueError('Assembly stage must be 0-8')
    if core!=core_frame or core not in (0,1):raise ValueError('Core frame must be 0 or 1')
    # Build the palette before stage filtering so colours never change with stage.
    palette={};used=set()
    for key in sorted({identity(p) for p in scene['parts'] if core_part(p)}):
        salt=0
        while True:
            raw=hashlib.sha256((key+':'+str(salt)).encode()).digest()
            rgb=tuple(64+int(v)*160//256 for v in raw[:3])
            if rgb not in used:break
            salt+=1
        palette[key]=rgb;used.add(rgb)
    selected=[p for p in scene['parts'] if stage(p)<level and (not core or core_part(p))]
    keys=[identity(p) for p in selected]
    ids=['P-'+hashlib.sha256(k.encode()).hexdigest()[:16] for k in keys]
    rgba=[palette[k]+(255,) if core else COLORS.get(p['material'],COLORS['object']) for p,k in zip(selected,keys)]
    legend=[]
    if core:
        for key in sorted(set(keys)):
            matching=[(p,i) for p,k,i in zip(selected,keys,ids) if k==key]
            p,type_id=matching[0];rgb=palette[key]
            legend.append(type_id+' | RGB '+','.join(map(str,rgb))+' | '+str(len(matching))+' pcs | '+p['material']+' | '+' x '.join(f'{v:g}' for v in sorted(p['size']))+' mm')
    label='0 / Empty' if not level else str(level)+' / '+STAGES[level-1][0]
    return dict(parts=selected,type_ids=ids,rgba=rgba,legend=legend,status=label+' | '+str(len(selected))+' visible parts | '+('Core frame: colours = provisional manufacturing types' if core else 'Complete model: material colours'))
