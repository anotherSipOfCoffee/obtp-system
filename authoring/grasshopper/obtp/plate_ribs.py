"""B: independent, open-ended insulated plate-rib geometry study, mm.
No strength, composite action, fastening or supplier compatibility is asserted.
"""
import hashlib,json,math
from .manufacturing import analyse

def _integer(name,value,lo,hi):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or int(value)!=value or not lo<=value<=hi:
        raise ValueError('%s must be an integer in %s..%s'%(name,lo,hi))
    return int(value)

def subtract(box,cut):
    """Disjoint rectangular remainder, used only to cut insulation around solids."""
    lo,size=box;hi=[lo[k]+size[k] for k in range(3)]
    a=[max(lo[k],cut['origin'][k]) for k in range(3)]
    b=[min(hi[k],cut['origin'][k]+cut['size'][k]) for k in range(3)]
    if any(b[k]-a[k]<=1e-7 for k in range(3)):return [box]
    pieces=[];low=list(lo);high=list(hi)
    for k in range(3):
        for end in (0,1):
            l=low[:];h=high[:]
            if end==0:h[k]=a[k]
            else:l[k]=b[k]
            if h[k]-l[k]>1e-7:pieces.append((l,[h[j]-l[j] for j in range(3)]))
        low[k]=a[k];high[k]=b[k]
    return pieces

def merge_boxes(boxes):
    """Join adjacent insulation blanks across complete matching faces."""
    boxes=list(boxes)
    changed=True
    while changed:
        changed=False
        for i,(a,sa) in enumerate(boxes):
            for j in range(i+1,len(boxes)):
                b,sb=boxes[j]
                for k in range(3):
                    if all(abs(a[q]-b[q])<1e-7 and abs(sa[q]-sb[q])<1e-7 for q in range(3) if q!=k) and (abs(a[k]+sa[k]-b[k])<1e-7 or abs(b[k]+sb[k]-a[k])<1e-7):
                        lo=list(a);size=list(sa);lo[k]=min(a[k],b[k]);size[k]=sa[k]+sb[k]
                        boxes[i]=(lo,size);boxes.pop(j);changed=True;break
                if changed:break
            if changed:break
    return boxes

def build(bays=4,pitch=900,span=3600,height=2100,thickness=45,depth=240):
    bays=_integer('bays',bays,1,8)
    pitch=_integer('pitch',pitch,600,1200)
    if pitch not in (600,900,1200):raise ValueError('Pitch must be 600, 900 or 1200')
    span=_integer('span',span,2400,4800);height=_integer('height',height,2100,2700)
    thickness=_integer('thickness',thickness,27,75);depth=_integer('depth',depth,180,360)
    # x = repetition, y = transverse span, z = elevation.
    # First/last ribs are flush to envelope ends; intermediate ribs are centred.
    length=bays*pitch;skin=18;gusset=18;reach=2*depth;floor=depth+skin
    parts=[];joints=[]
    def add(id,family,material,origin,size,assembly,role,grain='unresolved'):
        if min(size)<=0:raise ValueError('Nonpositive part '+id)
        parts.append(dict(id=id,family=family,material=material,origin=list(origin),size=list(size),assembly=assembly,
          manufacturing=dict(material_spec=('LVL grade/product unselected' if material=='timber' else material),grain_axis=grain,
            machining='straight rectangular cuts; holes and reliefs unspecified',handedness='rectangular blank; final handing unresolved',
            connection_detail=role+'; fastening pattern unresolved',verified=False)))
    for i in range(bays+1):
        x=0 if i==0 else length-thickness if i==bays else i*pitch-thickness/2
        a='B/rib-%02d'%i
        add(a+'/floor','floor','timber',[x,0,0],[thickness,span,depth],a,'floor-rib','span-y')
        add(a+'/left','walls','timber',[x,0,floor],[thickness,depth,height],a,'wall-rib','vertical-z')
        add(a+'/right','walls','timber',[x,span-depth,floor],[thickness,depth,height],a,'wall-rib','vertical-z')
        add(a+'/roof','roof','timber',[x,0,floor+height],[thickness,span,depth],a,'roof-rib','span-y')
        # Two surface-mounted cheeks per knee, reachable from opposite x faces.
        for side,y in [('left',0),('right',span-reach)]:
            ids=[a+'/'+side,a+'/roof'];cheeks=[]
            for face,xx in [('a',x-gusset),('b',x+thickness)]:
                pid=a+'/knee-'+side+'-'+face
                add(pid,'walls','plywood',[xx,y,floor+height-depth],[gusset,reach,2*depth],a,'knee-cheek','cross-laminated specification unresolved');cheeks.append(pid)
            joints.append(dict(id=a+'/joint-'+side,parts=ids+cheeks,type='butt-bearing with paired external cheeks',insertion_axis='x, opposite sides',fasteners=None,capacity=None))
        joints.extend([dict(id=a+'/base-'+side,parts=[a+'/'+side,a+'/floor'],type='bearing through floor deck; tie-down unresolved',fasteners=None,capacity=None) for side in ('left','right')])
    # Deck and longitudinal wall skins are non-composite candidate diaphragms.
    # Seams along x fall on the ribs. Transverse deck seams need backing below.
    for b in range(bays):
        x=b*pitch;a='B/infill-%02d'%b
        for j in range(math.ceil(span/1200)):
            y=j*1200;w=min(1200,span-y)
            add(a+'/floor-skin-%d'%j,'floor','plywood',[x,y,depth],[pitch,w,skin],a,'floor-skin','major-y')
            add(a+'/roof-skin-%d'%j,'roof','plywood',[x,y,floor+height+depth],[pitch,w,skin],a,'roof-skin','major-x')
        for j in range(1,math.ceil(span/1200)):
            for level,z,family in [('floor',depth-90,'floor'),('roof',floor+height+depth-90,'roof')]:
                lo=x+thickness if b==0 else x+thickness/2
                hi=x+pitch-thickness if b==bays-1 else x+pitch-thickness/2
                add(a+'/'+level+'-seam-%d'%j,family,'timber',[lo,j*1200-45,z],[hi-lo,90,90],a,level+'-seam-backing','long-x')
        # Exterior skins offset past terminal knee cheeks only in x, not y.
        for side,y in [('left',-skin),('right',span)]:
            add(a+'/wall-skin-'+side,'walls','plywood',[x,y,floor],[pitch,skin,height+depth],a,'wall-skin','major-z')
    structural=list(parts)
    for b in range(bays):
        a='B/infill-%02d'%b
        lo=thickness if b==0 else b*pitch+thickness/2
        hi=length-thickness if b==bays-1 else (b+1)*pitch-thickness/2
        domains=[('floor',[lo,0,0],[hi-lo,span,depth]),('roof',[lo,0,floor+height],[hi-lo,span,depth]),
                 ('left',[lo,0,floor],[hi-lo,depth,height]),('right',[lo,span-depth,floor],[hi-lo,depth,height])]
        for tag,origin,size in domains:
            boxes=[(origin,size)]
            for cut in structural:boxes=[q for box in boxes for q in subtract(box,cut)]
            for j,(o,s) in enumerate(merge_boxes(boxes)):add(a+'/insulation-'+tag+'-%d'%j,'insulation','mineral-wool',o,s,a,'insulation-cut-'+tag)
    holds=[
      'Experimental open-ended chassis, not a complete weatherproof building; no door/window/end-wall design is claimed.',
      'LVL product/grade and stock size unselected. Thickness and depth are geometry inputs, not span ratings.',
      'Butt knees with paired rectangular cheek plates require engineered fasteners and rotational stiffness. No moment-frame capacity assumed.',
      'Longitudinal skin diaphragms, seam backing attachment, out-of-plane restraint, hold-downs and foundations require engineering.',
      'No structural glue or composite action assumed. COMPAS Wood informed contact/insertion metadata; its kernel is not required or executed here.',
      'Insulation fits geometric cavities only. End seals, membrane continuity, external continuous insulation, fire and moisture require design.',
      'Ribs are assembled from separate pieces; whole-rib lifting and temporary bracing are unverified.',
      'Fasteners, seals, membranes and end closures are not quantified. Counts cannot be compared as complete-building savings.'
    ]
    scene=dict(version='GH-R22-B-PLATE-RIBS',status='EXPERIMENTAL GEOMETRY / NOT ENGINEERED',config=dict(id='B-%dx%d-%d'%(bays,pitch,span),bays=bays,pitch=pitch,span=span,height=height,thickness=thickness,depth=depth),parts=parts,joints=joints,holds=holds,checks=dict(positive_dimensions=True),metrics={})
    scene['geometry_sha256']=hashlib.sha256(json.dumps(parts,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    scene['manufacturing']=analyse(scene,True)
    scene['metrics']=dict(length_mm=length,span_mm=span,clear_width_mm=span-2*depth,clear_height_mm=height,
      lvl_blank_volume_m3=sum(math.prod(p['size'])/1e9 for p in parts if p['material']=='timber'),
      plywood_volume_m3=sum(math.prod(p['size'])/1e9 for p in parts if p['material']=='plywood'),
      insulation_volume_m3=sum(math.prod(p['size'])/1e9 for p in parts if p['material']=='mineral-wool'),
      joint_interfaces=len(joints),fastener_quantity=None,cutting_waste=None)
    return scene
