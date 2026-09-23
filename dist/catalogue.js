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
const joints=[
{id:'wall-wall',name:'Wall / wall',ids:['W-S','TIE-FULL'],rule:'Adjacent W-S blocks on a 600 mm pitch, with full ties in the six paired side sockets on each face.',evidence:'Pinned source sockets and TIES.dxf; two sampled depths at a representative socket. Remaining repeated sockets use their source coordinates.',scene:wallPair},
{id:'floor-wall',name:'Floor / wall',ids:['F-S','W-S','TIE-FULL'],rule:'W-S sits on the F-S deck datum at 380 mm. Three full ties connect each face through the matching end and wall sockets.',evidence:'Source mesh fit sampled at both depth steps, all three positions and both faces; see audit.',scene:()=>[floor(),front(),...verticalTies(380,['front'])]},
{id:'wall-roof',name:'Wall / roof',ids:['W-S','R-S','TIE-FULL'],rule:'R-S bearing datum meets the W-S top at 2,480 mm; three full ties connect each face. Roof slope is retained.',evidence:'Source mesh fit sampled at both depth steps, all three positions and both faces. One roof Brep remains open.',scene:()=>[front(),roof(),...verticalTies(2480,['front'])]}
];
function assembly(layer='all'){const out=[floor()];if(layer==='floor')return out;out.push(front(),back());if(layer==='walls')return out;out.push(roof());if(layer==='all')out.push(...verticalTies(380),...verticalTies(2480));return out;}
function counts(items){return parts.map(p=>({id:p.id,count:items.filter(i=>i.block===p.id).length})).filter(r=>r.count);}
g.OBTPCatalogue={pin,parts,joints,assembly,counts,item};if(typeof module!=='undefined')module.exports=g.OBTPCatalogue;
})(globalThis);
