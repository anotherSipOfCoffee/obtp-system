const assert=require('node:assert/strict'),api=require('../dist/cassette/system.js'),details=require('../dist/cassette/details/detail.js');
let count=0;
for(let bays=1;bays<=8;bays++)for(const height of [2100,2700]){
 const scene=api.generate({bays,height,connectionRevision:'revised'});
 function members(id){const i=scene.allItems.find(i=>i.id===id);return scene.models.find(m=>m.id===i.block).assets.map(a=>({id:a.id,bounds:api.worldBounds(i,a)}));}
 for(const j of scene.joints.filter(j=>['corner','wall-floor','wall-roof'].includes(j.type))){
  let head,axis,pair,grain;
  const side=j.a.startsWith('west')||j.a.startsWith('east');
  if(j.type==='corner'){
   const west=j.b.startsWith('west'),front=j.a.startsWith('front');
   head=[west?240:4332,front?45:scene.length-45,238+height/2];axis=[west?-1:1,0,0];grain=2;
   pair=[j.a,j.b].map(id=>members(id).filter(m=>m.id.endsWith('stud')).find(m=>{const h=details.interval(m.bounds,head,axis);return h&&h[1]>0;}));
  }else{
   const roof=j.type==='wall-roof';head=j.point.slice();head[side?0:1]=side?(j.a.startsWith('west')?45:4527):(j.a.startsWith('front')?45:scene.length-45);head[2]=roof?238+height-45:283;axis=[0,0,roof?1:-1];grain=side?1:0;
   pair=[members(j.a).find(m=>m.id===(roof?'top-plate':'bottom-plate')),members(j.b).find(m=>m.id===(side?(j.a.startsWith('west')?'blocking-0':'blocking-4527'):(j.a.startsWith('front')?'edge-a':'edge-b')))];
  }
  for(const m of pair){assert(m,j.id);const h=details.interval(m.bounds,head,axis);assert(h&&h[1]>h[0],j.id+' intersects timber');const drive=axis.findIndex(v=>v),cross=[0,1,2].find(k=>k!==drive&&k!==grain);const end=Math.min(head[grain]-m.bounds[0][grain],m.bounds[1][grain]-head[grain]);const edge=Math.min(head[cross]-m.bounds[0][cross],m.bounds[1][cross]-head[cross]);assert(end>=60,j.id+' end');assert(edge>=35,j.id+' edge');}
  const hit=details.interval(pair[1].bounds,head,axis),length=j.type==='corner'?80:120;
  assert.equal(Math.min(hit[1],length)-Math.max(hit[0],0),j.type==='corner'?35:j.type==='wall-floor'?57:75,j.id+' receiver penetration');count++;
 }
}
console.log('PASS: '+count+' revised corner/perimeter positions across all 16 assemblies; unchanged end/edge screen and expected timber penetration. No structural resistance assessed.');
