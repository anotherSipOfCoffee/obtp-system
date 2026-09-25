const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{const browser=await chromium.launch({headless:true,args:['--use-gl=angle','--use-angle=swiftshader','--enable-webgl']});try{
 const page=await browser.newPage({viewport:{width:1440,height:1050}}),errors=[];page.on('pageerror',e=>errors.push(e.message));fs.mkdirSync('qa',{recursive:true});
 const state=fn=>page.evaluate(fn),view=v=>page.locator('[data-view="'+v+'"]').click(),type=t=>page.locator('[data-type="'+t+'"]').click();
 await page.goto(new URL('cassette/',process.env.OBTP_BASE_URL||'http://127.0.0.1:8765/').href);await page.waitForFunction(()=>window.OBTPCassetteView?.scene.connectionRevision==='revised');
 assert.equal(await page.locator('aside select').first().getAttribute('id'),'version');assert.equal(await state(()=>OBTPCassetteView.items.length),31);
 await type('Floors');assert.equal(await page.locator('#part option').count(),8);assert.equal(await state(()=>OBTPCassetteView.renderer.object),true);
 await page.locator('#skin').check();assert.equal(await state(()=>OBTPCassetteView.renderer.meshes.values().next().value.parts.length),7);
 const vertices=await state(()=>OBTPCassetteView.catalogue.find(e=>e.id===OBTPCassetteView.selected).model.assets.map(a=>a.vertices));
 await page.locator('#explode').fill('70');await page.locator('#explode').dispatchEvent('input');
 const rendered=await state(()=>{const r=OBTPCassetteView.renderer,m=r.meshes.values().next().value;return {object:r.object,explode:r.explode,offsets:m.parts.map(p=>p.asset.explode.map(v=>v*r.explode))};});
 assert.equal(rendered.object,true);assert.equal(rendered.explode,.7);assert(rendered.offsets.every(v=>v.some(n=>n!==0)));assert.notDeepEqual(rendered.offsets[0],rendered.offsets[1]);
 await page.screenshot({path:'qa/floor-constituent-parts-exploded.png',fullPage:true});
 await page.locator('#part').selectOption('edge-a');assert.equal(await state(()=>OBTPCassetteView.renderer.isolate),'0');assert.match(await page.locator('#status').textContent(),/1 visible part/);
 await page.locator('#part').selectOption('blocking-2263.5');assert.equal(await state(()=>OBTPCassetteView.part),'blocking-2263.5');await page.screenshot({path:'qa/cross-member-isolated.png',fullPage:true});
 await page.locator('#reset').click();assert.equal(await page.locator('#part').inputValue(),'');assert.equal(await state(()=>OBTPCassetteView.renderer.explode),0);assert.deepEqual(await state(()=>OBTPCassetteView.catalogue.find(e=>e.id===OBTPCassetteView.selected).model.assets.map(a=>a.vertices)),vertices);
 await view('connection');await page.locator('#joint').selectOption('frame-frame');assert.equal(await page.locator('#occurrence option').count(),6);assert.equal(await state(()=>OBTPCassetteView.items.length),2);await page.locator('#occurrence').selectOption({index:5});await page.screenshot({path:'qa/internal-blocking-joint.png',fullPage:true});
 await page.locator('#joint').selectOption('panel-frame');assert((await page.locator('#occurrence option').count())>=6);
 assert.equal(await page.locator('#joint option[value="roof-seam"]').count(),0);await page.locator('#connection-scope').selectOption('all');
 for(const key of ['wall-seam','corner','wall-floor','wall-roof','floor-seam','roof-seam']){
  await page.locator('#joint').selectOption(key);assert.equal(await page.locator('#joint-view').inputValue(),'measured');assert.match(await page.locator('#status').textContent(),/passes/);
  assert.equal(await state(()=>OBTPCassetteView.exportDetail.capacity),null);assert.equal(await state(()=>OBTPCassetteView.renderer.gl.getError()),0);
 }
 await page.locator('#joint').selectOption('corner');await page.locator('#revision').selectOption('baseline');assert.match(await page.locator('#status').textContent(),/fails/);await page.locator('#revision').selectOption('revised');assert.match(await page.locator('#status').textContent(),/passes/);
 const measuredDownload=page.waitForEvent('download');await page.locator('#export-detail').click();const md=await measuredDownload;const probe=JSON.parse(fs.readFileSync(await md.path(),'utf8'));assert.equal(probe.revision,'revised');assert.equal(probe.capacity,null);assert.equal(probe.manufacturingRelease,false);
 await page.screenshot({path:'qa/integrated-measured-joint.png',fullPage:true});
 await page.locator('#joint-view').selectOption('detail');assert.match(await page.locator('#detail').textContent(),/HOLD/);assert((await page.locator('#connection-record a').count())>0);
 const conceptDownload=page.waitForEvent('download');await page.locator('#export-detail').click();const cd=await conceptDownload;assert.equal(JSON.parse(fs.readFileSync(await cd.path(),'utf8')).detail.capacity,null);
 await page.locator('#joint-view').selectOption('context');assert.equal(await state(()=>OBTPCassetteView.items.length),2);
 await page.locator('#joint').selectOption('foundation');assert(await page.locator('#empty-view').isVisible());assert.equal(await state(()=>OBTPCassetteView.items.length),0);assert.match(await page.locator('#status').textContent(),/Undesigned/);
 await type('Connectors');assert.equal(await page.locator('#objects button').count(),11);
 for(const id of ['HBS580','HBS5120','splice','corner-angle','base-tie','roof-tie','frame-angle']){await page.locator('[data-connector="'+id+'"]').click();assert.equal(await state(()=>OBTPCassetteView.renderer.meshes.values().next().value.parts.length),1);assert(await page.locator('#explode').isDisabled());}
 await page.locator('[data-connector="HBS580"]').click();await page.screenshot({path:'qa/connector-catalogue.png',fullPage:true});
 await page.locator('[data-open-joint="wall-seam"]').click();assert.equal(await page.locator('#joint').inputValue(),'wall-seam');await page.locator('[data-open-connector="HBS580"]').click();assert.equal(await state(()=>OBTPCassetteView.type),'Connectors');
 for(const id of ['ABR','WHT','sheathing-fastener','foundation-anchor']){await page.locator('[data-connector="'+id+'"]').click();assert(await page.locator('#empty-view').isVisible());assert.equal(await state(()=>OBTPCassetteView.items.length),0);}
 await type('Walls');await page.locator('#height').selectOption('2700');assert((await page.locator('#part option[value="sheet-seam-backing"]').count())===1);await page.locator('#skin').check();await page.locator('#explode').fill('60');await page.locator('#explode').dispatchEvent('input');await page.screenshot({path:'qa/wall-constituent-parts-exploded.png',fullPage:true});
 await type('Roofs');await view('assembly');await page.locator('#bays').selectOption('8');assert.equal(await state(()=>OBTPCassetteView.items.length),47);await page.locator('#layer').selectOption('floor');assert.equal(await state(()=>OBTPCassetteView.items.length),9);await page.locator('#layer').selectOption('all');await page.locator('#bays').selectOption('4');await page.locator('#height').selectOption('2100');
 const download=page.waitForEvent('download');await page.locator('#export').click();const d=await download;const geometry=JSON.parse(fs.readFileSync(await d.path(),'utf8'));assert.equal(geometry.manufacturingRelease,false);assert.equal(geometry.connectionRevision,'revised');assert(geometry.parts.length>100);assert(geometry.inspectionRegister.some(r=>r.id==='foundation'&&r.status==='Undesigned'));assert(geometry.interfaces.every(j=>j.capacity===null&&j.fasteners===null));
 assert(await page.locator('fieldset input').first().isDisabled());
 await page.setViewportSize({width:390,height:844});
 for(const t of ['Walls','Floors','Connectors']){await type(t);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
 await type('Floors');await view('connection');await page.locator('#connection-scope').selectOption('all');await page.locator('#joint').selectOption('wall-floor');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.screenshot({path:'qa/inspection-mobile.png',fullPage:true});
 await page.locator('#version').selectOption('../index.html');await page.waitForFunction(()=>window.OBTPSystem?.selected==='W-S');await page.locator('#version').selectOption('cassette/index.html');await page.waitForFunction(()=>window.OBTPCassetteView?.scene.connectionRevision==='revised');
 assert.deepEqual(errors,[]);console.log('PASS: real part explosion/isolation/reset, six blocking contacts, connector objects and honest unmodelled entries, related connections, integrated original/revised probes, exports, assembly controls, mobile and version navigation.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
