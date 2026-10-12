(function(){'use strict';const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),smooth=t=>t*t*(3-2*t),mix=(a,b,t)=>a.map((v,i)=>v+(b[i]-v)*smooth(clamp(t,0,1)));
window.ChillBagMotion={
 load(a){if(window.ChillResources29?.modern(a))return;const spec=CHILL_BAG_SPRITES.characters.find(c=>c.key===a.key);if(!spec)return;a.bagSpec=spec;new THREE.TextureLoader().load(spec.url,t=>{for(let i=0;i<3;i++){const c=document.createElement('canvas');c.width=c.height=256;c.getContext('2d').drawImage(t.image,i*256,0,256,256,0,0,256,256);const tx=new THREE.CanvasTexture(c);tx.magFilter=tx.minFilter=THREE.LinearFilter;tx.generateMipmaps=false;tx.colorSpace=THREE.SRGBColorSpace;a.textures['bag_'+i]=tx;}a.bagReady=true;t.dispose();});},
 sample(a){const b=a.bagAnimation;if(!b)return null;const t=Math.max(0,b.time-.9);if(b.time<.9)return{pose:'bag_0',index:0,anchor:a.bagSpec.frames[0].bagAnchorPx,itemVisible:false,bagProgress:b.time/.9};
 if(b.eat&&t>=1.35&&t<5.5){let q=t-1.35;return {pose:q<.65?'meal_1':q<1.2?'meal_2':q<3.5?'meal_3':'meal_4',index:2,anchor:a.bagSpec.frames[2].heldItemAnchorPx,itemVisible:!b.consumed};}
 const end=b.eat?5.5:3.15,q=b.eat&&t>=end?t-end+3.15:t;
 let index=q<.7?0:q<1.35?1:q<3.15?2:q<3.8?1:0;
 const f=a.bagSpec.frames,bag=f[0].bagAnchorPx;
 let anchor=q<.35?bag:q<.7?mix(bag,f[0].heldItemAnchorPx,(q-.35)/.35):q<1.35?mix(f[0].heldItemAnchorPx,f[1].heldItemAnchorPx,(q-.7)/.65):q<1.7?mix(f[1].heldItemAnchorPx,f[2].heldItemAnchorPx,(q-1.35)/.35):q<3.15?f[2].heldItemAnchorPx:q<3.8?mix(f[2].heldItemAnchorPx,f[1].heldItemAnchorPx,(q-3.15)/.65):q<4.15?mix(f[1].heldItemAnchorPx,f[0].heldItemAnchorPx,(q-3.8)/.35):mix(f[0].heldItemAnchorPx,bag,(q-4.15)/.35);
 return {pose:'bag_'+index,index,anchor,itemVisible:!b.consumed&&q>=.35&&q<4.45};
 },
 pose(a){return this.sample(a)?.pose;},
 render(a,cafe){const state=this.sample(a),c=cafe.c;if(!a.bagProps){let bag=new THREE.Group(),mat=new THREE.MeshStandardMaterial({color:'#ba8c58',roughness:1}),pouch=new THREE.Mesh(new THREE.SphereGeometry(1,16,10),mat);pouch.scale.set(.18,.14,.08);pouch.position.y=-.14;bag.add(pouch);const rim=new THREE.Mesh(new THREE.TorusGeometry(.12,.022,6,20),new THREE.MeshStandardMaterial({color:'#6f523b',roughness:1}));rim.rotation.x=Math.PI/2;rim.scale.set(1.35,.55,1);bag.add(rim);c.scene.add(bag);a.bagProps={bag,item:null,key:null};}
 const p=a.bagProps,visible=!!state&&a.room===cafe.view;p.bag.visible=visible;if(p.item)p.item.visible=false;if(!state)return;
 const f=a.bagSpec.frames[state.index],origin=c.spriteAnchorWorld(a,f.bagAnchorPx.map(n=>n/256),.1),separation=Math.abs(a.bagSpec.frames[0].activeHandAnchorPx[0]-a.bagSpec.frames[0].supportHandAnchorPx[0])/256*a.scale;
 p.bag.position.copy(origin);p.bag.quaternion.copy(c.camera.quaternion);p.bag.scale.setScalar(Math.max(.55,separation/.32));
 const selected=cafe.collections.state.bags[a.id]?.equippedBag,bought=(window.CHILL_TAILOR_GOODS35||[]).find(x=>x.id===selected&&cafe.collections.items(a.id)[selected]>0);if(p.bagSkin!==bought?.id){if(p.bagSprite){p.bag.remove(p.bagSprite);p.bagSprite.material.map.dispose();p.bagSprite.material.dispose();delete p.bagSprite;}p.bagSkin=bought?.id;for(const child of p.bag.children)child.visible=!bought;if(bought){const tx=new THREE.TextureLoader().load(bought.url);tx.colorSpace=THREE.SRGBColorSpace;p.bagSprite=new THREE.Sprite(new THREE.SpriteMaterial({map:tx,transparent:true,depthWrite:false}));p.bagSprite.scale.set(.5,.5,1);p.bagSprite.position.y=-.11;p.bag.add(p.bagSprite);}}p.bag.scale.multiplyScalar(state.bagProgress===undefined?1:.15+.85*smooth(state.bagProgress));
 const key=a.bagAnimation.item;
 if(p.key!==key){if(p.item){c.scene.remove(p.item);if(p.item.userData.plushRoot){ChillPlushModels.dispose(p.item.userData.plushRoot);p.item.remove(p.item.userData.plushRoot);}p.item.traverse(o=>{o.geometry?.dispose();if(o.material?.map&&o.userData.ownsTexture)o.material.map.dispose();});}p.key=key;p.item=new THREE.Group();const icon=[...CHILL_KEYCHAINS,...(window.CHILL_TAILOR_GOODS35||[]),...(window.CHILL_BREAD36||[])].find(k=>k.id===key);
 if(icon){const tx=new THREE.TextureLoader().load(icon.url);tx.magFilter=tx.minFilter=THREE.LinearFilter;tx.colorSpace=THREE.SRGBColorSpace;const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:tx,transparent:true,alphaTest:.1,depthWrite:false}));sprite.center.set(.5,1-icon.anchor[1]/256);sprite.scale.set(.52,.52,1);sprite.userData.ownsTexture=true;p.item.add(sprite);}
 else if(key.startsWith('P-')&&window.ChillPlushModels){const built=ChillPlushModels.create(key,THREE),model=built.group;p.item.userData.plushRoot=model;model.scale.setScalar(.3);model.position.fromArray(built.spec.gripPoint).multiplyScalar(-.3);p.item.add(model);}
 else if(['dorayaki','omelet','soup'].includes(key)){ChillLiving.meal(p.item,{kind:key},null);p.item.scale.setScalar(.55);}
 else{const ball=new THREE.Mesh(new THREE.SphereGeometry(.1,12,8),new THREE.MeshStandardMaterial({color:'#dabc79'}));p.item.add(ball);}
 c.scene.add(p.item);}
 const anchor=state.anchor.map(n=>n/256);if(a.bagAnimation.eat&&a.bagAnimation.time>=2.25&&a.bagAnimation.time<2.9){const start=anchor,mouth=(a.mealFrameMeta?.[2]?.mouthAnchorPx||[128,155]).map(n=>n/256),u=(a.bagAnimation.time-2.25)/.65;anchor[0]=start[0]+(mouth[0]-start[0])*smooth(u);anchor[1]=start[1]+(mouth[1]-start[1])*smooth(u);}
 p.item.position.copy(c.spriteAnchorWorld(a,anchor,.13));p.item.visible=visible&&state.itemVisible;const goods=(window.CHILL_TAILOR_GOODS35||[]).find(g=>g.id===key);for(const child of p.item.children)if(child.isSprite)child.material.rotation=goods&&!a.bagAnimation.eat&&state.index===2?Math.sin((a.bagAnimation.time-2.25)*3)*.12:0;
 }
};
})();
