import bpy,os,sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'arcade_machines.blend'))
s=bpy.context.scene;s.cycles.samples=12;s.cycles.use_denoising=True;s.render.resolution_x=900;s.render.resolution_y=900
ids=['gacha','capsule','ufo','race','race_course','kart']
for id in ids:bpy.data.collections[id].hide_viewport=False
for id,target,view,size in [('gacha',(0,-.35,.75),(2,-5,2),1.2),('ufo',(0,.11,1.97),(2,-5,.15),1.10),('race',(-.68,-.18,.75),(2,-5,2),1.6),('capsule',(0,0,.32),(3,-5,2),.92)]:
 if '--ufo-only' in sys.argv and id!='ufo':continue
 for name in ids:bpy.data.collections[name].hide_render=name!=id
 if id=='ufo':
  for o in bpy.data.collections[id].objects:
   if o.get('node') in ['glass','roof']:o.hide_render=True
 if id=='capsule':
  for o in bpy.data.collections[id].objects:
   if o.get('node')=='capsule_top':o.location.z+=.18;o.location.x+=.10
 cam=s.camera;v=Vector(target);cam.location=v+Vector(view);cam.rotation_euler=(v-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;s.render.filepath=os.path.join(ROOT,id+'_detail.png');bpy.ops.render.render(write_still=True)
