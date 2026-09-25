'use strict';
const assert=require('node:assert/strict');
const S=require('../dist/cassette/system.js');
for(const bays of [1,4,8,18]){
 const bare=S.generate({bays,connectionRevision:'revised'});
 const supported=S.generate({bays,connectionRevision:'revised',includeFoundation:true});
 const f=supported.models.find(m=>m.id.startsWith('FOUNDATION-STRIP'));
 assert(f&&f.assets.length===2);
 assert.equal(supported.foundation.spacing,4572);
 assert.equal(supported.allJoints.filter(j=>j.type==='floor-support').length,bays);
 assert(supported.allJoints.filter(j=>j.type==='floor-support').every(j=>j.capacity===null&&j.fasteners===null));
 assert.equal(supported.allItems.filter(i=>i.stage==='foundation').length,1);
 const a=S.woodVolume(bare),b=S.woodVolume(supported);
 assert(Math.abs(a.total-b.total)<1e-10);
 assert(a.timber>0&&a.plywood>0);
 assert(S.woodVolume(S.generate({bays,connectionRevision:'revised',skin:true})).total>S.woodVolume(S.generate({bays,connectionRevision:'revised',skin:false})).total);
}
const o=S.openingStudy();
assert.equal(o.aperture.width,1020);
assert.equal(o.model.assets.length,6);
assert(!S.generate({}).models.some(m=>m.id===o.model.id));
console.log('PASS: optional bearing lines, null-capacity support interface, measured wood solids and detached window study');
