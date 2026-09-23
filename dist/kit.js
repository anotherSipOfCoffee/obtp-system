/* Units: metres. Geometric study, not structural member sizing. */
(function(g){
const parts=[
{id:'post01',type:'Posts',d:[.16,.16,2.4],role:'Vertical frame member',faces:'Top bearing; four vertical faces; base',axis:'Z vertical; origin at lower corner'},
{id:'beam01',type:'Beams',d:[2.56,.16,.32],role:'Transverse beam over posts',faces:'Bottom bearing at post axes; side faces for long beams',axis:'X length; rotated 90° in the assembly'},
{id:'beam02',type:'Beams',d:[3.44,.16,.32],role:'Longitudinal beam between transverse beams',faces:'Both ends; top roof bearing',axis:'X length; clear distance between transverse beam faces'},
{id:'floor01',type:'Floors',d:[1.2,2.4,.24],role:'Repeated floor cassette envelope',faces:'Long edges; end bearing; upper floor plane',axis:'X repeat; Y cassette span'},
{id:'wall01',type:'Walls',d:[1.2,.18,2.4],role:'Solid non-load-bearing enclosure panel',faces:'Vertical edges; back attachment plane; bottom support',axis:'X repeat; Y thickness; Z height'},
{id:'wall02',type:'Walls',d:[1.2,.18,2.4],role:'Window panel; 900 × 1200 mm opening',faces:'Same outer interfaces as wall01; opening perimeter',axis:'Sill 900 mm above panel base'},
{id:'wall03',type:'Walls',d:[1.2,.18,2.4],role:'Door panel; 900 × 2100 mm opening',faces:'Same outer interfaces as wall01; threshold and opening perimeter',axis:'Opening starts at panel base'},
{id:'roof01',type:'Roofs',d:[1.2,2.56,.2],role:'Repeated flat roof cassette envelope',faces:'Long edges; end bearing; upper weathering zone',axis:'X repeat; Y span; drainage unresolved'}];
// The agreed list contains eight definitions (1 + 2 + 1 + 3 + 1).
const joints=[
{id:'j01',name:'Post / transverse beam',ids:['post01','beam01'],rule:'Beam underside meets the post top at z = 2.64 m.',open:'Bearing verification, restraint and fastening unresolved.'},
{id:'j02',name:'Beam / beam',ids:['beam01','beam02'],rule:'Long beam ends meet the transverse beam faces.',open:'An end connection is required; face contact alone cannot support this beam.'},
{id:'j03',name:'Frame / wall',ids:['post01','wall01'],rule:'Wall back plane is outside the frame; attachment coordinates require a rail or brackets.',open:'Intermediate supports, fixings and movement allowance unresolved.'},
{id:'j04',name:'Floor / wall',ids:['floor01','wall03'],rule:'Panel bottom and floor top share z = 0.24 m.',open:'80 mm edge gap requires a support/threshold detail. No direct bearing is assumed.'},
{id:'j05',name:'Beam / roof',ids:['beam02','roof01'],rule:'Roof underside meets beam top at z = 2.96 m.',open:'Bearing, uplift restraint, slope and weathering unresolved.'},
{id:'j06',name:'Wall / wall',ids:['wall01','wall02'],rule:'Adjacent panels share a 1.20 m pitch.',open:'Nominal edge contact only; sealing and manufacturing clearance unresolved.'}];
function shape(id){const p=parts.find(p=>p.id===id);if(!p)throw Error('Unknown part');const [w,d,h]=p.d;const box=(x,y,z,a,b,c)=>({p:[x,y,z],d:[a,b,c]});if(!['wall02','wall03'].includes(id))return[box(0,0,0,w,d,h)];const z=id==='wall02'?.9:0,out=[box(0,0,0,.15,d,h),box(1.05,0,0,.15,d,h),box(.15,0,2.1,.9,d,.3)];if(z)out.push(box(.15,0,0,.9,d,z));return out;}
function assembly(n=1){if(![1,2].includes(n))throw Error('Only one or two bays');const items=[];const add=(part,p,rot=0)=>items.push({id:part+'-'+(items.length+1),part,p,rot});const L=3.6*n;
for(let i=0;i<=n;i++){const x=i*3.6;for(const y of [0,2.4])add('post01',[x-.08,y-.08,.24]);add('beam01',[x+.08,-.08,2.64],90);}
for(let i=0;i<n;i++){for(const y of [-.08,2.32])add('beam02',[i*3.6+.08,y,2.64]);for(let j=0;j<3;j++){const x=i*3.6+j*1.2;add('floor01',[x,0,0]);add('roof01',[x,-.08,2.96]);add(i===0&&j===0?'wall03':j===1?'wall02':'wall01',[x,-.26,.24]);add(j===1?'wall02':'wall01',[x,2.48,.24]);}}
for(const x of [-.08,L+.26])for(let j=0;j<2;j++)add('wall01',[x,j*1.2,.24],90);
return items;}
function boxes(items,{explode=0,layer='all',highlight=''}={}){const allowed=layer==='frame'?['Posts','Beams']:layer==='floor'?['Posts','Beams','Floors']:layer==='walls'?['Posts','Beams','Floors','Walls']:parts.map(p=>p.type);const out=[];for(const inst of items){const p=parts.find(p=>p.id===inst.part);if(!allowed.includes(p.type))continue;const e=explode/100;for(const b of shape(inst.part)){let pos=b.p.map((v,i)=>v+inst.p[i]),d=[...b.d];if(inst.rot===90){pos=[inst.p[0]-b.p[1]-b.d[1],inst.p[1]+b.p[0],inst.p[2]+b.p[2]];d=[b.d[1],b.d[0],b.d[2]];}if(p.type==='Roofs')pos[2]+=e*1.4;if(p.type==='Walls'){if(inst.rot===90)pos[0]+=inst.p[0]<0?-e:e;else pos[1]+=inst.p[1]<0?-e:e;}out.push({p:pos,d,part:inst.part,instance:inst.id,blue:inst.part===highlight});}}return out;}
function counts(items){return parts.map(p=>({id:p.id,count:items.filter(i=>i.part===p.id).length}));}
g.OBTPKit={parts,joints,shape,assembly,boxes,counts};if(typeof module!=='undefined')module.exports=g.OBTPKit;
})(globalThis);
