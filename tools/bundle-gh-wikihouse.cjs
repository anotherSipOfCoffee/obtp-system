// Reproduce the GH-only source snapshot from the existing pinned System catalogue.
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),c=require(path.join(root,'dist/catalogue.js'));
const dest=path.join(root,'authoring/grasshopper/comparison_data');fs.mkdirSync(dest,{recursive:true});
const assemblies={};for(let n=1;n<=8;n++)for(const layer of ['floor','walls','roof','all'])assemblies[n+'/'+layer]=c.multiAssembly(n,layer);
const data={pin:c.pin,objects:c.parts,assemblies,connections:c.joints.map(j=>({id:j.id,name:j.name,rule:j.rule,evidence:j.evidence,items:j.scene()}))};
fs.writeFileSync(path.join(dest,'wikihouse.json.gz'),require('zlib').gzipSync(JSON.stringify(data)));
for(const p of c.parts)fs.copyFileSync(path.join(root,'dist/catalogue',p.id+'.json'),path.join(dest,p.id+'.json'));
fs.copyFileSync(path.join(root,'dist/catalogue/NOTICE.md'),path.join(dest,'WIKIHOUSE_NOTICE.md'));
