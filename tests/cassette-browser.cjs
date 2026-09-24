const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{const browser=await chromium.launch({headless:true,args:['--use-gl=angle','--use-angle=swiftshader','--enable-webgl']});try{
 const page=await browser.newPage({viewport:{width:1440,height:1050}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(new URL('cassette/', process.env.OBTP_BASE_URL || 'http://127.0.0.1:8765/').href);await page.locator('#status').filter({hasText:'30 cassette instances · geometry ready'}).waitFor();
 assert.equal(await page.locator('canvas').evaluate(c=>c.getContext('webgl').getError()),0);
 await page.locator('#bays').selectOption('8');await page.locator('#status').filter({hasText:'46 cassette instances'}).waitFor();
 await page.locator('#height').selectOption('2700');await page.locator('#skin').check();assert.equal(await page.evaluate(()=>OBTPCassetteView.scene.height),2700);
 await page.locator('#mode').selectOption('object');assert.equal(await page.evaluate(()=>OBTPCassetteView.items.length),1);
 fs.mkdirSync('qa',{recursive:true});
 for(const type of ['panel-frame','wall-seam','corner','wall-floor','wall-roof','slab-seam','frame-frame']){
  await page.locator('#mode').selectOption('connection');await page.locator('#joint').selectOption(type);
  assert.equal(await page.evaluate(()=>OBTPConnectionStudy.type),type);assert(await page.locator('#connection-record').isVisible());assert.match(await page.locator('#detail').textContent(),/HOLD/);
  assert((await page.locator('#connection-record a').count())>0);assert.equal(await page.locator('canvas').evaluate(c=>c.getContext('webgl').getError()),0);
  await page.screenshot({path:'qa/connection-'+type+'.png',fullPage:true});
 }
 await page.locator('#joint').selectOption('wall-floor');const detailDownload=page.waitForEvent('download');await page.locator('#export-detail').click();const dd=await detailDownload;await dd.saveAs('qa/connection-detail.json');const dj=JSON.parse(fs.readFileSync('qa/connection-detail.json'));assert.equal(dj.manufacturingRelease,false);assert.equal(dj.detail.capacity,null);assert(dj.sources.P05);
 await page.locator('#joint-view').selectOption('context');assert.equal(await page.evaluate(()=>OBTPCassetteView.items.length),2);
 await page.locator('#bays').selectOption('1');await page.locator('#joint').selectOption('slab-seam');assert.match(await page.locator('#connection-record').textContent(),/no adjacent/);
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'qa/connection-mobile.png',fullPage:true});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.setViewportSize({width:1440,height:1050});
 await page.locator('#bays').selectOption('8');await page.locator('#joint-view').selectOption('detail');
 await page.locator('#mode').selectOption('assembly');await page.locator('#layer').selectOption('floor');assert.equal(await page.evaluate(()=>OBTPCassetteView.items.length),8);
 await page.locator('#layer').selectOption('all');await page.locator('#bays').selectOption('4');await page.locator('#height').selectOption('2100');await page.locator('#skin').uncheck();
 await page.locator('#explode').fill('40');await page.locator('#explode').dispatchEvent('input');assert.equal(await page.evaluate(()=>OBTPCassetteView.renderer.explode),.4);await page.locator('#reset').click();assert.equal(await page.evaluate(()=>OBTPCassetteView.renderer.explode),0);
 assert(await page.locator('fieldset input').first().isDisabled());
 fs.mkdirSync('qa',{recursive:true});await page.screenshot({path:'qa/cassette-desktop.png',fullPage:true});
 await page.locator('#revision').selectOption('revised');assert.equal(await page.evaluate(()=>OBTPCassetteView.scene.connectionRevision),'revised');
 const download=page.waitForEvent('download');await page.locator('#export').click();const d=await download;await d.saveAs('qa/cassette-rhino.json');const geometry=JSON.parse(fs.readFileSync('qa/cassette-rhino.json'));assert.equal(geometry.manufacturingRelease,false);assert(geometry.parts.length>100);assert.equal(geometry.units,'mm');assert.equal(geometry.connectionRevision,'revised');assert.equal(geometry.connectionResearch.manufacturingRelease,false);assert.equal(geometry.connectionResearch.interfaces.length,geometry.interfaces.length);
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'qa/cassette-mobile.png',fullPage:true});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.locator('a[href="research.html"]').click();await page.locator('h1').first().waitFor();assert.deepEqual(errors,[]);console.log('PASS cassette browser controls, export, desktop/mobile, no page errors');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
