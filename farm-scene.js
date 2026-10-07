/* Mesh-only farm; no generated crop/animal PNGs and no resident substitutes. */
(function(root){'use strict';
class FarmScene {
  constructor(THREE){this.T=THREE;this.group=new THREE.Group();this.materials={};this.pickables=[];this.plots=[];this.crops=[];this.eggMeshes=[];this.build();}
  material(color){return this.materials[color]||(this.materials[color]=new this.T.MeshStandardMaterial({color,roughness:.88}));}
  mesh(parent,geometry,color,x,y,z,sx=1,sy=1,sz=1){const m=new this.T.Mesh(geometry,this.material(color));m.position.set(x,y,z);m.scale.set(sx,sy,sz);m.castShadow=m.receiveShadow=true;parent.add(m);return m;}
  ball(g,c,x,y,z,sx,sy,sz){return this.mesh(g,new this.T.SphereGeometry(1,12,8),c,x,y,z,sx,sy,sz);}
  box(g,c,x,y,z,w,h,d){return this.mesh(g,new this.T.BoxGeometry(w,h,d),c,x,y,z);}
  post(g,c,x,y,z,r,h){return this.mesh(g,new this.T.CylinderGeometry(r,r,h,10),c,x,y,z);}
  pick(group,action,index){group.traverse(o=>{if(o.isMesh){o.userData.farmAction={action,index};this.pickables.push(o);}});}
  fence(x1,x2,z){for(let x=x1;x<=x2+.01;x+=.8)this.post(this.group,'#edce94',x,.46,z,.065,.85);for(const y of [.32,.66])this.box(this.group,'#f6dfb2',(x1+x2)/2,y,z,x2-x1,.09,.08);}
  build(){const T=this.T,g=this.group;
    this.box(g,'#bfcea0',0,-.2,0,10.8,.35,8.4);
    this.box(g,'#e9d6aa',0,-.01,2.7,10.5,.08,1.35);
    this.fence(-4.8,4.8,-3.7);this.fence(-4.8,-2.4,3.55);this.fence(2.4,4.8,3.55);
    for(let i=0;i<9;i++){let x=(i%3-1)*1.15-1.3,z=(Math.floor(i/3)-1)*1.15-.5,p=new T.Group();p.position.set(x,0,z);g.add(p);this.box(p,'#815d42',0,.04,0,1.02,.16,1.02);for(let r=-1;r<=1;r++)this.box(p,'#9b7050',r*.26,.135,0,.11,.045,.9);this.plots.push(p);this.pick(p,'plot',i);const crop=new T.Group();p.add(crop);this.crops.push(crop);}
    // Separate livestock patch beside the 3x3 cultivated beds.
    this.box(g,'#d8d4a2',3.05,-.005,-.35,3.1,.11,5.8);
    this.fence(1.65,4.45,-2.9);
    this.cow=new T.Group();this.cow.position.set(3.15,0,-1.65);g.add(this.cow);this.buildCow(this.cow);this.pick(this.cow,'milk');
    this.hen=new T.Group();this.hen.position.set(2.35,0,.65);g.add(this.hen);this.buildHen(this.hen);this.pick(this.hen,'egg');
    const nest=new T.Group();nest.position.set(3.55,0,1.05);g.add(nest);this.ball(nest,'#b99559',0,.12,0,.65,.14,.48);
    for(let i=0;i<3;i++){const e=this.ball(nest,'#fff2d5',(i-1)*.29,.3,(i%2)*.1,.12,.17,.12);this.eggMeshes.push(e);}this.pick(nest,'egg');
    this.milkBubble=new T.Group();this.milkBubble.position.set(3.15,2.1,-1.65);g.add(this.milkBubble);this.ball(this.milkBubble,'#fff5d5',0,0,0,.3,.3,.15);this.post(this.milkBubble,'#c0e5e4',0,0,.16,.11,.24);this.pick(this.milkBubble,'milk');
    const store=new T.Group();store.position.set(-3.7,0,2.2);g.add(store);this.box(store,'#bd8352',0,.35,0,1.05,.7,.65);this.box(store,'#edc692',0,.74,0,1.14,.12,.73);this.box(store,'#6e513c',0,.42,.34,.16,.17,.04);this.pick(store,'storage');
    const scare=new T.Group();scare.position.set(-4.1,0,-2.8);g.add(scare);this.post(scare,'#8e6945',0,.8,0,.07,1.6);this.box(scare,'#c28c55',0,1.17,0,1.25,.09,.1);this.ball(scare,'#282726',0,1.7,0,.32,.32,.25);this.ball(scare,'#393635',0,1.9,-.01,.36,.18,.29);for(let x of [-.23,.23]){const ear=this.mesh(scare,new T.ConeGeometry(.14,.28,4),'#393635',x,2.08,-.01);ear.rotation.y=Math.PI/4;}for(let x of [-.12,.12]){let rim=this.mesh(scare,new T.TorusGeometry(.105,.025,6,16),'#161616',x,1.71,.235);this.ball(scare,'#c6c4b2',x,1.71,.242,.075,.075,.014);}this.box(scare,'#161616',0,1.72,.26,.08,.025,.025);
    const cv=document.createElement('canvas');cv.width=256;cv.height=96;const ctx=cv.getContext('2d');ctx.fillStyle='#f6e1b9';ctx.fillRect(0,0,256,96);ctx.fillStyle='#5e4835';ctx.font='bold 58px sans-serif';ctx.textAlign='center';ctx.fillText('MOB',128,69);const mat=new T.MeshStandardMaterial({map:new T.CanvasTexture(cv),roughness:1});let sign=new T.Mesh(new T.BoxGeometry(.9,.34,.06),mat);sign.position.set(0,1.02,.13);scare.add(sign);
  }
  buildHen(g){this.ball(g,'#fff4de',0,.57,0,.43,.45,.48);this.ball(g,'#fffaf0',0,.99,-.19,.26,.29,.27);for(let x of [-.15,.15]){this.ball(g,'#35302b',x,1.04,-.4,.038,.048,.035);this.post(g,'#df9d37',x,.17,0,.036,.25);this.box(g,'#df9d37',x,.06,-.09,.2,.05,.25);}this.ball(g,'#eaba47',0,.92,-.45,.1,.08,.13);for(let i=0;i<3;i++)this.ball(g,'#d87968',0,1.24+i*.025,-.22+i*.13,.07,.13,.09);this.ball(g,'#e6d9bd',.37,.55,.01,.11,.26,.3);this.ball(g,'#e6d9bd',-.37,.55,.01,.11,.26,.3);this.ball(g,'#fff4de',0,.72,.4,.18,.3,.22);}
  buildCow(g){this.ball(g,'#fff3de',0,.86,0,.61,.5,.85);this.ball(g,'#68584b',.48,.92,.2,.17,.31,.32);this.ball(g,'#68584b',-.3,1.18,.35,.22,.12,.28);for(let x of [-.37,.37])for(let z of [-.49,.49]){this.post(g,'#f6e8d2',x,.35,z,.11,.6);this.post(g,'#67564a',x,.1,z,.12,.18);}this.ball(g,'#fff3de',0,1.23,-.68,.44,.47,.36);this.ball(g,'#e7b59c',0,1.04,-.97,.38,.23,.15);for(let x of [-.22,.22]){this.ball(g,'#332f2b',x,1.37,-.97,.044,.061,.025);this.ball(g,'#a47561',x*.65,1.09,-1.11,.027,.04,.015);this.ball(g,'#f1d1b7',x*2.3,1.39,-.64,.19,.085,.13);this.mesh(g,new this.T.ConeGeometry(.07,.2,8),'#c8ae81',x,1.72,-.62);}this.ball(g,'#e3af98',0,.46,.1,.23,.15,.27);const tail=this.post(g,'#e1ceb1',.2,.84,.83,.045,.65);tail.rotation.x=.35;this.ball(g,'#68584b',.2,.55,.94,.075,.11,.075);}
  buildCrop(g,kind,stage){if(stage===0)return;const scale=[0,.26,.46,.72,1][stage];for(let i=0;i<3;i++){const p=new this.T.Group();p.position.set((i-1)*.27,.12,(i%2)*.27-.13);g.add(p);const height=kind==='corn'?1.2:kind==='beans'?.65:.8;this.post(p,kind==='wheat'&&stage===4?'#c4a357':'#71974d',0,height*scale/2,0,.023,height*scale);for(let side of [-1,1]){let leaf=this.ball(p,'#789e53',side*.12*scale,height*scale*.55,0,.2*scale,.035*scale,.065*scale);leaf.rotation.z=side*.4;}if(stage>=3){if(kind==='wheat'){for(let n=0;n<4;n++)this.ball(p,stage===4?'#e7c36d':'#9bab60',(n%2?1:-1)*.045,height*scale+n*.04,0,.055,.06,.04);}else if(kind==='corn'){this.ball(p,stage===4?'#f4d36c':'#a7b15c',.08,height*scale*.7,0,.085,.21,.085);}else for(let n=0;n<2;n++)this.ball(p,stage===4?'#a57659':'#8cb168',(n?1:-1)*.1,height*scale*.6,0,.05,.14,.055);}}}
  update(model,at,time=0){for(let i=0;i<9;i++){const p=model.plot(i,at),key=p.crop+':'+p.stage;const g=this.crops[i];if(g.userData.key!==key){while(g.children.length){const c=g.children[0];g.remove(c);c.traverse(o=>o.geometry?.dispose());}if(p.crop)this.buildCrop(g,p.crop,p.stage);g.userData.key=key;}}this.eggMeshes.forEach((e,i)=>e.visible=i<model.state.hen.eggs);this.milkBubble.visible=model.state.cow.ready;this.hen.rotation.y=Math.PI+Math.sin(time*.8)*.1;this.cow.rotation.y=Math.PI+Math.sin(time*.4)*.035;}
  dispose(){this.group.traverse(o=>o.geometry?.dispose());Object.values(this.materials).forEach(m=>m.dispose());this.group.parent?.remove(this.group);}
}
root.ChillFarmScene=FarmScene;
})(window);
