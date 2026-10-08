/* Runtime meshes exported from editable Blender sources; no procedural replacements. */
(()=>{'use strict';
const T=THREE,cache=new Map();
function floats(value){if(Array.isArray(value))return new Float32Array(value);const raw=atob(value),b=new Uint8Array(raw.length);for(let i=0;i<raw.length;i++)b[i]=raw.charCodeAt(i);return new Float32Array(b.buffer);}
function create(id,options={}){
 const spec=CHILL_BLENDER_DATA[id];if(!spec)throw new Error('Missing Blender model: '+id);
 const group=new T.Group(),nodes={},materials=[],buckets=new Map();group.name='Blender:'+id;
 for(const part of spec.parts){const key=part.node+'|'+JSON.stringify(part.material);if(!buckets.has(key))buckets.set(key,{node:part.node||'static',material:part.material,parts:[]});buckets.get(key).parts.push(part);}
 for(const bucket of buckets.values()){
  const node=nodes[bucket.node]||(nodes[bucket.node]=new T.Group());node.name=bucket.node;if(!node.parent)group.add(node);
  const m=bucket.material,pivot=options.pivots?.[bucket.node]||[0,0,0];node.position.fromArray(pivot);
  const pos=[],norm=[],uv=[];for(const part of bucket.parts){const p=floats(part.positions),n=floats(part.normals),offset=options.partOffset?.(part,p)||[0,0,0];for(let i=0;i<p.length;i++)pos.push(p[i]+offset[i%3]-pivot[i%3]);for(const v of n)norm.push(v);if(part.uv)for(const v of floats(part.uv))uv.push(v);}
  const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(pos,3));geo.setAttribute('normal',new T.Float32BufferAttribute(norm,3));if(uv.length===pos.length/3*2)geo.setAttribute('uv',new T.Float32BufferAttribute(uv,2));geo.computeBoundingSphere();
  let color=new T.Color().setRGB(...(m.color||[.6,.6,.6]));if(options.colors?.[m.name])color=new T.Color(options.colors[m.name]);
  const mat=new T.MeshStandardMaterial({color,roughness:m.roughness??.85,metalness:m.metallic??0,opacity:m.opacity??1,transparent:(m.opacity??1)<1,depthWrite:(m.opacity??1)>=1,side:T.DoubleSide});mat.name=m.name||'';
  if(m.texture){let tx=cache.get(m.texture);if(!tx){tx=new T.TextureLoader().load(m.texture);tx.colorSpace=T.SRGBColorSpace;cache.set(m.texture,tx);}mat.map=tx;mat.color.setRGB(1,1,1);}
  const mesh=new T.Mesh(geo,mat);mesh.name=bucket.node+':'+m.name;mesh.castShadow=!mat.transparent;mesh.receiveShadow=true;node.add(mesh);materials.push(mat);
 }
 group.userData.blenderAsset=id;return {group,nodes,materials,anchors:spec.anchors||{},bounds:spec.bounds,triangleCount:spec.triangleCount};
}
window.ChillBlender={create,ids:()=>Object.keys(CHILL_BLENDER_DATA),dispose(group){group.traverse(o=>{o.geometry?.dispose();if(o.material)for(const m of Array.isArray(o.material)?o.material:[o.material])m.dispose();});}};
})();
