import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js';

const $ = (id) => document.getElementById(id);
const root = $('gameRoot');
const titleScreen = $('titleScreen');
const mainScreen = $('mainScreen');
const titleStartBtn = $('titleStartBtn');
const battleStartBtn = $('battleStartBtn');
const howToBtn = $('howToBtn');
const settingsBtn = $('settingsBtn');
const modalBackdrop = $('modalBackdrop');
const howToModal = $('howToModal');
const settingsModal = $('settingsModal');
const shakeToggle = $('shakeToggle');
const flashToggle = $('flashToggle');
const autoAimToggle = $('autoAimToggle');
const bestScoreEl = $('bestScore');
const bestWaveEl = $('bestWave');
const hudEl = $('hud');
const crosshairEl = $('crosshair');
const mobileControlsEl = $('mobileControls');
const helpEl = $('help');
const questEl = $('quest');
const hpEl = $('hp');
const waveEl = $('wave');
const scoreEl = $('score');
const levelTextEl = $('levelText');
const xpTextEl = $('xpText');
const xpFillEl = $('xpFill');
const specialTextEl = $('specialText');
const specialFillEl = $('specialFill');
const lockTextEl = $('lockText');
const bossHud = $('bossHud');
const bossFillEl = $('bossFill');
const levelUpOverlay = $('levelUpOverlay');
const levelChoicesEl = $('levelChoices');
const messageEl = $('message');
const messageText = $('messageText');
const speakerEl = $('speaker');
const toastEl = $('toast');
const damageFlashEl = $('damageFlash');
const attackBtn = $('attackBtn');
const dashBtn = $('dashBtn');
const specialBtn = $('specialBtn');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x8bcdf6);
scene.fog = new THREE.Fog(0xb8e5ff, 30, 84);

const camera = new THREE.PerspectiveCamera(56, innerWidth / innerHeight, 0.1, 220);
const renderer = new THREE.WebGLRenderer({ antialias:true, powerPreference:'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.55));
renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
root.prepend(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff, 0x5b7561, 1.18));
const sun = new THREE.DirectionalLight(0xffffff, 1.35);
sun.position.set(18,26,14);
sun.castShadow = true;
sun.shadow.mapSize.set(1024,1024);
sun.shadow.camera.left=-45; sun.shadow.camera.right=45; sun.shadow.camera.top=45; sun.shadow.camera.bottom=-45;
scene.add(sun);

const mats = {
  sand:new THREE.MeshLambertMaterial({color:0xd4bd8d}),
  sand2:new THREE.MeshLambertMaterial({color:0xc8ae78}),
  road:new THREE.MeshLambertMaterial({color:0x9f8760}),
  dark:new THREE.MeshLambertMaterial({color:0x202936}),
  black:new THREE.MeshLambertMaterial({color:0x11151d}),
  pink:new THREE.MeshLambertMaterial({color:0xf05f96}),
  pink2:new THREE.MeshLambertMaterial({color:0xd73f79}),
  yellow:new THREE.MeshLambertMaterial({color:0xf4d63f}),
  yellow2:new THREE.MeshLambertMaterial({color:0xdfbe26}),
  gun:new THREE.MeshLambertMaterial({color:0x2a313d}),
  glow:new THREE.MeshBasicMaterial({color:0xffe36b}),
  bullet:new THREE.MeshBasicMaterial({color:0xffe45a}),
  heart:new THREE.MeshBasicMaterial({color:0xff6d8a}),
  exp:new THREE.MeshBasicMaterial({color:0x8ee6ff}),
};

const enemyPalette = {
  chaser: 0x7d38d1,
  gunner: 0x24b8d7,
  shield: 0x768b58,
  rusher: 0xe05a59,
  boss: 0xf08a27,
};

const keys = {up:false,down:false,left:false,right:false};
let attackHeld = false;
const blockers=[];
const projectiles=[];
const enemyProjectiles=[];
const particles=[];
const pickups=[];
const enemies=[];
let lockTarget=null;
let bossRef=null;
let toastTimer=0;

const saveKey='mob-gun-cat-v04';
function loadSave(){
  try{
    const raw=JSON.parse(localStorage.getItem(saveKey)||'{}');
    return {bestScore:Number(raw.bestScore)||0,bestWave:Math.max(1,Number(raw.bestWave)||1)};
  }catch{return {bestScore:0,bestWave:1};}
}
function saveBest(){
  try{localStorage.setItem(saveKey,JSON.stringify({bestScore:state.bestScore,bestWave:state.bestWave}));}catch{}
}
const saved=loadSave();

const state={
  hp:6,maxHp:6,wave:1,score:0,
  level:1,xp:0,xpNext:100,pendingLevelUps:0,levelUpOpen:false,
  damage:1,fireInterval:.145,bulletSpeed:20,moveSpeed:6.2,bulletCount:1,pierce:0,crit:.08,
  special:0,specialMax:100,specialGain:1,
  waveClearDelay:0,messageQueue:[],messageOpen:false,
  invincible:0,shootCooldown:0,dashCooldown:0,dashTimer:0,shotSide:0,
  gameOver:false,inGame:false,bestScore:saved.bestScore,bestWave:saved.bestWave,
  cameraShake:true,damageFlash:true,autoAim:true,shakeStrength:0,damageFlashTimer:0,
};

function boxMesh(g,m){const o=new THREE.Mesh(g,m);o.castShadow=true;o.receiveShadow=true;return o;}
function box(w,h,d,mat,x,y,z,cast=true){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);m.castShadow=cast;m.receiveShadow=true;scene.add(m);return m;}
function addBlocker(x,z,w,d){blockers.push({x,z,w,d});}
function collides(x,z,r=.45){if(x<-39||x>39||z<-39||z>39)return true;return blockers.some(b=>Math.abs(x-b.x)<b.w/2+r&&Math.abs(z-b.z)<b.d/2+r);}

// arena
box(84,1,84,mats.sand,0,-.5,0,false);
for(let x=-38;x<=38;x+=4){for(let z=-38;z<=38;z+=4){if((Math.abs(x+z))%10===0)box(3.95,.04,3.95,mats.sand2,x,.02,z,false);}}
box(74,.06,10,mats.road,0,.03,0,false);box(10,.06,74,mats.road,0,.03,0,false);
function crate(x,z,w=2,h=2,d=2,color=0x687281){const mat=new THREE.MeshLambertMaterial({color});box(w,h,d,mat,x,h/2,z);addBlocker(x,z,w,d);}
function barrel(x,z){const g=new THREE.Group();const c1=new THREE.Mesh(new THREE.CylinderGeometry(.55,.55,1.25,10),new THREE.MeshLambertMaterial({color:0x4b5c6a}));c1.position.y=.62;g.add(c1);const cap=new THREE.Mesh(new THREE.CylinderGeometry(.58,.58,.12,10),new THREE.MeshLambertMaterial({color:0x9db4c8}));cap.position.y=.08;g.add(cap);const cap2=cap.clone();cap2.position.y=1.16;g.add(cap2);g.position.set(x,0,z);scene.add(g);addBlocker(x,z,1.1,1.1);}
[[-18,-16],[-18,16],[18,-16],[18,16],[-28,0],[28,0],[0,-28],[0,28],[-6,13],[6,-13],[-13,-6],[13,6]].forEach(p=>crate(p[0],p[1],2.4,2.4,2.4));
[[-23,8],[-23,-8],[23,8],[23,-8],[-8,23],[8,23],[-8,-23],[8,-23]].forEach(p=>barrel(p[0],p[1]));
for(let i=0;i<18;i++){const x=Math.cos(i*.35)*34,z=Math.sin(i*.35)*34;crate(x,z,1.6,2.4,1.6,i%2?0x60768a:0x8d7263);}

// player - temporary code model
const player=new THREE.Group();
function buildGun(){const g=new THREE.Group();const base=boxMesh(new THREE.BoxGeometry(.56,.26,.26),mats.gun);base.position.set(0,0,.18);g.add(base);const barrel=boxMesh(new THREE.BoxGeometry(.24,.18,.36),mats.black);barrel.position.set(0,0,.48);g.add(barrel);const grip=boxMesh(new THREE.BoxGeometry(.18,.34,.14),mats.black);grip.position.set(0,-.22,.07);grip.rotation.x=-.28;g.add(grip);const cyl=new THREE.Mesh(new THREE.CylinderGeometry(.11,.11,.18,8),new THREE.MeshLambertMaterial({color:0x454d59}));cyl.rotation.z=Math.PI/2;cyl.position.set(.02,0,.22);g.add(cyl);return g;}
function buildPlayer(){
  const body=boxMesh(new THREE.BoxGeometry(1.18,1,.86),mats.pink);body.position.y=1;player.add(body);
  const belly=boxMesh(new THREE.BoxGeometry(.86,.52,.52),mats.pink2);belly.position.set(0,.82,.43);player.add(belly);
  const head=boxMesh(new THREE.BoxGeometry(1.25,1,1.02),mats.yellow);head.position.y=1.92;player.add(head);
  const hood=boxMesh(new THREE.BoxGeometry(1.48,1.18,1.18),mats.pink);hood.position.set(0,2,0);player.add(hood);
  const face=boxMesh(new THREE.BoxGeometry(1.02,.76,.28),mats.yellow2);face.position.set(0,1.85,.53);player.add(face);
  const mouth=boxMesh(new THREE.BoxGeometry(.54,.055,.05),mats.black);mouth.position.set(0,1.53,.7);player.add(mouth);
  const ringMat=new THREE.MeshBasicMaterial({color:0x101214});
  for(const sx of [-.28,.28]){const ring=new THREE.Mesh(new THREE.TorusGeometry(.22,.055,8,20),ringMat);ring.position.set(sx,1.83,.73);ring.rotation.x=Math.PI/2;player.add(ring);}
  const bridge=boxMesh(new THREE.BoxGeometry(.15,.05,.05),mats.black);bridge.position.set(0,1.83,.73);player.add(bridge);
  const earG=new THREE.ConeGeometry(.24,.42,4);const earL=new THREE.Mesh(earG,mats.pink);earL.position.set(-.46,2.68,-.04);earL.rotation.z=.16;player.add(earL);const earR=earL.clone();earR.position.x=.46;earR.rotation.z=-.16;player.add(earR);
  const armL=boxMesh(new THREE.BoxGeometry(.34,.75,.34),mats.yellow);armL.position.set(-.77,1.1,.08);player.add(armL);const armR=armL.clone();armR.position.x=.77;player.add(armR);
  const legL=boxMesh(new THREE.BoxGeometry(.4,.7,.45),mats.yellow);legL.position.set(-.35,.34,.05);player.add(legL);const legR=legL.clone();legR.position.x=.35;player.add(legR);
  const tail=boxMesh(new THREE.BoxGeometry(.9,.18,.18),mats.yellow);tail.position.set(.62,.55,-.25);tail.rotation.y=-.7;player.add(tail);
  const gunL=buildGun();gunL.position.set(-.95,1.16,.26);gunL.rotation.y=Math.PI/2;player.add(gunL);const gunR=buildGun();gunR.position.set(.95,1.16,.26);gunR.rotation.y=Math.PI/2;player.add(gunR);
  player.userData.leftMuzzle=new THREE.Vector3(-1.19,1.16,.74);player.userData.rightMuzzle=new THREE.Vector3(1.19,1.16,.74);
}
buildPlayer();player.position.set(0,.05,18);scene.add(player);
function worldPos(local){return player.localToWorld(local.clone());}

function updateHUD(){
  hpEl.textContent='HP '+'♥'.repeat(Math.max(0,state.hp))+'♡'.repeat(Math.max(0,state.maxHp-state.hp));
  waveEl.textContent=`WAVE ${state.wave}`;scoreEl.textContent=`SCORE ${Math.floor(state.score)}`;
  levelTextEl.textContent=String(state.level);xpTextEl.textContent=`${Math.floor(state.xp)} / ${state.xpNext}`;xpFillEl.style.width=`${Math.min(100,state.xp/state.xpNext*100)}%`;
  specialTextEl.textContent=`${Math.floor(state.special/state.specialMax*100)}%`;specialFillEl.style.width=`${Math.min(100,state.special/state.specialMax*100)}%`;
  specialBtn.classList.toggle('ready',state.special>=state.specialMax);
  state.bestScore=Math.max(state.bestScore,Math.floor(state.score));state.bestWave=Math.max(state.bestWave,state.wave);bestScoreEl.textContent=String(state.bestScore);bestWaveEl.textContent=String(state.bestWave);saveBest();
}
function setQuest(t){questEl.textContent=t;}
function toast(t){toastEl.textContent=t;toastEl.classList.remove('hidden');toastTimer=2;}
function say(speaker,lines){state.messageQueue=lines.map(text=>({speaker,text}));nextMessage();}
function nextMessage(){if(state.messageQueue.length===0){state.messageOpen=false;messageEl.classList.add('hidden');return;}const m=state.messageQueue.shift();state.messageOpen=true;speakerEl.textContent=m.speaker;messageText.textContent=m.text;messageEl.classList.remove('hidden');}

function findNearestEnemy(maxDist=26){let best=null,bestD=maxDist;for(const e of enemies){if(e.dead)continue;const d=player.position.distanceTo(e.group.position);if(d<bestD){bestD=d;best=e;}}return best;}
function enemyAimPoint(e){
  const y=e.type==='boss'?1.35:e.type==='shield'?1.0:.86;
  return e.group.position.clone().add(new THREE.Vector3(0,y,0));
}
function enemyHitRadius(e){
  // Mobile-friendly hit assist: intentionally larger than the visible body.
  return e.type==='boss'?1.75:e.type==='shield'?1.28:1.05;
}
function updateLock(){lockTarget=state.autoAim&&state.inGame&&!state.gameOver&&!state.levelUpOpen?findNearestEnemy(30):null;if(lockTarget){const d=player.position.distanceTo(lockTarget.group.position);lockTextEl.textContent=`LOCK: ${lockTarget.label} ${d.toFixed(1)}m`; }else lockTextEl.textContent='LOCK: ---';}

function damagePlayer(amount=1){if(state.invincible>0||state.gameOver||!state.inGame||state.levelUpOpen)return;state.hp=Math.max(0,state.hp-amount);state.invincible=.72;if(state.cameraShake)state.shakeStrength=Math.max(state.shakeStrength,.5);if(state.damageFlash)state.damageFlashTimer=.14;updateHUD();burst(player.position.clone().add(new THREE.Vector3(0,1.5,0)),0xff8fb3,12,1.7);if(state.hp<=0){state.gameOver=true;attackHeld=false;say('SYSTEM',['やられてしまった……','E / Enter または射撃ボタンでリスタートできます。']);setQuest('GAME OVER');}}
function healPlayer(amount=1){state.hp=Math.min(state.maxHp,state.hp+amount);updateHUD();}

function buildEnemy(type='chaser',x=0,z=0){
  const isBoss=type==='boss';const g=new THREE.Group();const mat=new THREE.MeshLambertMaterial({color:enemyPalette[type]||0x7d38d1});
  const scale=isBoss?1.5:type==='shield'?1.18:1;
  const body=boxMesh(new THREE.BoxGeometry(1.05*scale,.92*scale,.84*scale),mat);body.position.y=.64*scale;g.add(body);
  const hood=boxMesh(new THREE.BoxGeometry(1.2*scale,.98*scale,.96*scale),mats.dark);hood.position.y=1.28*scale;g.add(hood);
  const face=boxMesh(new THREE.BoxGeometry(.82*scale,.56*scale,.12),mats.black);face.position.set(0,1.26*scale,.5*scale);g.add(face);
  const eyeMat=new THREE.MeshBasicMaterial({color:isBoss?0xffda66:0xffff94});for(const sx of [-.2,.2]){const eye=new THREE.Mesh(new THREE.BoxGeometry(.12*scale,.12*scale,.04),eyeMat);eye.position.set(sx*scale,1.27*scale,.56*scale);g.add(eye);}
  if(type==='gunner'||type==='boss'){const gun=buildGun();gun.scale.set(.82*scale,.82*scale,.82*scale);gun.position.set(.62*scale,.72*scale,.1);gun.rotation.y=Math.PI/2;g.add(gun);}
  if(type==='shield'){const shield=boxMesh(new THREE.BoxGeometry(1.05,.9,.18),new THREE.MeshLambertMaterial({color:0x48563e}));shield.position.set(0,.86,.68);g.add(shield);}
  if(type==='rusher'){const hornMat=new THREE.MeshBasicMaterial({color:0xff8a70});for(const sx of [-.32,.32]){const horn=new THREE.Mesh(new THREE.ConeGeometry(.14,.38,5),hornMat);horn.position.set(sx,1.95,0);horn.rotation.z=sx<0?.22:-.22;g.add(horn);}}
  if(isBoss){for(const sx of [-.38,.38]){const horn=new THREE.Mesh(new THREE.ConeGeometry(.18,.48,5),mats.glow);horn.position.set(sx,2.25,0);horn.rotation.z=sx<0?.22:-.22;g.add(horn);}}
  g.position.set(x,.05,z);scene.add(g);
  const hpBase={chaser:3,gunner:4,shield:9,rusher:4,boss:40+state.wave*5}[type]||3;
  const e={group:g,type,label:{chaser:'CHASER',gunner:'GUNNER',shield:'SHIELD',rusher:'RUSHER',boss:'VOLT BRUTE'}[type],hp:hpBase,maxHp:hpBase,speed:{chaser:2.7,gunner:1.65,shield:1.45,rusher:2.1,boss:1.85}[type],dead:false,shootCd:1.2+Math.random()*.8,phase:Math.random()*10,rushCd:1.6+Math.random()*1.4,rushTimer:0,rushDir:new THREE.Vector3(),shieldAngle:0};
  enemies.push(e);if(isBoss){bossRef=e;bossHud.classList.remove('hidden');updateBossHud();}return e;
}
function updateBossHud(){if(!bossRef||bossRef.dead){bossHud.classList.add('hidden');return;}bossHud.classList.remove('hidden');bossFillEl.style.width=`${Math.max(0,bossRef.hp/bossRef.maxHp*100)}%`;}
function clearEnemies(){while(enemies.length){const e=enemies.pop();scene.remove(e.group);}bossRef=null;bossHud.classList.add('hidden');}

function spawnWave(wave){
  clearEnemies();
  const spots=[[-30,-30],[30,-30],[-30,30],[30,30],[0,-34],[34,0],[-34,0],[0,34]];
  const total=Math.min(18,4+wave*2);
  for(let i=0;i<total;i++){
    const [bx,bz]=spots[i%spots.length];const x=bx+(Math.random()-.5)*6,z=bz+(Math.random()-.5)*6;
    let type='chaser';
    if(wave>=2&&i%4===0)type='gunner';
    if(wave>=3&&i%5===0)type='shield';
    if(wave>=4&&i%6===0)type='rusher';
    buildEnemy(type,x,z);
  }
  if(wave%5===0){buildEnemy('boss',0,-30);toast('BOSS / VOLT BRUTE');}
  setQuest(`WAVE ${wave} を生き残れ`);updateHUD();
}

function spawnPickup(pos,kind='heart'){const g=new THREE.Group();const mat=kind==='heart'?mats.heart:mats.exp;const mesh=new THREE.Mesh(new THREE.OctahedronGeometry(.42),mat);mesh.position.y=.7;g.add(mesh);const ring=new THREE.Mesh(new THREE.TorusGeometry(.58,.04,8,20),new THREE.MeshBasicMaterial({color:kind==='heart'?0xffa2ba:0x8ee6ff}));ring.rotation.x=Math.PI/2;ring.position.y=.7;g.add(ring);g.position.copy(pos);g.position.y=.05;scene.add(g);pickups.push({group:g,kind,phase:Math.random()*10,life:15});}

function gainXp(amount){state.xp+=amount;while(state.xp>=state.xpNext){state.xp-=state.xpNext;state.level++;state.xpNext=Math.floor(state.xpNext*1.25+20);state.pendingLevelUps++;}updateHUD();if(state.pendingLevelUps>0&&!state.levelUpOpen&&!state.gameOver)openLevelUp();}
const upgrades=[
  {id:'damage',icon:'💥',name:'POWER UP',desc:'弾丸ダメージ +35%',apply:()=>state.damage*=1.35},
  {id:'rapid',icon:'⚡',name:'RAPID FIRE',desc:'連射速度 +18%',apply:()=>state.fireInterval=Math.max(.065,state.fireInterval*.82)},
  {id:'speed',icon:'👟',name:'SPEED',desc:'移動速度 +12%',apply:()=>state.moveSpeed*=1.12},
  {id:'hp',icon:'♥',name:'MAX HP',desc:'最大HP +1、HPを2回復',apply:()=>{state.maxHp++;state.hp=Math.min(state.maxHp,state.hp+2)}},
  {id:'multishot',icon:'✦',name:'TWIN BURST',desc:'同時発射数 +1（最大3）',apply:()=>state.bulletCount=Math.min(3,state.bulletCount+1)},
  {id:'pierce',icon:'➤',name:'PIERCE',desc:'貫通回数 +1',apply:()=>state.pierce++},
  {id:'crit',icon:'★',name:'CRITICAL',desc:'クリティカル率 +8%',apply:()=>state.crit=Math.min(.5,state.crit+.08)},
  {id:'special',icon:'◎',name:'SPECIAL CHARGE',desc:'必殺ゲージ獲得量 +25%',apply:()=>state.specialGain*=1.25},
  {id:'dodge',icon:'↯',name:'DODGE TECH',desc:'回避クールダウン -15%',apply:()=>state.dashCooldownBase=Math.max(.55,(state.dashCooldownBase||1.15)*.85)},
];
function pickUpgradeChoices(){const arr=[...upgrades];for(let i=arr.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]];}return arr.slice(0,3);}
function openLevelUp(){if(state.pendingLevelUps<=0)return;state.levelUpOpen=true;attackHeld=false;levelChoicesEl.innerHTML='';for(const u of pickUpgradeChoices()){const btn=document.createElement('button');btn.type='button';btn.className='level-choice';btn.innerHTML=`<div class="icon">${u.icon}</div><div><strong>${u.name}</strong><p>${u.desc}</p><small>SELECT</small></div>`;btn.addEventListener('click',()=>{u.apply();state.pendingLevelUps--;state.levelUpOpen=false;levelUpOverlay.classList.add('hidden');updateHUD();toast(`${u.name} 獲得`);if(state.pendingLevelUps>0)setTimeout(openLevelUp,80);});levelChoicesEl.appendChild(btn);}levelUpOverlay.classList.remove('hidden');}

function shootPlayer(){
  if(!state.inGame||state.levelUpOpen)return;if(state.messageOpen){nextMessage();return;}if(state.gameOver){restartGame();return;}if(state.shootCooldown>0)return;
  const target=state.autoAim?findNearestEnemy(30):null;
  let fallbackDir=new THREE.Vector3(0,0,1).applyQuaternion(player.quaternion).normalize();
  let aimPoint=null;
  if(target){
    aimPoint=enemyAimPoint(target);
    const bodyDir=new THREE.Vector3().subVectors(aimPoint,player.position.clone().add(new THREE.Vector3(0,1,0))).normalize();
    player.rotation.y=Math.atan2(bodyDir.x,bodyDir.z);
    fallbackDir=bodyDir;
  }
  state.shootCooldown=state.fireInterval;
  for(let n=0;n<state.bulletCount;n++){
    state.shotSide=1-state.shotSide;
    const muzzle=worldPos(state.shotSide?player.userData.leftMuzzle:player.userData.rightMuzzle);
    // Dual-handgun cross auto aim: every barrel converges on the same target point.
    // This avoids the old parallel-shot gap where a centered enemy could slip between both bullets.
    const dir=aimPoint?new THREE.Vector3().subVectors(aimPoint,muzzle).normalize():fallbackDir.clone();
    if(!aimPoint&&state.bulletCount>1){
      const spread=(n-(state.bulletCount-1)/2)*.035;
      dir.applyAxisAngle(new THREE.Vector3(0,1,0),spread).normalize();
    }
    const crit=Math.random()<state.crit;
    const mesh=new THREE.Mesh(new THREE.SphereGeometry(crit?.16:.13,8,8),new THREE.MeshBasicMaterial({color:crit?0xff9cf0:0xffe45a}));
    mesh.position.copy(muzzle);scene.add(mesh);
    projectiles.push({mesh,dir,life:1.35,damage:state.damage*(crit?2:1),pierce:state.pierce,crit,target});
    muzzleFlash(muzzle,dir);
  }
}
function enemyShoot(e){e.shootCd=e.type==='boss'?.72:1.55+Math.random()*.45;const from=e.group.position.clone().add(new THREE.Vector3(0,e.type==='boss'?1.3:.82,0));const aim=new THREE.Vector3().subVectors(player.position.clone().add(new THREE.Vector3(0,.65,0)),from).normalize();const shots=e.type==='boss'&&e.hp<e.maxHp*.5?3:1;for(let s=0;s<shots;s++){const dir=aim.clone().applyAxisAngle(new THREE.Vector3(0,1,0),(s-(shots-1)/2)*.13);const mesh=new THREE.Mesh(new THREE.SphereGeometry(e.type==='boss'?.19:.13,8,8),new THREE.MeshBasicMaterial({color:e.type==='boss'?0xffa53a:0x79f8ff}));mesh.position.copy(from);scene.add(mesh);enemyProjectiles.push({mesh,dir,life:2.5,damage:e.type==='boss'?2:1});}}

function dash(){if(!state.inGame||state.messageOpen||state.gameOver||state.levelUpOpen||state.dashCooldown>0)return;let mx=(keys.right?1:0)-(keys.left?1:0),mz=(keys.down?1:0)-(keys.up?1:0);if(mx===0&&mz===0){mx=Math.sin(player.rotation.y);mz=Math.cos(player.rotation.y);}const len=Math.hypot(mx,mz)||1;mx/=len;mz/=len;for(let i=1;i<=7;i++){const nx=player.position.x+mx*.82,nz=player.position.z+mz*.82;if(!collides(nx,nz)){player.position.x=nx;player.position.z=nz;}}state.dashCooldown=state.dashCooldownBase||1.15;state.dashTimer=.24;state.invincible=Math.max(state.invincible,.34);burst(player.position.clone().add(new THREE.Vector3(0,.8,0)),0x8ef4ff,16,2.5);}

function useSpecial(){if(!state.inGame||state.gameOver||state.messageOpen||state.levelUpOpen)return;if(state.special<state.specialMax){toast(`SPECIAL ${Math.floor(state.special/state.specialMax*100)}%`);return;}state.special=0;state.invincible=Math.max(state.invincible,1.0);state.shakeStrength=.7;const count=32;for(let i=0;i<count;i++){const a=i/count*Math.PI*2;const dir=new THREE.Vector3(Math.sin(a),0,Math.cos(a));const muzzle=player.position.clone().add(new THREE.Vector3(0,1.1,0)).addScaledVector(dir,.9);const mesh=new THREE.Mesh(new THREE.SphereGeometry(.16,8,8),new THREE.MeshBasicMaterial({color:i%2?0xfff26e:0xff72c8}));mesh.position.copy(muzzle);scene.add(mesh);projectiles.push({mesh,dir,life:1.65,damage:state.damage*2.2,pierce:2,special:true});}burst(player.position.clone().add(new THREE.Vector3(0,1,0)),0xffdf59,30,4.2);toast('SPECIAL / 360° DUAL BARRAGE!');updateHUD();}

function muzzleFlash(pos,dir){const m=new THREE.Mesh(new THREE.SphereGeometry(.18,6,6),new THREE.MeshBasicMaterial({color:0xfff2a2,transparent:true,opacity:1}));m.position.copy(pos).addScaledVector(dir,.2);scene.add(m);particles.push({mesh:m,vel:new THREE.Vector3(),life:.08,fade:.08});}
function burst(pos,color=0xffe45a,count=10,speed=1.8){for(let i=0;i<count;i++){const mesh=new THREE.Mesh(new THREE.BoxGeometry(.08,.08,.08),new THREE.MeshBasicMaterial({color,transparent:true,opacity:1}));mesh.position.copy(pos);scene.add(mesh);particles.push({mesh,vel:new THREE.Vector3((Math.random()-.5)*speed,Math.random()*speed,(Math.random()-.5)*speed),life:.5,fade:.5});}}

function killEnemy(e){if(e.dead)return;e.dead=true;e.group.visible=false;const base={chaser:120,gunner:180,shield:260,rusher:220,boss:1800}[e.type]||100;state.score+=base;gainXp(e.type==='boss'?160:({chaser:24,gunner:32,shield:42,rusher:36}[e.type]||20));state.special=Math.min(state.specialMax,state.special+(e.type==='boss'?45:12)*state.specialGain);if(Math.random()<(e.type==='boss'?.9:.18))spawnPickup(e.group.position.clone(),Math.random()<.55?'heart':'exp');if(e.type==='boss'){bossRef=null;bossHud.classList.add('hidden');toast('BOSS DEFEATED!');}else toast(`${e.label} DOWN`);updateHUD();}

function updateEnemies(dt,t){
  for(const e of enemies){if(e.dead)continue;const p=e.group.position;const toP=new THREE.Vector3(player.position.x-p.x,0,player.position.z-p.z);const d=toP.length();if(d>.01)e.group.rotation.y=Math.atan2(toP.x,toP.z);
    if(e.type==='chaser'){if(d>1.25){toP.normalize();moveEnemy(e,toP.x*e.speed*dt,toP.z*e.speed*dt);}if(d<1.25)damagePlayer(1);}
    else if(e.type==='gunner'){if(d>10){toP.normalize();moveEnemy(e,toP.x*e.speed*dt,toP.z*e.speed*dt);}else if(d<6){toP.normalize();moveEnemy(e,-toP.x*e.speed*.65*dt,-toP.z*e.speed*.65*dt);}e.shootCd-=dt;if(e.shootCd<=0&&d<20)enemyShoot(e);}
    else if(e.type==='shield'){if(d>1.55){toP.normalize();moveEnemy(e,toP.x*e.speed*dt,toP.z*e.speed*dt);}if(d<1.55)damagePlayer(1);}
    else if(e.type==='rusher'){e.rushCd-=dt;if(e.rushTimer>0){e.rushTimer-=dt;moveEnemy(e,e.rushDir.x*8.5*dt,e.rushDir.z*8.5*dt);if(d<1.35)damagePlayer(1);}else if(e.rushCd<=0&&d<16){e.rushDir=toP.normalize().clone();e.rushTimer=.48;e.rushCd=2.2+Math.random();burst(p.clone().add(new THREE.Vector3(0,.8,0)),0xff796b,8,1.5);}else if(d>4){toP.normalize();moveEnemy(e,toP.x*e.speed*dt,toP.z*e.speed*dt);}}
    else if(e.type==='boss'){const phase2=e.hp<e.maxHp*.5;const sp=e.speed*(phase2?1.5:1);if(d>7){toP.normalize();moveEnemy(e,toP.x*sp*dt,toP.z*sp*dt);}e.shootCd-=dt;if(e.shootCd<=0&&d<25)enemyShoot(e);if(d<1.8)damagePlayer(2);if(phase2&&Math.sin(t*2.8)>0.96)burst(p.clone().add(new THREE.Vector3(0,1,0)),0xff9a45,5,1.8);}
  }
}
function moveEnemy(e,dx,dz){const p=e.group.position;const nx=p.x+dx,nz=p.z+dz;if(!collides(nx,p.z,.45))p.x=nx;if(!collides(p.x,nz,.45))p.z=nz;}

function segmentSphereHit(a,b,center,radius){
  const ab=new THREE.Vector3().subVectors(b,a);
  const len2=ab.lengthSq();
  if(len2<=0.000001)return a.distanceToSquared(center)<=radius*radius;
  const t=THREE.MathUtils.clamp(new THREE.Vector3().subVectors(center,a).dot(ab)/len2,0,1);
  const closest=a.clone().addScaledVector(ab,t);
  return closest.distanceToSquared(center)<=radius*radius;
}
function updateProjectiles(dt){
  for(let i=projectiles.length-1;i>=0;i--){
    const p=projectiles[i];
    const prev=p.mesh.position.clone();
    const next=prev.clone().addScaledVector(p.dir,dt*state.bulletSpeed);
    p.mesh.position.copy(next);
    p.life-=dt;
    let remove=p.life<=0;
    for(const e of enemies){
      if(e.dead)continue;
      const hitPos=enemyAimPoint(e);
      const radius=enemyHitRadius(e);
      // Swept hit test prevents fast bullets from tunneling through enemies on slower phones.
      if(segmentSphereHit(prev,next,hitPos,radius)){
        let damage=p.damage;
        if(e.type==='shield'){
          const front=new THREE.Vector3(0,0,1).applyQuaternion(e.group.quaternion);
          const incoming=p.dir.clone().negate();
          if(front.dot(incoming)>.1)damage*=.42;
        }
        e.hp-=damage;
        burst(hitPos,p.crit?0xff83e7:0xffef75,p.special?10:6,p.special?2.8:1.7);
        if(e.type==='boss')updateBossHud();
        if(e.hp<=0)killEnemy(e);
        if(p.pierce>0){p.pierce--;p.mesh.position.addScaledVector(p.dir,.6);}else remove=true;
        break;
      }
    }
    if(remove){scene.remove(p.mesh);projectiles.splice(i,1);}
  }
  for(let i=enemyProjectiles.length-1;i>=0;i--){const p=enemyProjectiles[i];p.mesh.position.addScaledVector(p.dir,dt*10);p.life-=dt;let remove=p.life<=0;if(!remove&&p.mesh.position.distanceTo(player.position.clone().add(new THREE.Vector3(0,1,0)))<.86){damagePlayer(p.damage);remove=true;}if(remove){scene.remove(p.mesh);enemyProjectiles.splice(i,1);}}
}
function updatePickups(dt,t){for(let i=pickups.length-1;i>=0;i--){const p=pickups[i];p.life-=dt;p.group.rotation.y+=dt;p.group.position.y=.25+Math.sin(t*3+p.phase)*.12;if(p.group.position.distanceTo(player.position)<1.6){if(p.kind==='heart'){healPlayer(1);toast('HP +1');}else{gainXp(30);state.special=Math.min(state.specialMax,state.special+15);toast('ENERGY +');}burst(p.group.position.clone().add(new THREE.Vector3(0,.8,0)),p.kind==='heart'?0xff8ba7:0x8ee6ff,10,2);scene.remove(p.group);pickups.splice(i,1);continue;}if(p.life<=0){scene.remove(p.group);pickups.splice(i,1);}}}
function updateParticles(dt){for(let i=particles.length-1;i>=0;i--){const p=particles[i];p.life-=dt;p.mesh.position.addScaledVector(p.vel,dt);p.mesh.material.opacity=Math.max(0,p.life/p.fade);if(p.life<=0){scene.remove(p.mesh);particles.splice(i,1);}}}

function updateWave(dt){if(state.gameOver||state.levelUpOpen)return;const alive=enemies.some(e=>!e.dead);if(!alive){if(state.waveClearDelay<=0){state.waveClearDelay=2.2;toast(`WAVE ${state.wave} CLEAR!`);setQuest('次のウェーブ準備中…');}else{state.waveClearDelay-=dt;if(state.waveClearDelay<=0){state.wave++;spawnWave(state.wave);}}}}

function restartGame(){
  state.inGame=true;clearBattleObjects();state.hp=state.maxHp=6;state.wave=1;state.score=0;state.level=1;state.xp=0;state.xpNext=100;state.pendingLevelUps=0;state.levelUpOpen=false;state.damage=1;state.fireInterval=.145;state.bulletSpeed=20;state.moveSpeed=6.2;state.bulletCount=1;state.pierce=0;state.crit=.08;state.special=0;state.specialGain=1;state.dashCooldownBase=1.15;state.waveClearDelay=0;state.invincible=0;state.shootCooldown=0;state.dashCooldown=0;state.dashTimer=0;state.gameOver=false;state.messageQueue=[];state.messageOpen=false;messageEl.classList.add('hidden');levelUpOverlay.classList.add('hidden');player.position.set(0,.05,18);player.rotation.y=Math.PI;player.visible=true;spawnWave(1);updateHUD();setQuest('WAVE 1 を生き残れ');}
function stopMovement(){keys.up=keys.down=keys.left=keys.right=false;attackHeld=false;document.querySelectorAll('.ctl').forEach(b=>b.classList.remove('pressed'));}
function clearBattleObjects(){while(projectiles.length)scene.remove(projectiles.pop().mesh);while(enemyProjectiles.length)scene.remove(enemyProjectiles.pop().mesh);while(pickups.length)scene.remove(pickups.pop().group);clearEnemies();}
function setGameplayUi(visible){hudEl.classList.toggle('hidden',!visible);crosshairEl.classList.toggle('hidden',!visible);mobileControlsEl.classList.toggle('hidden',!visible);helpEl.classList.toggle('hidden',!visible);if(!visible)bossHud.classList.add('hidden');}
function closeModal(){modalBackdrop.classList.add('hidden');howToModal.classList.add('hidden');settingsModal.classList.add('hidden');modalBackdrop.setAttribute('aria-hidden','true');}
function openModal(which){modalBackdrop.classList.remove('hidden');modalBackdrop.setAttribute('aria-hidden','false');howToModal.classList.toggle('hidden',which!=='how');settingsModal.classList.toggle('hidden',which!=='settings');}
function showMain(){state.inGame=false;stopMovement();closeModal();setGameplayUi(false);messageEl.classList.add('hidden');levelUpOverlay.classList.add('hidden');titleScreen.classList.remove('active');mainScreen.classList.add('active');clearBattleObjects();state.gameOver=false;player.visible=true;player.position.set(0,.05,8);player.rotation.y=Math.PI;updateHUD();}
function startBattle(){closeModal();titleScreen.classList.remove('active');mainScreen.classList.remove('active');setGameplayUi(true);restartGame();say('SYSTEM',['BATTLE START！','近い敵を自動ロック。Space / ⚡長押しで二丁拳銃を連射します。','EXPでレベルアップ、SPECIALが100%になったら360°乱射が使えます。']);}

titleStartBtn.addEventListener('click',showMain);battleStartBtn.addEventListener('click',startBattle);howToBtn.addEventListener('click',()=>openModal('how'));settingsBtn.addEventListener('click',()=>openModal('settings'));document.querySelectorAll('[data-close-modal]').forEach(b=>b.addEventListener('click',closeModal));modalBackdrop.addEventListener('pointerdown',e=>{if(e.target===modalBackdrop)closeModal();});$('menuBtn').addEventListener('click',showMain);shakeToggle.addEventListener('change',()=>state.cameraShake=shakeToggle.checked);flashToggle.addEventListener('change',()=>state.damageFlash=flashToggle.checked);autoAimToggle.addEventListener('change',()=>state.autoAim=autoAimToggle.checked);

window.addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' ','Enter','KeyE','KeyQ','ShiftLeft','ShiftRight','KeyW','KeyA','KeyS','KeyD'].includes(e.code))e.preventDefault();if(e.code==='KeyW'||e.code==='ArrowUp')keys.up=true;if(e.code==='KeyS'||e.code==='ArrowDown')keys.down=true;if(e.code==='KeyA'||e.code==='ArrowLeft')keys.left=true;if(e.code==='KeyD'||e.code==='ArrowRight')keys.right=true;if(e.code==='Space')attackHeld=true;if(e.code==='ShiftLeft'||e.code==='ShiftRight')dash();if(e.code==='KeyQ')useSpecial();if(e.code==='KeyE'||e.code==='Enter'){if(state.messageOpen)nextMessage();else if(state.gameOver&&state.inGame)restartGame();}if(e.code==='Escape'&&state.inGame)showMain();});
window.addEventListener('keyup',e=>{if(e.code==='KeyW'||e.code==='ArrowUp')keys.up=false;if(e.code==='KeyS'||e.code==='ArrowDown')keys.down=false;if(e.code==='KeyA'||e.code==='ArrowLeft')keys.left=false;if(e.code==='KeyD'||e.code==='ArrowRight')keys.right=false;if(e.code==='Space')attackHeld=false;});

document.querySelectorAll('.ctl').forEach(btn=>{const k=btn.dataset.key;const on=e=>{e.preventDefault();keys[k]=true;btn.classList.add('pressed')};const off=e=>{e.preventDefault();keys[k]=false;btn.classList.remove('pressed')};btn.addEventListener('pointerdown',on);btn.addEventListener('pointerup',off);btn.addEventListener('pointercancel',off);btn.addEventListener('pointerleave',off);});
const startFire=e=>{e.preventDefault();attackHeld=true;shootPlayer();attackBtn.classList.add('pressed')};const stopFire=e=>{e.preventDefault();attackHeld=false;attackBtn.classList.remove('pressed')};attackBtn.addEventListener('pointerdown',startFire);attackBtn.addEventListener('pointerup',stopFire);attackBtn.addEventListener('pointercancel',stopFire);attackBtn.addEventListener('pointerleave',stopFire);dashBtn.addEventListener('pointerdown',e=>{e.preventDefault();dash()});specialBtn.addEventListener('pointerdown',e=>{e.preventDefault();useSpecial()});messageEl.addEventListener('pointerdown',e=>{e.preventDefault();if(state.messageOpen)nextMessage();else if(state.gameOver)restartGame();});

function updatePlayer(dt){if(!state.inGame||state.messageOpen||state.gameOver||state.levelUpOpen)return;let mx=(keys.right?1:0)-(keys.left?1:0),mz=(keys.down?1:0)-(keys.up?1:0);const len=Math.hypot(mx,mz);if(len>0){mx/=len;mz/=len;const speed=state.moveSpeed*(state.dashTimer>0?1.65:1);const nx=player.position.x+mx*speed*dt,nz=player.position.z+mz*speed*dt;if(!collides(nx,player.position.z))player.position.x=nx;if(!collides(player.position.x,nz))player.position.z=nz;if(!(state.autoAim&&lockTarget&&attackHeld))player.rotation.y=Math.atan2(mx,mz);}if(attackHeld)shootPlayer();if(state.invincible>0)player.visible=Math.floor(performance.now()/65)%2===0;else player.visible=true;}

const camTarget=new THREE.Vector3();let last=performance.now();
function loop(now){requestAnimationFrame(loop);const dt=Math.min((now-last)/1000,.05);last=now;const t=now/1000;
  state.shootCooldown=Math.max(0,state.shootCooldown-dt);state.dashCooldown=Math.max(0,state.dashCooldown-dt);state.dashTimer=Math.max(0,state.dashTimer-dt);state.invincible=Math.max(0,state.invincible-dt);state.damageFlashTimer=Math.max(0,state.damageFlashTimer-dt);state.shakeStrength=Math.max(0,state.shakeStrength-dt*2.8);if(toastTimer>0){toastTimer-=dt;if(toastTimer<=0)toastEl.classList.add('hidden');}
  damageFlashEl.classList.toggle('hidden',!(state.damageFlashTimer>0&&state.inGame));updateLock();updatePlayer(dt);
  if(state.inGame&&!state.messageOpen&&!state.gameOver&&!state.levelUpOpen){updateEnemies(dt,t);updateProjectiles(dt);updatePickups(dt,t);updateParticles(dt);updateWave(dt);}else{updateParticles(dt);}
  const desired=new THREE.Vector3(player.position.x+9,11.5,player.position.z+12);if(state.cameraShake&&state.shakeStrength>0){desired.x+=(Math.random()-.5)*state.shakeStrength;desired.y+=(Math.random()-.5)*state.shakeStrength;desired.z+=(Math.random()-.5)*state.shakeStrength;}camera.position.lerp(desired,1-Math.pow(.001,dt));camTarget.set(player.position.x,1.4,player.position.z);camera.lookAt(camTarget);renderer.render(scene,camera);
}
window.addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(Math.min(devicePixelRatio,1.55));});

bestScoreEl.textContent=String(state.bestScore);bestWaveEl.textContent=String(state.bestWave);updateHUD();showMain();titleScreen.classList.add('active');mainScreen.classList.remove('active');requestAnimationFrame(loop);
