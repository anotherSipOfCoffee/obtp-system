(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.OBTPMeshRenderer=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
function shade(hex,f){return '#'+hex.slice(1).match(/../g).map(v=>Math.max(0,Math.min(255,Math.round(parseInt(v,16)*f))).toString(16).padStart(2,'0')).join('');}
function materials(m){return{...m.palette,base:'#adae9e',floor:'#c7b995',wet:'#b7c9c7',entryFloor:'#bbb59f',partition:'#e3ddcc',door:'#c5ba9b',furniture:'#b6a17a',bed:'#ddd5bd',linen:'#f0e8d5',sofa:'#abb39b',kitchen:'#a99877',glass:'#87a19f',metal:'#465148',cladding:shade(m.palette.wall,.83),roofSeam:shade(m.palette.roof,.78)};}
function clipBelow(points,z){
 const out=[];for(let i=0;i<points.length;i++){const a=points[i],b=points[(i+1)%points.length],ai=a[2]<=z,bi=b[2]<=z;if(ai)out.push(a);if(ai!==bi){const t=(z-a[2])/(b[2]-a[2]);out.push([a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1]),z]);}}return out;
}
function meshFaces(packet,model,cutaway){
 const mat=materials(model),faces=[];
 for(const object of packet.objects){
  if(cutaway&&['roof','detail'].includes(object.kind))continue;
  for(const indices of object.faces){
   let points=indices.map(i=>object.vertices[i]);
   if(cutaway&&['wall','partition','door','slider','window'].includes(object.kind))points=clipBelow(points,1.05);
   if(cutaway&&object.kind==='furniture')points=clipBelow(points,.8);
   if(points.length<3)continue;
   const a=points[0],b=points[1],c=points[2],u=b.map((v,i)=>v-a[i]),v=c.map((v,i)=>v-a[i]);
   const normal=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],length=Math.hypot(...normal)||1;
   const light=.83+.2*Math.abs(normal[2]/length)+.07*Math.abs(normal[1]/length);
   faces.push({pts:points,color:shade(mat[object.material]||'#aaaa99',light)});
  }
 }
 return faces;
}
function raster(packet,m,width,height,rotation,cutaway){
 const pixels=new Uint8ClampedArray(width*height*4),depth=new Float64Array(width*height);depth.fill(-Infinity);
 const theta=rotation*Math.PI/180,cs=Math.cos(theta),sn=Math.sin(theta),elev=.47,up=Math.sqrt(1-elev*elev);
 const project=p=>{const x=p[0]-m.L/2,y=p[1]-m.W/2,rx=x*cs-y*sn,ry=x*sn+y*cs;return[rx,elev*ry-up*p[2],up*ry+elev*p[2]];};
 const faces=meshFaces(packet,m,cutaway),all=meshFaces(packet,m,false).flatMap(f=>f.pts.map(project));
 if(!all.length)return pixels;const minx=all.reduce((v,p)=>Math.min(v,p[0]),Infinity),maxx=all.reduce((v,p)=>Math.max(v,p[0]),-Infinity),miny=all.reduce((v,p)=>Math.min(v,p[1]),Infinity),maxy=all.reduce((v,p)=>Math.max(v,p[1]),-Infinity);
 const scale=Math.min((width-40)/(maxx-minx),(height-64)/(maxy-miny)),ox=(width-(maxx+minx)*scale)/2,oy=(height-(maxy+miny)*scale)/2-5;
 function triangle(a,b,c,rgb){
  const area=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);if(Math.abs(area)<1e-8)return;
  const x0=Math.max(0,Math.floor(Math.min(a[0],b[0],c[0]))),x1=Math.min(width-1,Math.ceil(Math.max(a[0],b[0],c[0]))),y0=Math.max(0,Math.floor(Math.min(a[1],b[1],c[1]))),y1=Math.min(height-1,Math.ceil(Math.max(a[1],b[1],c[1])));
  for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){
   const px=x+.5,py=y+.5,u=((b[0]-px)*(c[1]-py)-(b[1]-py)*(c[0]-px))/area,v=((c[0]-px)*(a[1]-py)-(c[1]-py)*(a[0]-px))/area,w=1-u-v;
   if(u<-.000001||v<-.000001||w<-.000001)continue;const z=u*a[2]+v*b[2]+w*c[2],i=y*width+x;
   if(z>=depth[i]){depth[i]=z;const j=i*4;pixels[j]=rgb[0];pixels[j+1]=rgb[1];pixels[j+2]=rgb[2];pixels[j+3]=255;}
  }
 }
 faces.forEach(f=>{const p=f.pts.map(project).map(p=>[ox+p[0]*scale,oy+p[1]*scale,p[2]]),rgb=f.color.slice(1).match(/../g).map(v=>parseInt(v,16));for(let i=1;i<p.length-1;i++)triangle(p[0],p[i],p[i+1],rgb);});
 return pixels;
}
return {raster,meshFaces};
});
