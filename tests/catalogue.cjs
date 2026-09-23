const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');const root=path.join(__dirname,'..'),kit=require('../dist/catalogue.js');assert.equal(kit.parts.length,8);const packets=new Map();for(const p of kit.parts){const m=JSON.parse(fs.readFileSync(path.join(root,'dist/catalogue',p.id+'.json')));packets.set(p.id,m);assert.equal(m.units,'mm');assert.equal(m.source.commit,kit.pin);assert(m.assets.length);for(const a of m.assets){assert(a.vertices.every(p=>p.length===3&&p.every(Number.isFinite)));assert(a.faces.every(f=>f.length===3&&f.every(i=>Number.isInteger(i)&&i>=0&&i<a.vertices.length)));}}
for(const items of [...kit.joints.map(j=>j.scene()),kit.assembly()])for(const item of items){assert(packets.has(item.block));const r=item.rotation;for(let i=0;i<3;i++)for(let j=0;j<3;j++){let dot=0;for(let k=0;k<3;k++)dot+=r[i*3+k]*r[j*3+k];assert(Math.abs(dot-(i===j?1:0))<1e-8);}assert(item.translation.every(Number.isFinite));}
assert.deepEqual(kit.counts(kit.assembly()),[{id:'W-S',count:2},{id:'F-S',count:1},{id:'R-S',count:1},{id:'TIE-FULL',count:24}]);assert.equal(kit.assembly('floor').length,1);assert.equal(kit.assembly('walls').length,3);assert.equal(kit.assembly('roof').length,4);
const samples=JSON.parse(fs.readFileSync(path.join(root,'docs/BLOCK_INTERFACE_FIT_CHECK.json')));assert.equal(samples.length,48);assert(samples.every(s=>s.overlap_mm2<1&&s.material_section_area_mm2>1000));console.log('PASS eight source objects; finite geometry and valid indices; rigid-only placements; counts/stages; 48 sampled interface fits below 1 mm² overlap.');

for(const n of [1,2,4,8]){
 const items=kit.multiAssembly(n);assert.equal(items.length,52*n-24);
 assert.equal(new Set(items.map(p=>p.instanceId)).size,items.length);
 const c=Object.fromEntries(kit.counts(items).map(r=>[r.id,r.count]));
 assert.deepEqual(c,{'W-S':2*n,'F-S':n,'R-S':n,'TIE-FULL':48*n-24});
 for(const [layer,count] of [['floor',n],['walls',3*n],['roof',4*n]])assert.equal(kit.multiAssembly(n,layer).length,count);
 for(let bay=0;bay<n;bay++){const moved=items.filter(p=>p.instanceId.startsWith('bay-'+(bay+1)+'/'));for(const [i,p] of moved.entries()){const original=kit.assembly()[i];assert.equal(p.block,original.block);assert.deepEqual(p.rotation,original.rotation);assert(p.translation.every((v,k)=>Math.abs(v-(k===0?600*bay:0)-original.translation[k])<1e-8));}}
 for(const p of items)assert(p.translation.every(Number.isFinite));
}
for(const n of [0,9,1.5,NaN])assert.throws(()=>kit.multiAssembly(n));
const seams=kit.multiAssembly(2).filter(p=>p.instanceId.startsWith('seam-'));
assert.equal(seams.length,24);assert(seams.every(p=>p.translation[0]===600));
assert.deepEqual([...new Set(seams.map(p=>p.translation[1]))].sort((a,b)=>a-b),[0,186,4386,4572]);
console.log('PASS repeated rigid slices; unique IDs; shared wall-pair seam placement; counts; bounds on module control.');
