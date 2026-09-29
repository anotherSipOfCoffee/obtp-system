"""Orthographic z-buffer for source-mesh review images (not generative imagery)."""
def render(result,path,width=1200,height=850):
 import numpy as np
 from PIL import Image
 allv=np.array([v for m in result['meshes'] for v in m['vertices']],float)
 def project(v):return np.column_stack((.8660254*(v[:,0]+v[:,1]),.5*(v[:,0]-v[:,1])-v[:,2],v[:,0]-v[:,1]+v[:,2]))
 q=project(allv);lo=q[:,:2].min(0);hi=q[:,:2].max(0);scale=min((width-60)/(hi[0]-lo[0]),(height-60)/(hi[1]-lo[1]));pad=(np.array([width,height])-(hi-lo)*scale)/2
 pixels=np.full((height,width,3),[246,244,238],dtype=np.uint8);depth=np.full((height,width),-np.inf)
 for mesh in result['meshes']:
  vs=np.array(mesh['vertices'],float);qs=project(vs);qs[:,:2]=(qs[:,:2]-lo)*scale+pad
  for face in mesh['faces']:
   for tri in ([face[:3]] if len(face)==3 else [face[:3],[face[0],face[2],face[3]]]):
    v=vs[tri];normal=np.cross(v[1]-v[0],v[2]-v[0]);length=np.linalg.norm(normal)
    if length==0 or normal@np.array([1,-1,1])<=0:continue
    p=qs[tri];x0,y0=np.maximum(0,np.floor(p[:,:2].min(0)).astype(int));x1,y1=np.minimum([width-1,height-1],np.ceil(p[:,:2].max(0)).astype(int))
    if x1<x0 or y1<y0:continue
    yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
    den=(p[1,1]-p[2,1])*(p[0,0]-p[2,0])+(p[2,0]-p[1,0])*(p[0,1]-p[2,1])
    if abs(den)<1e-9:continue
    a=((p[1,1]-p[2,1])*(xx-p[2,0])+(p[2,0]-p[1,0])*(yy-p[2,1]))/den
    b=((p[2,1]-p[0,1])*(xx-p[2,0])+(p[0,0]-p[2,0])*(yy-p[2,1]))/den;c=1-a-b
    z=a*p[0,2]+b*p[1,2]+c*p[2,2];buf=depth[y0:y1+1,x0:x1+1];mask=(a>=-1e-8)&(b>=-1e-8)&(c>=-1e-8)&(z>buf)
    shade=.64+.36*max(0,float(normal/length@np.array([.35,-.45,.82])))
    colour=np.clip(np.array(mesh['rgba'][:3])*shade,0,255).astype(np.uint8)
    pixels[y0:y1+1,x0:x1+1][mask]=colour;buf[mask]=z[mask]
 Image.fromarray(pixels).save(path)
