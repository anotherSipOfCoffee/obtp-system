'use strict';
/* Original OBTP review geometry. Not a fastening schedule or engineering release. */
(function(root){
 const S=typeof module==='undefined'?root.OBTPCassette:require('./system.js');
 const I=[1,0,0,0,1,0,0,0,1];
 const hold={capacity:null,fasteners:null,manufacturingRelease:false,status:'Design study; member sizing, fasteners and load capacity unverified'};
 function opening(kind='door'){
  if(!['door','window'].includes(kind))throw Error('Unknown opening type');
  const w=1200,h=S.spec.defaultHeight,d=S.spec.wallDepth,head=1900,sill=kind==='door'?0:900;
  const a=[S.box('king-left',[0,0,0],[45,d,h-45]),S.box('king-right',[w-45,0,0],[45,d,h-45]),S.box('jack-left',[45,0,0],[45,d,head]),S.box('jack-right',[w-90,0,0],[45,d,head]),S.box('lintel',[45,0,head],[w-90,d,h-45-head]),S.box('top-plate',[0,0,h-45],[w,d,45])];
  // Separate sheathing rectangles leave the aperture physically open.
  a.push(S.box('skin-left',[0,-12,0],[90,12,h],'plywood'),S.box('skin-right',[w-90,-12,0],[90,12,h],'plywood'),S.box('skin-head',[90,-12,head],[w-180,12,h-head],'plywood'));
  if(sill){a.push(S.box('sill',[90,0,sill-45],[w-180,d,45]),S.box('bottom-plate',[90,0,0],[w-180,d,45]),S.box('sill-support',[w/2-22.5,0,45],[45,d,sill-90]),S.box('skin-sill',[90,-12,0],[w-180,12,sill],'plywood'));}
  const frame=S.model('W1200-'+kind.toUpperCase()+'-REVIEW',a),models=[frame],items=[{id:'opening-frame',block:frame.id,translation:[0,0,0],rotation:I}],joinery=[];
  if(kind==='door'){
   // Generic frame and leaf: review the rough opening first; not a specified product.
   joinery.push(S.box('door-jamb-left',[90,75,0],[30,45,head],'furniture-study'),S.box('door-jamb-right',[1080,75,0],[30,45,head],'furniture-study'),S.box('door-head',[120,75,head-30],[960,45,30],'furniture-study'));
   // Leaf is displayed open outwards, with 5 mm nominal reveal.
   joinery.push(S.box('door-leaf-open',[125,-880,5],[40,950,head-40],'furniture-study'));
   const door=S.model('DOOR-JOINERY-REVIEW',joinery);models.push(door);items.push({id:'door-joinery',block:door.id,translation:[0,0,0],rotation:I});
  }
  return {models,items,aperture:{width:1020,height:head-sill,sill,head},...hold,description:'Two 600 mm bays form one 1,200 mm opening object. King studs, jack studs, bearing lintel and top plate form a continuous geometric path; plywood is cut around the aperture. Generic door frame and leaf are separate from structure. Not installed in the Sauna or WikiHouse assembly.'};
 }
 function wallConnectors(model){
  if(!model.id.startsWith('W'))return model;
  const a=model.assets,plate=a.find(p=>p.id==='bottom-plate'),top=a.find(p=>p.id==='top-plate');
  if(!plate||!top)return model;
  const added=[];
  for(const side of ['left','right']){
   const stud=a.find(p=>p.id===side+'-stud');if(!stud)continue;
   const x=side==='left'?stud.bounds[1][0]:stud.bounds[0][0],dir=side==='left'?1:-1;
   for(const end of ['bottom','top']){
    const z=end==='bottom'?plate.bounds[1][2]:top.bounds[0][2],up=end==='bottom'?1:-1;
    const pieces=[S.box('horizontal',[dir===1?x:x-90,60,up===1?z:z-3],[90,75,3],'steel-study'),S.box('vertical',[dir===1?x:x-3,60,up===1?z+3:z-90],[3,75,87],'steel-study')];
    // Both legs are one inspectable connector, not separately manufactured parts.
    const vertices=pieces.flatMap(p=>p.vertices),faces=pieces.flatMap((p,i)=>p.faces.map(f=>f.map(n=>n+i*8)));
    const bounds=[0,1].map(b=>[0,1,2].map(k=>Math[b?'max':'min'](...pieces.map(p=>p.bounds[b][k]))));
    added.push({id:'joint-study-'+side+'-'+end,label:'Angle study · '+side+' '+end,material:'steel-study',vertices,faces,bounds,dimensions:bounds[1].map((v,k)=>v-bounds[0][k]),explode:[dir*100,220,up*100],...hold});
   }
  }
  return {...model,assets:[...a,...added]};
 }
 function partitionSupport({bays=3,axis=1500}={}){
  if(!Number.isInteger(axis)||axis<90||axis>S.spec.width-90)throw Error('Partition axis must be within the floor');
  const source=S.generate({bays,layer:'floor',skin:true,connectionRevision:'revised'}),models=[],items=[];
  const added=[],half=45;
  // Partition runs perpendicular to the continuous long joists. In every
  // cavity, add only the missing timber beneath its 90 mm sole plate.
  for(const item of source.items){
   const original=source.models.find(m=>m.id===item.block),assets=original.assets.map(a=>({...a}));
   const near=assets.find(a=>a.id==='edge-a').bounds[1][1],far=assets.find(a=>a.id==='edge-b').bounds[0][1];
   let intervals=[[axis-half,axis+half]];
   for(const b of assets.filter(a=>a.id.startsWith('blocking-'))){const lo=b.bounds[0][0],hi=b.bounds[1][0];intervals=intervals.flatMap(([s,e])=>hi<=s||lo>=e?[[s,e]]:[[s,Math.min(e,lo)],[Math.max(s,hi),e]].filter(([l,r])=>r>l));}
   for(const [j,[lo,hi]] of intervals.entries()){const p=S.box('partition-backing-'+j,[lo,near,0],[hi-lo,far-near,S.spec.joistDepth]);assets.push(p);added.push({floor:item.id,part:p.id,bounds:p.bounds,...hold});}
   const m=S.model(original.id+'-PARTITION',assets);models.push(m);items.push({...item,block:m.id});
  }
  const L=bays*600,z=S.spec.joistDepth+S.spec.floorSkin,parts=[S.box('partition-sole',[axis-half,0,z],[90,L,45]),S.box('partition-head',[axis-half,0,z+2055],[90,L,45])];
  for(let y=0;y<L;y+=600)parts.push(S.box('partition-stud-'+y,[axis-half,y,z+45],[90,45,2010]));
  parts.push(S.box('partition-stud-end',[axis-half,L-45,z+45],[90,45,2010]));
  const p=S.model('PARTITION-90-REVIEW',parts);models.push(p);items.push({id:'partition-review',block:p.id,translation:[0,0,0],rotation:I,stage:'partition',explode:[0,0,450]});
  return {models,items,added,axis,...hold,description:'Non-load-bearing partition at an independent axis. Full-depth backing closes each floor cavity below the sole plate without moving the room or cutting continuous joists. Existing blocking is reused where it overlaps. Joist line loads, blocking-end connections and roof deflection allowance still require design. 90 mm is a framing study, not a finished sauna wall thickness.'};
 }
 const api={opening,wallConnectors,partitionSupport};root.OBTPDevelopment=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window==='undefined'?globalThis:window);
