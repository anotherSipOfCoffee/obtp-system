'use strict';
(()=>{const $=id=>document.getElementById(id),api=OBTPCassette;let renderer,scene;
for(let n=1;n<=8;n++)$('bays').add(new Option(n+' · '+(n*.6).toFixed(1)+' m',n));$('bays').value='4';
for(const [k,v] of Object.entries(OBTPConnections.details))$('joint').add(new Option(v.name,k));
try{renderer=new SourceMeshView($('diagram'));}catch(e){$('status').textContent=e.message;return;}
function render(){try{
scene=api.generate({bays:Number($('bays').value),height:Number($('height').value),layer:$('layer').value,skin:$('skin').checked});
// Models vary with height and panel visibility; clear GPU buffers before replacement.
for(const m of renderer.meshes.values())for(const p of m.parts)renderer.gl.deleteBuffer(p.buffer);renderer.meshes.clear();
scene.models.forEach(m=>renderer.register(m));
const old=$('object').value;$('object').replaceChildren();for(const m of scene.models)$('object').add(new Option(m.id,m.id));if(scene.models.some(m=>m.id===old))$('object').value=old;
const mode=$('mode').value;$('connection-record').hidden=mode!=='connection';$('object-controls').hidden=mode!=='object';$('joint-controls').hidden=mode!=='connection';let items=scene.items;
$('title').textContent='Rectangular studio · '+scene.bays+' modules';
$('detail').textContent='Proposed geometry, not a construction release. Joist spans, racking, fasteners, uplift and foundations require engineering. End walls close the frame; openings and weatherproof closure are unresolved.';
if(mode==='object'){
 items=[{block:$('object').value,translation:[0,0,0],rotation:[1,0,0,0,1,0,0,0,1]}];$('title').textContent=$('object').value+' · cassette';
 $('detail').textContent='Timber ribs with supported CNC plywood panels. Nominal part geometry only: sheet gaps, measured stock thickness, fastener holes and machining allowances are not released.';
}else if(mode==='connection'){
 const type=$('joint').value,d=OBTPConnections.details[type],study=OBTPConnections.build(type,api);
 const matches=scene.allJoints.filter(j=>j.type===type),context=$('joint-view').value==='context';
 if(context&&matches.length){const j=matches[0];items=scene.allItems.filter(i=>[j.a,j.b].includes(i.id)).map(i=>({...i,highlight:i.id===j.b}));}
 else {study.models.forEach(m=>renderer.register(m));items=study.items;}
 $('title').textContent=d.id+' · '+d.name;
 $('detail').textContent=d.principle+' HOLD: geometry study only; no selected product or fastening schedule. '+(context&&matches.length?'Showing the first matching interface.':study.geometryScope);
 const record=$('connection-record');record.replaceChildren();
 const para=(title,value)=>{const h=document.createElement('h3');h.textContent=title;const q=document.createElement('p');q.textContent=value;record.append(h,q);};
 para('Intended load path',d.loadPath.join(' · '));
 para('Assembly and access',d.access.join(' '));
 para('Failure modes to check',d.failureModes.join(' · '));
 para('Test before release',d.test);
 para('Evidence and adaptation',d.adaptation);
 const ul=document.createElement('ul');for(const id of d.sources){const r=OBTPConnections.sources[id],li=document.createElement('li'),a=document.createElement('a');a.href=r.url;a.textContent=id+' · '+r.citation;a.target='_blank';a.rel='noopener';li.append(a);ul.append(li);}record.append(ul);
 para('Existing screw-position checks','The measured HBS studies remain available through Inspect measured screw positions. Corner, wall–floor and wall–roof probes fail the existing conditional distance screen. These alternative concepts do not overturn those results.');
 para('Drawing status','Timber sections follow the nominal cassette concept. Violet plates are original study envelopes; amber volumes are fastener zones. Plate sizes and zones are not sourced product dimensions or installation instructions. No numeric clearance, spacing or capacity is approved.');
 if(context&&!matches.length)para('Context unavailable',type==='panel-frame'||type==='frame-frame'?'This is an internal cassette joint, shown as a local detail.':'There is no adjacent floor/roof cassette seam in a one-module assembly; showing the local study.');
 window.OBTPConnectionStudy=study;

}
if(scene.height===2700)$('detail').textContent+=' Narrow panels at this height are outside the width condition of simplified wall method A in the reviewed guidance; see connection research. No racking resistance is assigned.';
renderer.setScene(items,{explode:Number($('explode').value)/100});
$('dimensions').textContent=scene.length.toLocaleString('en')+' × 4,572 mm frame setting-out · '+scene.height.toLocaleString('en')+' mm wall height';
$('status').textContent=mode==='connection'&&items.some(i=>i.block.startsWith('detail-'))?items.length+' study envelopes · not construction hardware':items.length+' cassette instances · geometry ready';$('module-count').textContent=mode==='connection'&&($('joint-view').value==='detail'||!scene.allJoints.some(j=>j.type===$('joint').value))?'Local detail':items.length;$('joint-count').textContent=scene.joints.length;
$('schedule').replaceChildren();for(const r of (mode==='connection'&&items.some(i=>i.block.startsWith('detail-')||i.block.startsWith('TIE-zone-'))?window.OBTPConnectionStudy.parts.map(p=>({id:p.id,count:'Study envelope'})):api.schedule({items}))){const tr=document.createElement('tr');for(const v of [r.id,r.count,'Proposed']){const td=document.createElement('td');td.textContent=v;tr.append(td);}$('schedule').append(tr);}
window.OBTPCassetteView={scene,items,renderer};
}catch(e){$('status').textContent=e.message;throw e;}}
for(const id of ['bays','height','layer','mode','object','joint','joint-view','skin'])$(id).onchange=render;
$('explode').oninput=()=>{$('amount').textContent=$('explode').value+'%';renderer.explode=Number($('explode').value)/100;renderer.draw();};
$('reset').onclick=()=>{$('explode').value=0;$('amount').textContent='0%';renderer.explode=0;renderer.reset();};
$('export').onclick=()=>{
 const full=api.generate({bays:scene.bays,height:scene.height}),parts=[];
 for(const item of full.items)for(const a of full.models.find(m=>m.id===item.block).assets)parts.push({id:item.id+'/'+a.id,material:a.material,corners:a.vertices.map(v=>api.transform(item,v))});
 const data={schema:'obtp-cassette-boxes/1',units:'mm',system:api.spec.id,revision:api.spec.revision,bays:scene.bays,height:scene.height,status:api.spec.status,manufacturingRelease:false,parts,interfaces:full.joints,connectionResearch:OBTPConnections.coverage(full)};
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='OBTP-Cassette-01-'+scene.bays+'-modules.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
$('export-detail').onclick=()=>{
 const study=OBTPConnections.build($('joint').value,api),data={schema:'obtp-connection-study/1',...study,sources:Object.fromEntries(study.detail.sources.map(id=>[id,OBTPConnections.sources[id]]))};
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download=study.id+'-connection-study.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};render();})();
