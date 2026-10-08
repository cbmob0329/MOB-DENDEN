/* Visual-only replacement. Ledger, save schema, routes and furniture sockets stay owned by the game. */
(()=>{'use strict';const T=THREE,B=ChillBlender;
const put=(id,parent,pos=[0,0,0],options={})=>{const m=B.create(id,options);m.group.position.fromArray(pos);parent.add(m.group);return m;};
function ufoModel(parent){const a=CHILL_BLENDER_DATA.ufo.anchors,pivots={claw:a.clawPivot,cable:a.cableTop,carriage:a.carriage};for(let i=0;i<3;i++)pivots['finger_'+i]=a['fingerPivot_'+i];return put('ufo',parent,[0,0,0],{pivots});}
function syncClaw(m,game){
 const a=m.anchors,n=m.nodes,local=p=>p.clone().multiplyScalar(.5).add(new T.Vector3(0,1.05,0));
 const base=local(game.base);n.claw.position.copy(base);n.carriage.position.set(base.x,2.58,base.z);
 const cableTop=2.58;n.cable.position.set(base.x,cableTop,base.z);n.cable.scale.y=Math.max(.02,(cableTop-base.y)/(a.cableTop[1]-a.clawPivot[1]));
 for(let i=0;i<3;i++){const f=game.fingers[i],node=n['finger_'+i],start=local(game.base.clone().add(new T.Vector3(Math.cos(f.angle)*.14,0,Math.sin(f.angle)*.14))),end=local(f.tip.position.clone().add(game.base));const source=new T.Vector3(...a['fingerTip_'+i]).sub(new T.Vector3(...a['fingerPivot_'+i])),target=end.sub(start);node.position.copy(start);node.quaternion.setFromUnitVectors(source.clone().normalize(),target.clone().normalize());node.scale.setScalar(target.length()/source.length());}
}
const U=ChillUfoGame.prototype,oldUfoBuild=U.build,oldPosition=U.positionClaw;
U.build=function(){oldUfoBuild.call(this);const bodies=new Set(this.bodies.map(b=>b.group));for(const o of this.scene.children)if(o.isMesh&&!bodies.has(o))o.visible=false;this.claw.traverse(o=>{if(o.isMesh)o.visible=false;});this.blender15=ufoModel(this.scene);this.blender15.group.scale.setScalar(2);this.blender15.group.position.y=-2.1;if(this.blender15.nodes.roof)this.blender15.nodes.roof.visible=false;this.blender15.nodes.glass?.traverse(o=>{if(o.isMesh)o.material.opacity=.08;});syncClaw(this.blender15,this);};
U.positionClaw=function(){oldPosition.call(this);if(this.blender15)syncClaw(this.blender15,this);};
const Base=ChillCafe;window.ChillCafe=class extends Base{
 constructor(c){super(c);this.blenderModels15=[];this.installBlender15();this.townDock15=document.createElement('div');this.townDock15.className='town-dock15';this.townDock15.setAttribute('aria-label','町の施設へ入る');for(const {el}of this.townLabels14)this.townDock15.appendChild(el);document.body.appendChild(this.townDock15);}
 installBlender15(){
  const c=this.c,s=this.arcadeScene,remember=m=>(this.blenderModels15.push(m),m);
  c.room.static.clear();remember(put('home_shell',c.room.static));
  for(const child of this.group.children.slice(0,3))child.visible=false;
  remember(put('cafe_shell',this.group,[14,0,0]));
  const steam=new Set(this.steam14);for(const child of this.bath.group.children)if(!steam.has(child))child.visible=false;
  this.blenderBath15=remember(put('bath_interior',this.bath.group,[28,0,0]));
  this.waterTime15={value:0};this.blenderBath15.nodes.water?.traverse(o=>{if(!o.isMesh)return;o.material.roughness=.24;o.material.metalness=.08;o.material.color.set('#80c8bd');o.material.onBeforeCompile=shader=>{shader.uniforms.waterTime15=this.waterTime15;shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 waterPosition15;').replace('#include <begin_vertex>','#include <begin_vertex>\nwaterPosition15=position;');shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nuniform float waterTime15; varying vec3 waterPosition15;').replace('#include <color_fragment>','#include <color_fragment>\nfloat wave15=sin(waterPosition15.x*8.0+waterPosition15.z*5.0+sin(waterPosition15.z*3.0+waterTime15*.6)*1.2+waterTime15*.8)+sin(waterPosition15.z*13.0-waterPosition15.x*3.0-waterTime15*.6)*.6+sin(waterPosition15.x*3.0-waterPosition15.z*8.0+waterTime15*.35)*.4; diffuseColor.rgb+=vec3(.09,.12,.11)*smoothstep(1.1,1.7,wave15);').replace('#include <normal_fragment_begin>','#include <normal_fragment_begin>\nnormal=normalize(normal+vec3(sin(waterPosition15.x*8.0+waterTime15)*.055,cos(waterPosition15.z*10.0-waterTime15*.7)*.055,0.0));');};});
  const steamCanvas=document.createElement('canvas');steamCanvas.width=steamCanvas.height=128;const ctx=steamCanvas.getContext('2d'),gradient=ctx.createRadialGradient(64,64,8,64,64,62);gradient.addColorStop(0,'rgba(255,255,243,.8)');gradient.addColorStop(.45,'rgba(255,255,243,.45)');gradient.addColorStop(1,'rgba(255,255,243,0)');ctx.fillStyle=gradient;ctx.fillRect(0,0,128,128);const steamMap=new T.CanvasTexture(steamCanvas);steamMap.colorSpace=T.SRGBColorSpace;
  this.steam14=this.steam14.map(old=>{this.bath.group.remove(old);old.geometry.dispose();old.material.dispose();const p=new T.Sprite(new T.SpriteMaterial({map:steamMap,transparent:true,depthWrite:false,opacity:.15}));p.userData.seed=old.userData.seed;this.bath.group.add(p);return p;});
  const targetGroups=new Set(s.targets.map(t=>t.group));for(const child of s.group.children)if(child!==s.raceGroup&&!targetGroups.has(child))child.visible=false;
  remember(put('arcade_shell',s.group));
  for(const [i,target]of s.targets.filter(t=>t.kind==='gacha').entries()){
   target.group.clear();const spec=CHILL_BLENDER_DATA.gacha;
   const model=remember(put('gacha',target.group,[0,0,0],{pivots:{knob:spec.anchors.knob}}));
   if(i)for(const mat of model.materials)if(/green/i.test(mat.name))mat.color.set('#5bafbf');
   target.handle=model.nodes.knob;
   const capsule=remember(put('capsule',target.group));capsule.group.scale.setScalar(.5);capsule.group.visible=false;target.capsule=capsule.group;
  }
  const u=s.targets.find(t=>t.kind==='ufo');u.group.clear();this.blenderUfo15=remember(ufoModel(u.group));u.group.add(s.ufoDisplay);
  this.worldClaw14=new T.Group();this.worldClaw14.visible=false;u.group.add(this.worldClaw14);
  for(const t of s.targets.filter(t=>t.kind==='race'))t.group.clear();
  const race=remember(put('race',s.group,[-.02,0,2.26]));
  for(const key of ['screen_left','screen_right'])race.nodes[key]?.traverse(o=>{if(o.isMesh){o.material.map=s.raceScreenTexture;o.material.color.set('#ffffff');o.material.emissive.set('#ffffff');o.material.emissiveMap=s.raceScreenTexture;o.material.emissiveIntensity=.4;}});
  if(CHILL_BLENDER_DATA.race_course){for(const child of [...s.raceGroup.children])if(!s.carts.includes(child))s.raceGroup.remove(child);remember(put('race_course',s.raceGroup,[0,0,0],{partOffset:(part,p)=>{if(/topiary|clipped tree/i.test(part.name))return[0,0,-3.8];if(/^Spectator/.test(part.name)){let z=0;for(let i=2;i<p.length;i+=3)z+=p[i];return[0,0,Math.sign(z)*1.25];}return[0,0,0];}}));s.raceGroup.userData.decorated=true;for(const [id,x,z,angle]of [['town_cafe',-4.8,-4.7,.25],['town_home',4.8,4.8,Math.PI+.2],['town_bath',-4.7,4.8,Math.PI-.2],['town_farm',4.8,-4.6,-.25]]){const scenery=remember(put(id,s.raceGroup,[x,0,z]));scenery.group.scale.setScalar(.45);scenery.group.rotation.y=angle;}}
  if(CHILL_BLENDER_DATA.kart)for(let i=0;i<s.carts.length;i++){const cart=s.carts[i];cart.clear();const model=remember(put('kart',cart));cart.scale.setScalar(.65);for(const m of model.materials)if(m.name==='cyan')m.color.set(['#dfad81','#91bea1','#ba9abe','#e9cb69'][i]);}
  this.installTownBlender15(remember);
  this.nightMaterials15=[];for(const m of this.blenderModels15)for(const [name,node]of Object.entries(m.nodes))if(/window|lamp|light/i.test(name))node.traverse(o=>{if(o.isMesh)this.nightMaterials15.push({m:o.material,lamp:/lamp|light/i.test(name),color:o.material.color.clone()});});
 }
 installTownBlender15(remember){
  const town=this.town14;if(!CHILL_BLENDER_DATA.town_terrain)return;
  const proxies=new Set(town.residentProxies.map(p=>p.sprite));for(const child of [...town.group.children])if(!proxies.has(child))town.group.remove(child);
  remember(put('town_terrain',town.group));
  for(const f of town.facilities){const p=f.group.position.clone();f.group=new T.Group();f.group.position.copy(p);town.group.add(f.group);remember(put('town_'+f.id,f.group));}
  const train=remember(put('town_train',town.group,[0,CHILL_BLENDER_TOWN.rail.trainOriginY,-13.6]));town.train=train.group;town.windows=[];town.lamps=[];town.lots=CHILL_BLENDER_TOWN.emptyLots.map(l=>({x:l.center[0],z:l.center[2]}));
 }
 update(a,dt){const result=super.update(a,dt);if(a.arcadeTarget?.kind==='race'&&['waiting','racing'].includes(a.arcadeMode))a.pos.y=.74;return result;}
 prepareRace14(){super.prepareRace14();if(this.raceRun)this.raceRun.progress=[0,-.04,-.08,-.12];}
 setupRaceView(){super.setupRaceView();this.raceFloor.scale.set(4,1,4);this.raceFloor.material.color.setRGB(.16,.43,.07);this.raceCamera.fov=54;this.raceCamera.updateProjectionMatrix();}
 updateRaceCamera14(instant=false){super.updateRaceCamera14(instant);const own=this.racePreviewGroup?.getObjectByName('race-cart-0');if(own)own.visible=!!this.raceChase14;if(this.raceCamera&&!this.raceChase14){const r=this.raceRun||this.lastRace14,a=(r?.progress[0]||0)*Math.PI*2,lane=r?.lane||0,cart=this.arcadeScene.carts[0],tangent=new T.Vector3(-Math.sin(a)*2.76,0,Math.cos(a)*1.2).normalize();this.raceCamera.position.copy(cart.position).addScaledVector(tangent,.05);this.raceCamera.position.y+=.7;this.raceCamera.lookAt(Math.cos(a+.52)*(2.76+lane),.23,Math.sin(a+.52)*(1.2+lane));}}
 afterRender(){super.afterRender();const phase=(this.clock14%CHILL_WORLD_CONFIG.daySeconds)/CHILL_WORLD_CONFIG.daySeconds,night=phase*24<5||phase*24>=19;
  for(const {m,lamp,color}of this.nightMaterials15){m.color.copy(color);m.emissive.set(night?(lamp?'#ffcf7f':'#e6ad61'):'#000000');m.emissiveIntensity=night?(lamp?.9:.45):0;}
  if(this.autoUfo&&!this.autoUfo.closed)syncClaw(this.blenderUfo15,this.autoUfo);
  this.waterTime15.value=this.clock14;this.townDock15.hidden=this.view!=='town'||document.querySelector('#modal').open;
 }
};
})();
