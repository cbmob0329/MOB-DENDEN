import bpy,os
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));bpy.ops.wm.open_mainfile(filepath=ROOT+'/slot_symbols.blend');s=bpy.context.scene;s.render.resolution_x=384;s.render.resolution_y=384;s.cycles.samples=32;s.render.film_transparent=True;cam=s.camera;cam.location=(0,-1,.35);cam.rotation_euler=(Vector((0,0,.045))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.18
roots=[o for o in bpy.data.objects if o.type=='EMPTY' and o.name.startswith('SYMBOL_') and o.parent is None]
for o in bpy.data.objects:
 if o.type not in ['LIGHT','CAMERA']:o.hide_render=True
for root in roots:
 name=root['symbol_id'];root.location=(0,0,0);obs=[root]+list(root.children_recursive)
 for o in obs:o.hide_render=False
 cam.data.ortho_scale=.26 if 'MOB' in name else .18
 if name in ['Denden','Pink']:
  cam.location=(0,-1,.06);cam.rotation_euler=(Vector((0,0,.06))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.132
 else:
  cam.location=(0,-1,.35);cam.rotation_euler=(Vector((0,0,.045))-cam.location).to_track_quat('-Z','Y').to_euler()
 s.render.filepath=ROOT+'/symbols/symbol_'+name+'.png';bpy.ops.render.render(write_still=True)
 for o in obs:o.hide_render=True
print('ICONS_COMPLETE')
