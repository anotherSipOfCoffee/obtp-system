const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{const browser=await chromium.launch({headless:true,args:['--use-gl=angle','--use-angle=swiftshader','--enable-webgl']});try{
 const page=await browser.newPage({viewport:{width:1440,height:1100}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8765/cassette/details/');await page.locator('#status').filter({hasText:'Geometry ready'}).waitFor();
 for(const key of ['wall-seam','floor-seam','roof-seam','corner','wall-floor','wall-roof']){
  await page.locator('#joint').selectOption(key);const pass=key.endsWith('seam');assert.match(await page.locator('#status').textContent(),pass?/passes conditionally/:/fails/);
  const before=await page.evaluate(()=>OBTPDetailView.scene.detail.checks);await page.locator('#cutaway').uncheck();assert.deepEqual(await page.evaluate(()=>OBTPDetailView.scene.detail.checks),before);await page.locator('#cutaway').check();
  assert.equal(await page.locator('#checks tr').count(),2);assert.equal(await page.locator('canvas').evaluate(c=>c.getContext('webgl').getError()),0);
 }
 await page.locator('#joint').selectOption('wall-seam');await page.locator('#explode').fill('50');await page.locator('#explode').dispatchEvent('input');assert.equal(await page.evaluate(()=>OBTPDetailView.renderer.explode),.5);await page.locator('#reset').click();assert.equal(await page.locator('#explode').inputValue(),'0');
 fs.mkdirSync('qa',{recursive:true});await page.screenshot({path:'qa/detail-wall-seam.png',fullPage:true});
 await page.locator('#joint').selectOption('wall-floor');await page.screenshot({path:'qa/detail-wall-floor-rejected.png',fullPage:true});
 const downloadPromise=page.waitForEvent('download');await page.locator('#export').click();const download=await downloadPromise;const data=JSON.parse(fs.readFileSync(await download.path(),'utf8'));assert.equal(data.manufacturingRelease,false);assert.equal(data.capacity,null);assert.equal(data.receiverPenetration,57);assert.equal(data.screenPass,false);
 await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.locator('#diagram').scrollIntoViewIfNeeded();await page.screenshot({path:'qa/detail-mobile.png'});
 await page.goto('http://127.0.0.1:8765/cassette/');await page.locator('a[href="details/index.html"]').click();await page.locator('#status').filter({hasText:'Geometry ready'}).waitFor();
 assert.deepEqual(errors,[]);console.log('PASS: six connection detail views, rejection labels, view-invariant checks, WebGL, cutaway, separation/reset, honest inspection export, mobile layout and System entry link.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
