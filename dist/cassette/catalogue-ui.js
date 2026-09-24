'use strict';
(()=>{
 const $=id=>document.getElementById(id);
 const family=id=>id.startsWith('W')?'Walls':id.startsWith('F')?'Floors':'Roofs';
 let type='Walls';
 function button(text,data,value,pressed){const b=document.createElement('button');b.textContent=text;b.dataset[data]=value;b.setAttribute('aria-pressed',String(pressed));return b;}
 function sync(){
  const state=window.OBTPCassetteView;if(!state)return;
  const mode=$('mode').value,models=state.scene.models,selected=$('object').value;
  if(mode==='object')type=family(selected);
  $('types').replaceChildren(...['Walls','Floors','Roofs'].map(t=>button(t+' · '+models.filter(m=>family(m.id)===t).length,'type',t,t===type)));
  $('objects').replaceChildren(...models.filter(m=>family(m.id)===type).map(m=>button(m.id,'part',m.id,mode==='object'&&selected===m.id)));
  document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===mode)));
  $('assembly-controls').hidden=mode!=='assembly';
 }
 document.addEventListener('cassette-render',sync);
 document.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  if(b.dataset.type){type=b.dataset.type;$('object').value=window.OBTPCassetteView.scene.models.find(m=>family(m.id)===type).id;$('mode').value='object';}
  else if(b.dataset.part){$('object').value=b.dataset.part;$('mode').value='object';}
  else if(b.dataset.view){$('mode').value=b.dataset.view;}
  else return;
  $('mode').dispatchEvent(new Event('change'));window.OBTPCassetteView.renderer.reset();
 });sync();
})();
