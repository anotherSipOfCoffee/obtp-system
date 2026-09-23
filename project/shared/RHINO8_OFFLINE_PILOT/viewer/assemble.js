(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.OBTPOffline=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const point=p=>Array.isArray(p)&&p.length===3&&p.every(n=>Number.isFinite(n)&&Math.abs(n)<1000);
function validate(kit){
 if(!kit||kit.schema!=='obtp-offline-kit/1'||kit.units!=='m'||kit.requestKey!=='offline-component-pilot-v1'||kit.scriptVersion!=='obtp-gh-0.1.0')throw Error('Unsupported kit version or units.');
 if(kit.producer!=='RhinoCommon via Grasshopper'||typeof kit.runtime!=='string'||!kit.runtime)throw Error('Missing Rhino/GH provenance.');
 if(!Array.isArray(kit.assets)||!kit.assets.length||kit.assets.length>2000||!Array.isArray(kit.variants)||kit.variants.length!==2)throw Error('Invalid pilot catalogue.');
 const ids=new Set();let vertices=0,faces=0;
 for(const a of kit.assets){if(!a||typeof a.id!=='string'||ids.has(a.id)||!Array.isArray(a.vertices)||!a.vertices.length||!Array.isArray(a.faces)||!a.faces.length)throw Error('Invalid or duplicate asset.');ids.add(a.id);
  vertices+=a.vertices.length;faces+=a.faces.length;if(vertices>200000||faces>300000)throw Error('Pilot mesh budget exceeded.');
  if(!a.vertices.every(point)||!a.faces.every(f=>Array.isArray(f)&&f.length===3&&f.every(i=>Number.isInteger(i)&&i>=0&&i<a.vertices.length)))throw Error('Invalid mesh coordinates or indices.');
 }
 const variants=new Set();for(const v of kit.variants){
  if(!v||typeof v.id!=='string'||variants.has(v.id)||![15,18].includes(v.envelope?.length)||v.envelope.width!==7.2||!Array.isArray(v.instances)||!v.instances.length||v.instances.length>2000)throw Error('Invalid variant manifest.');variants.add(v.id);
  if(!v.palette||!['wall','frame','post','roof','wood'].every(k=>/^#[0-9a-f]{6}$/i.test(v.palette[k])))throw Error('Invalid material palette.');
  const seen=new Set();for(const i of v.instances){if(!i||typeof i.id!=='string'||seen.has(i.id)||!ids.has(i.assetId)||!point(i.translation)||typeof i.kind!=='string'||typeof i.material!=='string')throw Error('Invalid component instance.');seen.add(i.id);}
 }
 return kit;
}
function assemble(kit,id){
 validate(kit);const v=kit.variants.find(v=>v.id===id);if(!v)throw Error('Unknown variant.');const assets=new Map(kit.assets.map(a=>[a.id,a]));
 const objects=v.instances.map(i=>{const a=assets.get(i.assetId);return {id:i.id,kind:i.kind,material:i.material,vertices:a.vertices.map(p=>p.map((n,j)=>n+i.translation[j])),faces:a.faces};});
 return {packet:{objects},model:{L:v.envelope.length,W:v.envelope.width,palette:v.palette},variant:v};
}
return {validate,assemble};
});
