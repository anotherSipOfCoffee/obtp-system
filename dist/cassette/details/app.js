'use strict';
(()=>{const $=id=>document.getElementById(id),api=OBTPConnectionDetails;let renderer,scene;
for(const [key,c]of Object.entries(api.cases))$('joint').add(new Option(c.name,key));
const initial=new URLSearchParams(location.search).get('joint');if(api.cases[initial])$('joint').value=initial;
try{renderer=new SourceMeshView($('diagram'));}catch(e){$('status').textContent=e.message;return;}
function render(){
 scene=api.geometry($('joint').value,{cutaway:$('view').value==='cutaway',revision:$('revision').value});const d=scene.detail,p=d.product;
 for(const m of renderer.meshes.values())for(const part of m.parts)renderer.gl.deleteBuffer(part.buffer);renderer.meshes.clear();scene.models.forEach(m=>renderer.register(m));renderer.setScene(scene.items,{explode:Number($('explode').value)/100});
 $('title').textContent=d.name;$('product').textContent=(d.revision==='revised'?'Revised / ':'Original / ')+p.code+' · '+p.diameter+' × '+p.length+' mm · single-position study';
 $('status').textContent='Geometry ready · '+(d.screenPass?'selected distance screen passes conditionally':'selected distance screen fails');
 $('decision').className='note '+(d.screenPass?'conditional':'reject');$('decision').textContent=d.screenPass?'Candidate for further design. The displayed end/edge distances pass the stated conditional screen; strength and installation are not validated.':'Reject this position for the stated reversible shear screen. A member or connector-detail redesign is required before this candidate can advance.';
 $('metrics').replaceChildren();for(const [label,value]of [['Receiver penetration',d.receiverPenetration],['Thread-envelope overlap',d.receiverThreadEnvelopeOverlap],['Tip cover',d.tipCover]]){const div=document.createElement('div'),strong=document.createElement('strong'),small=document.createElement('small');strong.textContent=value+' mm';small.textContent=label;div.append(strong,small);$('metrics').append(div);}
 $('checks').replaceChildren();for(const c of d.checks){const tr=document.createElement('tr');for(const value of [c.id,c.endDistance+' / '+c.requiredEnd+' mm',c.edgeDistance+' / '+c.requiredEdge+' mm',c.screenPass?'Conditional pass':'Fail']){const td=document.createElement('td');td.textContent=value;tr.append(td);}$('checks').append(tr);}
 $('conditions').textContent=d.conditions;$('reason').textContent=d.reason;$('source').href=d.source.url;
 window.OBTPDetailView={scene,renderer};
}
for(const id of ['joint','view','revision'])$(id).onchange=render;
$('explode').oninput=()=>{$('amount').textContent=$('explode').value+'%';renderer.explode=Number($('explode').value)/100;renderer.draw();};
$('reset').onclick=()=>{$('explode').value=0;$('amount').textContent='0%';renderer.explode=0;renderer.reset();};
$('export').onclick=()=>{const data={schema:'obtp-connection-inspection/1',units:'mm',...scene.detail},url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='cassette-'+scene.detail.key+'-'+scene.detail.revision+'-inspection.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};render();})();
