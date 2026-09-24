const assert=require('node:assert/strict');
const api=require('../dist/cassette/system.js'),lib=require('../dist/cassette/connections.js');
const overlap=(a,b)=>a.bounds[0].map((v,k)=>Math.min(a.bounds[1][k],b.bounds[1][k])-Math.max(v,b.bounds[0][k])).every(v=>v>1e-8);
assert.equal(Object.keys(lib.details).length,7);
for(const type of Object.keys(lib.details)){
 const s=lib.build(type,api),d=s.detail;
 assert.equal(d.capacity,null);assert.equal(d.fasteners,null);assert.equal(d.product,null);assert.equal(d.stiffness,null);assert.equal(s.manufacturingRelease,false);
 assert(d.sources.every(id=>lib.sources[id]?.url.startsWith('https://doi.org/')));
 assert(s.parts.length&&s.zones.length);
 for(const a of s.parts){assert(a.bounds.flat().every(Number.isFinite));assert(a.dimensions.every(v=>v>0));}
 const solids=s.parts.filter(p=>p.material!=='fastener-zone');
 for(let i=0;i<solids.length;i++)for(let j=i+1;j<solids.length;j++)assert(!overlap(solids[i],solids[j]),s.id+' physical solids overlap: '+solids[i].id+' / '+solids[j].id);
 for(const z of s.parts.filter(p=>p.material==='fastener-zone'))assert(solids.some(p=>p.material==='timber'&&overlap(z,p)),s.id+' detached fastening zone');
}
for(let bays=1;bays<=8;bays++)for(const height of [2100,2700]){
 const s=api.generate({bays,height}),c=lib.coverage(s);
 assert.equal(c.interfaces.length,s.allJoints.length);assert(c.interfaces.every(j=>j.detailId&&!j.constructionReady&&j.placement==='not-designed'));
 assert.equal(c.manufacturingRelease,false);assert.equal(c.foundation,'not-designed');assert.deepEqual(c.internalDetailIds,['A01','A07']);
}
assert.throws(()=>lib.build('unknown',api));
console.log('PASS: seven original connection studies; finite geometry, no solid clashes, timber-intersecting fastening zones, evidence references and non-release status; coverage across 16 assemblies. Not a hardware, capacity, clearance or access test.');
