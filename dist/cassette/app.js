'use strict';
(()=>{
 const $=id=>document.getElementById(id),S=OBTPCassette,C=OBTPConnections,D=OBTPConnectionDetails,A=OBTPInspection;
 let renderer,scene,catalogue=[],selected='',type='Walls',mode='assembly',part='',connector='HBS580',joint='wall-seam',kind='measured',occurrence='',exportDetail=null;
 const option=(value,name)=>new Option(name,value);
 const button=(name,attr,value,active)=>{const b=document.createElement('button');b.textContent=name;b.dataset[attr]=value;b.setAttribute('aria-pressed',String(active));return b;};
 function options(el,values,current){el.replaceChildren(...values.map(v=>option(v.id,v.name)));if(values.some(v=>v.id===current))el.value=current;return el.value;}
 function text(tag,value){const e=document.createElement(tag);e.textContent=value;return e;}
 function para(parent,title,value){parent.append(text('h3',title),text('p',value));}
 function link(parent,name,url){const a=document.createElement('a');a.textContent=name;a.href=url;if(/^https:/.test(url)){a.target='_blank';a.rel='noopener';}parent.append(a);return a;}
 function table(parent,head,rows){const t=document.createElement('table'),h=document.createElement('thead'),tr=document.createElement('tr');head.forEach(v=>tr.append(text('th',v)));h.append(tr);t.append(h);const b=document.createElement('tbody');for(const row of rows){const tr=document.createElement('tr');row.forEach(v=>tr.append(text('td',String(v))));b.append(tr);}t.append(b);parent.append(t);return t;}
 function showModels(models,items,settings={}){for(const m of renderer.meshes.values())for(const p of m.parts)renderer.gl.deleteBuffer(p.buffer);renderer.meshes.clear();models.forEach(m=>renderer.register(m));renderer.setScene(items,{explode:Number($('explode').value)/100,...settings});return items;}
 function resetExplosion(){part='';occurrence='';$('explode').value='0';$('amount').textContent='0%';renderer.reset();}
 for(let n=1;n<=8;n++)$('bays').add(option(n,n+' · '+(n*.6).toFixed(1)+' m'));$('bays').value='4';
 try{renderer=new SourceMeshView($('diagram'));}catch(e){$('status').textContent=e.message;return;}
 function render(){try{
  scene=S.generate({bays:Number($('bays').value),height:Number($('height').value),layer:$('layer').value,skin:true,connectionRevision:$('revision').value});catalogue=A.catalogue(scene);
  let obj=catalogue.find(e=>e.id===selected)||catalogue.find(e=>e.type===type)||catalogue[0];selected=obj.id;
  $('types').replaceChildren(...['Walls','Floors','Roofs','Connectors'].map(t=>button(t+' · '+(t==='Connectors'?Object.keys(A.connectors).length:catalogue.filter(m=>m.type===t).length),'type',t,type===t)));
  $('objects').replaceChildren(...(type==='Connectors'?Object.entries(A.connectors).map(([id,c])=>button(c.name,'connector',id,connector===id)):catalogue.filter(m=>m.type===type).map(m=>button(m.name,'object',m.id,selected===m.id))));
  document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===mode)));
  $('mode').value=mode;$('assembly-controls').hidden=mode!=='assembly';$('joint-controls').hidden=mode!=='connection';$('object-controls').hidden=mode!=='object';$('part-controls').hidden=mode!=='object'||type==='Connectors';$('connection-record').hidden=mode!=='connection';$('connection-record').replaceChildren();$('object-record').replaceChildren();$('object-record').hidden=mode!=='object';$('schedule-section').hidden=mode==='connection';$('empty-view').hidden=true;$('diagram').hidden=false;$('export-detail').disabled=false;
  $('explode').disabled=mode==='object'&&type==='Connectors';$('explode-label').textContent=mode==='object'?'Separate parts':mode==='connection'?'Separate members':'Separate cassettes';
  $('title').textContent=mode==='assembly'?'Rectangular studio · '+scene.bays+' modules':type==='Connectors'?A.connectors[connector].name:obj.name;
  $('dimensions').textContent=scene.length.toLocaleString('en')+' × 4,572 mm frame setting-out · '+scene.height.toLocaleString('en')+' mm walls';
  $('detail').textContent='Proposed geometry. Sections, fastening, spans, racking, uplift and foundations remain unverified.';
  $('status').textContent='Geometry ready';$('schedule').replaceChildren();exportDetail=null;let items=[];
  if(mode==='assembly'){
   const assembly=$('foundation').checked?S.generate({bays:scene.bays,height:scene.height,layer:$('layer').value,skin:true,connectionRevision:scene.connectionRevision,includeFoundation:true}):scene;
   const models=assembly.models.map(m=>$('skin').checked?m:S.model(m.id,m.assets.filter(a=>a.material!=='plywood')));items=showModels(models,assembly.items);
   $('status').textContent=items.length+' cassette instances · geometry ready';
   for(const r of S.schedule({items})){const tr=document.createElement('tr');[r.id,r.count,'Proposed'].forEach(v=>tr.append(text('td',v)));$('schedule').append(tr);}
  }else if(mode==='object'&&type!=='Connectors'){
   const full=obj.model;if(!full.assets.some(a=>a.id===part))part='';
   options($('part'),[{id:'',name:'All constituent parts'},...full.assets.map(a=>({id:a.id,name:A.label(a)}))],part);
   if(part&&full.assets.find(a=>a.id===part).material==='plywood')$('skin').checked=true;
   const m=$('skin').checked?full:S.model(full.id,full.assets.filter(a=>a.material!=='plywood'));
   const index=part?String(m.assets.findIndex(a=>a.id===part)):'';
   items=showModels([m],[{block:m.id,translation:[0,0,0]}],{object:true,isolate:index});
   const dims=full.bounds[1].map((v,k)=>v-full.bounds[0][k]);$('dimensions').textContent=dims.join(' × ')+' mm · '+full.assets.length+' constituent parts';
   const visible=part?1:m.assets.length;$('status').textContent=visible+' visible part'+(visible===1?'':'s')+' · '+full.assets.length+' total · geometry ready';
   $('detail').textContent='Each timber member and plywood panel is a separate part. Long joists remain continuous; cross-members meet their faces. Explosion is a viewing aid, not an erection sequence or an approved joint design.';
   const record=$('object-record');para(record,'Part composition',obj.type==='Walls'?'Studs, plates, plywood and any panel-seam backing. Their contact geometry is modelled; fastening and tolerances remain unresolved.':'Two continuous long joists, three cross-members and two plywood panels. The middle cross-member does not divide either long joist. Internal fastening and deck attachment remain unresolved.');
   para(record,'Used in assembly',obj.instances.join(', '));
   for(const a of full.assets){const tr=document.createElement('tr'),td=document.createElement('td'),b=button(A.label(a),'isolate',a.id,part===a.id);td.append(b);tr.append(td,text('td',a.dimensions.join(' × ')+' mm'),text('td',a.material+(!$('skin').checked&&a.material==='plywood'?' · hidden':'')));$('schedule').append(tr);}
   $('schedule-heading').textContent='Constituent parts · select to isolate';
   $('schedule-head').replaceChildren(...['Part','Dimensions','Material / visibility'].map(x=>text('th',x)));
  }else if(mode==='object'){
   const c=A.connectors[connector],m=A.connectorModel(connector);items=showModels(m?[m]:[],m?[{block:m.id,translation:[0,0,0],highlight:true}]:[]);
   $('dimensions').textContent=c.status;$('detail').textContent=c.note;$('status').textContent=m?'One connector · '+c.status.toLowerCase():'No geometry · '+c.status.toLowerCase();
   if(!m){$('diagram').hidden=true;$('empty-view').hidden=false;$('empty-view').textContent=c.note;}
   const rec=$('object-record');para(rec,'Status',c.status+'. Capacity and fastening schedule are not assigned.');
   if(c.product)table(rec,['Published dimension','Value'],Object.entries(c.product).filter(([k])=>k!=='code').map(([k,v])=>[k,v+' mm']));
   if(c.source)link(rec,'Source documentation ↗',c.source);
   para(rec,'Related connections','Select a connection to inspect its concept, measured position or actual cassette interface.');
   for(const [id,d]of Object.entries(A.connections))if(d.connectors.includes(connector))rec.append(button(d.name,'openJoint',id,false));
   $('schedule-section').hidden=true;
  }else{
   const allowed=Object.keys(A.connections).filter(k=>$('connection-scope').value==='all'||A.relevant(k,type,connector));
   if(!allowed.includes(joint))joint=allowed[0];options($('joint'),allowed.map(k=>({id:k,name:A.connections[k].name})),joint);
   const c=A.connections[joint],rec=$('connection-record');$('title').textContent=c.name;
   const views=c.hold?[{id:'unresolved',name:'Unresolved design'}]:[{id:'context',name:c.internal?'Actual part contacts':'Assembly interface'},...(c.probe?[{id:'measured',name:'Measured screw position'}]:[]),...(c.concept?[{id:'detail',name:'Research alternative'}]:[])];
   if(!views.some(v=>v.id===kind))kind=c.probe?'measured':'context';kind=options($('joint-view'),views,kind);
   $('occurrence-controls').hidden=kind!=='context';
   if(c.hold){items=showModels([],[]);$('diagram').hidden=true;$('empty-view').hidden=false;$('empty-view').textContent=c.hold;$('detail').textContent=c.hold;$('status').textContent='Undesigned · no geometry assigned';$('dimensions').textContent='Design requirement';exportDetail={id:joint,status:'undesigned',capacity:null,fasteners:null,manufacturingRelease:false};}
   else if(kind==='measured'){
    const study=D.geometry(c.probe,{revision:$('revision').value,cutaway:false}),d=study.detail;items=showModels(study.models,study.items);
    $('dimensions').textContent='Representative 2-bay / 2,100 mm study · '+d.product.code+' · '+d.revision;
    $('status').textContent=d.screenPass?'Conditional distance screen passes · strength unverified':'Original position fails distance screen';$('detail').textContent=d.reason;
    table(rec,['Member','End / required','Edge / required','Screen'],d.checks.map(x=>[x.id,x.endDistance+' / '+x.requiredEnd+' mm',x.edgeDistance+' / '+x.requiredEdge+' mm',x.screenPass?'Conditional pass':'Fail']));
    para(rec,'Scope',d.conditions+' One screw is a position probe, not a fastening quantity. These measurements do not follow the selected assembly occurrence, module count or wall height.');
    link(rec,'Measured dimensions source ↗',d.source.url);exportDetail={schema:'obtp-connection-inspection/1',units:'mm',...d};
   }else if(kind==='detail'){
    const study=C.build(c.concept,S),d=study.detail;items=showModels(study.models,study.items);$('dimensions').textContent='Independent research alternative · nominal display envelopes';$('detail').textContent=d.principle+' HOLD: product, fastening and resistance unverified.';$('status').textContent='Concept geometry ready · not the R90 screw detail';
    para(rec,'Load path',d.loadPath.join(' → '));para(rec,'Access',d.access.join(' '));para(rec,'Failure checks',d.failureModes.join(' · '));para(rec,'Evidence limits',d.adaptation);para(rec,'Prototype',d.test);
    for(const id of d.sources){const p=text('p','');link(p,id+' · '+C.sources[id].citation,C.sources[id].url);rec.append(p);}
    exportDetail={schema:'obtp-connection-study/1',...study,sources:Object.fromEntries(d.sources.map(id=>[id,C.sources[id]]))};window.OBTPConnectionStudy=study;
   }else if(c.internal){
    const list=A.contacts(obj.model,joint);occurrence=options($('occurrence'),list,occurrence);
    if(list.length){const contact=list.find(i=>i.id===occurrence),study=A.contactScene(obj.model,contact);items=showModels(study.models,study.items);$('detail').textContent=contact.status+'. No screw, nail or bracket placement is implied.';$('status').textContent=list.length+' actual part interfaces · selected contact ready';exportDetail={schema:'obtp-internal-interface/1',object:obj.id,contact,capacity:null,fasteners:null,manufacturingRelease:false};}
    else{items=showModels([],[]);$('status').textContent='No matching contact in this object';}
    $('dimensions').textContent=obj.name+' · actual constituent parts';para(rec,'Part-to-part assembly','These are the actual touching members of the selected cassette. Explode separates them for inspection. Mechanical fastening, tolerances and erection order still require a coordinated design.');
   }else{
    let list=A.instances(scene,joint);if($('connection-scope').value!=='all'&&type!=='Connectors')list=list.filter(j=>obj.instances.includes(j.a)||obj.instances.includes(j.b));
    occurrence=options($('occurrence'),list.map(j=>({id:j.id,name:j.a+' ↔ '+j.b})),occurrence);
    if(list.length){const j=list.find(i=>i.id===occurrence);items=showModels(scene.models,scene.allItems.filter(i=>[j.a,j.b].includes(i.id)).map(i=>({...i,highlight:i.id===j.b})));exportDetail={schema:'obtp-interface-context/1',interface:j,connectionRevision:scene.connectionRevision,capacity:null,fasteners:null,manufacturingRelease:false};$('status').textContent=list.length+' assembly interfaces · selected pair ready';}
    else{items=showModels([],[]);$('diagram').hidden=true;$('empty-view').hidden=false;$('empty-view').textContent='No matching interface for this object and assembly. Increase module count or choose All connections.';$('status').textContent='No matching assembly interface';}
    $('dimensions').textContent='Selected assembly interface · '+scene.connectionRevision;$('detail').textContent='Actual cassette placement. Interface records identify contact, not installed hardware or verified load transfer.';
   }
   para(rec,'Connectors and unresolved selections',c.connectors.length?'Inspect the related connector candidates below. A concept envelope is not a selected product.':'No connector selected.');
   for(const id of c.connectors){const b=button(A.connectors[id].name+' · '+A.connectors[id].status,'openConnector',id,false);rec.append(b);}
   $('export-detail').disabled=!exportDetail;
  }
  if(mode==='assembly'){$('schedule-heading').textContent='Shown cassette quantities';$('schedule-head').replaceChildren(...['Object','Quantity','Status'].map(x=>text('th',x)));}
  $('module-count').textContent=mode==='assembly'?items.length:mode==='object'&&type!=='Connectors'?obj.model.assets.length:items.length;$('count-label').textContent=mode==='assembly'?'Cassette instances':mode==='object'&&type!=='Connectors'?'Constituent parts':'Shown objects';$('joint-count').textContent=scene.allJoints.length;
  window.OBTPCassetteView={scene,items,renderer,catalogue,selected,type,mode,part,connector,joint,kind,occurrence,exportDetail};
 }catch(e){$('status').textContent=e.message;console.error(e);}}
 document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
  if(b.dataset.type){type=b.dataset.type;selected=catalogue.find(m=>m.type===type)?.id||selected;mode='object';resetExplosion();}
  else if(b.dataset.object){selected=b.dataset.object;mode='object';resetExplosion();}
  else if(b.dataset.connector){connector=b.dataset.connector;mode='object';resetExplosion();}
  else if(b.dataset.view){mode=b.dataset.view;resetExplosion();}
  else if(b.dataset.isolate){part=b.dataset.isolate;render();return;}
  else if(b.dataset.openConnector){connector=b.dataset.openConnector;type='Connectors';mode='object';resetExplosion();}
  else if(b.dataset.openJoint){joint=b.dataset.openJoint;mode='connection';kind=A.connections[joint].probe?'measured':'context';resetExplosion();}
  else return;render();
 });
 for(const id of ['bays','height','revision','layer','skin','foundation','connection-scope'])$(id).onchange=()=>{part='';occurrence='';render();};
 $('part').onchange=()=>{part=$('part').value;render();};$('joint').onchange=()=>{joint=$('joint').value;kind=A.connections[joint].probe?'measured':'context';resetExplosion();render();};$('joint-view').onchange=()=>{kind=$('joint-view').value;occurrence='';render();};$('occurrence').onchange=()=>{occurrence=$('occurrence').value;render();};
 $('opening-study').onclick=()=>{const s=S.openingStudy(),m=s.model;showModels([m],[{id:'standalone-window-study',block:m.id,translation:[0,0,0]}]);$('diagram').hidden=false;$('empty-view').hidden=true;$('title').textContent='Cassette window wall · detached study';$('dimensions').textContent='1,200 × 195 × 2,100 mm · nominal aperture 1,020 × 855 mm';$('status').textContent='Standalone geometric study · not placed in assembly';$('detail').textContent=s.status;};
 $('explode').oninput=()=>{$('amount').textContent=$('explode').value+'%';renderer.explode=Number($('explode').value)/100;renderer.draw();};$('reset').onclick=()=>{resetExplosion();render();};
 function download(data,name){const u=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);}
 $('export').onclick=()=>{const full=S.generate({bays:scene.bays,height:scene.height,connectionRevision:scene.connectionRevision}),parts=[];for(const item of full.items)for(const a of full.models.find(m=>m.id===item.block).assets)parts.push({id:item.id+'/'+a.id,material:a.material,corners:a.vertices.map(v=>S.transform(item,v))});download({schema:'obtp-cassette-boxes/1',units:'mm',system:S.spec.id,revision:S.spec.revision,connectionRevision:scene.connectionRevision,bays:scene.bays,height:scene.height,status:S.spec.status,manufacturingRelease:false,parts,interfaces:full.joints,connectionResearch:C.coverage(full),inspectionRegister:A.register(full)},'OBTP-Cassette-01-'+scene.bays+'-modules.json');};
 $('export-detail').onclick=()=>{if(exportDetail)download(exportDetail,'OBTP-'+joint+'-'+kind+'.json');};
 render();
})();
