import bpy, sys, os, json, math
from mathutils import Vector
BASE='/workspace/scratch/f7102a0fad56/coin-pusher-assets'
sys.path.insert(0,BASE)
import prizes
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
a=prizes.build_prizes()
report={}
for key,obs in a.items():
    coll=bpy.data.collections.new(key);bpy.context.scene.collection.children.link(coll)
    for ob in obs:
        for old in list(ob.users_collection):old.objects.unlink(ob)
        coll.objects.link(ob)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in obs:ob.select_set(True)
    bpy.context.view_layer.objects.active=obs[0]
    path=os.path.join(BASE,'exports',key+'.glb')
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_extras=True,export_cameras=False,export_lights=False)
    bbox=[ob.matrix_world@v.co for ob in obs if ob.type=='MESH' for v in ob.data.vertices]
    report[key]={'triangles':sum(prizes._triangles(o) for o in obs),'objects':len(obs),'file_bytes':os.path.getsize(path),'dimensions_m':[round(max(v[i] for v in bbox)-min(v[i] for v in bbox),6) for i in range(3)],'reward_coins':obs[0].get('reward_coins'),'modifier_count':sum(len(o.modifiers) for o in obs)}
    print('EXPORTED',key,report[key])
for j,c in enumerate(['red','blue','green']):
    for i,g in enumerate('MOB'):a[f'letter_{g}_{c}'][0].location=(-.30+i*.12,.16-j*.16,0)
for key,pos in [('coin',(.10,-.19,0)),('dorayaki',(.29,-.16,0)),('coin_bag',(.10,.005,0)),('wood_chest',(.28,.005,0)),('gold_chest',(.20,.18,0))]:a[key][0].location=pos
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1.0
bpy.context.scene['library_readme']='Fourteen individual collectible assets. Each collection has one bottom-center ROOT. Move its ROOT as a unit. Both chest lids have a rear-edge LID_PIVOT; rotate local X from 0 to -105 degrees to open. GLBs are individually exported at the origin. Letters are 85 mm tall and worth 100 coins; dorayaki is worth 80. Coin radius 26 mm, complete thickness 5 mm, 148 triangles including MOB relief.'
bpy.ops.object.select_all(action='DESELECT')
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_location=(0,.015,.04)
            area.spaces.active.region_3d.view_distance=.92
            area.spaces.active.region_3d.view_rotation=(Vector((.27,-.80,.64))-Vector((0,.015,.035))).to_track_quat('Z','Y')
            area.spaces.active.region_3d.view_perspective='ORTHO'
            area.spaces.active.shading.color_type='MATERIAL'
            area.spaces.active.overlay.show_floor=False
bpy.context.scene.world.color=(.2,.2,.2)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BASE,'prize_library.blend'))
with open(os.path.join(BASE,'prizes_export_qa.json'),'w') as f:json.dump(report,f,indent=2)
