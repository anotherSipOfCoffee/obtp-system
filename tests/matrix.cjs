const assert=require('node:assert/strict');
const base=require('../dist/cassette/system.js'),matrix=require('../dist/cassette/matrix.js');

function inspect(columns,rows,area,instances){
 const scene=matrix.generate({columns,rows}),ids=new Set(scene.allItems.map(i=>i.id));
 assert.equal(scene.allItems.length,instances);assert.equal(ids.size,instances);
 assert.equal(scene.clear[0],columns*600);assert.equal(scene.clear[1],rows*600);
 assert.equal(((scene.clear[0]+414)*(scene.clear[1]+414))/1e6,area);
 assert(scene.allJoints.every(j=>ids.has(j.a)&&ids.has(j.b)&&j.capacity===null&&j.fasteners===null));
 const parts=[],models=new Map(scene.models.map(m=>[m.id,m]));
 for(const item of scene.allItems)for(const part of models.get(item.block).assets){
  const bounds=base.worldBounds(item,part);assert(bounds.flat().every(Number.isFinite));
  assert(bounds[1].every((v,k)=>v>bounds[0][k]));parts.push({id:item.id+'/'+part.id,bounds});
  if(part.material==='plywood'&&part.id==='deck')assert(part.dimensions[0]<=2400&&part.dimensions[1]<=1200);
 }
 for(let a=0;a<parts.length;a++)for(let b=a+1;b<parts.length;b++){
  const A=parts[a].bounds,B=parts[b].bounds;
  assert(![0,1,2].every(k=>Math.min(A[1][k],B[1][k])-Math.max(A[0][k],B[0][k])>1e-6),'Nominal clash '+parts[a].id+' / '+parts[b].id);
 }
 for(const layer of ['floor','walls','roof']){
  const filtered=matrix.generate({columns,rows,layer,skin:false});
  assert(filtered.models.every(m=>m.assets.every(p=>p.material!=='plywood')));
  assert(filtered.items.every(i=>ids.has(i.id)));
  assert(filtered.joints.every(j=>filtered.items.some(i=>i.id===j.a)&&filtered.items.some(i=>i.id===j.b)));
 }
 return scene;
}
inspect(1,1,1.028196,26);
inspect(4,4,7.918596,64);
const large=inspect(8,12,39.699396,156);
assert.equal(large.allItems.filter(i=>i.id.startsWith('floor-core-')).length,12);
assert.equal(large.allItems.filter(i=>i.id.startsWith('corner-')).length,4);
inspect(8,15,49.084596,182);
assert.throws(()=>matrix.generate({columns:9}),/columns/);
assert.throws(()=>matrix.generate({rows:19}),/rows/);
console.log('PASS: Matrix nominal grid, parts, corners, staged joints and clash checks; capacities remain on hold');
