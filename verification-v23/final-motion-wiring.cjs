const fs=require('fs');
let f='residents-v23.js',s=fs.readFileSync(f,'utf8');
s=s.replace("if(p.domestic){", "if(/^turnDance/.test(name)&&p.turnjoy)return p.turnjoy[n%16];if(/^taso/.test(name)&&p.taso)return p.taso[n%16];if(/^music|^dance/.test(name)&&p.dance)return p.dance[n%16];if(/joy|cheer_cheeks/.test(name)&&p.cheeks)return p.cheeks[6+n%6];if(p.domestic){");
s=s.replace("this.c.room.static.visible=false;this.group.visible=false;", "this.group.visible=false;");
s=s.replace("else if(a.social23||a.speech>0)","else if(a.key==='denden'&&p.cheeks&&(a.phase?.pose==='joy'||a.arcadeJoyTime>0&&!a.arcadeSad14))tex=p.cheeks[Math.min(15,Math.floor((a.phaseTime||this.clock14)*5)%16)];else if(a.key==='denden'&&p.turnjoy&&a.phase?.pose==='turnDance')tex=p.turnjoy[Math.floor(a.phaseTime*5)%16];else if(a.key==='denden'&&p.dance&&['music','dance'].includes(a.phase?.pose))tex=p.dance[Math.floor(a.phaseTime*5)%16];else if(a.social23||a.speech>0&&!a.phase)");
fs.writeFileSync(f,s);
f='verification-v23/prepare-assets.cjs';s=fs.readFileSync(f,'utf8').replace('town|domestic)', 'town|domestic|turnjoy|cheeks)');fs.writeFileSync(f,s);
f='verification-v23/behaviors.cjs';s=fs.readFileSync(f,'utf8').replace("a.bathMode==='entryWait'&&a.propPark23","['enter','soak'].includes(a.bathMode)&&a.propPark23").replace('result.bath.picked);','result.bath.picked&&result.bath.parkedBeforeSoak);');fs.writeFileSync(f,s);
