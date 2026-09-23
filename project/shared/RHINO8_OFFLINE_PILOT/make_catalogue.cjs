// Development-time generator; source foundation is the sibling working checkpoint.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const E=require('../geometry_infrastructure_v01/src/geometry-engine.js'),P=require('../geometry_infrastructure_v01/src/profile.js');
const prototypes=new Map(),variants=[],round=n=>Math.round(n*1e8)/1e8;
for(const bedrooms of [3,4]){
 const config={bedrooms,workspace:true,length:'auto',arrangement:0,kitchen:'open',work:'switchable',slider:'closed',palette:'olive'};
 const result=E.createEngine(P).generate(config);if(result.status!=='supported')throw Error(result.message);const d=result.definition,instances=[];
 for(const c of d.components){
  const g=c.geometry;let origin,local;
  if(g.type==='box'){origin=[g.x,g.y,g.z];local={...g,x:0,y:0,z:0};}
  else{origin=[0,1,2].map(i=>Math.min(...g.vertices.map(v=>v[i])));local={type:'polygon',vertices:g.vertices.map(v=>v.map((n,i)=>round(n-origin[i])))};}
  const id='asset-'+crypto.createHash('sha256').update(E.canonical(local)).digest('hex').slice(0,16);
  if(!prototypes.has(id))prototypes.set(id,{id,kind:c.kind,material:c.material,geometry:local});
  instances.push({id:c.id,assetId:id,kind:c.kind,material:c.material,translation:origin.map(round)});
 }
 variants.push({id:'house-'+d.envelope.length,name:bedrooms+' bedrooms / '+d.envelope.length+' m',envelope:d.envelope,palette:d.palette,configuration:d.configuration,instances});
}
const request={schema:'obtp-gh-input/1',units:'m',scriptVersion:'obtp-gh-0.1.0',requestKey:'offline-component-pilot-v1',components:[...prototypes.values()],variants};
fs.writeFileSync(path.join(__dirname,'examples/reference.request.json'),JSON.stringify(request,null,2));
const uses=new Map();for(const v of variants)for(const i of v.instances){if(!uses.has(i.assetId))uses.set(i.assetId,new Set());uses.get(i.assetId).add(v.id);}
const report={assets:prototypes.size,instances:variants.map(v=>({variant:v.id,count:v.instances.length})),assetsUsedInBoth:[...uses.values()].filter(x=>x.size===2).length,scope:'Exact local shape reuse; translation only; no arbitrary mesh stretching. Dimensions remain provisional.',rhinoExecuted:false};
fs.writeFileSync(path.join(__dirname,'examples/catalogue-report.json'),JSON.stringify(report,null,2));console.log(report);
