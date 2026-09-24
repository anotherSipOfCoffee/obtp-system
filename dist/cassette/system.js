'use strict';
/* Original OBTP concept geometry. No WikiHouse CAD or connection profiles. */
(function(root){
 const spec=Object.freeze({id:'obtp-cassette-01',revision:1,units:'mm',pitch:600,width:4572,wallDepth:195,stud:45,joistDepth:220,floorSkin:18,wallSkin:12,roofSkin:18,defaultHeight:2100,sheet:[1220,2440],status:'Proposed geometry; structural and envelope design not validated'});
 const connectionTypes=Object.freeze({
  'panel-frame':{name:'Plywood to timber',principle:'Mechanical sheathing fasteners into supported timber edges',source:'R1 / R3',release:'HOLD: product, spacing, edge distances and racking design'},
  'wall-seam':{name:'Wall to wall',principle:'Abutting boundary studs, mechanically connected from accessible cavity',source:'R1',release:'HOLD: screw specification, splitting and load transfer'},
  'corner':{name:'Corner return',principle:'End cassette bears against side-wall stud face; mechanical restraint',source:'R1',release:'HOLD: corner fastening, hold-down and weather wrap'},
  'wall-floor':{name:'Wall to floor',principle:'Bottom plate bearing over rim/blocking; separate shear and uplift restraint',source:'R1 / R2',release:'HOLD: fastener and anchorage design'},
  'wall-roof':{name:'Roof to wall',principle:'Joist bearing on top plate; engineered uplift restraint',source:'R1 / R2',release:'HOLD: bearing, uplift and diaphragm transfer'},
  'slab-seam':{name:'Floor / roof seam',principle:'Adjacent boundary joists mechanically linked; supported plywood edges',source:'R1',release:'HOLD: fastener schedule, diaphragm and differential movement'}
 });
 const faces=[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]];
 function box(id,p,s,material='timber'){
  const [x,y,z]=p,[a,b,c]=s;
  if(s.some(v=>!Number.isFinite(v)||v<=0))throw Error('Invalid part '+id);
  return {id,material,dimensions:s,bounds:[p,p.map((v,k)=>v+s[k])],vertices:[[x,y,z],[x+a,y,z],[x+a,y+b,z],[x,y+b,z],[x,y,z+c],[x+a,y,z+c],[x+a,y+b,z+c],[x,y+b,z+c]],faces,explode:[0,0,0]};
 }
 function model(id,assets){return {id,units:'mm',schema:'obtp-source-mesh/1',assets,bounds:[[0,1,2].map(k=>Math.min(...assets.map(a=>a.bounds[0][k]))),[0,1,2].map(k=>Math.max(...assets.map(a=>a.bounds[1][k])))],provenance:'Original OBTP proposed cassette geometry; not a fabrication release'};}
 function wall(w,h){
  const a=[box('left-stud',[0,0,45],[45,195,h-90]),box('right-stud',[w-45,0,45],[45,195,h-90]),box('bottom-plate',[0,0,0],[w,195,45]),box('top-plate',[0,0,h-45],[w,195,45])];
  // A backed sheet seam for the taller study; no nominal panel exceeds 2440 mm.
  if(h>2440)a.push(box('sheet-seam-backing',[45,0,h/2-22.5],[w-90,195,45]));
  const panels=h>2440?2:1;
  for(let j=0;j<panels;j++)a.push(box('ply-'+j,[0,-12,j*h/panels],[w,12,h/panels],'plywood'));
  return model('W'+w+'H'+h,a);
 }
 function slab(kind){
  const w=spec.width,a=[box('edge-a',[0,0,0],[w,45,220]),box('edge-b',[0,555,0],[w,45,220])];
  for(const x of [0,w/2-22.5,w-45])a.push(box('blocking-'+x,[x,45,0],[45,510,220]));
  for(let j=0;j<2;j++)a.push(box('ply-'+j,[j*w/2,0,220],[w/2,600,18],'plywood'));
  return model(kind,a);
 }
 function generate({bays=4,height=2100,layer='all',skin=true}={}){
  if(!Number.isInteger(bays)||bays<1||bays>8)throw Error('Choose 1–8 modules');
  if(![2100,2700].includes(height))throw Error('Unsupported height');
  if(!['all','floor','walls','roof'].includes(layer))throw Error('Unsupported layer');
  const L=bays*600,H=height,F=238,models=[slab('F600'),slab('R600'),wall(600,H),wall(582,H)],items=[],joints=[];
  const I=[1,0,0,0,1,0,0,0,1],R90=[0,-1,0,1,0,0,0,0,1],RN90=[0,1,0,-1,0,0,0,0,1],R180=[-1,0,0,0,-1,0,0,0,1];
  const add=(id,block,translation,rotation,stage,explode)=>items.push({id,block,translation,rotation,stage,explode});
  const join=(type,a,b,point)=>joints.push({id:type+':'+a+':'+b,type,a,b,point,status:'proposed-interface',capacity:null,fasteners:null});
  for(let i=0;i<bays;i++){
   add('floor-'+i,'F600',[0,i*600,0],I,'floor',[0,0,-300]);
   add('west-'+i,'W600H'+H,[0,(i+1)*600,F],RN90,'walls',[-350,0,0]);
   add('east-'+i,'W600H'+H,[4572,i*600,F],R90,'walls',[350,0,0]);
   add('roof-'+i,'R600',[0,i*600,F+H],I,'roof',[0,0,450]);
   for(const side of ['west','east']){
    const x=side==='west'?22.5:4549.5;
    join('wall-floor',side+'-'+i,'floor-'+i,[x,i*600+300,F]);
    join('wall-roof',side+'-'+i,'roof-'+i,[x,i*600+300,F+H]);
    if(i)join('wall-seam',side+'-'+(i-1),side+'-'+i,[x,i*600,F+H/2]);
   }
   if(i)for(const s of ['floor','roof'])join('slab-seam',s+'-'+(i-1),s+'-'+i,[2286,i*600,s==='floor'?110:F+H+110]);
  }
  for(const end of ['front','back'])for(let j=0;j<7;j++){
   const w=j===6?582:600,id=end+'-'+j;
   add(id,'W'+w+'H'+H,end==='front'?[195+j*600,0,F]:[4377-j*600,L,F],end==='front'?I:R180,'walls',[0,end==='front'?-350:350,0]);
   const x=end==='front'?195+j*600+w/2:4377-j*600-w/2,y=end==='front'?22.5:L-22.5,k=end==='front'?0:bays-1;
   join('wall-floor',id,'floor-'+k,[x,y,F]);join('wall-roof',id,'roof-'+k,[x,y,F+H]);
   if(j)join('wall-seam',end+'-'+(j-1),id,[end==='front'?195+j*600:4377-j*600,y,F+H/2]);
   if(j===0||j===6){const side=(end==='front')===(j===0)?'west':'east';join('corner',id,side+'-'+k,[side==='west'?195:4377,y,F+H/2]);}
  }
  const allItems=items.slice(),stages={floor:0,walls:1,roof:2,all:2},visible=items.filter(i=>stages[i.stage]<=stages[layer]),ids=new Set(visible.map(i=>i.id));
  const selectedModels=models.map(m=>skin?m:model(m.id,m.assets.filter(a=>a.material!=='plywood')));
  return {spec,bays,height,length:L,width:4572,clear:[4182,L-390,H],models:selectedModels,items:visible,allItems,joints:joints.filter(j=>ids.has(j.a)&&ids.has(j.b)),allJoints:joints,openings:{enabled:false,reason:'No designed lintel, jamb, sill, fastening or weathering detail'},status:spec.status};
 }
 function transform(item,p){const r=item.rotation;return [0,1,2].map(k=>r[k*3]*p[0]+r[k*3+1]*p[1]+r[k*3+2]*p[2]+item.translation[k]);}
 function worldBounds(item,asset){const p=asset.vertices.map(v=>transform(item,v));return [0,1].map(b=>[0,1,2].map(k=>Math[b?'max':'min'](...p.map(v=>v[k]))));}
 function schedule(scene){const rows=new Map();for(const i of scene.items)rows.set(i.block,(rows.get(i.block)||0)+1);return [...rows].map(([id,count])=>({id,count}));}
 const api={spec,connectionTypes,generate,transform,worldBounds,schedule,box,model};
 if(typeof module!=='undefined')module.exports=api;root.OBTPCassette=api;
})(typeof window==='undefined'?globalThis:window);
