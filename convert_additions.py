import bpy,os,json,math,base64,hashlib,bmesh
from mathutils import Vector
OUT=os.path.join(os.path.dirname(__file__),'model-additions');os.makedirs(OUT,exist_ok=True)
source=bpy.data.filepath;key='P-10' if 'MOBTETSU' in source else 'P-09';sha=hashlib.sha256(open(source,'rb').read()).hexdigest()
for o in bpy.data.objects:
 if o.type=='ARMATURE':o.animation_data_clear();o.data.pose_position='REST'
objects=[o for o in bpy.data.objects if o.type=='MESH' and not any(n in o.name.lower() for n in ['revolver','katana','studio','cord','string'])]
for o in objects:
 for mod in o.modifiers:
  if key=='P-09' and mod.type=='SUBSURF':mod.show_viewport=False
deps=bpy.context.evaluated_depsgraph_get();export=[];allco=[]
for o in objects:
 e=o.evaluated_get(deps);mesh=bpy.data.meshes.new_from_object(e);ob=bpy.data.objects.new('plush_'+o.name,mesh);bpy.context.collection.objects.link(ob);ob.matrix_world=o.matrix_world.copy();bpy.context.view_layer.objects.active=ob;ob.select_set(True)
 if key=='P-10' and 'Character_Body' in o.name:
  bm=bmesh.new();bm.from_mesh(mesh);visited=set();remove=[]
  for v in bm.verts:
   if v in visited:continue
   comp=[];todo=[v];visited.add(v)
   while todo:
    q=todo.pop();comp.append(q)
    for edge in q.link_edges:
     n=edge.other_vert(q)
     if n not in visited:visited.add(n);todo.append(n)
   low=Vector([min(q.co[i] for q in comp) for i in range(3)]);high=Vector([max(q.co[i] for q in comp) for i in range(3)]);mid=(low+high)/2;size=high-low
   if .05<abs(mid.x)<.105 and mid.y<-.12 and .62<mid.z<.75 and size.x<.07 and size.y<.08 and size.z<.16:remove.extend(comp)
  bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.to_mesh(mesh);bm.free();print('REMOVED_CORD_VERTS',len(remove))
 mesh.calc_loop_triangles();tri=len(mesh.loop_triangles)
 if tri>(1500 if key=='P-09' else 350):
  mod=ob.modifiers.new('Static plush reduction','DECIMATE');mod.ratio=.4 if key=='P-09' else .24;bpy.ops.object.modifier_apply(modifier=mod.name)
 allco.extend([ob.matrix_world@v.co for v in ob.data.vertices]);export.append(ob);ob.select_set(False)
lo=Vector([min(v[i] for v in allco) for i in range(3)]);hi=Vector([max(v[i] for v in allco) for i in range(3)]);scale=1.6/(hi.z-lo.z);center=(hi+lo)/2
parts={};textures={}
for ob in export:
 mesh=ob.data;mesh.calc_loop_triangles();uv=mesh.uv_layers.active.data if mesh.uv_layers.active else None
 for tri in mesh.loop_triangles:
  mat=mesh.materials[tri.material_index] if len(mesh.materials) else None;name=mat.name if mat else 'default'
  if name not in parts:
   color=list(mat.diffuse_color[:3]) if mat else [.7,.7,.7];im=None
   if mat and mat.use_nodes:
    bs=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if bs:color=list(bs.inputs['Base Color'].default_value[:3])
    im=next((n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image),None)
   tex=None
   if im:
    if im.name not in textures:
     if max(im.size)>1024:im.scale(1024,1024)
     dest=os.path.join(OUT,key+'-texture.png');im.filepath_raw=dest;im.file_format='PNG';im.save();textures[im.name]='data:image/png;base64,'+base64.b64encode(open(dest,'rb').read()).decode()
    tex=textures[im.name]
   parts[name]={'position':[],'normal':[],'uv':[],'color':color,'texture':tex}
  part=parts[name]
  for li in tri.loops:
   v=mesh.vertices[mesh.loops[li].vertex_index];co=ob.matrix_world@v.co;n=ob.matrix_world.to_3x3()@v.normal
   part['position'].extend([round((co.x-center.x)*scale,5),round((co.z-lo.z)*scale,5),round(-(co.y-center.y)*scale,5)])
   part['normal'].extend([round(n.x,4),round(n.z,4),round(-n.y,4)]);part['uv'].extend([round(uv[li].uv.x,5),round(uv[li].uv.y,5)] if uv else [0,0])
info={'id':key,'source':source,'sourceSHA256':sha,'triangles':sum(len(p['position'])//9 for p in parts.values()),'materials':len(parts),'removed':['weapons','studio','drawcord meshes'],'parts':list(parts.values())}
json.dump(info,open(os.path.join(OUT,key+'.json'),'w'),separators=(',',':'))
for o in list(bpy.data.objects):
 if o not in export:bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,key+'-plush.blend'))
print('EXPORTED',key,info['triangles'],len(parts),sha==hashlib.sha256(open(source,'rb').read()).hexdigest())

