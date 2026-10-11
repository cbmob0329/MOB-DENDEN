import bpy,os,json,math
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));bpy.ops.wm.open_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend');scene=bpy.context.scene
cols=[bpy.data.collections['CABINET_RED'],bpy.data.collections['CABINET_BLUE']]
for col,suffix in zip(cols,['','_Coral']):
 panel=bpy.data.objects['ControlPanel'+suffix];panel.location.x=-.438;panel.scale.x=.215;panel.name='ControlPod_L'+suffix
 other=panel.copy();col.objects.link(other);other.location.x=.438;other.name='ControlPod_R'+suffix
 for side,x in [('L',-.438),('R',.438)]:
  for name in ['Button_'+side,'Button_'+side+'_Socket','Control_Label_'+side]:bpy.data.objects[name+suffix].location.x=x
 label=bpy.data.objects['Label_Select'+suffix];label.location=(0,-.463,.725);label.rotation_euler=(math.pi/2,0,0)
 bpy.data.objects['Win_CatchRamp'+suffix].rotation_euler.x=.55
# Independent static collision helpers for field: existing surfaces have real thickness.
# Assure moving collider remains attached after transform export.
def exp(fn,obs):
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.hide_set(False);o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.export_scene.gltf(filepath=ROOT+'/exports/'+fn+'.glb',export_format='GLB',use_selection=True,export_animations=True,export_extras=True)
 for o in obs:
  if o.name.startswith('COL_'):o.hide_set(True)
for col,fn in zip(cols,['cabinet_red','cabinet_blue']):
 root=next(o for o in col.objects if o.name.startswith('CabinetRoot'));pos=root.location.copy();root.location=(0,0,0);exp(fn,[o for o in col.objects if not o.name.startswith('DisplayCoin')]);root.location=pos
exp('two_cabinets',list(cols[0].objects)+list(cols[1].objects))
# Actual evaluated geometry budget after side-pod change.
def tri(o):
 if o.type!='MESH':return 0
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();n=len(me.loop_triangles);ev.to_mesh_clear();return n
manifest=json.load(open(ROOT+'/assets_manifest.json'));manifest['counts_triangles']={fn:sum(tri(o) for o in c.objects if not o.name.startswith(('COL_','DisplayCoin'))) for c,fn in zip(cols,['cabinet_red','cabinet_blue'])};manifest['physics']['front_clearance']='Two side control pods leave a 0.66m center opening; catch ramp slopes forward/downward.';json.dump(manifest,open(ROOT+'/assets_manifest.json','w'),ensure_ascii=False,indent=2)
scene.cycles.samples=112;scene.render.resolution_x=1500;scene.render.resolution_y=1400;bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend')
scene.render.filepath=ROOT+'/previews/FINAL_01_two_cabinets.png';bpy.ops.render.render(write_still=True)
for o in cols[1].objects:o.hide_render=True
for o in cols[0].objects:
 if any(s in o.name for s in ['Front_Glass','Header','Display_','Marquee','Reel_','StockLamp','Side_Glass','Mascot_']):o.hide_render=True
cam=scene.camera;cam.location=(1.3,-3.4,3.35);cam.rotation_euler=(Vector((-.70,0,1.03))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.55;scene.render.resolution_x=1250;scene.render.resolution_y=1250;scene.cycles.samples=80;scene.render.filepath=ROOT+'/previews/FINAL_02_mechanism_cutaway.png';bpy.ops.render.render(write_still=True)
for o in cols[0].objects:
 if not o.name.startswith('COL_'):o.hide_render=False
for name,loc,target,scale in [('03_front',(-.7,-5,1.4),(-.7,0,1.4),3.1),('04_side',(4,0,1.4),(-.7,0,1.4),3.1),('05_top',(-.7,-.04,5),(-.7,0,1),1.5)]:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.cycles.samples=40;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.filepath=ROOT+'/previews/FINAL_'+name+'.png';bpy.ops.render.render(write_still=True)
print('CLEARANCE_PATCH_COMPLETE',manifest['counts_triangles'])
