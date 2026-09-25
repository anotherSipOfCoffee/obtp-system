'use strict';
/* Matrix is a geometric study on the OBTP 600 mm setting-out grid.
   It does not assign structural capacities, supports, fasteners or roof finishes. */
(function(root){
 const api=root.OBTPCassette||(typeof require==='function'?require('./system.js'):null);
 if(!api)throw Error('Load the OBTP cassette system before Matrix');
 const P=600,D=195,F=238,H=2100,I=[1,0,0,0,1,0,0,0,1];
 const R90=[0,-1,0,1,0,0,0,0,1],RN90=[0,1,0,-1,0,0,0,0,1],R180=[-1,0,0,0,-1,0,0,0,1];
 function panel(kind,w,d){
  const a=[
   api.box('edge-low',[0,0,0],[w,45,220]),
   api.box('edge-high',[0,d-45,0],[w,45,220]),
   api.box('end-low',[0,45,0],[45,d-90,220]),
   api.box('end-high',[w-45,45,0],[45,d-90,220])
  ];
  if(d===1200)a.push(api.box('centre-joist',[45,577.5,0],[w-90,45,220]));
  a.push(api.box('deck',[0,0,220],[w,d,18],'plywood'));
  return api.model(kind+'-'+w+'x'+d,a);
 }
 function corner(key){
  // Four placeholder posts occupy the corner zone. The bearing and hold-down
  // assembly is explicitly unresolved; the skins only expose the outside face.
  const a=[];
  for(const x of [0,150])for(const y of [0,150])a.push(api.box('post-'+x+'-'+y,[x,y,0],[45,45,H]));
  const west=key.includes('w'),south=key.includes('s');
  a.push(api.box('outer-x-skin',[west?-12:195,0,0],[12,195,H],'plywood'));
  a.push(api.box('outer-y-skin',[0,south?-12:195,0],[195,12,H],'plywood'));
  a.push(api.box('skin-return',[west?-12:195,south?-12:195,0],[12,12,H],'plywood'));
  return api.model('M-CORNER-'+key,a);
 }
 function generate({columns=4,rows=4,layer='all',skin=true}={}){
  if(!Number.isInteger(columns)||columns<1||columns>8)throw Error('Matrix columns: choose 1–8 for this study');
  if(!Number.isInteger(rows)||rows<1||rows>18)throw Error('Matrix rows: choose 1–18');
  if(!['floor','walls','roof','all'].includes(layer))throw Error('Unsupported Matrix layer');
  const W=columns*P,L=rows*P,models=[],items=[],joints=[];
  const baseWall=api.generate({bays:1,height:H,skin:true,connectionRevision:'revised'}).models.find(m=>m.id==='W600H2100');
  if(!baseWall)throw Error('Missing shared 600 mm wall cassette');
  models.push(baseWall);
  const types=new Set(),addModel=(kind,w,d)=>{const id=kind+'-'+w+'x'+d;if(!types.has(id)){types.add(id);models.push(panel(kind,w,d));}return id;};
  const add=(id,block,p,rotation,stage,explode)=>items.push({id,block,translation:p,rotation,stage,explode});
  const join=(type,a,b,point)=>joints.push({id:type+':'+a+':'+b,type,a,b,point,status:'research-interface',capacity:null,fasteners:null});
  const slabItems={floor:[],roof:[]};
  for(const stage of ['floor','roof']){
   const z=stage==='floor'?0:F+H,kind=stage==='floor'?'M-F':'M-R';
   const addSlab=(id,x,y,w,d)=>{add(id,addModel(kind,w,d),[x,y,z],I,stage,[0,0,stage==='floor'?-300:450]);slabItems[stage].push({id,x,y,w,d});};
   for(let x=0;x<W;x+=2400)for(let y=0;y<L;y+=1200)addSlab(stage+'-core-'+x+'-'+y,x,y,Math.min(2400,W-x),Math.min(1200,L-y));
   for(let y=0;y<L;y+=P){addSlab(stage+'-west-'+y,-D,y,D,P);addSlab(stage+'-east-'+y,W,y,D,P);}
   for(let x=0;x<W;x+=P){addSlab(stage+'-south-'+x,x,-D,P,D);addSlab(stage+'-north-'+x,x,L,P,D);}
   for(const x of [-D,W])for(const y of [-D,L])addSlab(stage+'-corner-'+x+'-'+y,x,y,D,D);
   const row=slabItems[stage];
   for(let a=0;a<row.length;a++)for(let b=a+1;b<row.length;b++){
    const u=row[a],v=row[b],xTouch=u.x+u.w===v.x||v.x+v.w===u.x,yTouch=u.y+u.d===v.y||v.y+v.d===u.y;
    if(xTouch&&Math.min(u.y+u.d,v.y+v.d)>Math.max(u.y,v.y))join('slab-seam',u.id,v.id,[xTouch?(u.x+u.w===v.x?v.x:u.x):0,Math.max(u.y,v.y),z+110]);
    else if(yTouch&&Math.min(u.x+u.w,v.x+v.w)>Math.max(u.x,v.x))join('slab-seam',u.id,v.id,[Math.max(u.x,v.x),u.y+u.d===v.y?v.y:u.y,z+110]);
   }
  }
  for(let i=0;i<rows;i++){
   const y=i*P;
   add('west-'+i,baseWall.id,[-D,y+P,F],RN90,'walls',[-350,0,0]);
   add('east-'+i,baseWall.id,[W+D,y,F],R90,'walls',[350,0,0]);
   for(const side of ['west','east']){
    const id=side+'-'+i,x=side==='west'?-D/2:W+D/2;
    join('wall-floor',id,'floor-'+side+'-'+y,[x,y+P/2,F]);
    join('wall-roof',id,'roof-'+side+'-'+y,[x,y+P/2,F+H]);
    if(i)join('wall-seam',side+'-'+(i-1),id,[x,y,F+H/2]);
   }
  }
  for(let i=0;i<columns;i++){
   const x=i*P;
   add('south-'+i,baseWall.id,[x,-D,F],I,'walls',[0,-350,0]);
   add('north-'+i,baseWall.id,[x+P,L+D,F],R180,'walls',[0,350,0]);
   for(const side of ['south','north']){
    const id=side+'-'+i,y=side==='south'?-D/2:L+D/2;
    join('wall-floor',id,'floor-'+side+'-'+x,[x+P/2,y,F]);
    join('wall-roof',id,'roof-'+side+'-'+x,[x+P/2,y,F+H]);
    if(i)join('wall-seam',side+'-'+(i-1),id,[x,y,F+H/2]);
   }
  }
  for(const key of ['sw','se','nw','ne']){
   const x=key.includes('w')?-D:W,y=key.includes('s')?-D:L,id='corner-'+key;
   models.push(corner(key));add(id,'M-CORNER-'+key,[x,y,F],I,'walls',[key.includes('w')?-350:350,key.includes('s')?-350:350,0]);
   join('wall-floor',id,'floor-corner-'+x+'-'+y,[x+D/2,y+D/2,F]);
   join('wall-roof',id,'roof-corner-'+x+'-'+y,[x+D/2,y+D/2,F+H]);
   join('corner',id,(key.includes('w')?'west-':'east-')+(key.includes('s')?0:rows-1),[x+D/2,y+D/2,F+H/2]);
   join('corner',id,(key.includes('s')?'south-':'north-')+(key.includes('w')?0:columns-1),[x+D/2,y+D/2,F+H/2]);
  }
  const stageOrder={floor:0,walls:1,roof:2,all:2},visible=items.filter(i=>stageOrder[i.stage]<=stageOrder[layer]),ids=new Set(visible.map(i=>i.id));
  const selected=models.map(m=>skin?m:api.model(m.id,m.assets.filter(a=>a.material!=='plywood')));
  return {spec:{...api.spec,id:'obtp-matrix-study',status:'Research geometry only; corner, transverse seams, bearing and anchorage on hold'},columns,rows,height:H,width:W+2*D,length:L+2*D,clear:[W,L,H],models:selected,items:visible,allItems:items,joints:joints.filter(j=>ids.has(j.a)&&ids.has(j.b)),allJoints:joints,openings:{enabled:false,reason:'No Matrix lintel, jamb or structural opening design'},status:'Matrix study; structural support and connection design unresolved'};
 }
 const exported={generate};
 if(typeof module!=='undefined')module.exports=exported;
 root.OBTPMatrix=exported;
})(typeof window==='undefined'?globalThis:window);
