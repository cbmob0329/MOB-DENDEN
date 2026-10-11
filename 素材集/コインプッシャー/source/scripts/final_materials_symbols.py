import bpy,os,json,math
ROOT=os.path.dirname(os.path.abspath(__file__));bpy.ops.wm.open_mainfile(filepath=ROOT+'/slot_symbols.blend')
# Gold chest body only: explicit saturated yellow; preserve bronze hardware and wood.
gold=bpy.data.materials.new('MOBP_chest_bright_yellow_gold');gold.use_nodes=True;gold.diffuse_color=(1,.78,.025,1);p=gold.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(1,.78,.025,1);p.inputs['Metallic'].default_value=.32;p.inputs['Roughness'].default_value=.30
root=bpy.data.objects['SYMBOL_goldchest_ROOT']
for o in root.children_recursive:
 if o.type=='MESH':
  for slot in o.material_slots:
   if slot.material and slot.material.name=='MOBP_warm_gold':slot.link='OBJECT';slot.material=gold
# Export centered gold symbol while keep sheet layout.
pos=root.location.copy();root.location=(0,0,0);bpy.ops.object.select_all(action='DESELECT')
for o in [root]+list(root.children_recursive):o.hide_set(False);o.select_set(True)
bpy.context.view_layer.objects.active=root;bpy.ops.export_scene.gltf(filepath=ROOT+'/symbols/symbol_goldchest.glb',export_format='GLB',use_selection=True,export_extras=True);root.location=pos
# Cream background and readable labels; texture portraits retain supplied art colors.
s=bpy.context.scene;s.render.film_transparent=False;s.world.use_nodes=True;bg=s.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.83,.76,.62,1);bg.inputs['Strength'].default_value=.8;s.render.engine='BLENDER_EEVEE_NEXT';s.eevee.taa_render_samples=32
for o in bpy.data.objects:
 if o.type=='FONT':o.data.size=.023
 if o.type=='LIGHT':o.data.energy=120
for name in ['Denden','Pink']:
 ma=bpy.data.materials['SYMBOL_'+name+'_ReferencePortrait'];p=ma.node_tree.nodes.get('Principled BSDF');im=next(n for n in ma.node_tree.nodes if n.type=='TEX_IMAGE');ma.node_tree.links.new(im.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=.5
s.render.filepath=ROOT+'/previews/CLEAN_06_ten_slot_symbols.png';bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/slot_symbols.blend');bpy.ops.render.render(write_still=True)
# Update only goldchest PNG using the same corrected material.
from mathutils import Vector
for o in bpy.data.objects:
 if o.type not in ['LIGHT','CAMERA']:o.hide_render=True
for o in [root]+list(root.children_recursive):o.hide_render=False
root.location=(0,0,0);cam=s.camera;cam.location=(0,-1,.35);cam.rotation_euler=(Vector((0,0,.045))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.18;s.render.resolution_x=384;s.render.resolution_y=384;s.render.film_transparent=True;s.render.filepath=ROOT+'/symbols/symbol_goldchest.png';bpy.ops.render.render(write_still=True)
print('SYMBOL_MATERIALS_COMPLETE')
