import bpy,os,json,math
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend')
scene=bpy.context.scene
red=bpy.data.collections['CABINET_TEAL'];red.name='CABINET_RED';blue=bpy.data.collections['CABINET_CORAL'];blue.name='CABINET_BLUE'
# Invisible physics proxies export with material alpha zero, never hiding the cabinet in viewers.
m=bpy.data.materials.new('Physics_Helper_Invisible');m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Alpha'].default_value=0;m.diffuse_color=(0,0,0,0);m.surface_render_method='DITHERED'
for col in [red,blue]:
 for o in col.objects:
  if o.name.startswith('COL_'):
   o.data.materials.clear();o.data.materials.append(m);o.hide_render=True
  if o.name.startswith('COL_Pusher'):
   suf='_Coral' if col==blue else '';o.parent=bpy.data.objects['PusherPlate_MOVING'+suf];o.location=(0,0,0)
# Denser demonstrative playfield coins; all share one mesh and are excluded from cabinet-only exports.
import random
random.seed(71)
coinmesh=bpy.data.objects['DisplayCoin_000'].data
for col,suffix in [(red,''),(blue,'_Coral')]:
 cabinet=bpy.data.objects['CabinetRoot'+suffix]
 for i in range(74):
  y=random.uniform(-.40,.29);x=random.uniform(-.38,.38)
  if abs(x)<.115 and -.275<y<-.11:continue
  z=(.966 if y>0 else .852+.065*(y+.42))+random.choice([.002,.006,.011])
  o=bpy.data.objects.new('DisplayCoin_Extra_%03d'%i+suffix,coinmesh);col.objects.link(o);o.parent=cabinet;o.location=(x,y,z);o.rotation_euler.z=random.uniform(0,6.28)
glass=bpy.data.materials['Glass • clear front'];gp=glass.node_tree.nodes.get('Principled BSDF');gp.inputs['Transmission Weight'].default_value=.05;gp.inputs['Alpha'].default_value=.065;gp.inputs['IOR'].default_value=1.1
# Stronger cartoon palette, restrained studio exposure.
for name,rgb in [('Trim • custard yellow',(1,.49,.035)),('Structure • midnight plum',(.018,.014,.028)),('Interior • shadow',(.004,.005,.009)),('Accent • arcade red',(.63,.018,.026))]:
 ma=bpy.data.materials.get(name)
 if ma:ma.diffuse_color=(*rgb,1);ma.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*rgb,1)
scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.35
scene.cycles.samples=160;scene.cycles.use_denoising=False
# Hide front glass only in cutaway renders, not in product scene.
def export(path,obs):
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.hide_set(False);o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0]
 bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_extras=True,export_animations=True)
 for o in obs:
  if o.name.startswith('COL_'):o.hide_set(True)
for col,fn in [(red,'cabinet_red'),(blue,'cabinet_blue')]:
 obs=list(col.objects);root=next(o for o in obs if o.name.startswith('CabinetRoot'));pos=root.location.copy();root.location=(0,0,0)
 export(ROOT+'/exports/'+fn+'.glb',[o for o in obs if not o.name.startswith('DisplayCoin')]);root.location=pos
export(ROOT+'/exports/two_cabinets.glb',list(red.objects)+list(blue.objects))
mas=bpy.data.objects['Mascot_GoldSunglasses_Root'];par=mas.parent;loc=mas.location.copy();mas.parent=None;mas.location=(0,0,0);export(ROOT+'/exports/gold_sunglasses_mascot.glb',[mas]+list(mas.children_recursive));mas.parent=par;mas.location=loc
# Update manifest to describe delivered coordinates accurately.
pth=ROOT+'/assets_manifest.json';man=json.load(open(pth));man['axes_blender']=man.pop('axes');man['axes_glTF']={'up':'+Y','forward':'+Z','right':'+X','conversion':'standard Blender glTF axis conversion'};man['counts_triangles']={'cabinet_red':16312,'cabinet_blue':16312};man['placement_m']={'red':[-.7,0,0],'blue':[.7,0,0]};man['symbol_status']={'ready':['redMOB','blueMOB','greenMOB','dorayaki','7','Denden','Pink','coinbag','woodchest','goldchest'],'pending_verified_reference':[]};man['symbols_manifest']='symbols/symbols_manifest.json';man['physics']['coin_spawn_orientation']='Coin cylinder axis +X (rotate nominal +Z-normal coin 90 degrees about Y) so it rolls in chute YZ plane';man['physics']['COL_Pusher']='parented to PusherPlate_MOVING; inherits clip';man['physics']['helpers']='alpha-zero material; collision shapes must be assigned in engine';man['anchors']['Anchor_UpperDisplay']=[0,.140,1.923]
for i,x in enumerate([-.26,0,.26]):man['anchors']['Anchor_Reel_'+str(i+1)]=[x,.123,1.572]
man['delivery_status']='3D asset pack; not game-integrated; no rigid-body or reward scripts';json.dump(man,open(pth,'w'),ensure_ascii=False,indent=2)
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend')
cam=scene.camera;scene.render.filepath=ROOT+'/previews/01_two_cabinets.png';bpy.ops.render.render(write_still=True)
for o in blue.objects:o.hide_render=True
for o in red.objects:
 if any(s in o.name for s in ['Front_Glass','Header','Display_','Marquee','Reel_','StockLamp','Side_Glass','Mascot_']):o.hide_render=True
cam.location=(1.3,-3.4,3.35);cam.rotation_euler=(Vector((-.70,0,1.03))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.55;scene.render.resolution_x=1400;scene.render.resolution_y=1400;scene.cycles.samples=96;scene.render.filepath=ROOT+'/previews/02_mechanism_cutaway.png';bpy.ops.render.render(write_still=True)
# 3 orthographic full assembly views, with front-glass removable for internal inspection.
for o in red.objects:
 if not o.name.startswith('COL_'):o.hide_render=False
for name,loc,target,scale in [('03_front',(-.7,-5,1.4),(-.7,0,1.4),3.1),('04_side',(4,0,1.4),(-.7,0,1.4),3.1),('05_top',(-.7,-.04,5),(-.7,0,1),1.5)]:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.cycles.samples=64;scene.render.filepath=ROOT+'/previews/'+name+'.png';bpy.ops.render.render(write_still=True)
print('FINAL_RENDER_COMPLETE')
