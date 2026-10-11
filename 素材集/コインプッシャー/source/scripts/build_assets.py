import bpy, math, json, os, sys, random
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,ROOT)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
 if c.name!='Collection': bpy.data.collections.remove(c)
BASE=bpy.data.collections.get('Collection'); BASE.name='CABINET_TEAL'
COL=BASE

def move(o):
 for c in list(o.users_collection): c.objects.unlink(o)
 COL.objects.link(o);return o

def mat(n,c,metal=0,rough=.45,emission=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emission:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emission
 return m
cream=mat('Shell • warm porcelain',(.93,.80,.57)); teal=mat('Accent • arcade red',(.65,.035,.045)); coral=mat('Accent • watermelon coral',(.10,.37,.51)); dark=mat('Structure • midnight plum',(.075,.067,.135)); gold=mat('Trim • custard yellow',(1,.62,.10),.25); white=mat('Lettering • ivory',(1,.96,.80)); field=mat('Playfield • deep jade',(.035,.21,.20));steel=mat('Mechanism • blue steel',(.31,.51,.54),.35); black=mat('Interior • shadow',(.024,.025,.049)); lamp=mat('Lamp • butter glow',(1,.78,.17),emission=1.4);red=mat('Input • red',(.97,.23,.21));blue=mat('Input • blue',(.10,.49,.9))
glass=mat('Glass • clear front',(.70,.95,1),rough=.08);p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.96;p.inputs['IOR'].default_value=1.45;p.inputs['Alpha'].default_value=.18;glass.surface_render_method='DITHERED'

def cube(n,loc,dim,ma,bev=.025):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=move(bpy.context.object);o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if ma:o.data.materials.append(ma)
 if bev:
  b=o.modifiers.new('Soft rounded edges','BEVEL');b.width=bev;b.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
  o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 return o

def cyl(n,loc,r,depth,ma,verts=20,rot=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=depth,location=loc);o=move(bpy.context.object);o.name=n
 if rot:o.rotation_euler=rot
 if ma:o.data.materials.append(ma)
 bevel=o.modifiers.new('Rim bevel','BEVEL');bevel.width=min(.008,depth*.18);bevel.segments=1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=bevel.name);o.modifiers.new('Normals','WEIGHTED_NORMAL');return o

def txt(n,s,loc,size,ma,rot=(math.pi/2,0,0),extr=.0015):
 bpy.ops.object.text_add(location=loc,rotation=rot);o=move(bpy.context.object);o.name=n;o.data.body=s;o.data.align_x='CENTER';o.data.align_y='CENTER';o.data.size=size;o.data.extrude=extr;o.data.bevel_depth=.0007;o.data.bevel_resolution=0;o.data.resolution_u=3;o.data.materials.append(ma);bpy.ops.object.convert(target='MESH');return o

def empty(n,loc,typ='PLAIN_AXES'):
 o=bpy.data.objects.new(n,None);COL.objects.link(o);o.location=loc;o.empty_display_type=typ;o.empty_display_size=.06;return o

def mesh(n,v,f,ma):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);COL.objects.link(o);o.data.materials.append(ma);return o

def slopepatch(n,x1,x2,y1,y2):
 z=lambda y:.845+.065*(y+.42)
 v=[(x1,y1,z(y1)),(x2,y1,z(y1)),(x2,y2,z(y2)),(x1,y2,z(y2))];o=mesh(n,v,[(0,1,2,3)],field);s=o.modifiers.new('Physical thickness','SOLIDIFY');s.thickness=.012;bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.modifier_apply(modifier=s.name);o.select_set(False);return o

# Cabinet cabinet origin at floor; forward is negative Y.
root=empty('CabinetRoot',(0,0,0));root['asset']='MOB_CHILL_LIFE_COIN_PUSHER';root['forward']='-Y'
cube('Base_Plinth',(0,0,.085),(1.08,.98,.17),dark,.055)
for x in [-.39,.39]:
 for y in [-.32,.32]:cyl('Foot', (x,y,.035),.055,.07,dark)
cube('Base_LowerBody',(0,.03,.40),(1.00,.88,.66),teal,.065)
cube('Front_CreamFascia',(0,-.431,.48),(.88,.045,.53),cream,.04)
cube('Front_Payout_Recess',(0,-.46,.46),(.64,.045,.20),dark,.045)
cube('Payout_Bowl_Base',(0,-.53,.365),(.68,.23,.045),gold,.018)
cube('Payout_Bowl_Lip',(0,-.636,.407),(.68,.035,.10),cream,.018)
for x in [-.327,.327]:cube('Payout_Bowl_Side',(x,-.53,.408),(.03,.22,.09),cream,.012)
txt('Label_Payout','WIN!',(0,-.463,.63),.072,teal)
cube('Bay_Floor',(0,0,.76),(.98,.89,.10),cream,.025)
cube('Back_Shell',(0,.41,1.20),(1.01,.075,.91),teal,.04)
cube('Back_InnerPanel',(0,.363,1.17),(.87,.025,.68),dark,.018)
for x in [-.478,.478]:
 cube('Side_Pillar_Front',(x,-.40,1.19),(.09,.10,.84),cream,.027)
 cube('Side_Pillar_Rear',(x,.37,1.23),(.085,.085,.90),cream,.025)
 cube('Side_Lower_Rail',(x,-.005,.84),(.075,.82,.10),teal,.025)
 cube('Side_Upper_Rail',(x,-.005,1.59),(.075,.82,.10),teal,.025)
 cube('Side_Glass',(x,.015,1.235),(.008,.68,.62),glass,.002)
# Real fixed lower field with a rectangular opening around x +/- .085 y[-.24,-.14].
for name,a,b,c,d in [('Left',-.423,-.085,-.42,.19),('Right',.085,.423,-.42,.19),('Front',-.085,.085,-.42,-.24),('Rear',-.085,.085,-.14,.19)]:slopepatch('FixedField_'+name,a,b,c,d)
# Four elevated guide rails outline the real opening; no surface spans it.
for x in [-.094,.094]:cube('Slot_SideRim',(x,-.19,.864),(.015,.12,.012),gold,.004)
for y in [-.247,-.133]:cube('Slot_EndRim',(0,y,.864),(.202,.014,.012),gold,.004)
cube('Slot_Tunnel_Left',(-.086,-.19,.80),(.012,.102,.11),dark,.002);cube('Slot_Tunnel_Right',(.086,-.19,.80),(.012,.102,.11),dark,.002)
for y in [-.243,-.137]:cube('Slot_Tunnel_End',(0,y,.80),(.175,.012,.11),dark,.002)
txt('Label_Slot','SLOT',(0,-.300,.855),.052,gold,rot=(0,0,0),extr=.0004)
# Reciprocating upper shelf covers the rear part of fixed shelf.
pusher=cube('PusherPlate_MOVING',(0,.17,.935),(.80,.34,.055),steel,.010)
pusher['travel_m']=.115;pusher['axis']='Y';pusher['motion']='front negative Y';
for fr,y in [(1,.17),(41,.055),(81,.17)]:pusher.location.y=y;pusher.keyframe_insert(data_path='location',frame=fr)
if pusher.animation_data:
 pusher.animation_data.action.name='Pusher_Reciprocate_2s'
 for fc in pusher.animation_data.action.fcurves:
  for k in fc.keyframe_points:k.interpolation='LINEAR'
cube('Pusher_BackGuard',(0,.343,.97),(.82,.025,.12),steel,.01)
for x in [-.435,.435]:cube('Field_SideFence',(x,-.08,.928),(.022,.64,.13),steel,.008)
cube('Front_WinEdge',(0,-.43,.833),(.855,.028,.022),gold,.006)
# The win edge drops into a physical catch ramp leading to collection bowl.
catch=cube('Win_CatchRamp',(0,-.451,.742),(.79,.18,.015),dark,.006);catch.rotation_euler.x=-.55
# Twin input ramps. Coins enter above upper shelf and fall from chute exits.
for tag,x,ma in [('L',-.255,red),('R',.255,blue)]:
 ramp=cube('Chute_'+tag+'_Floor',(x,.251,1.14),(.075,.23,.018),gold,.006);ramp.rotation_euler.x=math.radians(61)
 for sx in [-.041,.041]:
  rail=cube('Chute_'+tag+'_Rail',(x+sx,.25,1.151),(.014,.24,.05),cream,.006);rail.rotation_euler.x=math.radians(61)
 cyl('Input_'+tag+'_Bezel',(x,.352,1.29),.060,.021,ma,rot=(math.pi/2,0,0))
 cube('Input_'+tag+'_Slot',(x,.336,1.29),(.039,.006,.009),black,.003)
 empty('Anchor_Input_'+tag,(x,.31,1.28));empty('Anchor_ChuteExit_'+tag,(x,.15,1.041))
 txt('Label_Input_'+tag,tag,(x,.324,1.375),.05,white)
# Clear front is a real thin pane and separate for renderer material tuning.
cube('Front_Glass',(0,-.435,1.24),(.84,.008,.61),glass,.002)
cube('ControlPanel',(0,-.492,.94),(.97,.22,.085),teal,.025)
for tag,x,ma in [('L',-.28,red),('R',.28,blue)]:
 cyl('Button_'+tag+'_Socket',(x,-.51,.986),.058,.012,dark)
 cyl('Button_'+tag,(x,-.51,1.000),.044,.02,ma)
 txt('Control_Label_'+tag,tag,(x,-.585,.988),.037,white,rot=(0,0,0))
txt('Label_Select','SELECT',(0,-.50,.988),.032,white,rot=(0,0,0))
# Oversized rounded head, separated marquee and three inset physical reels.
cube('Header_Shell',(0,0,1.81),(1.12,.92,.44),teal,.065)
cube('Header_Face',(0,-.473,1.82),(1.00,.035,.35),cream,.038)
cube('Marquee_Inset',(0,-.498,1.932),(.88,.018,.10),dark,.020)
txt('Marquee_Title','MOB CHILL LIFE',(0,-.512,1.933),.064,white)
for i,x in enumerate([-.27,0,.27]):
 cube('Reel_'+str(i+1)+'_Surround',(x,-.501,1.786),(.247,.045,.162),gold,.02)
 cube('Reel_'+str(i+1)+'_Screen',(x,-.527,1.789),(.211,.012,.129),white,.012)
 txt('Reel_'+str(i+1)+'_Demo7','7',(x,-.539,1.793),.112,[red,teal,blue][i])
 empty('Anchor_Reel_'+str(i+1),(x,-.538,1.789))
for i,x in enumerate([-.16,-.08,0,.08,.16]):cyl('StockLamp_'+str(i+1),(x,-.502,1.67),.022,.012,lamp,16,rot=(math.pi/2,0,0))
cube('Top_CreamCap',(0,0,2.055),(1.04,.83,.07),cream,.034)
# Small playful side stripes.
for x in [-.506,.506]:
 for z,w in [(.36,.42),(.44,.30),(.52,.18)]:cube('Side_Stripe',(x,.03,z),(.012,w,.027),gold,.009)
# Physics helpers intentionally separate from render mesh.
for name,loc,dim in [('CabinetBounds',(0,0,1.4),(1.13,1.10,2.8)),('Pusher',(0,.17,.935),(.80,.34,.055)),('FrontWinTrigger',(0,-.455,.79),(.83,.10,.09)),('SlotTrigger',(0,-.19,.79),(.16,.09,.04))]:
 o=cube('COL_'+name,loc,dim,None,0);o.hide_render=True;o.display_type='WIRE';o['physics_role']='trigger' if 'Trigger' in name else 'solid';o['export_helper']=True
for name,loc in [('WinCollection',(0,-.54,.44)),('FrontFall',(0,-.46,.80)),('SlotCoinAndSpin',(0,-.19,.80)),('PrizeSpawn',(0,.05,1.08)),('LidService',(0,.4,1.7))]:empty('Anchor_'+name,loc)
# Reference-guide silhouette: tall rear head, open sloped bay, golden sunglasses mascot.
# Rebuild the head so its black display sits above the three reels rather than projecting over the playfield.
for o in list(BASE.objects):
 if any(o.name.startswith(n) for n in ['Header','Marquee','Reel_','StockLamp','Top_CreamCap','Side_Upper_Rail','Side_Glass','Front_Glass']):bpy.data.objects.remove(o,do_unlink=True)
for o in BASE.objects:
 if o.name.startswith('Side_Pillar_Front'):o.location.z=.94;o.scale.z=.31
 if o.name.startswith('Side_Pillar_Rear'):o.location.z=1.15;o.scale.z=.78
cube('Header_Shell',(0,.34,1.75),(1.04,.22,1.00),teal,.045)
cube('Header_GoldOutline',(0,.215,1.82),(.97,.034,.79),gold,.02)
cube('Header_RedInset',(0,.190,1.82),(.92,.024,.74),teal,.012)
cube('Display_Frame',(0,.170,1.923),(.79,.025,.415),gold,.015)
cube('Display_BlankBlack',(0,.151,1.923),(.735,.014,.365),black,.008)
empty('Anchor_UpperDisplay',(0,.140,1.923))
for i,x in enumerate([-.26,0,.26]):
 cube('Reel_'+str(i+1)+'_Surround',(x,.162,1.572),(.25,.045,.168),gold,.013)
 cube('Reel_'+str(i+1)+'_Screen',(x,.135,1.572),(.218,.012,.132),white,.008)
 txt('Reel_'+str(i+1)+'_Demo7','7',(x,.123,1.572),.11,[red,teal,blue][i])
for i,x in enumerate([-.16,-.08,0,.08,.16]):cyl('StockLamp_'+str(i+1),(x,.150,1.428),.023,.012,lamp,16,rot=(math.pi/2,0,0))
cube('Header_TopTrim',(0,.34,2.261),(1.09,.27,.060),gold,.015)
for x in [-.454,.454]:
 for z in [1.65,1.83,2.01]:
  cube('Display_SideLampHousing',(x,.179,z),(.073,.033,.14),gold,.014)
  cube('Display_SideLampGlow',(x,.157,z),(.042,.018,.093),lamp,.018)
# Sloping side panels and glass rails frame the playfield.
for x in [-.473,.473]:
 v=[(x,-.42,.84),(x,.35,.84),(x,.35,1.40),(x,-.42,1.025)]
 ob=mesh('Side_Glass_Sloped',v,[(0,1,2,3)],glass);sol=ob.modifiers.new('Pane thickness','SOLIDIFY');sol.thickness=.007
 rail=cube('Side_Upper_Rail',(x,-.035,1.225),(.065,.85,.055),gold,.016);rail.rotation_euler.x=math.atan2(.375,.77)
# Clear lid follows same ramp; modeled but removable for mobile visibility.
g=cube('Front_Glass',(0,-.035,1.225),(.87,.85,.004),glass,.001);g.rotation_euler.x=math.atan2(.375,.77)
# Body side profile avoids a square glass box appearance.
for x in [-.498,.498]:
 v=[(x,-.43,.18),(x,.44,.18),(x,.44,1.45),(x,.28,1.45),(x,-.43,.89)]
 ob=mesh('Side_ProfilePanel',v,[(0,1,2,3,4)],teal);sol=ob.modifiers.new('Shell thickness','SOLIDIFY');sol.thickness=.025
for o in BASE.objects:
 if o.name.startswith('Anchor_Reel_'):o.location.y=.123;o.location.z=1.572
# Separate collectible-style mascot, shared meshes with simple round glasses.
def sphere(n,loc,scale,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=10,location=loc);o=move(bpy.context.object);o.name=n;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma)
 for p in o.data.polygons:p.use_smooth=True
 return o
masroot=empty('Mascot_GoldSunglasses_Root',(0,.32,2.30))
mas=[]
mas.append(sphere('Mascot_BlobBody',(0,.32,2.44),(.24,.18,.21),gold))
for x,y,z,sc in [(-.24,.29,2.34,(.12,.12,.08)),(.24,.29,2.34,(.12,.12,.08)),(-.14,.15,2.32,(.12,.10,.065)),(.14,.15,2.32,(.12,.10,.065))]:mas.append(sphere('Mascot_BlobFoot',(x,y,z),sc,gold))
for x in [-.095,.095]:
 mas.append(cyl('Mascot_GlassesGoldRim',(x,.143,2.455),.082,.018,gold,24,rot=(math.pi/2,0,0)))
 mas.append(cyl('Mascot_GlassesBlackLens',(x,.127,2.455),.068,.014,dark,24,rot=(math.pi/2,0,0)))
 mas.append(sphere('Mascot_LensHighlight',(x-.025,.114,2.481),(.014,.003,.022),white))
mas.append(cube('Mascot_GlassesBridge',(0,.122,2.46),(.035,.015,.013),dark,.004))
mas.append(cyl('Mascot_TopCoin',(0,.30,2.715),.085,.018,gold,24,rot=(math.pi/2-.22,0,.15)))
mas.append(txt('Mascot_Coin_M','M',(0,.28,2.715),.082,cream))
for o in mas:o.parent=masroot;o.location-=masroot.location
# Attach all geometry without changing transforms.
for o in list(COL.objects):
 if o!=root and o.parent is None:o.parent=root
bpy.context.scene.frame_set(1)
# Hide helper bounding meshes in viewport by default, retain them in exports.
for o in COL.objects:
 if o.name.startswith('COL_'):o.hide_set(True)
# Awaited externally verified symbol artwork is represented by material anchors only.
for name in ['Denden','Pink']:
 m=mat('SYMBOL_PENDING_'+name,(.3,.3,.3));m['status']='requires_verified_reference';m['texture_anchor']=name
# Export helper.
def export(path,objs):
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.hide_set(False);o.select_set(True)
 bpy.context.view_layer.objects.active=next((o for o in objs if o.type=='MESH'),objs[0])
 bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_animations=True,export_extras=True)
 for o in objs:
  if o.name.startswith('COL_'):o.hide_set(True)
base_objs=list(BASE.objects)
export(ROOT+'/exports/cabinet_red.glb',base_objs)
# Second cabinet linked mesh geometry, material overrides only.
COR=bpy.data.collections.new('CABINET_CORAL');bpy.context.scene.collection.children.link(COR)
mapdup={}
for o in base_objs:
 n=o.copy();COR.objects.link(n);n.name=o.name+'_Coral';mapdup[o]=n
 if n.type=='MESH':
  for slot in n.material_slots:
   if slot.material==teal:slot.link='OBJECT';slot.material=coral
for o,n in mapdup.items():n.parent=mapdup.get(o.parent)
corroot=mapdup[root]
export(ROOT+'/exports/cabinet_blue.glb',list(COR.objects))
# Prize library and arranged display coins injected from independently authored module.
PR=bpy.data.collections.new('PRIZE_LIBRARY');bpy.context.scene.collection.children.link(PR)
prize_assets={}
try:
 import prizes
 prize_assets=prizes.build_prizes()
 for asset,obs in prize_assets.items():
  export(ROOT+'/exports/'+asset+'.glb',obs)
  for o in obs:
   for c in list(o.users_collection):c.objects.unlink(o)
   PR.objects.link(o);o.hide_render=True;o.hide_set(True)
except ImportError:print('PRIZES_PENDING')
# Coins on field use a compact shared mesh.
random.seed(12)
COL=BASE
if 'coin' in prize_assets:
 coinmesh=next(o.data for o in prize_assets['coin'] if o.type=='MESH')
else:
 co=cyl('CoinTemplate',(0,0,-1),.026,.005,gold,24);coinmesh=co.data;co.hide_render=True
for i in range(65):
 y=random.uniform(-.40,.29);x=random.uniform(-.38,.38)
 if abs(x)<.115 and -.275<y<-.11:continue
 z=(.966 if y>.0 else .852+.065*(y+.42)) +random.choice([0,.004,.008])
 o=bpy.data.objects.new('DisplayCoin_%03d'%i,coinmesh);BASE.objects.link(o);o.location=(x,y,z);o.rotation_euler.z=random.uniform(0,6.28);o.parent=root
for o in list(BASE.objects):
 if o.name.startswith('DisplayCoin'):
  n=o.copy();COR.objects.link(n);n.parent=corroot;n.name=o.name+'_Coral'
root.location.x=-.70;corroot.location.x=.70
# Studio scene.
ST=bpy.data.collections.new('PREVIEW_STUDIO');bpy.context.scene.collection.children.link(ST);COL=ST
floor=mat('Studio • pale mint',(.60,.76,.73));cube('Studio_Ground',(0,0,-.065),(200,200,.10),floor,0)
world=bpy.context.scene.world or bpy.data.worlds.new('World');bpy.context.scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.68,.80,.83,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35
for name,loc,power,size in [('Key',(-3,-4,7),900,5),('Fill',(4,-1,4),650,4),('Rim',(0,4,5),1000,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=move(bpy.context.object);o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(3.7,-6.4,3.9));cam=move(bpy.context.object);cam.name='Presentation_Camera';cam.rotation_euler=(Vector((0,-.03,1.30))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=4.2
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False;scene.render.resolution_x=1600;scene.render.resolution_y=1400;scene.render.resolution_percentage=100;scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False;scene.frame_end=81;scene.render.fps=40
# Combined exports preserve two scene instances with independent animation.
export(ROOT+'/exports/two_cabinets.glb',list(BASE.objects)+list(COR.objects))
# Counts use evaluated triangle meshes.
def tris(o):
 if o.type!='MESH':return 0
 me=o.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh();me.calc_loop_triangles();n=len(me.loop_triangles);o.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh_clear();return n
counts={c.name:sum(tris(o) for o in c.objects if not o.name.startswith(('COL_','DisplayCoin'))) for c in [BASE,COR]}
manifest={'asset':'MOB CHILL LIFE • cartoon coin pusher','version':'1.0','units':'meters','axes':{'up':'+Z','forward':'-Y','right':'+X'},'cabinet_dimensions_m':[1.12,1.12,2.80],'cabinet_origin':'floor center','placement_m':{'teal':[-.70,0,0],'coral':[.70,0,0]},'animation':{'clip':'Pusher_Reciprocate_2s','duration_seconds':2,'frame_range':[1,81],'fps':40,'travel_m':.115,'axis':'-Y then +Y'},'counts_triangles':counts,'prizes':{a:{'triangles':sum(tris(o) for o in obs),'file':'exports/'+a+'.glb'} for a,obs in prize_assets.items()},'anchors':{o.name:list(o.location) for o in base_objs if o.type=='EMPTY'},'physics':{'coin_mass_kg':.007,'letters_mass_kg':.018,'dorayaki_mass_kg':.020,'pusher':'kinematic; sync collision transform with animated visual','fixed_field':'static triangle mesh; preserve aperture','glass':'static box; separate visual transparent material','COL_CabinetBounds':'broadphase / placement only; DO NOT use as solid interior collision','COL_SlotTrigger':'award one coin and one spin once per entering coin','COL_FrontWinTrigger':'collection sensor; reward letters100/dorayaki80','chute':'static floor and side rail meshes; spawn coin vertical near Anchor_Input_L/R'},'symbol_status':{'ready':['redMOB','blueMOB','greenMOB','dorayaki','7','coinbag','woodchest','goldchest'],'pending_verified_reference':['Denden','Pink']},'notes':['Prototype geometry; runtime physics and reward logic not implemented.','Front Glass uses transmission and alpha; tune renderer for engine.','Two cabinets use shared mesh data in Blender, separate transforms.']}
with open(ROOT+'/assets_manifest.json','w') as f:json.dump(manifest,f,indent=2,ensure_ascii=False)
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend')
scene.render.filepath=ROOT+'/previews/01_two_cabinets.png';bpy.ops.render.render(write_still=True)
# Mechanics cutaway: left instance only, front glass and head removed for view.
for o in COR.objects:o.hide_render=True
for o in BASE.objects:
 if any(s in o.name for s in ['Front_Glass','Header','Marquee','Reel_','StockLamp','Top_Cream','Side_Glass']):o.hide_render=True
cam.location=(1.3,-3.4,3.35);cam.rotation_euler=(Vector((-.70,0,1.03))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.6;scene.render.resolution_x=1400;scene.render.resolution_y=1400;scene.render.filepath=ROOT+'/previews/02_mechanism_cutaway.png';bpy.ops.render.render(write_still=True)
for name,loc,scale in [('03_front',(-.70,-4,1.5),2.5),('04_side',(3,-.05,1.8),2.5),('05_top',(-.70,-.10,5),1.6)]:
 cam.location=loc;cam.rotation_euler=(Vector((-.70,0,1.05))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=ROOT+'/previews/'+name+'.png';bpy.ops.render.render(write_still=True)
print('FINISHED_ASSET_BUILD',counts)
