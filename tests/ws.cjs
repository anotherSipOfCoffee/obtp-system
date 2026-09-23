const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.join(__dirname,'..'),m=JSON.parse(fs.readFileSync(path.join(root,'dist/ws/model.json'))),audit=JSON.parse(fs.readFileSync(path.join(root,'docs/WS_GEOMETRY_AUDIT.json')));
assert.equal(m.schema,'obtp-source-mesh/1');assert.equal(m.units,'mm');assert.equal(m.assets.length,7);assert.equal(new Set(m.assets.map(a=>a.id)).size,7);
assert.equal(m.source.git_blob_sha,'932338ca81fdc2acdd345cd0fc9df09d2a9888b2');
for(const a of m.assets){assert(a.vertices.length>0);for(const v of a.vertices)assert(v.length===3&&v.every(Number.isFinite));for(const f of a.faces)assert(f.length===3&&f.every(i=>Number.isInteger(i)&&i>=0&&i<a.vertices.length));const row=audit.parts.find(p=>p.id===a.id);assert(row.valid&&row.solid);assert(row.bounds_delta_mm<.01);assert(row.coordinate_rounding_max_mm<=.00000051);}
assert.equal(m.assemblies[0].instances.length,7);assert.equal(audit.instance_transform[2][2],-1);
console.log('PASS: source identity, seven unique parts, valid indices and finite vertices, reflection, sub-0.01 mm topology-bound comparison. Browser and Rhino execution are separate checks.');
