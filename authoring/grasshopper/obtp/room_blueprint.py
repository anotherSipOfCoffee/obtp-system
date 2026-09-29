"""Legacy command-to-layout adapter used only while resolving saved architectural plans."""
from . import cells

def runs_from_commands(commands):
 runs=[]
 for c in commands:
  if c['kind']!='wall':continue
  name,base,axis,length=c['args'];kw=c['kwargs'];depth=kw.get('d',195);k=0 if axis=='x' else 1
  r=dict(id=name,base=base,axis=axis,length=length,depth=depth,skin_side=kw.get('side_skin',1),family=kw.get('family','walls'),side='front' if axis=='x' and base[1]==0 else 'back' if axis=='x' else 'west' if base[0]==0 else 'east',external=kw.get('family','walls')!='partitions')
  if kw.get('door'):
   u,w=kw['door'];fit=dict(start=u) if name=='annex-end' else cells.opening(base[k],base[k]+length,cells.X if k==0 else cells.Y,w,base[k]+u)
   o=list(base);o[k]+=fit['start'];r.update(door_width=w,opening_start=fit['start'],opening_origin=o,kind='window' if 'window' in name else 'door')
  runs.append(r)
 return runs
