/* Restricted glTF 2 loader for this uncompressed, unskinned, material-only asset pack.
 * The original node hierarchy/TRS, mesh indices, normals and materials are preserved.
 * Unsupported required extensions fail visibly instead of silently changing geometry. */
(()=>{'use strict';const T=THREE,cache=new Map();
function parse(encoded){
 const raw=atob(encoded),bytes=Uint8Array.from(raw,c=>c.charCodeAt(0)),view=new DataView(bytes.buffer);
 if(view.getUint32(0,true)!==0x46546c67||view.getUint32(4,true)!==2)throw Error('Invalid GLB');
 let doc,bin;for(let p=12;p<bytes.length;){const len=view.getUint32(p,true),type=view.getUint32(p+4,true);p+=8;if(type===0x4e4f534a)doc=JSON.parse(new TextDecoder().decode(bytes.subarray(p,p+len)));if(type===0x004e4942)bin=bytes.slice(p,p+len);p+=len;}
 if(doc.extensionsRequired?.length||doc.skins?.length)throw Error('Unsupported GLB extension/skin');
 const constructors={5120:Int8Array,5121:Uint8Array,5122:Int16Array,5123:Uint16Array,5125:Uint32Array,5126:Float32Array},sizes={SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT4:16};
 function accessor(id){const a=doc.accessors[id],b=doc.bufferViews[a.bufferView],C=constructors[a.componentType],size=sizes[a.type];if(a.sparse||b.byteStride&&b.byteStride!==size*C.BYTES_PER_ELEMENT)throw Error('Unsupported interleaved GLB');const offset=(b.byteOffset||0)+(a.byteOffset||0),data=new C(bin.buffer.slice(offset,offset+a.count*size*C.BYTES_PER_ELEMENT));return new T.BufferAttribute(data,size,!!a.normalized);}
 const mats=(doc.materials||[]).map(m=>{const p=m.pbrMetallicRoughness||{},c=p.baseColorFactor||[1,1,1,1];if(p.baseColorTexture)throw Error('Unexpected texture in cabinet/prize GLB');const mat=new T.MeshStandardMaterial({color:new T.Color().setRGB(...c.slice(0,3)),metalness:p.metallicFactor??1,roughness:p.roughnessFactor??1,opacity:c[3],transparent:m.alphaMode==='BLEND'||c[3]<1,side:m.doubleSided?T.DoubleSide:T.FrontSide,emissive:new T.Color().setRGB(...(m.emissiveFactor||[0,0,0]))});mat.name=m.name||'';if(mat.transparent)mat.depthWrite=false;return mat;});
 const meshes=(doc.meshes||[]).map(m=>{const g=new T.Group();for(const p of m.primitives){if(p.mode!==undefined&&p.mode!==4)throw Error('Unsupported primitive');const geo=new T.BufferGeometry();for(const [key,id]of Object.entries(p.attributes)){const name={POSITION:'position',NORMAL:'normal',TEXCOORD_0:'uv'}[key];if(name)geo.setAttribute(name,accessor(id));}if(p.indices!==undefined)geo.setIndex(accessor(p.indices));if(!geo.attributes.normal)geo.computeVertexNormals();const mesh=new T.Mesh(geo,mats[p.material]||new T.MeshStandardMaterial());mesh.castShadow=!mesh.material.transparent;mesh.receiveShadow=true;g.add(mesh);}return g;});
 const nodes=doc.nodes.map(n=>{const g=n.mesh===undefined?new T.Group():meshes[n.mesh].clone(true);g.name=n.name||'';g.userData={...n.extras};if(n.matrix)new T.Matrix4().fromArray(n.matrix).decompose(g.position,g.quaternion,g.scale);else{if(n.translation)g.position.fromArray(n.translation);if(n.rotation)g.quaternion.fromArray(n.rotation);if(n.scale)g.scale.fromArray(n.scale);}return g;});
 doc.nodes.forEach((n,i)=>n.children?.forEach(j=>nodes[i].add(nodes[j])));const root=new T.Group();for(const i of doc.scenes[doc.scene||0].nodes)root.add(nodes[i]);root.updateMatrixWorld(true);return root;
}
window.ChillPusherAssets={create(id){if(!cache.has(id)){const data=CHILL_PUSHER_ASSETS.models[id];if(!data)throw Error('Missing model '+id);cache.set(id,parse(data));}return cache.get(id).clone(true);},parse};
})();
