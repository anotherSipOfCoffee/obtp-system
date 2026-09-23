const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{const browser=await chromium.launch({headless:true,args:['--use-gl=angle','--use-angle=swiftshader','--enable-webgl']});try{
 const page=await browser.newPage({viewport:{width:1440,height:1050}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8765/cassette/');await page.locator('#status').filter({hasText:'30 cassette instances · geometry ready'}).waitFor();
 assert.equal(await page.locator('canvas').evaluate(c=>c.getContext('webgl').getError()),0);
 await page.locator('#bays').selectOption('8');await page.locator('#status').filter({hasText:'46 cassette instances'}).waitFor();
 await page.locator('#height').selectOption('2700');await page.locator('#skin').check();assert.equal(await page.evaluate(()=>OBTPCassetteView.scene.height),2700);
 await page.locator('#mode').selectOption('object');assert.equal(await page.evaluate(()=>OBTPCassetteView.items.length),1);
 for(const type of ['wall-seam','corner','wall-floor','wall-roof','slab-seam']){await page.locator('#mode').selectOption('connection');await page.locator('#joint').selectOption(type);assert.equal(await page.evaluate(()=>OBTPCassetteView.items.length),2);assert.match(await page.locator('#detail').textContent(),/HOLD/);}
 await page.locator('#mode').selectOption('assembly');await page.locator('#layer').selectOption('floor');assert.equal(await page.evaluate(()=>OBTPCassetteView.items.length),8);
 await page.locator('#layer').selectOption('all');await page.locator('#bays').selectOption('4');await page.locator('#height').selectOption('2100');await page.locator('#skin').uncheck();
 await page.locator('#explode').fill('40');await page.locator('#explode').dispatchEvent('input');assert.equal(await page.evaluate(()=>OBTPCassetteView.renderer.explode),.4);await page.locator('#reset').click();assert.equal(await page.evaluate(()=>OBTPCassetteView.renderer.explode),0);
 assert(await page.locator('fieldset input').first().isDisabled());
 fs.mkdirSync('qa',{recursive:true});await page.screenshot({path:'qa/cassette-desktop.png',fullPage:true});
 const download=page.waitForEvent('download');await page.locator('#export').click();const d=await download;await d.saveAs('qa/cassette-rhino.json');const geometry=JSON.parse(fs.readFileSync('qa/cassette-rhino.json'));assert.equal(geometry.manufacturingRelease,false);assert(geometry.parts.length>100);assert.equal(geometry.units,'mm');
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'qa/cassette-mobile.png',fullPage:true});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.locator('a[href="research.html"]').click();await page.locator('h1').first().waitFor();assert.deepEqual(errors,[]);console.log('PASS cassette browser controls, export, desktop/mobile, no page errors');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
