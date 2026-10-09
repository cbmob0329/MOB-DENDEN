const assert=require('node:assert/strict'),Run=require('../mob-play-v21.js'),voice=require('../voice-v21.js');
function started(mode){const r=new Run(mode);r.start();for(let i=0;i<61;i++)r.step(.05);assert.equal(r.phase,'run');assert.equal(r.distance,0);return r;}
const skate=started('skate');for(let i=0;i<10000&&skate.phase==='run';i++)skate.step(.02);assert.equal(skate.phase,'failed');assert.equal(skate.life,0);
const clear=started('skate');for(let i=0;i<10000&&clear.phase==='run';i++)clear.step(.02,{right:clear.lane<3});assert.equal(clear.phase,'goal');const time=clear.time;clear.step(.05);assert.equal(clear.time,time);
const hit=started('skate');hit.distance=69;hit.speed=25;hit.lane=0;hit.step(.05);assert.equal(hit.life,2);const jump=started('skate');jump.distance=59;jump.speed=25;jump.lane=0;jump.use();for(let i=0;i<12;i++)jump.step(.05);assert.equal(jump.life,3);assert(jump.jump>0);
const kart=started('kart');for(let i=0;i<60;i++)kart.step(.05,{accel:true});for(let i=0;i<20;i++)kart.step(.05,{accel:true,left:true,drift:true});kart.step(.05,{accel:true});assert(kart.boost>0);kart.item='shield';kart.use();assert(kart.shield>0&&!kart.item);const shield=kart.shield;kart.use();assert.equal(kart.shield,shield);
for(const text of ['うれしいであります！','ここで休むニョロ～','拙者も遊ぶでござる！','ほぅ～、いいでやんすね～。','ふふっ、楽しみですね！'])assert(!/あります|ニョロ|ござる|やんす|ふふっ/.test(voice.line({key:'nekokoo'},text)));
assert.equal(voice.line({key:'nyoro'},'休むニョロ～'),'休むニョロ～');assert.equal(voice.line({key:'mita'},'ありがとうございます♪'),'ありがとうございます♪');
console.log('PASS collision/failure, steering/clear, jump avoidance, countdown/goal freeze, drift boost, single item use, character voice isolation');
