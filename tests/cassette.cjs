const assert=require('node:assert/strict'),fs=require('node:fs'),api=require('../dist/cassette/system.js');
const reports=[];
for(const bays of [1,2,3,4,5,6,7,8])for(const height of [2100,2700]){
 const s=api.generate({bays,height}),ids=new Set(s.items.map(i=>i.id)),parts=[];
 assert.equal(s.items.length,4*bays+14);assert.equal(ids.size,s.items.length);assert.equal(s.length,bays*600);assert.deepEqual(s.clear,[4182,bays*600-390,height]);
 for(const i of s.items){const m=s.models.find(m=>m.id===i.block);assert(m);for(const a of m.assets){const b=api.worldBounds(i,a);assert(b.flat().every(Number.isFinite));parts.push({id:i.id+'/'+a.id,b});if(a.material==='plywood'){const d=a.dimensions.filter(v=>v!==12&&v!==18).sort((a,b)=>a-b);assert(d[0]<=1220&&d[1]<=2440);}}}
 // Exact axis-aligned parts and orthogonal rotations: positive volume intersections are defects.
 let maxOverlap=0;
 for(let i=0;i<parts.length;i++)for(let j=i+1;j<parts.length;j++){
  const a=parts[i],b=parts[j],d=[0,1,2].map(k=>Math.min(a.b[1][k],b.b[1][k])-Math.max(a.b[0][k],b.b[0][k]));
  if(d.every(x=>x>1e-8)){maxOverlap=Math.max(maxOverlap,d.reduce((p,x)=>p*x,1));assert.fail('Overlap '+a.id+' / '+b.id+' '+d);}
 }
 for(const j of s.joints){assert(ids.has(j.a)&&ids.has(j.b));assert.equal(j.capacity,null);assert.equal(j.fasteners,null);assert(api.connectionTypes[j.type]);
  for(const id of [j.a,j.b]){const item=s.items.find(i=>i.id===id),m=s.models.find(m=>m.id===item.block);assert(m.assets.some(a=>{const b=api.worldBounds(item,a);return j.point.every((v,k)=>v>=b[0][k]-1e-8&&v<=b[1][k]+1e-8);}),j.id+' point misses physical part '+id);}
 }
 // Interface graph must connect every cassette, not just contain valid IDs.
 const reached=new Set([s.items[0].id]);let before;do{before=reached.size;for(const j of s.joints)if(reached.has(j.a)||reached.has(j.b)){reached.add(j.a);reached.add(j.b);}}while(before!==reached.size);assert.equal(reached.size,ids.size);
 for(const end of ['front','back']){const walls=s.items.filter(i=>i.id.startsWith(end+'-'));const spans=walls.map(i=>{const b=api.worldBounds(i,s.models.find(m=>m.id===i.block).assets.find(a=>a.id==='bottom-plate'));return[b[0][0],b[1][0]];}).sort((a,b)=>a[0]-b[0]);assert.equal(spans[0][0],195);assert.equal(spans.at(-1)[1],4377);for(let k=1;k<spans.length;k++)assert.equal(spans[k][0],spans[k-1][1]);}
 for(const layer of ['floor','walls','roof','all']){const l=api.generate({bays,height,layer,skin:false});assert(l.models.every(m=>m.assets.every(a=>a.material==='timber')));assert.equal(l.items.length,layer==='floor'?bays:layer==='walls'?3*bays+14:4*bays+14);}
 reports.push({bays,height,cassettes:s.items.length,parts:parts.length,interfaces:s.joints.length,positiveVolumeIntersections:maxOverlap,connected:true});
}
for(const bays of [0,9,1.5,NaN])assert.throws(()=>api.generate({bays}));assert.throws(()=>api.generate({height:2200}));assert.throws(()=>api.generate({layer:'unknown'}));
fs.writeFileSync('cassette-validation.json',JSON.stringify({scope:'Software geometry only. No structural, tolerance, moisture or assembly-access validation.',cases:reports},null,2));
console.log('PASS: 16 configurations, all stage counts, sheet envelopes, no positive-volume part collisions, continuous end-wall framing and connected interface graphs and interface points touching real parts on both sides.');
