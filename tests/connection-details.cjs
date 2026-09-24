const assert=require('node:assert/strict'),api=require('../dist/cassette/details/detail.js');
const expected={'wall-seam':[35,35,10,true],'floor-seam':[35,35,10,true],'roof-seam':[35,35,10,true],corner:[35,35,160,false],'wall-floor':[57,57,163,false],'wall-roof':[75,60,145,false]};
for(const [key,values]of Object.entries(expected)){
 const d=api.probe(key);assert.deepEqual([d.receiverPenetration,d.receiverThreadEnvelopeOverlap,d.tipCover,d.screenPass],values,key);
 assert.equal(d.capacity,null);assert.equal(d.fasteningSchedule,null);assert.equal(d.manufacturingRelease,false);
 assert.equal(d.checks[0].interval[0],0);assert.equal(d.checks[0].interval[1],45);
 for(const cutaway of [false,true]){const s=api.geometry(key,{cutaway});assert.deepEqual(s.detail,d,'view must not change measured geometry');for(const m of s.models)for(const a of m.assets){assert(a.vertices.flat().every(Number.isFinite));assert(a.bounds[1].every((v,k)=>v>a.bounds[0][k]));assert(a.faces.flat().every(i=>i>=0&&i<a.vertices.length));}}
}
assert.equal(api.probe('wall-floor').checks[1].interval[0],63,'deck must not be counted as structural rim embedment');
assert.throws(()=>api.probe('invented'));
// A shorter screw must reduce overlap; this guards against fixed displayed numbers.
const p=api.products.HBS580,original=p.length;p.length=70;assert.equal(api.probe('wall-seam').receiverPenetration,25);p.length=original;
console.log('PASS: six source-member probes, independent penetration expectations, interleaf exclusion, rejected narrow-edge positions, view-invariant checks and finite envelope meshes. No resistance tested.');
