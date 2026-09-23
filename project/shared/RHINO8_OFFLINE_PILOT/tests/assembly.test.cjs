const assert=require('assert/strict'),fs=require('fs'),path=require('path');
const request=require('../examples/reference.request.json'),{assemble,validate}=require('../viewer/assemble');
// Explicit synthetic fixtures, solely to test placement and validation, not Rhino output.
const assets=request.components.map(c=>{const g=c.geometry;return {id:c.id,vertices:g.type==='box'?[[0,0,0],[g.width,0,0],[0,g.depth,g.height]]:g.vertices,faces:[[0,1,2]]};});
const kit={schema:'obtp-offline-kit/1',units:'m',producer:'RhinoCommon via Grasshopper',runtime:'TEST FIXTURE - NOT RHINO',scriptVersion:request.scriptVersion,requestKey:request.requestKey,assets,variants:request.variants};
for(const v of kit.variants){const a=assemble(kit,v.id);assert.equal(a.packet.objects.length,v.instances.length);for(let i=0;i<v.instances.length;i++){const inst=v.instances[i],asset=assets.find(x=>x.id===inst.assetId);assert.deepEqual(a.packet.objects[i].vertices[0],asset.vertices[0].map((n,j)=>n+inst.translation[j]));}}
for(const mutate of [k=>k.units='mm',k=>k.assets[0].faces[0][0]=999999,k=>k.variants[0].instances[0].assetId='missing',k=>k.assets.push(k.assets[0])]){const b=structuredClone(kit);mutate(b);assert.throws(()=>validate(b));}
const report={fixtureAssembly:'passed for both manifests',rejectionChecks:'units, indices, missing assets, duplicate IDs passed',rhinoExecution:'not performed',browserQA:'not performed'};
fs.writeFileSync(path.join(__dirname,'report.json'),JSON.stringify(report,null,2));console.log(report);
