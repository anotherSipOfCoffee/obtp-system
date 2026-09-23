'use strict';
(()=>{const $=id=>document.getElementById(id),api=OBTPCassette;let renderer,scene;
for(let n=1;n<=8;n++)$('bays').add(new Option(n+' · '+(n*.6).toFixed(1)+' m',n));$('bays').value='4';
for(const [k,v] of Object.entries(api.connectionTypes))if(k!=='panel-frame')$('joint').add(new Option(v.name,k));
try{renderer=new SourceMeshView($('diagram'));}catch(e){$('status').textContent=e.message;return;}
function render(){try{
scene=api.generate({bays:Number($('bays').value),height:Number($('height').value),layer:$('layer').value,skin:$('skin').checked});
// Models vary with height and panel visibility; clear GPU buffers before replacement.
for(const m of renderer.meshes.values())for(const p of m.parts)renderer.gl.deleteBuffer(p.buffer);renderer.meshes.clear();
scene.models.forEach(m=>renderer.register(m));
const old=$('object').value;$('object').replaceChildren();for(const m of scene.models)$('object').add(new Option(m.id,m.id));if(scene.models.some(m=>m.id===old))$('object').value=old;
const mode=$('mode').value;$('object-controls').hidden=mode!=='object';$('joint-controls').hidden=mode!=='connection';let items=scene.items;
$('title').textContent='Rectangular studio · '+scene.bays+' modules';
$('detail').textContent='Proposed geometry, not a construction release. Joist spans, racking, fasteners, uplift and foundations require engineering. End walls close the frame; openings and weatherproof closure are unresolved.';
if(mode==='object'){
 items=[{block:$('object').value,translation:[0,0,0],rotation:[1,0,0,0,1,0,0,0,1]}];$('title').textContent=$('object').value+' · cassette';
 $('detail').textContent='Timber ribs with supported CNC plywood panels. Nominal part geometry only: sheet gaps, measured stock thickness, fastener holes and machining allowances are not released.';
}else if(mode==='connection'){
 const type=$('joint').value,j=scene.allJoints.find(j=>j.type===type),d=api.connectionTypes[type];items=scene.allItems.filter(i=>[j.a,j.b].includes(i.id)).map(i=>({...i,highlight:i.id===j.b}));
 $('title').textContent=d.name;$('detail').textContent=d.principle+'. '+d.release+'. Source: '+d.source+'. Violet highlights the mating cassette; contact does not prove resistance.';
}
renderer.setScene(items,{explode:Number($('explode').value)/100});
$('dimensions').textContent=scene.length.toLocaleString('en')+' × 4,572 mm frame setting-out · '+scene.height.toLocaleString('en')+' mm wall height';
$('status').textContent=items.length+' cassette instances · geometry ready';$('module-count').textContent=items.length;$('joint-count').textContent=scene.joints.length;
$('schedule').replaceChildren();for(const r of api.schedule({items})){const tr=document.createElement('tr');for(const v of [r.id,r.count,'Proposed']){const td=document.createElement('td');td.textContent=v;tr.append(td);}$('schedule').append(tr);}
window.OBTPCassetteView={scene,items,renderer};
}catch(e){$('status').textContent=e.message;throw e;}}
for(const id of ['bays','height','layer','mode','object','joint','skin'])$(id).onchange=render;
$('explode').oninput=()=>{$('amount').textContent=$('explode').value+'%';renderer.explode=Number($('explode').value)/100;renderer.draw();};
$('reset').onclick=()=>{$('explode').value=0;$('amount').textContent='0%';renderer.explode=0;renderer.reset();};
$('export').onclick=()=>{
 const full=api.generate({bays:scene.bays,height:scene.height}),parts=[];
 for(const item of full.items)for(const a of full.models.find(m=>m.id===item.block).assets)parts.push({id:item.id+'/'+a.id,material:a.material,corners:a.vertices.map(v=>api.transform(item,v))});
 const data={schema:'obtp-cassette-boxes/1',units:'mm',system:api.spec.id,revision:1,bays:scene.bays,height:scene.height,status:api.spec.status,manufacturingRelease:false,parts,interfaces:full.joints};
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='OBTP-Cassette-01-'+scene.bays+'-modules.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};render();})();
