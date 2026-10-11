import bpy,os
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));bpy.ops.wm.open_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend');s=bpy.context.scene;s.render.engine='BLENDER_EEVEE_NEXT';s.eevee.taa_render_samples=48
m=bpy.data.materials.get('Glass • clear front');m.surface_render_method='BLENDED';m.use_transparency_overlap=False
s.render.resolution_x=1280;s.render.resolution_y=1195;s.render.resolution_percentage=100;s.render.filepath=ROOT+'/previews/CLEAN_01_two_cabinets.png';bpy.ops.render.render(write_still=True)
for o in bpy.data.collections['CABINET_BLUE'].objects:o.hide_render=True
for o in bpy.data.collections['CABINET_RED'].objects:
 if any(q in o.name for q in ['Front_Glass','Header','Display_','Marquee','Reel_','StockLamp','Side_Glass','Mascot_']):o.hide_render=True
cam=s.camera;cam.location=(1.3,-3.4,3.35);cam.rotation_euler=(Vector((-.70,0,1.03))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.55;s.render.resolution_x=1100;s.render.resolution_y=1100;s.render.filepath=ROOT+'/previews/CLEAN_02_mechanism_cutaway.png';bpy.ops.render.render(write_still=True)
print('CLEAN_PREVIEWS_COMPLETE')
