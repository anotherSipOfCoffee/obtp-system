'use strict';
/* Original analytical envelopes, not manufacturer CAD or machining geometry. */
(function(root){
 const api=typeof module==='undefined'?root.OBTPCassette:require('../system.js');
 const source={url:'https://www.rothoblaas.com/attachments/288905-product-241/hbs-en-technical-data-sheet.pdf',pages:'Printed 32–34 (PDF 3–5)',reviewed:'2026-09-24'};
 const products={HBS580:{code:'HBS580',diameter:5,length:80,threadLength:40,headDiameter:10,headThickness:3.1,shankDiameter:3.65},HBS5120:{code:'HBS5120',diameter:5,length:120,threadLength:60,headDiameter:10,headThickness:3.1,shankDiameter:3.65}};
 const cases={
  'wall-seam':{name:'Adjacent wall cassettes',product:'HBS580',head:[97.5,555,1288],axis:[0,1,0],members:[['west-0','left-stud',2],['west-1','right-stud',2]],reason:'Access through the open cavity. This single screw tests a position, not a complete seam or spacing schedule.'},
  'floor-seam':{name:'Adjacent floor cassettes',product:'HBS580',head:[2286,555,110],axis:[0,1,0],members:[['floor-0','edge-b',0],['floor-1','edge-a',0]],reason:'Fasten the paired edge joists before closing access. Deck seam, diaphragm chord and group design remain separate.'},
  'roof-seam':{name:'Adjacent roof cassettes',product:'HBS580',head:[2286,555,2448],axis:[0,1,0],members:[['roof-0','edge-b',0],['roof-1','edge-a',0]],reason:'Same nominal joist seam as the floor. Roof uplift and diaphragm forces still need separate design.'},
  'corner':{name:'Wall corner return',product:'HBS580',head:[240,22.5,1288],axis:[-1,0,0],members:[['front-0','left-stud',2],['west-0','right-stud',2]],reason:'Rejected for the displayed reversible cross-grain shear screen. Revise the receiving corner member or choose a differently assessed detail; do not force this screw pattern into the 45 mm face.'},
  'wall-floor':{name:'Wall bottom plate to floor rim',product:'HBS5120',head:[22.5,300,283],axis:[0,0,-1],members:[['west-0','bottom-plate',1],['floor-0','blocking-0',1]],interleaf:['floor-0','ply-0'],reason:'The 18 mm deck lies between plate and rim. Rejected for the displayed reversible cross-grain shear screen; a dedicated hold-down to the supports remains unresolved.'},
  'wall-roof':{name:'Wall top plate to roof rim',product:'HBS5120',head:[22.5,300,2293],axis:[0,0,1],members:[['west-0','top-plate',1],['roof-0','blocking-0',1]],reason:'Candidate driven upward through the plate before lining. Rejected for the displayed reversible cross-grain shear screen; neither uplift resistance nor overhead installation access is validated.'}
 };
 function part(scene,itemId,assetId,grain){
  const item=scene.allItems.find(i=>i.id===itemId),asset=scene.models.find(m=>m.id===item.block).assets.find(a=>a.id===assetId);
  return {id:itemId+'/'+assetId,bounds:api.worldBounds(item,asset),grain,material:asset.material};
 }
 function interval(bounds,p,d){
  let lo=-Infinity,hi=Infinity;
  for(let k=0;k<3;k++)if(d[k]){const a=(bounds[0][k]-p[k])/d[k],b=(bounds[1][k]-p[k])/d[k];lo=Math.max(lo,Math.min(a,b));hi=Math.min(hi,Math.max(a,b));}else if(p[k]<bounds[0][k]||p[k]>bounds[1][k])return null;
  return hi>=lo?[lo===0?0:lo,hi===0?0:hi]:null;
 }
 function probe(key){
  const c=cases[key];if(!c)throw Error('Unknown connection detail');
  const scene=api.generate({bays:2,height:2100,skin:true}),product=products[c.product],members=c.members.map(a=>part(scene,...a));
  const driveAxis=c.axis.findIndex(v=>v!==0),threadStart=product.length-product.threadLength;
  const checks=members.map(m=>{
   const hit=interval(m.bounds,c.head,c.axis);if(!hit)throw Error('Fastener misses '+m.id);
   const cross=[0,1,2].find(k=>k!==driveAxis&&k!==m.grain);
   const endDistance=Math.min(c.head[m.grain]-m.bounds[0][m.grain],m.bounds[1][m.grain]-c.head[m.grain]);
   const edgeDistance=Math.min(c.head[cross]-m.bounds[0][cross],m.bounds[1][cross]-c.head[cross]);
   // Explicit limited screen: pre-drilled, rho_k <=420, 0/90-degree reversible shear.
   // Apply the more restrictive loaded distance at each end/edge under reversal.
   const requiredEnd=12*product.diameter,requiredEdge=7*product.diameter;
   return {id:m.id,interval:hit,endDistance,edgeDistance,requiredEnd,requiredEdge,screenPass:endDistance>=requiredEnd&&edgeDistance>=requiredEdge,
    penetration:Math.max(0,Math.min(hit[1],product.length)-Math.max(hit[0],0)),threadEnvelopeOverlap:Math.max(0,Math.min(hit[1],product.length)-Math.max(hit[0],threadStart))};
  });
  const receiver=checks[1];
  return {key,...c,product,members,interleafPart:c.interleaf?part(scene,...c.interleaf):null,checks,
   receiverPenetration:receiver.penetration,receiverThreadEnvelopeOverlap:receiver.threadEnvelopeOverlap,tipCover:receiver.interval[1]-product.length,
   screenPass:checks.every(c=>c.screenPass),capacity:null,fasteningSchedule:null,manufacturingRelease:false,source,
   conditions:'Conditional distance screen only: pre-drilled solid softwood with characteristic density ≤420 kg/m³; assumed member grain directions; reversible shear at 0° and 90°. Stock and actual loads are not specified. Axial/group/fire/moisture checks are not included.'};
 }
 function roundPart(id,profile,p,axis){
  const k=axis.findIndex(v=>v),u=(k+1)%3,v=(k+2)%3,vertices=[],faces=[],n=32;
  for(const [t,r]of profile)for(let j=0;j<n;j++){const q=p.slice();q[k]+=axis[k]*t;q[u]+=r*Math.cos(j*2*Math.PI/n);q[v]+=r*Math.sin(j*2*Math.PI/n);vertices.push(q);}
  for(let i=0;i<profile.length-1;i++)for(let j=0;j<n;j++){const a=i*n+j,b=i*n+(j+1)%n,c=b+n,d=a+n;faces.push([a,b,c],[a,c,d]);}
  for(const ring of [0,profile.length-1]){const q=p.slice();q[k]+=axis[k]*profile[ring][0];const center=vertices.length;vertices.push(q);for(let j=0;j<n;j++)faces.push([center,ring*n+j,ring*n+(j+1)%n]);}
  const bounds=[0,1].map(b=>[0,1,2].map(k=>Math[b?'max':'min'](...vertices.map(v=>v[k]))));return {id,vertices,faces,bounds,material:'fastener-envelope'};
 }
 function geometry(key,{cutaway=true}={}){
  const detail=probe(key),p=detail.product,models=[],items=[],crop=[detail.head.map(v=>v-130),detail.head.map(v=>v+130)];
  const driveAxis=detail.axis.findIndex(v=>v),cutAxis=[0,1,2].find(k=>k!==driveAxis);
  for(const [i,m] of [...detail.members,...(detail.interleafPart?[detail.interleafPart]:[])].entries()){
   const lo=m.bounds[0].map((v,k)=>Math.max(v,crop[0][k])),hi=m.bounds[1].map((v,k)=>Math.min(v,crop[1][k]));
   // Retain the far half: the default camera sees the negative X/Y faces.
   if(cutaway)lo[cutAxis]=Math.max(lo[cutAxis],detail.head[cutAxis]);
   if(hi.some((v,k)=>v<=lo[k]))continue;
   const id='detail-member-'+i;models.push(api.model(id,[api.box(m.id,lo,hi.map((v,k)=>v-lo[k]),m.material)]));items.push({block:id,translation:[0,0,0],explode:detail.axis.map(v=>v*(i===0?-45:45))});
  }
  const A=p.length-p.threadLength;
  const screw=api.model('detail-screw',[
   roundPart('head-envelope',[[0,p.headDiameter/2],[p.headThickness,p.shankDiameter/2]],detail.head,detail.axis),
   roundPart('shank-envelope',[[p.headThickness,p.shankDiameter/2],[A,p.shankDiameter/2]],detail.head,detail.axis),
   roundPart('thread-envelope',[[A,p.diameter/2],[p.length,p.diameter/2]],detail.head,detail.axis)
  ]);models.push(screw);items.push({block:screw.id,translation:[0,0,0],highlight:true});
  return {detail,models,items};
 }
 const result={source,products,cases,probe,geometry,interval};if(typeof module!=='undefined')module.exports=result;root.OBTPConnectionDetails=result;
})(typeof window==='undefined'?globalThis:window);
