'use strict';
const assert=require('node:assert/strict'),S=require('../dist/cassette/system.js'),D=require('../dist/cassette/development.js'),A=require('../dist/cassette/inspection.js');
const overlap=(a,b)=>a.bounds[0].every((v,k)=>Math.min(a.bounds[1][k],b.bounds[1][k])-Math.max(v,b.bounds[0][k])>1e-7);
for(const kind of ['door','window']){
 const d=D.opening(kind),frame=d.models[0];
 assert.equal(d.capacity,null);assert.equal(d.fasteners,null);assert(!d.manufacturingRelease);
 const voidBox=S.box('void',[90,-12,d.aperture.sill],[1020,207,d.aperture.height]);
 assert(frame.assets.every(a=>!overlap(a,voidBox)),'The aperture must contain no structural material');
 for(let i=0;i<frame.assets.length;i++)for(let j=i+1;j<frame.assets.length;j++)assert(!overlap(frame.assets[i],frame.assets[j]),'Framing must not double-count timber');
 assert.equal(d.items.length,kind==='door'?2:1);
 if(kind==='door')assert.equal(d.models[1].assets.filter(a=>a.id==='door-leaf-open').length,1);
}
for(const axis of [300,1500,2260,2286,2300,4200]){
 const d=D.partitionSupport({axis}),floor=d.models.filter(m=>m.id.startsWith('F'));
 assert(!d.manufacturingRelease);assert.equal(d.capacity,null);
 for(const m of floor){
  const wood=m.assets.filter(a=>a.material==='timber');
  for(let i=0;i<wood.length;i++)for(let j=i+1;j<wood.length;j++)assert(!overlap(wood[i],wood[j]),'Backing must not overlap existing joists/blocking');
  // Sample every mm across the sole footprint, at every cavity and seam.
  for(let x=axis-45+.5;x<axis+45;x++)for(const y of [20,100,300,540,580])assert(wood.some(a=>a.bounds[0][0]<=x&&a.bounds[1][0]>=x&&a.bounds[0][1]<=y&&a.bounds[1][1]>=y&&a.bounds[1][2]===220),'Continuous support below the partition sole');
 }
}
const source=S.generate({connectionRevision:'revised'});
for(const e of A.catalogue(source).filter(e=>e.type==='Walls')){
 const before=JSON.stringify(e.model),m=D.wallConnectors(e.model),j=m.assets.filter(a=>a.id.startsWith('joint-study'));
 assert.equal(j.length,4);assert(j.every(a=>a.capacity===null&&a.fasteners===null&&a.explode.some(x=>x)));
 assert.equal(JSON.stringify(e.model),before);
 assert.deepEqual(m.assets.slice(0,e.model.assets.length),e.model.assets);
 for(const joint of j)for(const part of e.model.assets){
  // Axis-aligned legs are separate volumes within a single hardware asset.
  for(let k=0;k<16;k+=8){const vs=joint.vertices.slice(k,k+8),b={bounds:[0,1].map(n=>[0,1,2].map(c=>Math[n?'max':'min'](...vs.map(v=>v[c]))))};assert(!overlap(b,part),'Angle envelope must not penetrate timber or skin');}
 }
}
console.log('PASS: physical apertures and door joinery, nonoverlapping partition backing at six off-grid/on-grid axes, four rigid angle studies at real wall contacts');
