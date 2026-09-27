"""Exact-box orthographic review; depth buffer prevents hidden timber showing through."""
import base64,io,sys,tarfile,tempfile,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from compare_manufacturing import module,REPO,ROOT,PINS
from obtp.model import build,parameters

def view(scene,label):
 w,h=580,720;pixels=np.full((h,w,3),250,dtype=np.uint8);depth=np.full((h,w),-np.inf)
 L=scene['dimensions']['length_mm'];end=L+scene['dimensions']['annex_length_mm'];F=scene['dimensions']['floor_top_mm']
 az=np.deg2rad(-60 if label=='shower' else 60);el=np.deg2rad(15)
 R=np.array([[-np.sin(az),np.cos(az),0],[-np.cos(az)*np.sin(el),-np.sin(az)*np.sin(el),np.cos(el)],[np.cos(az)*np.cos(el),np.sin(az)*np.cos(el),np.sin(el)]])
 centre=np.array([L+450,400 if label=='shower' else 2100,1200]);scale=.24
 colors={'cladding-wood':(49,56,57),'plywood':(198,175,136),'timber':(209,180,129),'object':(170,151,121),'lining-wood':(210,185,148),'deck-wood':(167,142,113)}
 for p in scene['parts']:
  x,y,z=p['origin'];a,b,c=p['size']
  if x+a<L or x>=end+100 or z>F+2100 or p['family'] in ('roof','insulation','foundation'):continue
  if label=='shower' and y>950 or label=='seat' and y+b<1700:continue
  v=np.array([(x+i*a,y+j*b,z+k*c) for i,j,k in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]])
  q=(v-centre)@R.T;q[:,0]=w/2+q[:,0]*scale;q[:,1]=h/2-q[:,1]*scale
  for face,shade in [((0,1,2,3),.7),((4,5,6,7),1.15),((0,1,5,4),1),((1,2,6,5),.85),((2,3,7,6),1),((3,0,4,7),.85)]:
   color=np.clip(np.array(colors.get(p['material'],(180,180,180)))*shade,0,255).astype(np.uint8)
   for ids in ((face[0],face[1],face[2]),(face[0],face[2],face[3])):
    A,B,C=q[list(ids)];x0=max(0,int(min(A[0],B[0],C[0])));x1=min(w,int(max(A[0],B[0],C[0]))+1);y0=max(0,int(min(A[1],B[1],C[1])));y1=min(h,int(max(A[1],B[1],C[1]))+1)
    if x1<=x0 or y1<=y0:continue
    den=(B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
    if abs(den)<1e-8:continue
    yy,xx=np.mgrid[y0:y1,x0:x1];xx=xx+.5;yy=yy+.5
    aa=((B[1]-C[1])*(xx-C[0])+(C[0]-B[0])*(yy-C[1]))/den
    bb=((C[1]-A[1])*(xx-C[0])+(A[0]-C[0])*(yy-C[1]))/den;cc=1-aa-bb
    zz=aa*A[2]+bb*B[2]+cc*C[2];mask=(aa>=0)&(bb>=0)&(cc>=0)&(zz>depth[y0:y1,x0:x1])
    depth[y0:y1,x0:x1][mask]=zz[mask];pixels[y0:y1,x0:x1][mask]=color
 return Image.fromarray(pixels)

def render(out):
 with tempfile.TemporaryDirectory() as t:
  data=subprocess.check_output(['git','-C',str(REPO),'archive',PINS['previous'],'authoring/grasshopper'])
  with tarfile.open(fileobj=io.BytesIO(data)) as ar:ar.extractall(t,filter='data')
  old=module(Path(t)/'authoring/grasshopper','detail_previous')
  scenes=[old.build(old.parameters(3,roof_type=0)),build(parameters(3,roof_type=0))]
  canvas=Image.new('RGB',(1160,1500),'#fafafa');d=ImageDraw.Draw(canvas)
  for row,s in enumerate(scenes):
   for col,label in enumerate(('shower','seat')):
    canvas.paste(view(s,label),(col*580,row*750+30));d.text((col*580+30,row*750+10),('Previous R18' if row==0 else 'Revised R19')+' / '+label,fill='#222222',font_size=20)
  canvas.save(out/'niche-comparison.png')
  (out/'niche-finish.svg').write_text(('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1160 1500"><image href="data:image/png;base64,PNG_DATA" width="1160" height="1500"/></svg>').replace('PNG_DATA',base64.b64encode((out/'niche-comparison.png').read_bytes()).decode()))
if __name__=='__main__':render(Path(sys.argv[1]))

# A cropped plan compares actual member faces at two complete bay seams.
def terrace_plan(out):
 with tempfile.TemporaryDirectory() as t:
  data=subprocess.check_output(['git','-C',str(REPO),'archive',PINS['previous'],'authoring/grasshopper'])
  with tarfile.open(fileobj=io.BytesIO(data)) as ar:ar.extractall(t,filter='data')
  old=module(Path(t)/'authoring/grasshopper','terrace_previous')
  scenes=[old.build(old.parameters(2,roof_type=0)),build(parameters(2,roof_type=0))]
  svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 850"><rect width="1000" height="850" fill="white"/>']
  for col,s in enumerate(scenes):
   ox=40+col*500;scale=.22
   svg.append(f'<text x="{ox}" y="30" font-family="Arial" font-size="21">'+('R18: centred terrace axes' if col==0 else 'R19: aligned bay-edge faces')+'</text>')
   for p in s['parts']:
    if not (p['family']=='floor' and p['material']=='timber' or p['id'].startswith('terrace/joist-')):continue
    x,y,z=p['origin'];a,b,c=p['size'];lo=max(0,x);hi=min(1800,x+a)
    if hi<=lo:continue
    color='#a4cdaa' if p['family']=='floor' else '#356c4d'
    svg.append(f'<rect x="{ox+lo*scale}" y="{60+(2400-y-b)*scale}" width="{(hi-lo)*scale}" height="{b*scale}" fill="{color}"/>')
   for x in (0,900,1800):
    svg.append(f'<path d="M{ox+x*scale},50v800" stroke="#9b5050" stroke-width=".7" stroke-dasharray="5 4"/>')
  svg.append('<text x="40" y="837" font-family="Arial" font-size="15">900 mm bay edges align exactly; terrace keeps intermediate decking supports. Floor bays unchanged.</text></svg>')
  (out/'terrace-frame.svg').write_text(''.join(svg))
if __name__=='__main__':terrace_plan(Path(sys.argv[1]))
