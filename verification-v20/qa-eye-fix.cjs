const fs=require('fs'),assert=require('assert'),{chromium}=require('C:/Users/CB-Me/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
const b=await chromium.launch({channel:'msedge',headless:true,args:['--allow-file-access-from-files']}),p=await b.newPage({viewport:{width:1100,height:900}}),errors=[];
p.on('pageerror',e=>errors.push(e.message));
await p.goto('file:///C:/Users/CB-Me/Documents/GitHub/MOB-DENDEN/MOB_CHILL_LIFE.html');
await p.waitForFunction(()=>window.CHILL?.actors.every(a=>a.lifeReady20));
const results=await p.evaluate(()=>{
CHILL.reset();CHILL.setPaused(true);const c=CHILL.cafe;c.clock14=1175;c.routine.plan=()=>{};c.townActions19.next=1e9;c.arcadeNext=CHILL.actors.map(()=>1e9);c.bagIdle=CHILL.actors.map(()=>1e9);
for(const a of CHILL.actors){a.timer=a.cafeWait=1e9;a.phase=null;a.state='idle';a.path=[];a.cafePath=[];a.bathMode=a.arcadeMode=a.cafeMode=null;a.routineRest=a.routineNight=false;}
window.stepEye=()=>{c.clock14+=.2;CHILL.advance(.2);CHILL.tick(0);};
const start=CHILL.actors.map(a=>c.sleep20.request(a,null,true));for(let i=0;i<650;i++)stepEye();
const a=CHILL.actors[3],sleep={phase:a.rest20?.phase,place:a.rest20?.place.id,usesSleep:a.restSprite20?.material.map===a.life20.sleepSeat[Math.floor(a.rest20.time/1.8)%2]};
c.setView('cafe');CHILL.tick(0);return {start,sleep};});
assert(results.start.every(Boolean));assert.equal(results.sleep.phase,'sleep');assert(results.sleep.usesSleep);
await p.screenshot({path:__dirname+'/iruka-sleep-before-wake.png'});
results.wake=await p.evaluate(()=>{const c=CHILL.cafe,a=CHILL.actors[3];c.clock14=350;for(let i=0;i<180;i++)stepEye();return{rest:!!a.rest20,transit:!!a.transit20,planeVisible:!!a.restPlane20?.visible,spriteVisible:!!a.restSprite20?.visible,room:a.room};});
assert(!results.wake.rest&&!results.wake.planeVisible&&!results.wake.spriteVisible);
results.service=await p.evaluate(()=>{const c=CHILL.cafe,a=CHILL.actors[3],guest=CHILL.actors[4];CHILL.kitchen.inventory.soup=3;const deposit=c.ledger.deposit(CHILL.kitchen.inventory,'soup',3,c.c.save),visit=guest.room==='cafe'||c.visit(guest),frames=[],states=[];let served=false;window.carryCapture=null;
for(let i=0;i<1300;i++){stepEye();const idx=a.life20.walk.indexOf(a.sprite.material.map);if(idx>=0&&!frames.includes(idx))frames.push(idx);const mode=c.service?.stage;if(mode&&!states.includes(mode))states.push(mode);if(mode==='carry'&&idx>=0&&a.cafePath.length&&!window.carryCapture){window.carryCapture={idx,dir:a.walkDirection,image:a.sprite.material.map.image.toDataURL(),rest:!!a.rest20};}if(CHILL.actors.some(g=>g.id!==3&&g.cafeMode==='eating'&&g.mealKind==='soup')){served=true;break;}}
return{deposit,visit,served,frames,states,carry:window.carryCapture,remaining:c.ledger.stock,rest:!!a.rest20,sleepSpriteVisible:!!a.restSprite20?.visible,guest:{mode:guest.cafeMode,room:guest.room,rest:guest.rest20?.phase},seats:c.seats};});
console.log(JSON.stringify({...results,service:{...results.service,carry:!!results.service.carry}}));
assert(results.service.deposit&&results.service.visit&&results.service.served);assert(results.service.carry);assert(!results.service.rest&&!results.service.sleepSpriteVisible);assert(results.service.states.includes('carry')&&(results.service.states.includes('serve')||results.service.states.includes('land')));
const art=await p.evaluate(()=>({pink:[...CHILL.actors[1].life20.sleepLie,...CHILL.actors[1].life20.sleepSeat].map(t=>t.image.toDataURL()),walk:CHILL.actors[3].life20.walk.map(t=>t.image.toDataURL()),carry:window.carryCapture.image}));
const inspect=await b.newPage({viewport:{width:1200,height:950}});const ref=fs.readFileSync('C:/Users/CB-Me/Documents/GitHub/MOB-DENDEN/assets/pink/idle.png').toString('base64');
await inspect.setContent('<style>body{background:#ddd;font:20px sans-serif}section{display:flex;gap:12px}img{width:210px;height:210px;object-fit:contain;background:white}h2{font-size:20px}</style><h2>Original Pink / corrected sleeping poses (2 lying + 2 seated)</h2><section><img src="data:image/png;base64,'+ref+'">'+art.pink.map(s=>'<img src="'+s+'">').join('')+'</section><h2>Irukaeru front / back / left / right, 2 frames each</h2><section>'+art.walk.slice(0,4).map(s=>'<img src="'+s+'">').join('')+'</section><section>'+art.walk.slice(4).map(s=>'<img src="'+s+'">').join('')+'</section><h2>Actual carrying frame after waking</h2><img src="'+art.carry+'">');
await inspect.screenshot({path:__dirname+'/eye-fix-comparison.png',fullPage:true});
delete results.service.carry.image;assert.deepEqual(errors,[]);fs.writeFileSync(__dirname+'/eye-fix-results.json',JSON.stringify({results,errors},null,2));await b.close();console.log(JSON.stringify(results,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
