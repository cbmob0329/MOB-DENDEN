const {chromium}=require('../verification-v25/test-runtime.cjs');
const assert=require('assert/strict');
(async()=>{
 const server=await require('../verification-v29/server.cjs')();
 const browser=await chromium.launch({channel:'msedge',headless:true});
 try {
  const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:3});
  const errors=[];page.on('pageerror',e=>errors.push(e.stack));
  await page.goto(server.url+'/MOB_CHILL_LIFE.html');
  await page.waitForFunction(()=>window.CHILL?.cafe?.breadSeats36?.length===12);
  await page.waitForTimeout(1000);
  const state=await page.evaluate(()=>({plots:CHILL.cafe.farm.state.plots.length,seats:CHILL.cafe.breadSeats36.map(s=>s.room),eco:ChillPerformance41.eco,dpr:CHILL.renderer.getPixelRatio(),heart:typeof CHILL.cafe.emitHeart41}));
  assert.equal(state.plots,24);assert.equal(state.seats.filter(s=>s==='cafe').length,6);assert.equal(state.seats.filter(s=>s==='cafe2').length,6);
  assert(state.eco&&state.dpr<=1.25);assert.equal(state.heart,'function');assert.deepEqual(errors,[]);
  console.log('PASS built entry',state);
 } finally {await browser.close();await server.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
