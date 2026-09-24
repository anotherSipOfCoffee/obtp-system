'use strict';
/* Inspection metadata only. No geometry sizing, fastening schedule or structural release. */
(function(root){
 const S=typeof module==='undefined'?root.OBTPCassette:require('./system.js');
 const C=typeof module==='undefined'?root.OBTPConnections:require('./connections.js');
 const D=typeof module==='undefined'?root.OBTPConnectionDetails:require('./details/detail.js');
 const I=[1,0,0,0,1,0,0,0,1];
 const family=id=>id.startsWith('W')?'Walls':id.startsWith('F')?'Floors':'Roofs';
 function label(a){
  const names={'left-stud':'Left stud','right-stud':'Right stud','bottom-plate':'Bottom plate','top-plate':'Top plate','sheet-seam-backing':'Panel seam backing','edge-a':'Long joist A','edge-b':'Long joist B','blocking-0':'End cross-member A','blocking-2263.5':'Middle cross-member','blocking-4527':'End cross-member B','ply-0':'Plywood panel A','ply-1':'Plywood panel B'};
  return names[a.id]||a.label||a.id;
 }
 function offsets(model){
  const center=model.bounds[0].map((v,k)=>(v+model.bounds[1][k])/2);
  return {...model,assets:model.assets.map(a=>{
   let v=[0,0,0];
   if(a.material==='plywood')v=family(model.id)==='Walls'?[0,-260,0]:[0,0,300];
   else if(a.id==='left-stud')v=[-200,0,0];else if(a.id==='right-stud')v=[200,0,0];
   else if(a.id==='bottom-plate')v=[0,0,-160];else if(a.id==='top-plate')v=[0,0,160];
   else if(a.id==='sheet-seam-backing')v=[0,140,0];
   else if(a.id==='edge-a')v=[0,-220,0];else if(a.id==='edge-b')v=[0,220,0];
   else if(a.id.startsWith('blocking-')){const x=(a.bounds[0][0]+a.bounds[1][0])/2;v=[Math.abs(x-center[0])<1?0:(x<center[0]?-160:160),0,Math.abs(x-center[0])<1?160:0];}
   return {...a,label:label(a),explode:v};
  })};
 }
 function catalogue(scene){
  const groups=new Map();
  for(const model of scene.models){
   const type=family(model.id),signature=JSON.stringify([type,model.assets.map(a=>[a.id,a.material,a.bounds])]);
   if(!groups.has(signature))groups.set(signature,{id:model.id,type,model:offsets(model),modelIds:[],instances:[]});
   const g=groups.get(signature);g.modelIds.push(model.id);g.instances.push(...scene.allItems.filter(i=>i.block===model.id).map(i=>i.id));
  }
  const entries=[...groups.values()];
  for(const g of entries){
   const m=g.model,wide=m.assets.filter(a=>a.material==='timber'&&((a.id.includes('stud')&&a.dimensions[0]===90)||(a.id==='edge-a'||a.id==='edge-b')&&a.dimensions[1]===90||a.id.startsWith('blocking-')&&a.dimensions[0]===90));
   const base=g.type==='Walls'?'Wall '+(m.bounds[1][0]-m.bounds[0][0])+' mm':g.type==='Floors'?'Floor cassette':'Roof cassette';
   const long=wide.filter(a=>a.id==='edge-a'||a.id==='edge-b');
   g.name=base+(wide.length?(g.type==='Walls'?' · R90 '+wide.map(label).join(' + '):' · R90 '+(long.length===2?'both ends':long.length===0?'intermediate':long[0].id==='edge-a'?'end A':'end B')):' · standard');
  }
  return entries;
 }
 function contacts(model,kind){
  const out=[];
  for(let i=0;i<model.assets.length;i++)for(let j=i+1;j<model.assets.length;j++){
   const a=model.assets[i],b=model.assets[j],panel=a.material==='plywood'||b.material==='plywood';
   if(kind==='panel-frame'?!panel||a.material===b.material:panel)continue;
   const overlap=[0,1,2].map(k=>Math.min(a.bounds[1][k],b.bounds[1][k])-Math.max(a.bounds[0][k],b.bounds[0][k]));
   if(overlap.filter(v=>Math.abs(v)<1e-7).length!==1||overlap.some(v=>v< -1e-7)||overlap.filter(v=>v>1e-7).length!==2)continue;
   out.push({id:a.id+'|'+b.id,name:label(a)+' ↔ '+label(b),a,b,kind,status:'Contact geometry only; fastening unresolved',capacity:null,fasteners:null});
  }
  return out;
 }
 function contactScene(model,contact){
  const assets=[contact.a,contact.b],models=assets.map((a,k)=>S.model('internal-'+k,[{...a,label:label(a)}]));
  return {models,items:models.map((m,k)=>({id:assets[k].id,block:m.id,rotation:I,translation:[0,0,0],explode:model.assets.find(a=>a.id===assets[k].id).explode})),contact};
 }
 const connections={
  'panel-frame':{name:'Plywood → frame',types:['Walls','Floors','Roofs'],internal:true,concept:'panel-frame',connectors:['sheathing-fastener']},
  'frame-frame':{name:'Internal frame joints',types:['Walls','Floors','Roofs'],internal:true,concept:'frame-frame',connectors:['frame-angle']},
  'wall-seam':{name:'Wall → wall seam',types:['Walls'],concept:'wall-seam',probe:'wall-seam',connectors:['HBS580','splice']},
  corner:{name:'Wall corner return',types:['Walls'],concept:'corner',probe:'corner',connectors:['HBS580','corner-angle']},
  'wall-floor':{name:'Wall → floor',types:['Walls','Floors'],concept:'wall-floor',probe:'wall-floor',connectors:['HBS5120','base-tie','ABR','WHT']},
  'wall-roof':{name:'Roof → wall',types:['Walls','Roofs'],concept:'wall-roof',probe:'wall-roof',connectors:['HBS5120','roof-tie','ABR']},
  'floor-seam':{name:'Floor → floor seam',types:['Floors'],concept:'slab-seam',probe:'floor-seam',connectors:['HBS580']},
  'roof-seam':{name:'Roof → roof seam',types:['Roofs'],concept:'slab-seam',probe:'roof-seam',connectors:['HBS580']},
  foundation:{name:'Floor → support / foundation',types:['Floors','Walls'],connectors:['foundation-anchor','WHT'],hold:'Support arrangement, anchorage and continuous uplift load path are not designed. No anchor geometry or capacities assigned.'},
  openings:{name:'Opening jamb / header / sill',types:['Walls'],connectors:[],hold:'Opening framing, fastening and weathering details are not designed. Automatic openings remain disabled.'}
 };
 const connectors={
  HBS580:{name:'HBS580 · 5 × 80 mm',status:'Dimensioned candidate',kind:'screw',probe:'wall-seam',product:D.products.HBS580,source:D.source.url,note:'One physical screw. Head, shank and thread envelopes are display regions, not separate manufactured parts. Product assessment and required quantity remain unresolved.'},
  HBS5120:{name:'HBS5120 · 5 × 120 mm',status:'Dimensioned candidate',kind:'screw',probe:'wall-floor',product:D.products.HBS5120,source:D.source.url,note:'One physical screw. Simplified published-dimension envelope; not manufacturer CAD. No fastening schedule or resistance assigned.'},
  splice:{name:'Face splice plate',status:'Concept envelope',concept:'wall-seam',note:'Original plate envelope from the connection study. Thickness and dimensions are display assumptions; no product or hole pattern selected.'},
  'corner-angle':{name:'Corner angle',status:'Concept envelope',concept:'corner',note:'Two legs shown as one angle connector, not two independently fastened plates. Product, bend and fastening design unresolved.'},
  'base-tie':{name:'Wall–floor tie',status:'Concept envelope',concept:'wall-floor',note:'Local tie concept only. Does not provide a designed foundation anchor or complete uplift path.'},
  'roof-tie':{name:'Roof–wall tie',status:'Concept envelope',concept:'wall-roof',note:'Local tie concept only. Product, quantity and uplift resistance unresolved.'},
  'frame-angle':{name:'Internal frame angle',status:'Concept envelope',concept:'frame-frame',note:'One angle concept for comparison. Not an approved bracket or a fastening solution for every internal joint.'},
  ABR:{name:'ABR bracket family',status:'Research candidate · no model',source:'https://www.strongtie.co.uk/en-UK/products/reinforced-angle-bracket-abr',note:'Exact product, assessed fastening arrangement and fit remain unselected. No guessed hole coordinates or installed model.'},
  WHT:{name:'WHT hold-down family',status:'Research candidate · no model',source:'https://www.rothoblaas.com/products/fastening/brackets-and-plates/angle-brackets-and-plates-for-buildings/wht',note:'Stud/support compatibility and anchorage require design. Widening a receiver for the screw screen does not establish hold-down compatibility.'},
  'sheathing-fastener':{name:'Sheathing fastener',status:'Unselected · no model',note:'Select the product and panel-specific fastening schedule. No screw or nail spacing is released.'},
  'foundation-anchor':{name:'Foundation anchor',status:'Undesigned · no model',note:'Define the support and load path before choosing anchor type, product or placement.'}
 };
 function connectorModel(id){
  const c=connectors[id];if(!c)throw Error('Unknown connector');
  let assets;
  if(c.kind==='screw')assets=D.geometry(c.probe,{revision:'revised'}).models.find(m=>m.id==='detail-screw').assets;
  else if(c.concept)assets=C.build(c.concept,S).parts.filter(p=>p.material==='steel-study');
  else return null;
  const origin=[0,1,2].map(k=>Math.min(...assets.map(a=>a.bounds[0][k]))),vertices=[],faces=[];
  for(const a of assets){const start=vertices.length;vertices.push(...a.vertices.map(v=>v.map((n,k)=>n-origin[k])));faces.push(...a.faces.map(f=>f.map(i=>i+start)));}
  const bounds=[[0,0,0],[0,1,2].map(k=>Math.max(...vertices.map(v=>v[k])))];
  return S.model('connector-'+id,[{id,label:c.name,material:c.kind==='screw'?'fastener-envelope':'steel-study',vertices,faces,bounds,dimensions:bounds[1],explode:[0,0,0]}]);
 }
 function instances(scene,key){
  return scene.allJoints.filter(j=>key==='floor-seam'||key==='roof-seam'?j.type==='slab-seam'&&j.a.startsWith(key==='floor-seam'?'floor-':'roof-'):j.type===key);
 }
 function relevant(key,type,connector){return type==='Connectors'?connections[key].connectors.includes(connector):connections[key].types.includes(type);}
 function register(scene){return Object.entries(connections).map(([id,c])=>({id,name:c.name,status:c.hold?'Undesigned':c.probe?'Position screen available; design incomplete':'Concept / fastening unresolved',assemblyInterfaces:c.internal?null:instances(scene,id).length,connectorIds:c.connectors,capacity:null,fasteners:null,manufacturingRelease:false}));}
 const api={label,offsets,catalogue,contacts,contactScene,connections,connectors,connectorModel,instances,relevant,register};root.OBTPInspection=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window==='undefined'?globalThis:window);
