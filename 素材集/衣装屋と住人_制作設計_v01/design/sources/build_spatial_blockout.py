import bpy, math, json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).resolve().parents[1]
m=json.loads((OUT/'design_dimensions.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for datablocks in [bpy.data.materials,bpy.data.cameras,bpy.data.lights]:
 for d in list(datablocks):datablocks.remove(d)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=96;scene.cycles.use_denoising=False
scene.render.resolution_x=1440;scene.render.resolution_y=1280;scene.render.resolution_percentage=100
scene.world.color=(.75,.75,.75)
scene.view_settings.view_transform='AgX'
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.85,.82,.76,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.8
mats={}
for n,col in {'cream':(.88,.80,.64,1),'white':(.95,.93,.87,1),'red':(.52,.035,.075,1),'rose':(.80,.31,.37,1),'gold':(.75,.48,.11,1),'floor':(.57,.40,.23,1),'ink':(.10,.09,.08,1),'blue':(.12,.38,.52,1),'glass':(.43,.65,.68,1)}.items():
 a=bpy.data.materials.new(n);a.diffuse_color=col;a.use_nodes=True;a.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=col;a.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.65;mats[n]=a
colls={}
for n in ['F1','F2','STAIR','GUIDE','SETUP']:
 c=bpy.data.collections.new(n);scene.collection.children.link(c);colls[n]=c
current='F1'
def put(o,name,mat):
 o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 colls[current].objects.link(o);o.data.materials.append(mats[mat]);return o
def box(name,bs,mat='cream',bevel=.025):
 x0,y0,z0,x1,y1,z1=bs;bpy.ops.mesh.primitive_cube_add(size=1,location=((x0+x1)/2,(y0+y1)/2,(z0+z1)/2));o=put(bpy.context.object,name,mat);o.dimensions=(x1-x0,y1-y0,z1-z0);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('soft_edges','BEVEL');mod.width=bevel;mod.segments=3;o.modifiers.new('weighted_normals','WEIGHTED_NORMAL')
 return o
def rod(name,a,b,r=.035,mat='gold'):
 a,b=Vector(a),Vector(b);v=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=v.length,location=(a+b)/2);o=put(bpy.context.object,name,mat);o.rotation_euler=v.to_track_quat('Z','Y').to_euler();return o
def text(name,body,loc,size=.21,rot=(math.pi/2,0,0),mat='ink'):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.extrude=.001;o=bpy.data.objects.new(name,cu);colls[current].objects.link(o);o.location=loc;o.rotation_euler=rot;cu.materials.append(mats[mat]);return o
# Actual floor slabs.
current='F1';box('Floor_01',(0,0,-.20,8,7,0),'floor',.025)
box('Wall_01_Back',(0,6.8,0,8,7,2.4),'white');box('Wall_01_Left',(0,0,0,.2,6.8,2.4),'white')
# Low cutaway edges preserve footprint and doorway.
for x0,x1 in [(.2,3.2),(4.8,7.8)]:box('Front_01_Cutaway',(x0,0,0,x1,.2,.20),'cream')
box('Right_01_Cutaway',(7.8,.2,0,8,6.8,.2),'cream')
current='F2'
for name,bs in [('front',(0,0,2.4,8,3.6,2.6)),('left',(0,3.6,2.4,5.2,7,2.6)),('back',(5.2,6.8,2.4,8,7,2.6)),('right',(7.8,3.6,2.4,8,6.8,2.6))]:box('Floor_02_'+name,bs,'floor',.015)
box('Wall_02_Back',(0,6.8,2.6,8,7,5.0),'white');box('Wall_02_Left',(0,0,2.6,.2,6.8,5.0),'white')
box('Front_02_Cutaway',(.2,0,2.6,7.8,.2,2.8),'cream');box('Right_02_Cutaway',(7.8,.2,2.6,8,6.8,2.8),'cream')
# Furniture blocks: exact footprint and top height. Decorative features stay inside those bounds.
for f in m['furniture']:
 current='F'+str(f['floor']);z=0 if f['floor']==1 else 2.6;n=f['id'];x0,y0,x1,y1=f['bounds_xy'];h=f['height'];name=f'{current}_{n:02d}'
 if n in [1,2]:
  for y in [y0+.08,y1-.08]:rod(name+'_rack_post',( (x0+x1)/2,y,z+.05),((x0+x1)/2,y,z+h),.035)
  rod(name+'_rack_bar',((x0+x1)/2,y0+.06,z+h),((x0+x1)/2,y1-.06,z+h),.04)
  for i in range(5):
   y=y0+.22+i*((y1-y0)-.44)/4;box(name+f'_garment_{i}',(x0+.07,y-.065,z+.42,x1-.07,y+.065,z+1.10),'red' if i%2==0 else 'white',.035)
 elif n==6:
  box(name+'_mirror',(x0,y0,z,x1,y1,z+h),'cream');box(name+'_glass',(x0+.07,y1-.015,z+.12,x1-.07,y1+.001,z+h-.08),'glass',.01)
 elif n==8:
  box(name+'_bed_base',(x0,y0,z,x1,y1,z+h-.08),'cream');box(name+'_mattress',(x0+.03,y0+.03,z+h-.08,x1-.03,y1-.03,z+h),'red',.05)
  box(name+'_pillow',(x0+.16,y1-.51,z+h,x1-.16,y1-.10,z+h+.11),'white',.075)
 elif n==10:
  box(name+'_seat',(x0,y0,z,x1,y1,z+h),'rose',.07);box(name+'_back',(x0,y1-.16,z+h,x1,y1,z+.9),'red',.07)
 else:
  box(name,(x0,y0,z,x1,y1,z+h if n in [4,9] else z+h-.05),'cream' if n in [4,9] else 'red',.025)
  if n not in [4,9]:box(name+'_top',(x0,y0,z+h-.05,x1,y1,z+h),'cream',.025)
  if n in [4,9]:
   for lev in [.4,.85,1.25]:
    if lev<h:box(name+'_shelf',(x0+.05,y0-.01,z+lev,x1-.05,y0+.06,z+lev+.04),'gold',.01)
 # ID on horizontal footprint cap with white letter for legibility
 text(name+'_label',str(n),((x0+x1)/2,(y0+y1)/2,z+h+.025),.24,(0,0,0),'ink')
# Correct stair geometry, lower west flight + half landing + upper east return flight.
current='STAIR'
for i in range(7):
 y=3.6+.3*i;h=(i+1)*.1625;box(f'Lower_tread_{i+1}',(5.2,y,0,6.4,y+.3,h),'cream',.01);box(f'Lower_red_{i+1}',(5.4,y+.01,h+.001,6.2,y+.29,h+.012),'red',.003)
box('Half_landing',(5.2,5.7,1.12,7.8,6.8,1.30),'cream',.02);box('Half_red',(5.40,5.75,1.301,7.6,6.6,1.312),'red',.003)
for i in range(7):
 y=5.4-.3*i;h=1.3+(i+1)*.1625;box(f'Upper_tread_{i+1}',(6.6,y,h-.18,7.8,y+.3,h),'cream',.01);box(f'Upper_red_{i+1}',(6.8,y+.01,h+.001,7.6,y+.29,h+.012),'red',.003)
box('Arrival_platform',(6.6,3.25,2.40,7.8,3.6,2.60),'cream',.015)
for x in [5.2,6.4]:
 rod('Lower_rail',(x,3.62,.75),(x,5.7,2.05),.045,'red')
 for i in range(8):
  y=3.6+i*.3;h=min(1.3,(i+1)*.1625);rod('Lower_baluster',(x,y,h),(x,y,h+.67),.026,'cream')
for x in [6.6,7.8]:
 rod('Upper_rail',(x,3.6,3.35),(x,5.7,2.05),.045,'red')
 for i in range(8):
  y=3.6+i*.3;h=2.6-i*.1625;rod('Upper_baluster',(x,y,h),(x,y,h+.67),.026,'cream')
# second-floor guard rails, leave east flight arrival unobstructed
current='F2'
for a,b in [((5.2,3.6,3.35),(5.2,6.8,3.35)),((5.2,3.6,3.35),(6.6,3.6,3.35))]:rod('Opening_guard',a,b,.045,'red')
for y in [3.6+i*.4 for i in range(9)]:rod('Opening_baluster',(5.2,y,2.6),(5.2,y,3.35),.025,'cream')
for x in [5.2+i*.35 for i in range(5)]:rod('Opening_front_baluster',(x,3.6,2.6),(x,3.6,3.35),.025,'cream')
# Floor1 clear-area scale marker, a neutral measuring pole, not a character substitute.
current='GUIDE';rod('Resident_height_1p4',(4.6,2.0,0),(4.6,2.0,1.4),.04,'blue');rod('Resident_height_top',(4.42,2.0,1.4),(4.78,2.0,1.4),.025,'blue');text('Height_label','1.40 m',(4.6,1.95,1.49),.20,(math.pi/2,0,0),'blue')
# Camera and light setup.
current='SETUP'
bpy.ops.object.light_add(type='AREA',location=(3,-5,13));o=bpy.context.object;o.name='Key_soft';o.data.energy=1800;o.data.shape='DISK';o.data.size=8
bpy.ops.object.light_add(type='AREA',location=(-5,6,9));o=bpy.context.object;o.name='Fill_soft';o.data.energy=1200;o.data.size=7
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Design_camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.lens=40
# setup objects remain in default collection, intentionally always visible.
def aim(loc,look,scale):cam.location=loc;cam.rotation_euler=(Vector(look)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
# Ground plane for soft grounding.
box('Ground',(-200,-200,-.26,200,200,-.24),'white',0)
def vis(f1=True,f2=True,stair=True,guide=False):
 bpy.data.objects['Arrival_platform'].hide_render=f2
 bpy.data.objects['Arrival_platform'].hide_set(f2)
 for n,v in [('F1',f1),('F2',f2),('STAIR',stair),('GUIDE',guide)]:colls[n].hide_render=not v
# Stage 1 geometry reviewed. Save with complete actual stacked building.
vis(True,True,True,False);aim((13,-15,14),(4,3.5,2.0),13.8)
scene['status']='DESIGN BLOCKOUT ONLY; not finished shop asset';scene['dimensions_source']='design_dimensions.json';scene['stair']='16 rises x 0.1625 = 2.6 m; clear flight width 1.2 m'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'shop_spatial_blockout_v01.blend'))
vis(True,False,True,True);aim((12,-13,12.5),(4,3.5,.8),11.9);scene.render.filepath=str(OUT/'09_blender_ground_blockout.png');bpy.ops.render.render(write_still=True)
vis(True,True,True,False);aim((12,-13,16),(4,3.5,3.4),12.2);scene.render.filepath=str(OUT/'10_blender_residence_blockout.png');bpy.ops.render.render(write_still=True)
vis(False,False,True,False);aim((11.5,-3,8.5),(6.5,5.0,1.2),5.3);scene.render.resolution_x=1280;scene.render.resolution_y=1280;scene.render.filepath=str(OUT/'11_blender_stair_blockout.png');bpy.ops.render.render(write_still=True)
# Re-save actual stacked assembly as default, render state independent of deliverable inspections.
vis(True,True,True,False);aim((13,-15,14),(4,3.5,2.0),13.8);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'shop_spatial_blockout_v01.blend'))
print('SPATIAL_BLOCKOUT_COMPLETE')
