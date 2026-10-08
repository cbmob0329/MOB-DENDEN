import bpy
from pathlib import Path
P=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(P/'MOB_CHILL_TOWN.blend'))
for o in list(bpy.data.objects):
 if o.type=='MESH':o.hide_render=not (o.parent and o.parent.name=='town_terrain_origin')
bpy.context.scene.camera=bpy.data.objects['station_front'];bpy.context.scene.camera.location=(0,-18.5,8.8);bpy.context.scene.render.filepath=str(P/'station_front.png');bpy.ops.render.render(write_still=True)
