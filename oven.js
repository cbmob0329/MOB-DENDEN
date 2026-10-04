/* One saved batch, based on wall-clock time. No automatic material refills. */
(()=>{'use strict';
const duration=60000,clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
ChillRoom.prototype.buildOven=function(f){
 const b=(...a)=>this.box(f.group,...a),c=(...a)=>this.cyl(f.group,...a);f.w=1.15;f.d=1.3;
 f.sockets.entry=new THREE.Vector3(0,0,1.2);f.sockets.hands=new THREE.Vector3(0,.55,.61);
 const enamel=this.material('oven-enamel','#c6cfb4'),dark=this.material('oven-dark','#493f35');
 b(0,.16,0,1.15,.2,.94,this.oak);b(0,.22,-.39,1.1,.12,.15,dark);b(0,.54,-.43,1.12,.66,.1,enamel);
 for(const x of [-.54,.54])b(x,.54,0,.1,.68,.95,enamel);b(0,.91,0,1.2,.11,1.02,this.cream);b(0,.25,0,1.08,.07,.9,dark);
 for(const x of [-.37,.37])c(x,.075,.24,.055,.055,.15,this.wood);
 const cavity=new THREE.MeshStandardMaterial({color:'#a35c26',emissive:'#ff8a26',emissiveIntensity:0,roughness:.75});b(0,.52,-.365,.98,.49,.02,cavity);
 const door=new THREE.Group();door.position.set(0,.25,.5);f.group.add(door);
 const glass=new THREE.MeshStandardMaterial({color:'#927456',transparent:true,opacity:.26,roughness:.3,depthWrite:false});this.box(door,0,.27,0,.93,.49,.035,glass);
 for(const x of [-.49,.49])this.box(door,x,.27,.005,.045,.55,.06,enamel);
 for(const y of [.015,.53])this.box(door,0,y,.005,1.02,.04,.06,enamel);
 this.box(door,0,.47,.075,.48,.045,.055,this.wood);
 const tray=new THREE.Group();tray.position.set(0,.34,.02);f.group.add(tray);this.box(tray,0,0,0,.85,.025,.65,'#92958a');
 const cake=new THREE.Group();tray.add(cake);cake.position.y=.055;
 const dough=new THREE.MeshStandardMaterial({color:'#eddab0',roughness:.9});this.cyl(cake,0,0,0,.23,.23,.055,dough);this.cyl(cake,0,.065,0,.24,.24,.055,dough);this.cyl(cake,0,.032,0,.219,.219,.025,'#75452d');cake.visible=false;
 const light=new THREE.PointLight('#ffad4f',0,3,2);light.position.set(0,.59,.3);f.group.add(light);
 const leds=[];for(let i=0;i<4;i++){let m=new THREE.MeshStandardMaterial({color:'#879077',emissive:'#e8b753',emissiveIntensity:0}),o=b(-.22+i*.145,.977,.25,.08,.025,.06,m);leds.push(o)}
 const ingredients=[];for(let i=0;i<10;i++){let o=new THREE.Mesh(new THREE.SphereGeometry(i<5?.036:.046,7,6),new THREE.MeshStandardMaterial({color:i<5?'#773f32':'#ead7ae'}));f.group.add(o);ingredients.push(o)}
 const steam=[];for(let i=0;i<5;i++){let o=new THREE.Mesh(new THREE.SphereGeometry(.065,7,6),new THREE.MeshBasicMaterial({color:'#fff9e7',transparent:true,opacity:0,depthWrite:false}));f.group.add(o);steam.push(o)}
 f.oven={door,tray,cake,dough,cavity,light,leds,ingredients,steam};
};
window.ChillKitchen=class ChillKitchen{
 constructor(room,hooks){this.room=room;this.hooks=hooks;this.reset();this.lastNotice=null;this.lastUI='';}
 reset(){this.inventory={wheat:10,beans:10,dorayaki:0};this.batch=null;this.lastNotice=null;this.servedAt=0;}
 serialize(){return{v:1,inventory:{...this.inventory},batch:this.batch?{...this.batch}:null};}
 restore(data){this.reset();if(!data||data.v!==1)return;const n=v=>Number.isSafeInteger(v)&&v>=0?Math.min(v,999999):0;this.inventory={wheat:n(data.inventory?.wheat),beans:n(data.inventory?.beans),dorayaki:n(data.inventory?.dorayaki)};const b=data.batch;if(b&&(b.status==='baking'||b.status==='ready')&&Number.isFinite(b.startedAt)&&Number.isFinite(b.endsAt)&&b.endsAt-b.startedAt===duration)this.batch={status:b.status,startedAt:b.startedAt,endsAt:b.endsAt};}
 transaction(fn){const previous=this.serialize();fn();if(!this.hooks.save()){this.restore(previous);this.hooks.toast('保存できませんでした。ブラウザの保存設定を確認してください。');return false}this.render();return true;}
 start(){this.update();if(this.batch){this.hooks.toast(this.batch.status==='ready'?'焼けています。先に受け取ってください。':'いま焼いています。ひとつずつ作りましょう。');return false}if(this.inventory.wheat<1||this.inventory.beans<1){this.hooks.toast('小麦と小豆が1個ずつ必要です。');return false}const now=Date.now();const ok=this.transaction(()=>{this.inventory.wheat--;this.inventory.beans--;this.batch={status:'baking',startedAt:now,endsAt:now+duration}});if(ok){this.hooks.toast('小麦と小豆を投入。じっくり1分、焼きましょう。');this.hooks.tone(330);this.hooks.started?.()}return ok;}
 collect(){this.update();if(this.batch?.status!=='ready')return false;const ok=this.transaction(()=>{this.inventory.dorayaki++;this.batch=null;this.servedAt=Date.now()});if(ok){this.hooks.toast('焼きたてどら焼きを1個受け取りました。');this.hooks.tone(880)}return ok;}
 update(){const now=Date.now();if(this.batch?.status==='baking'&&now>=this.batch.endsAt){this.batch.status='ready';this.hooks.save();if(this.lastNotice!==this.batch.endsAt){this.lastNotice=this.batch.endsAt;this.hooks.toast('こんがり、できあがり！ オーブンから受け取れます。');this.hooks.tone(740)}}return now;}
 open(){this.update();this.hooks.modal('小さなオーブン',`<div class="oven-panel"><p class="oven-intro">小麦と小豆をひとつずつ。焼きたてを、ふたりへ。</p><div class="pantry large"><span>小麦 <b data-wheat></b></span><span>小豆 <b data-beans></b></span><span>どら焼き <b data-dorayaki></b></span></div><div class="oven-status" id="ovenStatus" role="status"></div><div class="bake-track"><i id="bakeProgress"></i></div><p id="ovenTime"></p><button class="primary" id="ovenStart">材料を入れて焼く</button><button class="primary" id="ovenCollect">焼きたてを受け取る</button><p class="oven-note">小麦1 ＋ 小豆1 → どら焼き1<br>実時間で60秒。画面を閉じても焼成は進みます。<br>材料の自動補充はありません。</p></div>`);document.querySelector('#ovenStart').onclick=()=>this.start();document.querySelector('#ovenCollect').onclick=()=>this.collect();this.lastUI='';this.render();document.querySelector('#modal').scrollTop=0;}
 render(){const now=this.update(),batch=this.batch,progress=batch?clamp((now-batch.startedAt)/duration,0,1):0,ready=batch?.status==='ready',baking=batch?.status==='baking',remaining=batch?Math.max(0,Math.ceil((batch.endsAt-now)/1000)):0;
 const stamp=[this.inventory.wheat,this.inventory.beans,this.inventory.dorayaki,batch?.status,remaining,!!document.querySelector('#ovenStart')].join(':');if(stamp!==this.lastUI){this.lastUI=stamp;for(let key of ['wheat','beans','dorayaki'])document.querySelectorAll('[data-'+key+']').forEach(e=>e.textContent=this.inventory[key]);const button=document.querySelector('#ovenButton');if(button){button.textContent=ready?'焼けた！':baking?'焼成 '+remaining+'秒':'オーブン';button.classList.toggle('ready',ready)}const status=document.querySelector('#ovenStatus');if(status){status.textContent=ready?'こんがり、できあがり':baking?'ふっくら焼いています':'次のひとつを、焼きましょう';document.querySelector('#ovenTime').textContent=ready?'1個できました。受け取ると所持数に加わります。':baking?'あと '+remaining+' 秒':'小麦1個と小豆1個を使います。';document.querySelector('#ovenStart').disabled=!!batch||this.inventory.wheat<1||this.inventory.beans<1;document.querySelector('#ovenCollect').hidden=!ready;document.querySelector('#ovenStart').hidden=ready}}
 const bar=document.querySelector('#bakeProgress');if(bar)bar.style.width=(progress*100)+'%';const f=this.room.furniture.oven?.oven;if(!f)return;const age=batch?(now-batch.startedAt)/1000:999,opening=ready?1:baking&&age<2?1-clamp(age/2,0,1):0;f.door.rotation.x=opening*1.22;f.tray.position.z=.02+opening*.39;f.cake.visible=!!batch;f.cake.scale.setScalar(.75+progress*.25);f.dough.color.copy(new THREE.Color('#eddab0')).lerp(new THREE.Color('#c98b43'),progress);f.cavity.emissiveIntensity=baking?.8+.1*Math.sin(now/350):ready?.24:0;f.light.intensity=baking?2.2+.3*Math.sin(now/350):ready?1.2:0;f.leds.forEach((o,i)=>{o.material.emissiveIntensity=ready?1+.4*Math.sin(now/400):baking&&progress>i/4?.9:0});f.ingredients.forEach((o,i)=>{const t=clamp((age-i*.08)/1.2,0,1);o.visible=baking&&age<2&&t<1;o.position.set((i<5?-.3:.3)*(1-t),.42+(1-t)*1.0+Math.sin(t*Math.PI)*.15,.1+(1-t)*.5);o.scale.setScalar(1-t*.3)});f.steam.forEach((o,i)=>{let t=(now/1800+i*.2)%1;o.visible=ready||baking&&progress>.65;o.position.set(Math.sin(i*2.3+t)*.2,1+t*.8,.1);o.scale.setScalar(.5+t);o.material.opacity=o.visible?(1-t)*.23:0});
 }
};})();
