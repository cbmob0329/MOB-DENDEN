import bpy, math, json, os, random, sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
M={}
def mat(name,c,metal=0,rough=.48,alpha=1):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,alpha);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,alpha);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=alpha
 if alpha<1:m.surface_render_method='DITHERED'
 M[name]=m;return m
mat('charcoal',(0.028,.037,.049));mat('rubber',(.013,.018,.022));mat('green',(.24,.83,.035));mat('cyan',(.012,.51,.95));mat('yellow',(1,.69,.025));mat('ivory',(.9,.93,.88));mat('steel',(.33,.4,.43),.6,.32);mat('glass',(.55,.82,.94),.05,.12,.17);mat('display',(.016,.063,.086));mat('red',(.95,.09,.08));mat('orange',(1,.3,.015));mat('purple',(.45,.15,.8))
assets={};current=None
BOLD=bpy.data.fonts.load('C:/Windows/Fonts/arialbd.ttf')
def finish(o,name,material,node='static'):
 o.name=name;o.data.materials.append(M[material]);o['node']=node
 for c in list(o.users_collection):c.objects.unlink(o)
 current.objects.link(o);return o
def box(n,p,s,m,r=.05,node='static'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.scale=s;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if r:mod=o.modifiers.new('Soft molded edges','BEVEL');mod.width=r;mod.segments=3;o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 return finish(o,n,m,node)
def sphere(n,p,s,m,node='static',seg=20):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=12,location=p);o=bpy.context.object;o.scale=s
 for f in o.data.polygons:f.use_smooth=True
 return finish(o,n,m,node)
def cyl(n,p,rad,depth,m,axis=None,node='static',verts=24):
 bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=rad,depth=depth,location=p);o=bpy.context.object
 if axis:o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
 mod=o.modifiers.new('Rounded machined lip','BEVEL');mod.width=min(.012,rad*.15);mod.segments=2;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return finish(o,n,m,node)
def rod(n,a,b,r,m,node='static'):
 a,b=Vector(a),Vector(b);return cyl(n,(a+b)/2,r,(b-a).length,m,b-a,node)
def tor(n,p,major,minor,m,axis=(0,0,1),node='static'):
 bpy.ops.mesh.primitive_torus_add(major_segments=28,minor_segments=8,location=p,major_radius=major,minor_radius=minor);o=bpy.context.object;o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
 for f in o.data.polygons:f.use_smooth=True
 return finish(o,n,m,node)
def profile(n,coords,y,depth,m,r=.035,node='static'):
 vs=[(x,y+d,z) for d in [-depth/2,depth/2] for x,z in coords];k=len(coords);fs=[tuple(reversed(range(k))),tuple(range(k,2*k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 mesh=bpy.data.meshes.new(n);mesh.from_pydata(vs,[],fs);mesh.update();o=bpy.data.objects.new(n,mesh);current.objects.link(o);o.data.materials.append(M[m]);o['node']=node
 if r:mod=o.modifiers.new('Molded profile radius','BEVEL');mod.width=r;mod.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def text(n,txt,p,size,m,node='static'):
 cu=bpy.data.curves.new(n,'FONT');cu.font=BOLD;cu.body=txt;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.008;cu.bevel_depth=.003;cu.bevel_resolution=1;o=bpy.data.objects.new(n,cu);current.objects.link(o);o.location=p;o.rotation_euler=(math.pi/2,0,0);cu.materials.append(M[m]);o['node']=node;return o
def start(id):
 global current
 current=bpy.data.collections.new(id);bpy.context.scene.collection.children.link(current);assets[id]={'collection':current,'anchors':{}}
def anchor(n,p):assets[current.name]['anchors'][n]=[p[0],p[2],-p[1]]
def ears(cx,y,z,spread,size,m):
 for s in [-1,1]:
  pts=[(cx+s*(spread-size*.55),z),(cx+s*(spread+size*.55),z),(cx+s*(spread+size*.5),z+size)]
  profile('Molded cat ear rim',pts,y,.15,'charcoal',.035)
  pts=[(cx+s*(spread-size*.3),z+.06),(cx+s*(spread+size*.3),z+.06),(cx+s*(spread+size*.3),z+size*.77)]
  profile('Cat ear color insert',pts,y-.085,.025,m,.015)
def hemisphere(n,p,r,top,m,node):
 N=28;R=8;vs=[]
 for j in range(R+1):
  phi=(j/R)*(math.pi/2)+(0 if top else math.pi/2)
  for i in range(N):a=i/N*2*math.pi;vs.append((p[0]+r*math.sin(phi)*math.cos(a),p[1]+r*math.sin(phi)*math.sin(a),p[2]+r*math.cos(phi)))
 fs=[]
 for j in range(R):
  for i in range(N):a=j*N+i;b=j*N+(i+1)%N;fs.append((a,b,b+N,a+N))
 mesh=bpy.data.meshes.new(n);mesh.from_pydata(vs,[],fs);mesh.update();o=bpy.data.objects.new(n,mesh);current.objects.link(o);o.data.materials.append(M[m]);o['node']=node
 for f in mesh.polygons:f.use_smooth=True
 sol=o.modifiers.new('Actual shell thickness','SOLIDIFY');sol.thickness=.009
 return o
def capsule(p,r=.13,color='green',prefix='Stored capsule',animate=False):
 before=set(current.objects)
 hemisphere(prefix+' colored lower shell',p,r,False,color,'capsule_bottom' if animate else 'static');hemisphere(prefix+' clear upper shell',p,r,True,'glass','capsule_top' if animate else 'glass');tor(prefix+' seam',p,r,.008,color,node='capsule_bottom' if animate else 'static')
 if not animate:
  from mathutils import Matrix,Euler
  rot=Euler((random.uniform(-.8,.8),random.uniform(-.8,.8),random.uniform(-.4,.4))).to_matrix().to_4x4();trans=Matrix.Translation(Vector(p))@rot@Matrix.Translation(-Vector(p))
  for o in set(current.objects)-before:o.matrix_world=trans@o.matrix_world
start('gacha')
box('Weighted rounded foot',(0,0,.105),(1.16,.94,.18),'charcoal',.10)
for x in [-.43,.43]:
 for y in [-.3,.3]:cyl('Rubber foot',(x,y,.035),.09,.07,'rubber')
box('Lower molded body',(0,.035,.57),(1.07,.80,.84),'charcoal',.14)
for x in [-.49,.49]:box('Replaceable color molding',(x,-.10,.65),(.105,.70,.91),'green',.05)
box('Control face',(0,-.398,.83),(.88,.065,.41),'rubber',.08)
cyl('Rotary knob bezel',(0,-.453,.83),.165,.065,'green',(0,1,0));cyl('Yellow twist knob',(0,-.502,.83),.137,.07,'yellow',(0,1,0),'knob');box('Raised knob handle',(0,-.55,.83),(.043,.045,.205),'yellow',.018,'knob');anchor('knob',(0,-.52,.83))
for x,m in [(-.32,'green'),(.32,'yellow')]:box('Soft square control button',(x,-.46,.80),(.21,.07,.19),m,.065)
box('Dark chute recess',(0,-.416,.37),(.62,.035,.31),'rubber',.075)
for x in [-.335,.335]:box('Chute curved side rail',(x,-.43,.37),(.065,.20,.34),'steel',.032)
box('Chute upper rim',(0,-.48,.535),(.70,.11,.055),'steel',.025);box('Catch tray',(0,-.44,.212),(.7,.28,.05),'steel',.025);box('Transparent swing hatch',(0,-.532,.38),(.60,.025,.255),'glass',.045,'hatch');anchor('capsuleOutlet',(0,-.48,.29));anchor('hatchPivot',(0,-.53,.50))
# Broad curved reservoir, rounded back and rim; real capsules visible inside.
box('Reservoir rear shell',(0,.24,1.39),(1.02,.31,.86),'charcoal',.17)
box('Reservoir clear curved cover',(0,-.04,1.39),(1.07,.75,.82),'glass',.21,'glass')
box('Reservoir base rim',(0,-.015,.985),(1.09,.79,.09),'green',.04)
random.seed(22)
for j in range(3):
 for i in range(3):capsule((-.31+i*.31,-.13+random.uniform(-.08,.09),1.12+j*.205),.14,['green','cyan','yellow','purple'][random.randrange(4)])
box('Crowned rounded header',(0,.015,1.865),(1.07,.79,.23),'green',.105)
box('Raised charcoal MOB badge',(0,-.398,1.875),(.68,.04,.175),'charcoal',.055);text('MOB brand','MOB',(0,-.432,1.88),.19,'yellow')
ears(0,.04,1.96,.34,.24,'green');anchor('displayCenter',(0,-.10,1.40))
start('capsule');capsule((0,0,.24),.23,'cyan',animate=True);anchor('splitCenter',(0,0,.24));anchor('prizeCenter',(0,0,.23))
start('ufo')
for x in [-1.1,1.1]:
 for y in [-.79,.79]:cyl('Cabinet rubber caster',(x,y,.07),.10,.14,'rubber')
box('Bottom reinforced chassis',(0,0,.19),(2.68,2.08,.18),'charcoal',.12)
box('Lower yellow cabinet',(0,.07,.61),(2.55,1.91,.73),'yellow',.13)
box('Lower front black inset',(0,-.936,.62),(2.25,.075,.60),'charcoal',.08)
box('Prize chute black cavity',(-.53,-.985,.53),(1.07,.04,.42),'rubber',.05)
for x in [-1.11,.05]:box('Prize chute rim',(x,-1.03,.53),(.045,.09,.50),'yellow',.02)
box('Prize chute bottom',(-.53,-1.005,.29),(1.2,.15,.055),'steel',.02);box('Prize chute lip',(-.53,-1.07,.35),(1.07,.045,.045),'charcoal',.015);anchor('chuteCenter',(-.53,-.73,1.02));anchor('chuteExit',(-.53,-1.05,.37))
box('Coin service door',(.72,-.989,.61),(.36,.045,.43),'steel',.025)
for z in [.7,.55]:box('Coin slot',(.72,-1.021,z),(.11,.017,.023),'rubber',.005)
cyl('Service lock',(.81,-1.025,.45),.022,.016,'rubber',(0,1,0))
box('Sloping control shelf',(0,-.84,1.035),(2.6,.51,.17),'yellow',.08)
box('Control black insert',(-.1,-.89,1.132),(1.95,.30,.038),'charcoal',.07)
cyl('Joystick socket',(-.67,-.9,1.18),.12,.035,'rubber');rod('Joystick stem',(-.67,-.9,1.19),(-.67,-.9,1.37),.035,'steel');sphere('Joystick golden ball',(-.67,-.9,1.40),(.10,.10,.10),'yellow')
cyl('Grab button bezel',(.48,-.9,1.17),.15,.04,'rubber');cyl('Grab button',(.48,-.9,1.21),.12,.045,'yellow')
box('Prize floor rear',(0,.365,1.06),(2.30,1.08,.085),'ivory',.03)
box('Prize floor front right',(.59,-.45,1.06),(1.12,.55,.085),'ivory',.03)
box('Prize floor front left rim',(-1.07,-.45,1.06),(.16,.55,.085),'ivory',.025)
box('Chute inner back wall',(-.50,-.18,.81),(1.04,.045,.43),'charcoal',.015)
anchor('prizeFloor',(0,.09,1.105));anchor('chuteCenter',(-.50,-.45,1.105));anchor('chuteOpeningMin',(-.99,-.175,1.105));anchor('chuteOpeningMax',(.03,-.725,1.105))
for x in [-1.21,1.21]:
 for y in [-.69,.94]:
  box('Steel upright',(x,y,1.82),(.105,.105,1.46),'steel',.04)
  box('Yellow upright inset',(x+(.012 if x<0 else -.012),y-.055,1.82),(.043,.025,1.34),'yellow',.01)
for x in [-1.19,1.19]:box('Clear side glazing',(x,.12,1.79),(.019,1.55,1.30),'glass',.005,'glass')
box('Clear front glazing',(0,-.681,1.83),(2.29,.018,1.29),'glass',.005,'glass');box('Rear glass',(0,.936,1.83),(2.29,.018,1.29),'glass',.005,'glass')
box('Upper molded crown',(0,.105,2.61),(2.66,1.95,.34),'charcoal',.13)
for x in [-1.23,1.23]:box('Golden crown edge',(x,.105,2.62),(.12,1.92,.28),'yellow',.055)
box('Illuminated header frame',(0,-.916,2.61),(2.32,.115,.34),'yellow',.08);box('Header dark enamel',(0,-.98,2.61),(2.17,.028,.255),'charcoal',.055);text('UFO molded MOB lettering','MOB',(0,-1.01,2.61),.27,'yellow')
for x in [-.91,.91]:sphere('Header corner lamp',(x,-1.012,2.61),(.055,.025,.075),'ivory')
for x in [-.96,.96]:rod('X gantry support',(x,-.5,2.405),(x,.76,2.405),.032,'steel')
rod('Claw carriage cross rail',(-.98,.10,2.405),(.98,.10,2.405),.04,'steel','carriage');box('Claw motor carriage',(0,.10,2.38),(.30,.25,.12),'charcoal',.035,'carriage');anchor('carriage',(0,.10,2.38))
rod('Claw cable',(0,.10,2.34),(0,.10,2.12),.019,'rubber','cable');anchor('cableTop',(0,.10,2.34))
cyl('Claw chrome spindle',(0,.10,2.12),.047,.12,'steel',node='claw');sphere('Claw golden housing',(0,.10,2.03),(.18,.15,.115),'yellow','claw');box('Claw black emblem',(0,-.04,2.04),(.18,.035,.10),'charcoal',.025,'claw');text('Claw MOB','MOB',(0,-.066,2.04),.062,'ivory','claw');anchor('clawPivot',(0,.10,2.12));anchor('gripPoint',(0,.10,1.78))
for i in range(3):
 a=math.pi/6+i*2*math.pi/3;v=Vector((math.cos(a),math.sin(a),0));p=Vector((0,.10,2.01));q=p+v*.24+Vector((0,0,-.17));r=p+v*.17+Vector((0,0,-.33));node='finger_'+str(i)
 sphere('Finger shoulder '+str(i),p+v*.12,(.045,.045,.045),'steel',node);rod('Finger upper '+str(i),p+v*.12,q,.034,'steel',node);rod('Finger hooked yellow tip '+str(i),q,r,.038,'yellow',node);anchor('fingerPivot_'+str(i),p+v*.12)
anchor('prizeBoundsMin',(-1.07,.77,1.11));anchor('prizeBoundsMax',(1.07,-.53,2.15))
# Expand the cabinet for the established physics chute in the left front corner.
for o in list(current.objects):
 o.location.x*=1.12;o.location.y*=1.14;o.scale.x*=1.12;o.scale.y*=1.14
 if o.name.startswith(('Prize floor','Chute inner back')):bpy.data.objects.remove(o,do_unlink=True)
 elif o.name.startswith(('Steel upright','Yellow upright inset')):
  o.location.x=math.copysign(1.475,o.location.x);o.location.y=-1.10 if o.location.y<0 else 1.0
 elif o.name.startswith('Clear side glazing'):o.location.x=math.copysign(1.48,o.location.x);o.location.y=-.05;o.scale.y*=2.02/(1.55*1.14)
 elif o.name.startswith('Clear front glazing'):o.location.y=-1.10;o.scale.x*=2.84/(2.29*1.12)
 elif o.name.startswith('Rear glass'):o.location.y=1.;o.scale.x*=2.84/(2.29*1.12)
for k,p in assets['ufo']['anchors'].items():p[0]*=1.12;p[2]*=1.14
for o in list(current.objects):
 if o.name.startswith(('Lower yellow cabinet','Lower front black inset','Prize chute')):bpy.data.objects.remove(o,do_unlink=True)
box('Open shell rear',(0,.75,.61),(2.856,.50,.73),'yellow',.065)
for x in [-1.4,1.4]:box('Open shell side',(x,-.20,.61),(.09,1.43,.73),'yellow',.035)
box('Front fascia beside chute',(.39,-1.065,.61),(2.04,.12,.73),'yellow',.06)
box('Front dark service fascia',(.39,-1.135,.61),(1.88,.035,.59),'charcoal',.035)
box('Chute dark interior back',(-1.1,-.60,.60),(.66,.04,.55),'charcoal',.02)
box('Chute catching tray',(-1.1,-.93,.30),(.66,.55,.04),'steel',.02)
for x in [-1.46,-.73]:box('Chute rounded entry rim',(x,-1.15,.57),(.06,.08,.55),'yellow',.025)
box('Chute entry top',(-1.095,-1.15,.86),(.79,.08,.065),'yellow',.025)
anchor('chuteExit',(-1.1,-1.18,.35))
box('Prize floor rear around real opening',(0,.175,1.01),(2.92,1.60,.08),'ivory',.01)
box('Prize floor right of opening',(.19,-.85,1.01),(2.43,.45,.08),'ivory',.01)
box('Prize opening outer lip',(-1.43,-.85,1.01),(.06,.45,.08),'yellow',.01)
anchor('prizeFloor',(0,0,1.05));anchor('chuteCenter',(-1.225,-.90,1.05));anchor('chuteOpeningMin',(-1.4,-.625,1.05));anchor('chuteOpeningMax',(-1.025,-1.05,1.05))
anchor('prizeBoundsMin',(-1.40,.92,1.05));anchor('prizeBoundsMax',(1.40,-1.05,2.15))
for i in range(3):
 a=math.pi/6+i*2*math.pi/3;anchor('fingerTip_'+str(i),(.17*math.cos(a)*1.12,(.10+.17*math.sin(a))*1.14,1.68))
anchor('gripCenter',(0,.114,1.76))
for o in current.objects:
 if o.name.startswith(('Upper molded crown','Golden crown edge','Illuminated header frame','Header dark enamel','UFO molded MOB','Header corner lamp')):o['node']='roof'
 if o.name.startswith('Sloping control shelf'):o.location.y=-1.22;o.scale.y*=.42/(.51*1.14)
 elif o.name.startswith('Control black insert'):o.location.y=-1.24;o.scale.y*=.27/(.30*1.14)
 elif o.name.startswith(('Joystick','Grab button')):o.location.y-=.23
for y in [-1.10,1.0]:rod('Upper glazing structural crossbar',(-1.475,y,2.44),(1.475,y,2.44),.035,'steel')
for x in [-1.475,1.475]:rod('Upper glazing structural side rail',(x,-1.10,2.44),(x,1.0,2.44),.035,'steel')
start('race')
box('Connected two seat plinth',(0,0,.10),(2.78,2.38,.18),'charcoal',.11)
for x,m in [(-.68,'green'),(.68,'cyan')]:
 box('Cabinet color side sill',(x,-.05,.22),(1.27,2.22,.08),m,.035)
 # tower tilted polygon silhouette rather than a box
 profile('Monitor tower side silhouette',[(x-.61,.23),(x+.61,.23),(x+.61,2.11),(x+.51,2.29),(x-.51,2.29),(x-.61,2.11)],.73,.35,'charcoal',.07)
 box('Monitor molded color bezel',(x,.485,1.64),(1.22,.12,.96),m,.065)
 box('Monitor inner black bezel',(x,.405,1.64),(1.11,.065,.85),'rubber',.045)
 # flat actual screen node, UV generated cube front good replaceable runtime material
 box('screen_'+('left' if x<0 else 'right'),(x,.365,1.65),(1.02,.012,.72),'display',.008,'screen_left' if x<0 else 'screen_right')
 box('Dashboard molded housing',(x,.22,1.05),(1.19,.69,.30),'charcoal',.10)
 box('Dashboard color stripe',(x,-.135,1.075),(1.05,.035,.08),m,.025)
 # wheel tilted around x, assembly visible to seated player
 axis=(0,-.9,.45);center=(x,-.205,1.115)
 rod('Steering column',(x,.08,.98),center,.055,'steel');tor('Soft steering wheel',center,.215,.04,'rubber',axis,'wheel_left' if x<0 else 'wheel_right')
 cyl('Steering colored hub',center,.073,.055,m,axis,'wheel_left' if x<0 else 'wheel_right')
 for a in [math.pi/2,math.pi/2+2*math.pi/3,math.pi/2+4*math.pi/3]:rod('Wheel spoke',center,(x+math.cos(a)*.19,-.205+math.sin(a)*.085,1.115+math.sin(a)*.17),.025,'steel','wheel_left' if x<0 else 'wheel_right')
 anchor('wheel_'+('left' if x<0 else 'right'),center)
 box('Pedal footwell',(x,-.005,.36),(.89,.62,.18),'rubber',.05)
 for dx in [-.18,.18]:
  o=box('Raised metal pedal',(x+dx,-.17,.46),(.17,.25,.045),'steel',.025);o.rotation_euler.x=.28
  for j in [-1,0,1]:box('Pedal grip',(x+dx,-.17+j*.058,.491),(.13,.014,.012),'rubber',.004)
 # contour shell formed by layered extruded outline, back at front of game
 box('Seat pedestal',(x,-.74,.36),(.95,.70,.31),'charcoal',.09)
 box('Seat cushion color shell',(x,-.60,.59),(.88,.79,.20),m,.10);box('Seat cushion upholstered',(x,-.60,.65),(.69,.65,.14),'charcoal',.075)
 outline=[(x-.43,.67),(x-.42,1.15),(x-.29,1.28),(x-.23,1.58),(x+.23,1.58),(x+.29,1.28),(x+.42,1.15),(x+.43,.67)]
 profile('Sculpted bucket seat shell',outline,-.99,.19,m,.055)
 inner=[(x-.33,.74),(x-.32,1.12),(x-.21,1.22),(x-.17,1.49),(x+.17,1.49),(x+.21,1.22),(x+.32,1.12),(x+.33,.74)]
 profile('Seat back upholstery',inner,-1.10,.06,'charcoal',.04)
 text('Seat number','01' if x<0 else '02',(x,-1.15,1.05),.18,m)
 for dx in [-.14,.14]:box('Harness aperture',(x+dx,-1.15,1.35),(.13,.025,.055),'rubber',.025)
 anchor('seat_'+('left' if x<0 else 'right'),(x,-.59,.74))
 # monochrome checker pattern genuinely raised molded tiles
 for row in range(2):
  for col in range(6):
   if (row+col)%2==0:box('Checker relief',(x-.38+col*.15,.291,2.08+row*.075),(.145,.018,.07),'ivory',.005)
box('Connected overhead MOB marquee',(0,.59,2.30),(2.72,.40,.32),'charcoal',.085)
for x,m in [(-1.24,'green'),(1.24,'cyan')]:box('Marquee colored wing',(x,.355,2.30),(.14,.06,.25),m,.04)
text('Main molded MOB header','MOB',(0,.345,2.33),.27,'yellow')
anchor('screen_left',(-.68,.351,1.65));anchor('screen_right',(.68,.351,1.65))

# Separate reusable racing diorama; oval driving centerline is unchanged.
mat('grass',(.16,.43,.07));mat('road',(.055,.080,.095));mat('sand',(.55,.37,.15));mat('leaf',(.09,.30,.035))
start('race_course')
box('Rounded grassy diorama',(0,0,-.015),(7.45,4.55,.20),'grass',.20)
def trackstrip(n,rin,rout,m,z=.12,N=112):
 vs=[]
 for i in range(N):
  a=2*math.pi*i/N
  for r in [rin,rout]:vs.append(((2.76+r)*math.cos(a),(1.2+r)*math.sin(a),z))
 fs=[(2*i,2*((i+1)%N),2*((i+1)%N)+1,2*i+1) for i in range(N)]
 mesh=bpy.data.meshes.new(n);mesh.from_pydata(vs,[],fs);mesh.update();o=bpy.data.objects.new(n,mesh);current.objects.link(o);o.data.materials.append(M[m]);o['node']='static'
trackstrip('Continuous asphalt oval',-.31,.31,'road')
for side in [-1,1]:
 for i in range(80):
  a=2*math.pi*i/80;b=2*math.pi*(i+1)/80;r=side*.35
  vs=[((2.76+rr)*math.cos(t),(1.2+rr)*math.sin(t),.143) for t in [a,b] for rr in [r-.045,r+.045]]
  mesh=bpy.data.meshes.new('Curved rumble strip');mesh.from_pydata(vs,[],[(0,2,3,1)]);mesh.update();o=bpy.data.objects.new('Red white curb',mesh);current.objects.link(o);o.data.materials.append(M['red' if i%2==0 else 'ivory']);o['node']='static'
trackstrip('Inner painted road edge',-.28,-.267,'ivory',.146);trackstrip('Outer painted road edge',.267,.28,'ivory',.146)
for i in range(32):
 a=2*math.pi*i/32;o=box('Dashed lane guide',(2.76*math.cos(a),1.2*math.sin(a),.126),(.16,.019,.006),'ivory',.002);o.rotation_euler.z=math.atan2(1.2*math.cos(a),-2.76*math.sin(a))
for j in range(6):
 for i in range(2):box('Start finish check',(-.06+i*.12,-1.45+j*.1,.15),(.118,.098,.01),'ivory' if (i+j)%2 else 'charcoal',.001)
for y in [-1.73,-.68]:
 cyl('Start arch foot',(0,y,.20),.10,.14,'charcoal');rod('Start arch tower',(0,y,.20),(0,y,1.11),.045,'yellow')
box('Starting arch overhead',(0,-1.205,1.12),(.16,1.20,.22),'charcoal',.045)
for y in [-1.51,-1.31,-1.11,-.91]:sphere('Race start signal',(-.092,y,1.12),(.025,.046,.046),'red')
anchor('startLine',(0,-1.2,.12));anchor('trackCenter',(0,0,.12))
# Rounded infield island, bunting, tire stacks and two small spectator stands.
box('Infield planted island',(0,0,.10),(3.35,1.00,.14),'leaf',.36)
for x in [-1.05,0,1.05]:
 cyl('Infield topiary pot',(x,0,.23),.19,.19,'sand');sphere('Round clipped tree',(x,0,.61),(.29,.25,.34),'green',seg=16);rod('Topiary trunk',(x,0,.20),(x,0,.5),.055,'sand')
for x in [-2.9,2.9]:
 for y in [-1.85,1.85]:
  rod('Pennant pole',(x,y,.10),(x,y,.88),.022,'steel');profile('Triangular race pennant',[(x,.86),(x+.3,.79),(x,.63)],y,.025,'yellow',.006)
for x in [-2.15,2.15]:
 for y in [-1.76,1.76]:
  for z in [.18,.30]:tor('Safety tire stack',(x,y,z),.10,.035,'rubber')
for sy in [-1,1]:
 y=sy*1.96
 box('Spectator stand lower',(0,y,.19),(2.8,.44,.18),'sand',.045)
 box('Spectator stand upper',(0,y+sy*.16,.31),(2.8,.21,.20),'yellow',.035)
 for i in range(7):
  x=-1.12+i*.37;sphere('Spectator hood body',(x,y,.48),(.10,.095,.13),['cyan','green','purple'][i%3],seg=12);sphere('Spectator cat head',(x,y,.68),(.12,.105,.115),'charcoal',seg=12)
  for dx in [-.072,.072]:profile('Spectator triangular ear',[(x+dx-.04,.72),(x+dx+.04,.72),(x+dx,.83)],y,.08,'charcoal',.009)
  # Glasses face the track, retain black mouthless face.
  front=y-sy*.105
  for dx in [-.047,.047]:tor('Spectator gold glasses',(x+dx,front,.685),.030,.008,'yellow',axis=(0,1,0))
start('kart')
box('Rounded bumper chassis',(0,0,.14),(.53,.79,.11),'rubber',.075)
profile('Sculpted kart nose',[(-.23,.16),(.23,.16),(.20,.28),(-.20,.28)],-.29,.25,'cyan',.055)
box('Cockpit body',(0,.03,.21),(.43,.52,.13),'cyan',.07)
box('Driver bucket',(0,.09,.29),(.26,.25,.15),'charcoal',.07);box('Driver seat back',(0,.23,.39),(.25,.085,.23),'charcoal',.045)
for x in [-.26,.26]:
 for y in [-.23,.25]:
  cyl('Racing rubber tire',(x,y,.135),.135,.11,'rubber',(1,0,0),node='wheels',verts=20);cyl('Alloy wheel hub',(x+(.06 if x>0 else -.06),y,.135),.068,.015,'steel',(1,0,0),node='wheels',verts=16)
for x in [-.16,.16]:rod('Rear spoiler support',(x,.27,.23),(x,.34,.44),.02,'charcoal')
box('Rear aerodynamic spoiler',(0,.35,.455),(.56,.13,.04),'cyan',.019)
rod('Kart steering column',(0,-.045,.25),(0,-.10,.38),.018,'steel');tor('Kart steering wheel',(0,-.10,.38),.079,.014,'rubber',(0,-.6,.8))
for x in [-.15,.15]:sphere('Headlamp',(x,-.407,.23),(.041,.014,.025),'yellow',seg=12)
anchor('driverSeat',(0,.07,.37));anchor('front',(0,-.41,.15));anchor('rear',(0,.39,.15))

def mesh_export(id,data):
 col=data['collection'];deps=bpy.context.evaluated_depsgraph_get();parts=[];tri=0;mins=[1e9]*3;maxs=[-1e9]*3
 for obj in col.objects:
  if obj.type not in ['MESH','FONT','CURVE']:continue
  ev=obj.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();pos=[];nor=[];uv=[]
  for t in me.loop_triangles:
   for li in t.loops:
    loop=me.loops[li];v=ev.matrix_world@me.vertices[loop.vertex_index].co;n=(ev.matrix_world.to_3x3().inverted().transposed()@me.vertices[loop.vertex_index].normal).normalized();p=[v.x,v.z,-v.y];pos.extend(round(a,6) for a in p);nor.extend([round(n.x,6),round(n.z,6),round(-n.y,6)])
    for k in range(3):mins[k]=min(mins[k],p[k]);maxs[k]=max(maxs[k],p[k])
    if me.uv_layers.active:uv.extend(round(a,6) for a in me.uv_layers.active.data[li].uv)
  if pos:
   material=obj.data.materials[0];bs=material.node_tree.nodes.get('Principled BSDF');p={'name':obj.name,'node':obj.get('node','static'),'positions':pos,'normals':nor,'material':{'name':material.name,'color':list(bs.inputs['Base Color'].default_value[:3]),'roughness':bs.inputs['Roughness'].default_value,'metallic':bs.inputs['Metallic'].default_value,'opacity':bs.inputs['Alpha'].default_value}}
   if uv:p['uv']=uv
   parts.append(p);tri+=len(pos)//9
  ev.to_mesh_clear()
 out={'id':id,'parts':parts,'anchors':data['anchors'],'bounds':{'min':mins,'max':maxs},'triangleCount':tri}
 with open(os.path.join(ROOT,id+'.json'),'w',encoding='utf8') as f:json.dump(out,f,separators=(',',':'))
 bpy.ops.object.select_all(action='DESELECT')
 for o in col.objects:o.select_set(True)
 bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,id+'.glb'),use_selection=True,export_apply=True,export_yup=True,export_materials='EXPORT',export_extras=True)
 return {'id':id,'triangleCount':tri,'objects':len(parts),'materials':len(set(p['material']['name'] for p in parts)),'dimensions':[round(maxs[i]-mins[i],4) for i in range(3)],'anchors':data['anchors'],'semanticNodes':sorted(set(p['node'] for p in parts))}
manifest={'sourceReferences':['005.png','006.png','007.png','008.png'],'method':'Blender bpy mesh modeling; no reference image planes or generated images','assets':[],'deviations':['Reference character illustrations and decorative lettering other than MOB omitted. Race header uses modeled MOB lettering and checker strips, without large illustrated mascot heads.','UFO cabinet is wider relative to height than reference to meet existing gameplay footprint. Plush prizes are supplied by existing game models, not duplicated into cabinet.','Race screens export plain replaceable display surfaces; live game will supply CanvasTexture.']}
for id,d in assets.items():manifest['assets'].append(mesh_export(id,d))
with open(os.path.join(ROOT,'manifest.json'),'w',encoding='utf8') as f:json.dump(manifest,f,ensure_ascii=False,indent=2)
# Render camera and lights are outside runtime asset collections.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.world.color=(.25,.25,.25)
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
def light(n,p,power,size):
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.name=n;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
light('Large softbox',(-3,-4,6),550,4);light('Fill softbox',(4,-2,4),360,3);light('Rim softbox',(0,4,5),600,3)
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO'
if '--no-render' in sys.argv:
 bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'arcade_machines.blend'));print('ARCADE_EXPORT_COMPLETE_NO_RENDER');sys.exit(0)
for id,d in assets.items():
 for id2,d2 in assets.items():d2['collection'].hide_render=id2!=id
 size={'gacha':2.7,'capsule':.65,'ufo':4.25,'race':3.9,'race_course':9.0,'kart':1.15}[id];target=Vector((0,0,{'gacha':1.1,'capsule':.24,'ufo':1.4,'race':1.2,'race_course':.25,'kart':.23}[id]))
 for view,vec in [('front',(0,-6,2.2)),('isometric',(4,-6,3.5)),('rear',(-4,6,3))]:
  cam.location=target+Vector(vec);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;scene.render.filepath=os.path.join(ROOT,id+'_'+view+'.png');bpy.ops.render.render(write_still=True)
for d in assets.values():d['collection'].hide_render=False
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'arcade_machines.blend'))
print('ARCADE_EXPORT_COMPLETE',json.dumps(manifest))
