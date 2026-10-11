import bpy,sys,os,math,json,shutil
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,ROOT)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
import prizes
assets=prizes.build_prizes()
for objs in assets.values():
 for o in objs:o.hide_render=True;o.hide_set(True)
os.makedirs(ROOT+'/symbols',exist_ok=True)
symbols={}
def root(name):
 o=bpy.data.objects.new('SYMBOL_'+name+'_ROOT',None);bpy.context.collection.objects.link(o);o['symbol_id']=name;return o

def dup(asset,parent,loc=(0,0,0),scale=1):
 old=assets[asset];ds={}
 for o in old:
  n=o.copy();bpy.context.collection.objects.link(n);n.hide_render=False;n.hide_set(False);n.name='SYMBOL_'+parent['symbol_id']+'_'+o.name;ds[o]=n
 for o,n in ds.items():n.parent=ds.get(o.parent,parent)
 r=ds[old[0]];r.location=loc;r.scale=(scale,)*3
 return list(ds.values())
for col in ['red','blue','green']:
 r=root(col+'MOB');obs=[r]
 for letter,x in zip('MOB',[-.068,0,.068]):obs+=dup('letter_'+letter+'_'+col,r,(x,0,0),.82)
 symbols[col+'MOB']=obs
for key,asset in [('dorayaki','dorayaki'),('coinbag','coin_bag'),('woodchest','wood_chest'),('goldchest','gold_chest')]:
 r=root(key);symbols[key]=[r]+dup(asset,r)
r=root('7');bpy.ops.object.text_add(rotation=(math.pi/2,0,0));o=bpy.context.object;o.name='SYMBOL_Lucky7_MESH';o.data.body='7';o.data.align_x='CENTER';o.data.size=.15;o.data.extrude=.007;o.data.bevel_depth=.002;o.data.bevel_resolution=1;o.data.resolution_u=4;o.data.materials.append(bpy.data.materials['MOBP_letter_red']);bpy.ops.object.convert(target='MESH');o.parent=r;symbols['7']=[r,o]
refs={'Denden':('/workspace/shared/mob_references/original_a/2245C966-C9B2-4D15-971E-A5BDA7141EA4(20261004-012331).jpeg',(400/1536,1-835/1369,1280/1536,1.0)), 'Pink':('/workspace/shared/mob_references/original_b/25FD9829-5E07-4020-AE0F-FDE216521516(3).jpeg',(255/1190,1-910/1536,1175/1190,1.0))}
for name,(path,uvbox) in refs.items():
 r=root(name);ma=bpy.data.materials.new('SYMBOL_'+name+'_ReferencePortrait');ma.use_nodes=True;n=ma.node_tree.nodes;p=n.get('Principled BSDF');im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(path);im.image.pack();ma.node_tree.links.new(im.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=1
 me=bpy.data.meshes.new('SYMBOL_'+name+'_Portrait');me.from_pydata([(-.06,0,0),(.06,0,0),(.06,0,.12),(-.06,0,.12)],[],[(0,1,2,3)]);me.update();o=bpy.data.objects.new('SYMBOL_'+name+'_Portrait',me);bpy.context.collection.objects.link(o);o.parent=r;o.data.materials.append(ma);layer=me.uv_layers.new();u1,v1,u2,v2=uvbox
 for loop,uv in zip(layer.data,[(u1,v1),(u2,v1),(u2,v2),(u1,v2)]):loop.uv=uv
 r['reference_source']=os.path.basename(path);r['identity']='verified user character reference';symbols[name]=[r,o]
for name,obs in symbols.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[-1]
 bpy.ops.export_scene.gltf(filepath=ROOT+'/symbols/symbol_'+name+'.glb',export_format='GLB',use_selection=True,export_extras=True)
 for o in obs:o.hide_render=True
# contact sheet of all actual 3D symbol models; no invented character artwork.
for idx,(name,obs) in enumerate(symbols.items()):
 r=obs[0];r.location=((idx%5-2)*.26,0,-(idx//5)*.25)
 for o in obs:o.hide_render=False
 bpy.ops.object.text_add(location=(r.location.x,-.01,r.location.z-.046),rotation=(math.pi/2,0,0));t=bpy.context.object;t.data.body=name;t.data.align_x='CENTER';t.data.size=.020
 ma=bpy.data.materials.get('ContactLabel')
 if not ma:ma=bpy.data.materials.new('ContactLabel');ma.diffuse_color=(.08,.07,.1,1)
 t.data.materials.append(ma)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False
scene.world.color=(.8,.8,.8)
bpy.ops.object.light_add(type='AREA',location=(0,-1,2));l=bpy.context.object;l.data.energy=80;l.data.size=3;l.rotation_euler=(Vector((0,0,0))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,-2,.35));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,-.045))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.42;scene.camera=cam;scene.render.resolution_x=1600;scene.render.resolution_y=750;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.film_transparent=True
scene.render.filepath=ROOT+'/previews/06_ten_slot_symbols.png'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/slot_symbols.blend');bpy.ops.render.render(write_still=True)
meta={name:{'file':'symbols/symbol_'+name+'.glb','type':'textured_reference_portrait' if name in refs else '3D_mesh','reference':refs[name][0].split('/')[-1] if name in refs else None} for name in symbols}
with open(ROOT+'/symbols/symbols_manifest.json','w') as f:json.dump(meta,f,indent=2)
