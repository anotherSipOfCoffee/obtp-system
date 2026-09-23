/* WikiHouse source models. All placement transforms are rigid; units millimetres. */
(function(g){'use strict';
const pin='6581cc1de0f4daef81a6b5c5a2eaed3c537d1d8f';
const parts=[
{id:'W-S',type:'Walls',role:'Standard load-bearing wall block',source:'Walls/W-S/W-S_detailed/W-S.3dm',note:'Seven original solid parts. Used in the chassis slice.'},
{id:'C-S-1',type:'Walls',role:'Integrated corner wall block',source:'Walls/C-S-1/C-S-1_detailed/C-S-1.3dm',note:'Official corner component. Corner placement is not yet included in the open chassis slice.'},
{id:'E-S',type:'Beams',role:'End-floor beam block',source:'Floors/E-S/E-S_detailed/E-S.3dm',note:'End-floor role, not a generic post-supported beam. Source nested definitions use E-M names; source IDs are retained. Not placed in this slice.'},
{id:'F-S',type:'Floors',role:'Floor beam / cassette block',source:'Floors/F-S/F-S_detailed/F-S.3dm',note:'600 mm repeated module; 4,572 mm overall source span. Used in the slice.'},
{id:'W-O-S-1',type:'Openings',role:'Wall opening block',source:'Openings/W-O-S-1/W-O-S-1_detailed/W-O-S-1.3dm',note:'Source height is 2,240 mm, unlike W-S at 2,100 mm. Kept as an object; not forced into this slice.'},
{id:'R-S',type:'Roofs',role:'Low-slope roof beam / cassette',source:'Roofs/R-S/R-S_detailed/R-S.3dm',note:'Source geometry includes one valid but open Brep. Displayed unchanged; repair/solid validation remains open.'},
{id:'TIE-FULL',type:'Connectors',role:'Full tie from official CNC profile',source:'Other/Ties/TIES.dxf',note:'18 mm sheet with 9 mm pockets, reconstructed from source cutter profiles. Arcs tessellated at 0.01 mm; not new CNC output.'},
{id:'TIE-HALF',type:'Connectors',role:'Half tie from official CNC profile',source:'Other/Ties/TIES.dxf',note:'Source half-tie profile, 18 mm sheet / 9 mm pocket. Included for inspection; not placed in the slice.'}
];
const I=[1,0,0,0,1,0,0,0,1],R180=[-1,0,0,0,-1,0,0,0,1],Rroof=[0,1,0,-1,0,0,0,0,1];
const item=(block,translation=[0,0,0],rotation=I,explode=[0,0,0])=>({block,translation,rotation,explode});
const floor=()=>item('F-S',[600,-732,380]);
const front=()=>item('W-S',[300,-50,380],I,[0,-350,0]);
const back=()=>item('W-S',[300,4622,380],R180,[0,350,0]);
const roof=()=>item('R-S',[1593.397095,-1232,2703.43837],Rroof,[0,0,600]);
function verticalTies(z,ends=['front','back']){const out=[];for(const end of ends){const planes=end==='front'?[[0,1],[186,-1]]:[[4572,-1],[4386,1]];for(const[y,sign]of planes)for(const x of[105.1,300,494.9])out.push(item('TIE-FULL',[x,y,z],[1,0,0,0,0,sign,0,1,0],[0,sign*-200,z===2480?600:0]));}return out;}
function wallPair(){const out=[item('W-S',[300,-50,0]),item('W-S',[900,-50,0],I,[300,0,0])];for(const z of[195.547,404.453,795.547,1004.453,1395.547,1604.453])for(const[y,sign]of[[0,1],[186,-1]])out.push(item('TIE-FULL',[600,y,z],[0,1,0,0,0,sign,1,0,0],[150,-sign*200,0]));return out;}

const floorSeamY=[583.453,988.547,1183.453,1588.547,1783.453,2188.547,2383.453,2788.547,2983.453,3388.547,3583.453,3988.547];
const roofSeamPositions=[[600,4190.457939994503,2834.2833584676464],[600,3981.583915953509,2837.9292681191],[600,3590.4623340077533,2844.7563207267904],[600,3381.5883109577308,2848.4022303609463],[600,2990.462401790549,2855.2293585005677],[600,2781.58813482357,2858.8752723923103],[600,2390.4667968122203,2865.70232074211],[600,2181.5925288368207,2869.3482346514543],[600,1790.558105341207,2876.173765902738],[600,1581.6840817913358,2879.8196755456192],[600,1190.4755858384174,2886.6482452429477],[600,981.601439825858,2890.294157023423],[600,590.4800412020634,2897.1212064312167],[600,381.60583471665655,2900.767119267249]];
function deckSeamTies(kind,offset=0){
 const c=Math.cos(Math.PI/180),s=Math.sin(Math.PI/180);
 const positions=kind==='floor'?floorSeamY.map(y=>[600,y,380]):roofSeamPositions;
 const rotation=kind==='floor'?[0,1,0,1,0,0,0,0,-1]:[0,1,0,-c,0,-s,s,0,-c];
 return positions.map(p=>item('TIE-FULL',[p[0]+offset,p[1],p[2]],rotation,[0,0,kind==='floor'?200:800]));
}

const joints=[
{id:'floor-floor',name:'Floor / floor',ids:['F-S','TIE-FULL'],rule:'Adjacent source floor modules at 600 mm pitch, joined by twelve full ties in the top-deck seam sockets.',evidence:'Both tie depths sampled at all twelve source socket positions. Bottom skin has no matching seam socket row. See EXTENDED_INTERFACE_AUDIT.json.',scene:()=>[floor(),item('F-S',[1200,-732,380]),...deckSeamTies('floor')]},
{id:'roof-roof',name:'Roof / roof',ids:['R-S','TIE-FULL'],rule:'Adjacent source roof modules at 600 mm pitch, joined by fourteen full ties on the original one-degree top plane.',evidence:'Both tie depths sampled at all fourteen source socket positions. Source roof defect retained. See EXTENDED_INTERFACE_AUDIT.json.',scene:()=>[roof(),item('R-S',[2193.397095,-1232,2703.43837],Rroof),...deckSeamTies('roof')]},
{id:'wall-wall',name:'Wall / wall',ids:['W-S','TIE-FULL'],rule:'Adjacent W-S blocks on a 600 mm pitch, with full ties in the six paired side sockets on each face.',evidence:'Pinned source sockets and TIES.dxf; two sampled depths at a representative socket. Remaining repeated sockets use their source coordinates.',scene:wallPair},
{id:'floor-wall',name:'Floor / wall',ids:['F-S','W-S','TIE-FULL'],rule:'W-S sits on the F-S deck datum at 380 mm. Three full ties connect each face through the matching end and wall sockets.',evidence:'Source mesh fit sampled at both depth steps, all three positions and both faces; see audit.',scene:()=>[floor(),front(),...verticalTies(380,['front'])]},
{id:'wall-roof',name:'Wall / roof',ids:['W-S','R-S','TIE-FULL'],rule:'R-S bearing datum meets the W-S top at 2,480 mm; three full ties connect each face. Roof slope is retained.',evidence:'Source mesh fit sampled at both depth steps, all three positions and both faces. One roof Brep remains open.',scene:()=>[front(),roof(),...verticalTies(2480,['front'])]}
];
function assembly(layer='all'){const out=[floor()];if(layer==='floor')return out;out.push(front(),back());if(layer==='walls')return out;out.push(roof());if(layer==='all')out.push(...verticalTies(380),...verticalTies(2480));return out;}

/* Reuse the single-slice and wall-pair transforms; no new joint geometry. */
function multiAssembly(bays=1,layer='all'){
 if(!Number.isInteger(bays)||bays<1||bays>8)throw Error('Choose 1–8 modules.');
 if(!['all','floor','walls','roof'].includes(layer))throw Error('Unknown assembly layer.');
 const out=[];
 for(let bay=0;bay<bays;bay++)for(const [index,p] of assembly(layer).entries())out.push({...p,translation:p.translation.map((v,k)=>v+(k===0?600*bay:0)),instanceId:`bay-${bay+1}/${p.block}-${index+1}`});
 if(layer==='all')for(let seam=0;seam<bays-1;seam++)for(const [index,p] of wallPair().filter(p=>p.block==='TIE-FULL').entries()){
  out.push({...p,translation:[p.translation[0]+600*seam,p.translation[1],p.translation[2]+380],explode:[0,-200,0],instanceId:`seam-${seam+1}/front-tie-${index+1}`});
  out.push({...p,translation:[1200-p.translation[0]+600*seam,4572-p.translation[1],p.translation[2]+380],rotation:p.rotation.map((v,k)=>k<6?-v:v),explode:[0,200,0],instanceId:`seam-${seam+1}/back-tie-${index+1}`});
 }
 if(layer==='all')for(let seam=0;seam<bays-1;seam++)for(const kind of ['floor','roof'])for(const [index,p]of deckSeamTies(kind,seam*600).entries())out.push({...p,instanceId:`seam-${seam+1}/${kind}-tie-${index+1}`});
 return out;
}

function counts(items){return parts.map(p=>({id:p.id,count:items.filter(i=>i.block===p.id).length})).filter(r=>r.count);}
g.OBTPCatalogue={pin,parts,joints,assembly,multiAssembly,deckSeamTies,counts,item};if(typeof module!=='undefined')module.exports=g.OBTPCatalogue;
})(globalThis);
