import bpy, sys, math
from mathutils import Vector
sys.path.insert(0,'/workspace/scratch/f7102a0fad56/coin-pusher-assets')
import prizes
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
a=prizes.build_prizes()
for j,c in enumerate(['red','blue','green']):
 for i,g in enumerate('MOB'): a[f'letter_{g}_{c}'][0].location=(-.30+i*.12,.16-j*.16,0)
for key,pos in [('coin',(.10,-.19,0)),('dorayaki',(.29,-.16,0)),('coin_bag',(.10,.005,0)),('wood_chest',(.28,.005,0)),('gold_chest',(.20,.18,0))]:a[key][0].location=pos
# A second copy of the gold chest is unnecessary: inspect its actual pivot separately.
for key in ('wood_chest','gold_chest'):
 pivot=next(o for o in a[key] if o.type=='EMPTY' and o.get('pivot_role'))
 if key=='gold_chest':pivot.rotation_euler.x=math.radians(-68)
 bpy.context.view_layer.update()
 print('PIVOT_QA',key,tuple(pivot.matrix_world.translation))
# Read and record all dimensions, triangle counts, modifiers, and source geometry.
bpy.context.view_layer.update()
for key,obs in a.items():
 co=[ob.matrix_world@v.co for ob in obs if ob.type=='MESH' for v in ob.data.vertices]
 print('QA',key,len(obs),obs[0]['triangle_count'],'bbox',tuple(round(max(p[i] for p in co)-min(p[i] for p in co),5) for i in range(3)), 'modifiers',sum(len(o.modifiers) for o in obs))
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));pl=bpy.context.object;pl.name='PREVIEW_FLOOR';pl.data.materials.append(prizes._mat('preview_background',(.65,.76,.83),0,.8))
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.62,.72,.86,1);world.node_tree.nodes['Background'].inputs[1].default_value=.4
for loc,power,size in [((-.4,-.4,.8),6,.5),((.5,-.15,.6),3,.35),((0,.5,.7),5,.4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);li=bpy.context.object;li.data.energy=power;li.data.shape='DISK';li.data.size=size;li.rotation_euler=(Vector((0,0,.04))-li.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(.27,-.80,.64));cam=bpy.context.object;cam.rotation_euler=(Vector((0,.015,.035))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.79;bpy.context.scene.camera=cam
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=32;sc.cycles.use_denoising=False;sc.render.resolution_x=1600;sc.render.resolution_y=1300;sc.render.resolution_percentage=100;sc.view_settings.view_transform='AgX';sc.render.image_settings.file_format='PNG';sc.render.filepath='/workspace/scratch/f7102a0fad56/coin-pusher-assets/prizes_preview.png'
bpy.ops.wm.save_as_mainfile(filepath='/workspace/scratch/f7102a0fad56/coin-pusher-assets/prizes_preview.blend');bpy.ops.render.render(write_still=True)
