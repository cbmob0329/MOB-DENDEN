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
const moveStickEl = $('moveStick');
const moveStickKnobEl = $('moveStickKnob');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x09101c);
scene.fog = new THREE.Fog(0x101828, 34, 88);

const camera = new THREE.PerspectiveCamera(56, innerWidth / innerHeight, 0.1, 220);
const renderer = new THREE.WebGLRenderer({ antialias:true, powerPreference:'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.55));
renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
root.prepend(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xccefff, 0x15081a, 0.94));
const sun = new THREE.DirectionalLight(0xb7d2ff, 0.92);
sun.position.set(18,30,14);
sun.castShadow = true;
sun.shadow.mapSize.set(1024,1024);
sun.shadow.camera.left=-45; sun.shadow.camera.right=45; sun.shadow.camera.top=45; sun.shadow.camera.bottom=-45;
scene.add(sun);

const magentaLight = new THREE.PointLight(0xff48b7, 1.6, 90, 2);
magentaLight.position.set(-22, 18, -10);
scene.add(magentaLight);
const cyanLight = new THREE.PointLight(0x39e0ff, 1.75, 90, 2);
cyanLight.position.set(20, 16, 14);
scene.add(cyanLight);
const purpleLight = new THREE.PointLight(0x8e68ff, 1.05, 70, 2);
purpleLight.position.set(0, 14, -26);
scene.add(purpleLight);

const mats = {
  sand:new THREE.MeshLambertMaterial({color:0x101828}),
  sand2:new THREE.MeshLambertMaterial({color:0x172335}),
  road:new THREE.MeshLambertMaterial({color:0x24293a}),
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
  metal:new THREE.MeshLambertMaterial({color:0x485469}),
  metalDark:new THREE.MeshLambertMaterial({color:0x2a3344}),
  vinyl:new THREE.MeshLambertMaterial({color:0x151a25}),
  speaker:new THREE.MeshLambertMaterial({color:0x303745}),
  speakerDark:new THREE.MeshLambertMaterial({color:0x161b24}),
  panel:new THREE.MeshLambertMaterial({color:0x26354c}),
  neonPink:new THREE.MeshBasicMaterial({color:0xff4fc3}),
  neonBlue:new THREE.MeshBasicMaterial({color:0x4de5ff}),
  neonPurple:new THREE.MeshBasicMaterial({color:0xa06dff}),
  neonGreen:new THREE.MeshBasicMaterial({color:0x89ff9d}),
};

const enemyPalette = {
  chaser: 0x7d38d1,
  gunner: 0x24b8d7,
  shield: 0x768b58,
  rusher: 0xe05a59,
  boss: 0xf08a27,
};

const keys = {up:false,down:false,left:false,right:false};
const stick = { x:0, y:0, active:false, pointerId:null };
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

const saveKey='mob-gun-cat-v08';
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
  damage:1,fireInterval:.145,bulletSpeed:20,moveSpeed:6.2,bulletCount:2,pierce:0,crit:.08,
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

// arena - neon city / DJ street stage
box(84,1,84,mats.sand,0,-.5,0,false);
for(let x=-38;x<=38;x+=4){
  for(let z=-38;z<=38;z+=4){
    const useAlt=((Math.round((x+40)/4)+Math.round((z+40)/4))%2===0);
    if(useAlt)box(3.96,.03,3.96,mats.sand2,x,.02,z,false);
  }
}
box(76,.08,14,mats.road,0,.03,0,false);
box(14,.08,76,mats.road,0,.03,0,false);
for(let x=-34;x<=34;x+=4){box(2.1,.03,.22,mats.neonPink,x,.055,-6.3,false);box(2.1,.03,.22,mats.neonBlue,x,.055,6.3,false);}
for(let z=-34;z<=34;z+=4){box(.22,.03,2.1,mats.neonPurple,-6.3,.055,z,false);box(.22,.03,2.1,mats.neonGreen,6.3,.055,z,false);}
box(10,.03,10,mats.neonBlue,0,.06,0,false);

function stagePillar(x,z,height=6,colorMat=mats.neonBlue){
  const g=new THREE.Group();
  const pole=boxMesh(new THREE.BoxGeometry(.7,height,.7),mats.metalDark); pole.position.y=height/2; g.add(pole);
  const ring1=boxMesh(new THREE.BoxGeometry(1.18,.16,1.18),colorMat); ring1.position.y=1.5; g.add(ring1);
  const ring2=boxMesh(new THREE.BoxGeometry(1.18,.16,1.18),colorMat); ring2.position.y=height-1.2; g.add(ring2);
  const cap=boxMesh(new THREE.BoxGeometry(1.05,.5,1.05),mats.panel); cap.position.y=height+.2; g.add(cap);
  g.position.set(x,0,z); scene.add(g); addBlocker(x,z,1.15,1.15);
}
function speakerStack(x,z,rot=0,colorMat=mats.neonBlue){
  const g=new THREE.Group();
  const base=boxMesh(new THREE.BoxGeometry(1.6,3.0,1.45),mats.speaker); base.position.y=1.5; g.add(base);
  const woofer1=new THREE.Mesh(new THREE.CylinderGeometry(.28,.28,.16,18),mats.speakerDark); woofer1.rotation.x=Math.PI/2; woofer1.position.set(0,1.05,.76); g.add(woofer1);
  const woofer2=woofer1.clone(); woofer2.position.y=1.95; g.add(woofer2);
  const glow1=new THREE.Mesh(new THREE.TorusGeometry(.34,.05,8,18),colorMat); glow1.rotation.x=Math.PI/2; glow1.position.set(0,1.05,.82); g.add(glow1);
  const glow2=glow1.clone(); glow2.position.y=1.95; g.add(glow2);
  const top=boxMesh(new THREE.BoxGeometry(1.72,.18,1.52),mats.metal); top.position.y=3.02; g.add(top);
  g.position.set(x,0,z); g.rotation.y=rot; scene.add(g); addBlocker(x,z,1.7,1.55);
}
function turntableDeck(x,z,rot=0){
  const g=new THREE.Group();
  const table=boxMesh(new THREE.BoxGeometry(3.3,1.15,1.95),mats.panel); table.position.y=.78; g.add(table);
  const top=boxMesh(new THREE.BoxGeometry(3.45,.16,2.1),mats.metal); top.position.y=1.43; g.add(top);
  const legPos=[[-1.32,.6,-.72],[1.32,.6,-.72],[-1.32,.6,.72],[1.32,.6,.72]];
  for(const [lx,ly,lz] of legPos){ const leg=boxMesh(new THREE.BoxGeometry(.16,1.2,.16),mats.metalDark); leg.position.set(lx,ly,lz); g.add(leg); }
  for(const sx of [-.95,.95]){
    const disc=new THREE.Mesh(new THREE.CylinderGeometry(.52,.52,.12,24),mats.vinyl); disc.rotation.x=Math.PI/2; disc.position.set(sx,1.55,-.05); g.add(disc);
    const center=new THREE.Mesh(new THREE.CylinderGeometry(.14,.14,.13,16),mats.neonPink); center.rotation.x=Math.PI/2; center.position.set(sx,1.56,-.05); g.add(center);
    const rim=new THREE.Mesh(new THREE.TorusGeometry(.56,.04,8,24),mats.neonBlue); rim.rotation.x=Math.PI/2; rim.position.set(sx,1.57,-.05); g.add(rim);
  }
  const mixer=boxMesh(new THREE.BoxGeometry(.6,.12,.9),mats.speakerDark); mixer.position.set(0,1.54,.18); g.add(mixer);
  for(let i=0;i<4;i++){ const knob=new THREE.Mesh(new THREE.CylinderGeometry(.05,.05,.08,12),i%2?mats.neonPurple:mats.neonGreen); knob.position.set(-.18+i*.12,1.63,-.1); g.add(knob); }
  const label=boxMesh(new THREE.BoxGeometry(1.1,.14,.22),mats.neonPink); label.position.set(0,1.55,.86); g.add(label);
  g.position.set(x,0,z); g.rotation.y=rot; scene.add(g); addBlocker(x,z,3.4,2.25);
}
function recordBarrier(x,z,rot=0){
  const g=new THREE.Group();
  const disc=new THREE.Mesh(new THREE.CylinderGeometry(1.0,1.0,.22,30),mats.vinyl); disc.rotation.z=Math.PI/2; disc.position.set(0,1.2,0); g.add(disc);
  const center=new THREE.Mesh(new THREE.CylinderGeometry(.24,.24,.24,18),mats.neonPink); center.rotation.z=Math.PI/2; center.position.set(0,1.2,0); g.add(center);
  const stand=boxMesh(new THREE.BoxGeometry(.2,1.1,1.5),mats.metalDark); stand.position.set(0,.55,0); g.add(stand);
  const base=boxMesh(new THREE.BoxGeometry(1.5,.18,1.5),mats.metal); base.position.y=.09; g.add(base);
  g.position.set(x,0,z); g.rotation.y=rot; scene.add(g); addBlocker(x,z,1.7,1.7);
}
function mobNeonSign(x,z,rot=0,colorMat=mats.neonPurple){
  const g=new THREE.Group();
  const post=boxMesh(new THREE.BoxGeometry(.22,4.2,.22),mats.metalDark); post.position.y=2.1; g.add(post);
  const board=boxMesh(new THREE.BoxGeometry(2.6,1.2,.18),mats.panel); board.position.set(0,4.05,0); g.add(board);
  const glowA=boxMesh(new THREE.BoxGeometry(2.1,.18,.22),colorMat); glowA.position.set(0,4.05,.12); g.add(glowA);
  const glowB=boxMesh(new THREE.BoxGeometry(.22,.82,.22),mats.neonBlue); glowB.position.set(-.62,4.05,.12); g.add(glowB);
  const glowC=boxMesh(new THREE.BoxGeometry(.22,.82,.22),mats.neonPink); glowC.position.set(0,4.05,.12); g.add(glowC);
  const glowD=boxMesh(new THREE.BoxGeometry(.22,.82,.22),mats.neonGreen); glowD.position.set(.62,4.05,.12); g.add(glowD);
  g.position.set(x,0,z); g.rotation.y=rot; scene.add(g);
}
function skylineBlock(x,z,w,h,d,color=0x0d1220){ box(w,h,d,new THREE.MeshLambertMaterial({color}),x,h/2,z,false); }

// decorative skyline around the arena edges
[[-35,-39,8,12,2],[-23,-39,6,16,2],[-10,-39,7,10,2],[3,-39,9,14,2],[18,-39,6,11,2],[31,-39,8,17,2],
 [-35,39,8,14,2],[-21,39,7,12,2],[-8,39,6,18,2],[7,39,8,11,2],[22,39,7,15,2],[34,39,8,13,2],
 [-39,-29,2,14,7],[-39,-10,2,11,8],[-39,11,2,16,8],[-39,29,2,12,6],[39,-28,2,12,8],[39,-9,2,18,6],[39,12,2,13,9],[39,30,2,15,7]].forEach(v=>skylineBlock(...v));

// stage obstacles / DJ props
[[ -18,-16,0],[ -18,16,Math.PI],[ 18,-16,0],[ 18,16,Math.PI],[-28,0,Math.PI/2],[28,0,-Math.PI/2],[0,-28,0],[0,28,Math.PI]].forEach(p=>turntableDeck(p[0],p[1],p[2]));
[[-23,8,0],[-23,-8,0],[23,8,Math.PI],[23,-8,Math.PI],[-8,23,Math.PI/2],[8,23,-Math.PI/2],[-8,-23,Math.PI/2],[8,-23,-Math.PI/2]].forEach(p=>recordBarrier(p[0],p[1],p[2]));
for(let i=0;i<18;i++){
  const x=Math.cos(i*.35)*34, z=Math.sin(i*.35)*34;
  speakerStack(x,z,Math.atan2(x,z),i%2?mats.neonBlue:mats.neonPink);
}
[[ -6,13,mats.neonBlue],[ 6,-13,mats.neonPink],[-13,-6,mats.neonPurple],[13,6,mats.neonGreen]].forEach(p=>stagePillar(p[0],p[1],6,p[2]));
[[ -31,-2,0],[31,2,Math.PI],[-2,31,Math.PI/2],[2,-31,-Math.PI/2]].forEach(p=>mobNeonSign(p[0],p[1],p[2]));
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
  {id:'multishot',icon:'✦',name:'TWIN BURST',desc:'同時発射数 +1（最大4）',apply:()=>state.bulletCount=Math.min(4,state.bulletCount+1)},
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

function dash(){
  if(!state.inGame||state.messageOpen||state.gameOver||state.levelUpOpen||state.dashCooldown>0)return;
  let mx=((keys.right?1:0)-(keys.left?1:0))+stick.x;
  let mz=((keys.down?1:0)-(keys.up?1:0))+stick.y;
  if(Math.hypot(mx,mz)<.08){mx=Math.sin(player.rotation.y);mz=Math.cos(player.rotation.y);}
  const len=Math.hypot(mx,mz)||1;mx/=len;mz/=len;
  // Safe short-step dodge. v0.6 could move almost six world units instantly and pass through obstacles.
  const totalDistance=2.55;
  const steps=10;
  const step=totalDistance/steps;
  for(let i=0;i<steps;i++){
    const nx=player.position.x+mx*step;
    const nz=player.position.z+mz*step;
    if(collides(nx,nz,.45))break;
    player.position.x=nx;
    player.position.z=nz;
  }
  player.rotation.y=Math.atan2(mx,mz);
  state.dashCooldown=state.dashCooldownBase||1.15;
  state.dashTimer=.18;
  state.invincible=Math.max(state.invincible,.38);
  burst(player.position.clone().add(new THREE.Vector3(0,.8,0)),0x8ef4ff,12,2.0);
}

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
  state.inGame=true;clearBattleObjects();state.hp=state.maxHp=6;state.wave=1;state.score=0;state.level=1;state.xp=0;state.xpNext=100;state.pendingLevelUps=0;state.levelUpOpen=false;state.damage=1;state.fireInterval=.145;state.bulletSpeed=20;state.moveSpeed=6.2;state.bulletCount=2;state.pierce=0;state.crit=.08;state.special=0;state.specialGain=1;state.dashCooldownBase=1.15;state.waveClearDelay=0;state.invincible=0;state.shootCooldown=0;state.dashCooldown=0;state.dashTimer=0;state.gameOver=false;state.messageQueue=[];state.messageOpen=false;messageEl.classList.add('hidden');levelUpOverlay.classList.add('hidden');player.position.set(0,.05,18);player.rotation.y=Math.PI;player.visible=true;spawnWave(1);updateHUD();setQuest('WAVE 1 を生き残れ');}
function stopMovement(){keys.up=keys.down=keys.left=keys.right=false;attackHeld=false;attackBtn.classList.remove('pressed');resetStick();}
function clearBattleObjects(){while(projectiles.length)scene.remove(projectiles.pop().mesh);while(enemyProjectiles.length)scene.remove(enemyProjectiles.pop().mesh);while(pickups.length)scene.remove(pickups.pop().group);clearEnemies();}
function isTouchUi(){
  return (navigator.maxTouchPoints||0)>0 || window.matchMedia('(pointer: coarse)').matches || window.matchMedia('(any-pointer: coarse)').matches || innerWidth<=1024;
}
function refreshInputUi(){
  const touch=isTouchUi();
  document.body.classList.toggle('touch-ui',touch);
  if(state.inGame){
    mobileControlsEl.classList.toggle('hidden',!touch);
    helpEl.classList.toggle('hidden',touch);
  }
}
function setGameplayUi(visible){
  hudEl.classList.toggle('hidden',!visible);
  crosshairEl.classList.toggle('hidden',!visible);
  if(visible){refreshInputUi();}
  else{mobileControlsEl.classList.add('hidden');helpEl.classList.add('hidden');}
  if(!visible)bossHud.classList.add('hidden');
}
function closeModal(){modalBackdrop.classList.add('hidden');howToModal.classList.add('hidden');settingsModal.classList.add('hidden');modalBackdrop.setAttribute('aria-hidden','true');}
function openModal(which){modalBackdrop.classList.remove('hidden');modalBackdrop.setAttribute('aria-hidden','false');howToModal.classList.toggle('hidden',which!=='how');settingsModal.classList.toggle('hidden',which!=='settings');}
function showMain(){state.inGame=false;stopMovement();closeModal();setGameplayUi(false);messageEl.classList.add('hidden');levelUpOverlay.classList.add('hidden');titleScreen.classList.remove('active');mainScreen.classList.add('active');clearBattleObjects();state.gameOver=false;player.visible=true;player.position.set(0,.05,8);player.rotation.y=Math.PI;updateHUD();}
function startBattle(){closeModal();titleScreen.classList.remove('active');mainScreen.classList.remove('active');setGameplayUi(true);restartGame();toast(isTouchUi()?'左PADで移動 / FIRE長押しで連射':'WASDで移動 / Space長押しで連射');}

titleStartBtn.addEventListener('click',showMain);battleStartBtn.addEventListener('click',startBattle);howToBtn.addEventListener('click',()=>openModal('how'));settingsBtn.addEventListener('click',()=>openModal('settings'));document.querySelectorAll('[data-close-modal]').forEach(b=>b.addEventListener('click',closeModal));modalBackdrop.addEventListener('pointerdown',e=>{if(e.target===modalBackdrop)closeModal();});$('menuBtn').addEventListener('click',showMain);shakeToggle.addEventListener('change',()=>state.cameraShake=shakeToggle.checked);flashToggle.addEventListener('change',()=>state.damageFlash=flashToggle.checked);autoAimToggle.addEventListener('change',()=>state.autoAim=autoAimToggle.checked);

window.addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' ','Enter','KeyE','KeyQ','ShiftLeft','ShiftRight','KeyW','KeyA','KeyS','KeyD'].includes(e.code))e.preventDefault();if(e.code==='KeyW'||e.code==='ArrowUp')keys.up=true;if(e.code==='KeyS'||e.code==='ArrowDown')keys.down=true;if(e.code==='KeyA'||e.code==='ArrowLeft')keys.left=true;if(e.code==='KeyD'||e.code==='ArrowRight')keys.right=true;if(e.code==='Space')attackHeld=true;if(e.code==='ShiftLeft'||e.code==='ShiftRight')dash();if(e.code==='KeyQ')useSpecial();if(e.code==='KeyE'||e.code==='Enter'){if(state.messageOpen)nextMessage();else if(state.gameOver&&state.inGame)restartGame();}if(e.code==='Escape'&&state.inGame)showMain();});
window.addEventListener('keyup',e=>{if(e.code==='KeyW'||e.code==='ArrowUp')keys.up=false;if(e.code==='KeyS'||e.code==='ArrowDown')keys.down=false;if(e.code==='KeyA'||e.code==='ArrowLeft')keys.left=false;if(e.code==='KeyD'||e.code==='ArrowRight')keys.right=false;if(e.code==='Space')attackHeld=false;});

function resetStick(){
  stick.x=0;stick.y=0;stick.active=false;stick.pointerId=null;
  if(moveStickKnobEl)moveStickKnobEl.style.transform='translate(0px,0px)';
}
function updateStickFromPointer(e){
  const rect=moveStickEl.getBoundingClientRect();
  const cx=rect.left+rect.width/2,cy=rect.top+rect.height/2;
  let dx=e.clientX-cx,dy=e.clientY-cy;
  const max=Math.max(42,Math.min(rect.width,rect.height)*.31);
  const dist=Math.hypot(dx,dy);
  if(dist>max){dx=dx/dist*max;dy=dy/dist*max;}
  stick.x=THREE.MathUtils.clamp(dx/max,-1,1);
  stick.y=THREE.MathUtils.clamp(dy/max,-1,1);
  const dead=.12;
  if(Math.abs(stick.x)<dead)stick.x=0;
  if(Math.abs(stick.y)<dead)stick.y=0;
  moveStickKnobEl.style.transform=`translate(${dx}px,${dy}px)`;
}
moveStickEl.addEventListener('pointerdown',e=>{
  e.preventDefault();e.stopPropagation();
  stick.active=true;stick.pointerId=e.pointerId;
  try{moveStickEl.setPointerCapture(e.pointerId);}catch{}
  updateStickFromPointer(e);
});
moveStickEl.addEventListener('pointermove',e=>{if(stick.active&&e.pointerId===stick.pointerId){e.preventDefault();updateStickFromPointer(e);}});
const endStick=e=>{if(stick.pointerId===null||e.pointerId===stick.pointerId){e.preventDefault();resetStick();}};
moveStickEl.addEventListener('pointerup',endStick);
moveStickEl.addEventListener('pointercancel',endStick);
moveStickEl.addEventListener('lostpointercapture',()=>resetStick());

const startFire=e=>{
  e.preventDefault();e.stopPropagation();
  attackHeld=true;
  try{attackBtn.setPointerCapture(e.pointerId);}catch{}
  shootPlayer();
  attackBtn.classList.add('pressed');
};
const stopFire=e=>{
  e.preventDefault();e.stopPropagation();
  attackHeld=false;
  attackBtn.classList.remove('pressed');
};
attackBtn.addEventListener('pointerdown',startFire);
attackBtn.addEventListener('pointerup',stopFire);
attackBtn.addEventListener('pointercancel',stopFire);
attackBtn.addEventListener('lostpointercapture',()=>{attackHeld=false;attackBtn.classList.remove('pressed');});
const pressDodge=e=>{e.preventDefault();e.stopPropagation();dashBtn.classList.add('pressed');dash();};
const releaseDodge=e=>{e.preventDefault();e.stopPropagation();dashBtn.classList.remove('pressed');};
dashBtn.addEventListener('pointerdown',pressDodge);
dashBtn.addEventListener('pointerup',releaseDodge);
dashBtn.addEventListener('pointercancel',releaseDodge);
dashBtn.addEventListener('pointerleave',releaseDodge);
specialBtn.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();try{specialBtn.setPointerCapture(e.pointerId);}catch{}useSpecial();});
messageEl.addEventListener('pointerdown',e=>{e.preventDefault();if(state.messageOpen)nextMessage();else if(state.gameOver)restartGame();});

// Prevent mobile Safari/Chrome from stealing long-press, text selection, context menu or double-tap zoom.
document.addEventListener('contextmenu',e=>e.preventDefault());
document.addEventListener('selectstart',e=>e.preventDefault());
document.addEventListener('dragstart',e=>e.preventDefault());
document.addEventListener('dblclick',e=>{e.preventDefault();e.stopPropagation();},{passive:false});
document.addEventListener('touchmove',e=>{if(root.contains(e.target))e.preventDefault();},{passive:false});
for(const type of ['gesturestart','gesturechange','gestureend'])document.addEventListener(type,e=>e.preventDefault(),{passive:false});

function updatePlayer(dt){if(!state.inGame||state.messageOpen||state.gameOver||state.levelUpOpen)return;let mx=((keys.right?1:0)-(keys.left?1:0))+stick.x,mz=((keys.down?1:0)-(keys.up?1:0))+stick.y;const len=Math.hypot(mx,mz);if(len>.04){mx/=Math.max(1,len);mz/=Math.max(1,len);const speed=state.moveSpeed*(state.dashTimer>0?1.65:1);const nx=player.position.x+mx*speed*dt,nz=player.position.z+mz*speed*dt;if(!collides(nx,player.position.z))player.position.x=nx;if(!collides(player.position.x,nz))player.position.z=nz;if(!(state.autoAim&&lockTarget&&attackHeld))player.rotation.y=Math.atan2(mx,mz);}if(attackHeld)shootPlayer();if(state.invincible>0)player.visible=Math.floor(performance.now()/65)%2===0;else player.visible=true;}

const camTarget=new THREE.Vector3();let last=performance.now();
function loop(now){requestAnimationFrame(loop);const dt=Math.min((now-last)/1000,.05);last=now;const t=now/1000;
  state.shootCooldown=Math.max(0,state.shootCooldown-dt);state.dashCooldown=Math.max(0,state.dashCooldown-dt);state.dashTimer=Math.max(0,state.dashTimer-dt);state.invincible=Math.max(0,state.invincible-dt);state.damageFlashTimer=Math.max(0,state.damageFlashTimer-dt);state.shakeStrength=Math.max(0,state.shakeStrength-dt*2.8);if(toastTimer>0){toastTimer-=dt;if(toastTimer<=0)toastEl.classList.add('hidden');}
  damageFlashEl.classList.toggle('hidden',!(state.damageFlashTimer>0&&state.inGame));updateLock();updatePlayer(dt);
  if(state.inGame&&!state.messageOpen&&!state.gameOver&&!state.levelUpOpen){updateEnemies(dt,t);updateProjectiles(dt);updatePickups(dt,t);updateParticles(dt);updateWave(dt);}else{updateParticles(dt);}
  const desired=new THREE.Vector3(player.position.x+9,11.5,player.position.z+12);if(state.cameraShake&&state.shakeStrength>0){desired.x+=(Math.random()-.5)*state.shakeStrength;desired.y+=(Math.random()-.5)*state.shakeStrength;desired.z+=(Math.random()-.5)*state.shakeStrength;}camera.position.lerp(desired,1-Math.pow(.001,dt));camTarget.set(player.position.x,1.4,player.position.z);camera.lookAt(camTarget);renderer.render(scene,camera);
}
window.addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(Math.min(devicePixelRatio,1.55));refreshInputUi();});
window.addEventListener('orientationchange',()=>setTimeout(refreshInputUi,120));

bestScoreEl.textContent=String(state.bestScore);bestWaveEl.textContent=String(state.bestWave);updateHUD();refreshInputUi();showMain();titleScreen.classList.add('active');mainScreen.classList.remove('active');requestAnimationFrame(loop);
