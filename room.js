/* Furniture owns geometry, collision bounds and action sockets. No character art is generated here. */
window.ChillRoom=class ChillRoom{
 constructor(scene){this.scene=scene;this.furniture={};this.layout=0;this.theme=0;this.preview=null;this.materials={};this.static=new THREE.Group();scene.add(this.static);this.buildShell();this.applyLayout(0);}
 material(name,color){return this.materials[name]||(this.materials[name]=new THREE.MeshStandardMaterial({color,roughness:.86}));}
 box(g,x,y,z,w,h,d,m,rot=0){let o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),typeof m==='string'?this.material(m,m):m);o.position.set(x,y,z);o.rotation.y=rot;o.castShadow=o.receiveShadow=true;g.add(o);return o;}
 cyl(g,x,y,z,rt,rb,h,m,n=28){let o=new THREE.Mesh(new THREE.CylinderGeometry(rt,rb,h,n),typeof m==='string'?this.material(m,m):m);o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;g.add(o);return o;}
 buildShell(){const g=this.static,b=(...a)=>this.box(g,...a);this.wood=this.material('wood','#b99062');this.oak=this.material('oak','#d9b483');this.cream=this.material('cream','#f0ead8');this.fabric=this.material('fabric','#8ea27b');this.blanket=this.material('blanket','#b2c4a1');this.accent=this.material('accent','#d4a590');this.leaf=this.material('leaf','#819b70');
 b(0,-.24,0,10.7,.48,8.7,this.cream);for(let z=-4;z<4;z+=.4)for(let x=-5;x<5;x+=2)b(x+1,.006,z+.2,1.982,.04,.385,(Math.round(z*10+x)%3===0)?'#d7b88e':'#e0c399');
 b(0,1.5,-4.13,10.4,3,.16,'#dfe1d0');b(-5.13,1.5,0,.16,3,8.4,'#e8e6d8');b(0,.13,-4,10,.2,.1,this.cream);b(-5,.13,0,.1,.2,8,this.cream);
 b(-2.3,2,-4,3.2,1.7,.13,this.oak);b(-2.3,2,-3.91,2.96,1.48,.1,'#b6d3ce');for(let x of [-3.75,-2.3,-.85])b(x,2,-3.82,.06,1.52,.1,this.cream);b(-2.3,2,-3.82,3.05,.06,.1,this.cream);b(-2.3,1.13,-3.75,3.45,.12,.45,this.cream);for(let x of [-4.04,-.56]){b(x,2,-3.72,.34,2.1,.13,'#f3eddf');for(let i=0;i<4;i++)b(x-.14+i*.095,2,-3.63,.03,2.08,.025,'#e1ddca')}
 b(-.7,.04,.65,3.9,.035,3.6,'#ded4bb');for(let z of [-1.08,2.37])b(-.7,.064,z,3.8,.008,.05,'#bfb091');
 b(.25,2.2,-3.98,.8,.8,.08,this.oak);b(.25,2.2,-3.92,.65,.65,.03,'#eee1c3');b(.2,2.24,-3.88,.28,.28,.02,this.accent,.4);
 this.cyl(g,-4.5,.8,2.85,.07,.18,1.6,this.wood);this.cyl(g,-4.5,1.7,2.85,.4,.25,.48,this.cream);
 }
 configs(){return [
 {sofa:[-3.85,.05,0],bed:[3.5,1.7,0],table:[1.0,-2.15,0],shelf:[3.55,-3.55,0],plant:[-4.3,-2.75,0],deck:[.5,2.65,0]},
 {sofa:[-3.8,.8,0],bed:[3.5,.95,0],table:[.55,-2.3,0],shelf:[3.55,-3.55,0],plant:[-4.3,-2.7,0],deck:[-.2,2.65,0]},
 {sofa:[-3.85,-.2,0],bed:[3.25,1.45,Math.PI/2],table:[.7,-1.95,0],shelf:[3.6,-3.55,0],plant:[-4.35,-2.75,0],deck:[-.45,2.65,0]}
 ];}
 create(key,x,z,rotation){let f={key,group:new THREE.Group(),sockets:{},w:1,d:1};f.group.position.set(x,0,z);f.group.rotation.y=rotation;this.scene.add(f.group);this.furniture[key]=f;const b=(...a)=>this.box(f.group,...a),c=(...a)=>this.cyl(f.group,...a);const socket=(k,a)=>f.sockets[k]=new THREE.Vector3(...a);
 if(key==='sofa'){f.w=1.6;f.d=2.7;b(0,.44,0,1.4,.65,2.6,this.fabric);b(-.61,.95,0,.25,1.2,2.7,this.fabric);for(let zz of [-1.25,1.25])b(0,.8,zz,1.6,.9,.2,this.fabric);for(let zz of [-.56,.5])b(.06,.82,zz,1.15,.19,.95,this.blanket);b(-.25,1.05,-.7,.3,.48,.5,this.accent);socket('entry',[1.13,0,.4]);socket('seat',[.18,.915,.4]);}
 if(key==='bed'){f.w=2;f.d=3;b(0,.33,0,2,.5,3,this.oak);b(0,.65,0,1.92,.3,2.94,this.cream);b(0,.83,.4,1.96,.13,1.93,this.blanket);for(let xx of [-.43,.43])b(xx,.85,-.95,.76,.1,.5,'#fffced');b(0,.9,-1.48,2.06,1.15,.12,this.oak);socket('entry',[-1.37,0,.3]);socket('edge',[-.68,.90,.3]);socket('center',[0,.90,0]);}
 if(key==='table'){f.w=1.6;f.d=1.6;c(0,.89,0,.78,.78,.11,this.oak);c(0,.44,0,.11,.35,.86,this.cream);c(.16,.969,.12,.24,.24,.025,'#fcf6e5');socket('entry',[.15,0,1.16]);socket('food',[.16,1.015,.12]);}
 if(key==='shelf'){f.w=2.1;f.d=.62;b(0,1.2,0,2.1,2.35,.5,this.oak);for(let y of [.38,1,1.68,2.35])b(0,y,.24,2.1,.085,.7,this.cream);for(let j=0;j<3;j++)for(let i=0;i<6;i++)b(-.85+i*.27,(j===0?.60:.54+j*.68),.17,.16,.39+(i%3)*.07,.3,['#8f9d85','#c99583','#e2cda6','#9eb9b1'][i%4]);socket('entry',[-.24,0,.99]);socket('book',[-.22,.45,.48]);}
 if(key==='plant'){f.w=.7;f.d=.7;c(0,.31,0,.31,.2,.62,'#c89979');f.leaves=[];for(let i=0;i<8;i++){let a=i*2.4,l=new THREE.Mesh(new THREE.SphereGeometry(.2,8,8),this.leaf);l.scale.set(.65,2,.65);l.position.set(Math.cos(a)*.22,.75+i*.06,Math.sin(a)*.22);l.rotation.z=Math.cos(a)*.5;f.group.add(l);f.leaves.push(l)}socket('entry',[.9,0,.2]);socket('water',[.18,.635,.1]);f.group.scale.y=.45;}
 if(key==='deck'){f.w=1.8;f.d=.78;
 // Low console, measured hand-height working platters, and a safe floor approach in front.
 b(0,.10,0,1.8,.16,.72,this.wood);b(0,.195,0,1.88,.03,.8,this.cream);
 for(let [i,xx]of [-.55,.55].entries()){let surface=i?.33:.27;b(xx,(surface+.20)/2,.06,.58,surface-.20,.62,'#4c5c52');let disc=c(xx,surface-.011,.17,.215,.215,.022,'#283d36');c(xx,surface+.006,.17,.065,.065,.012,this.accent);this.box(disc,.12,.018,0,.06,.008,.018,'#b3bfa7');f.discs=f.discs||[];f.discs.push(disc);b(xx+.19,surface+.025,-.02,.02,.025,.26,'#c4b887',.3);let speaker=c(xx,.12,-.374,.065,.065,.03,'#34463d');speaker.rotation.x=Math.PI/2;}
 for(let xx of [-.12,0,.12])b(xx,.237,.07,.04,.04,.28,'#718477');
 socket('entry',[0,0,.92]);socket('hands',[-.55,.27,.385]);socket('hands_denden',[-.55,.27,.385]);socket('hands_pink',[.55,.33,.385]);}

 return f;}
 applyLayout(index){for(let f of Object.values(this.furniture)){this.scene.remove(f.group);f.group.traverse(o=>o.geometry?.dispose())}this.furniture={};this.layout=index;for(let [key,v]of Object.entries(this.configs()[index]))this.create(key,...v);this.bounds=Object.values(this.furniture).map(f=>{let a=f.group.rotation.y;return{x:f.group.position.x,z:f.group.position.z,w:Math.abs(Math.cos(a))*f.w+Math.abs(Math.sin(a))*f.d+.36,d:Math.abs(Math.sin(a))*f.w+Math.abs(Math.cos(a))*f.d+.36,key:f.key}});this.bounds.push({x:-4.5,z:2.85,w:.7,d:.7,key:'lamp'});this.scene.updateMatrixWorld(true);}
 applyTheme(index){this.theme=index;const colors=[['#8ea27b','#b2c4a1','#d4a590'],['#c7999d','#e2c2b4','#a6b999'],['#7d969c','#b3c3bd','#d1b080']][index];this.fabric.color.set(colors[0]);this.blanket.color.set(colors[1]);this.accent.color.set(colors[2]);}
 socket(key,name){this.scene.updateMatrixWorld(true);return this.furniture[key].group.localToWorld(this.furniture[key].sockets[name].clone());}
 valid(x,z){return x>=-4.6&&x<=4.6&&z>=-3.55&&z<=3.65&&!this.bounds.some(o=>Math.abs(x-o.x)<o.w/2&&Math.abs(z-o.z)<o.d/2);}
 contactFloorValid(x,z,key){return x>=-4.6&&x<=4.6&&z>=-3.55&&z<=3.65&&!this.bounds.some(o=>{let inset=o.key===key?.12:0;return Math.abs(x-o.x)<(o.w-inset)/2&&Math.abs(z-o.z)<(o.d-inset)/2});}
 previewLayout(index){this.clearPreview();let g=new THREE.Group(),m=new THREE.MeshBasicMaterial({color:0x91ae85,transparent:true,opacity:.2,depthWrite:false});for(let [key,v]of Object.entries(this.configs()[index])){let f=this.furniture[key],o=new THREE.Mesh(new THREE.BoxGeometry(f.w,.08,f.d),m);o.position.set(v[0],.12,v[1]);o.rotation.y=v[2];g.add(o)}this.preview=g;this.scene.add(g);}
 clearPreview(){if(this.preview){this.scene.remove(this.preview);this.preview.traverse(o=>o.geometry?.dispose());this.preview=null;}}
};
