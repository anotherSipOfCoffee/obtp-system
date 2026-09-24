const assert=require('node:assert/strict'),S=require('../dist/cassette/system.js'),A=require('../dist/cassette/inspection.js');
for(const revision of ['baseline','revised'])for(const height of [2100,2700])for(const bays of [1,4,8]){
 const scene=S.generate({bays,height,connectionRevision:revision}),before=JSON.stringify(scene),entries=A.catalogue(scene);
 assert.equal(entries.reduce((n,e)=>n+e.instances.length,0),scene.allItems.length);
 assert.equal(new Set(entries.flatMap(e=>e.instances)).size,scene.allItems.length);
 for(const e of entries){
  const source=scene.models.find(m=>m.id===e.id);assert.deepEqual(e.model.assets.map(a=>a.vertices),source.assets.map(a=>a.vertices));
  assert(e.model.assets.every(a=>a.explode.some(v=>v!==0)));assert(new Set(e.model.assets.map(a=>a.explode.join(','))).size>=4);
  const frame=A.contacts(e.model,'frame-frame');assert.equal(frame.length,e.type==='Walls'?(height===2700?6:4):6);
  for(const c of [...frame,...A.contacts(e.model,'panel-frame')]){assert.equal(c.capacity,null);assert.equal(c.fasteners,null);assert.equal(A.contactScene(e.model,c).items.length,2);}
  if(e.type!=='Walls')for(const a of e.model.assets.filter(a=>a.id.startsWith('edge-')))assert.equal(a.dimensions[0],4572,'Long joist stays continuous');
 }
 assert.equal(JSON.stringify(scene),before,'Inspection cannot mutate source geometry');
 assert(A.instances(scene,'floor-seam').every(j=>j.a.startsWith('floor-')));assert(A.instances(scene,'roof-seam').every(j=>j.a.startsWith('roof-')));
 assert.equal(A.instances(scene,'floor-seam').length,bays-1);assert.equal(A.instances(scene,'roof-seam').length,bays-1);
 assert(A.register(scene).every(r=>r.capacity===null&&r.fasteners===null&&!r.manufacturingRelease));
}
for(const [id,c]of Object.entries(A.connectors)){
 const m=A.connectorModel(id);assert(Object.values(A.connections).some(d=>d.connectors.includes(id)));
 if(c.kind==='screw'||c.concept){assert.equal(m.assets.length,1,'One physical connector, not independently exploded head or angle legs');assert(m.assets[0].vertices.flat().every(Number.isFinite));assert.deepEqual(m.assets[0].explode,[0,0,0]);}
 else assert.equal(m,null,'Do not invent unselected hardware');
}
assert(A.relevant('floor-seam','Floors'));assert(!A.relevant('roof-seam','Floors'));assert(A.relevant('wall-floor','Connectors','HBS5120'));
console.log('PASS: constituent parts, continuous joists, 4/6 actual timber contacts, non-mutating explosion metadata, geometry-based catalogue grouping, distinct floor/roof seams and honest connector states.');
