import bpy, bmesh, math, random, json, os
from mathutils import Vector, Matrix
from pathlib import Path
random.seed(1708)
OUT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.materials): bpy.data.materials.remove(d)
M={}
def mat(name,c,emit=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*c,1); m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.82
 if emit:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emit
 M[name]=m;return m
for n,c in {'plaster':(.76,.61,.37),'cream':(.94,.81,.53),'wood':(.22,.086,.027),'wood_light':(.43,.22,.075),'wood_gold':(.62,.33,.095),'roof':(.085,.135,.21),'roof_light':(.14,.20,.29),'pink':(.63,.095,.20),'pink_light':(.84,.18,.31),'red':(.63,.085,.045),'teal':(.075,.31,.29),'teal_light':(.11,.48,.39),'charcoal':(.035,.045,.062),'gold':(.9,.51,.08),'glass':(.11,.3,.32),'stone':(.41,.43,.36),'stone_light':(.61,.59,.44),'earth':(.26,.15,.059),'soil':(.38,.23,.085),'grass':(.25,.43,.095),'grass_light':(.4,.56,.16),'leaf':(.11,.30,.055),'leaf_light':(.3,.48,.06),'flower':(.91,.28,.37),'water':(.08,.39,.52),'asphalt':(.25,.28,.25),'sand':(.58,.45,.24),'steel':(.23,.27,.30),'white':(.95,.91,.71),'window':(.98,.60,.15),'lamp':(1,.70,.24),'mountain':(.13,.31,.17)}.items():mat(n,c,1.1 if n in ['window','lamp'] else 0)
ASSETS={}; ROOT=None; COL=None
def asset(name,at):
 global ROOT,COL
 COL=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(COL)
 ROOT=bpy.data.objects.new(name+'_origin',None);COL.objects.link(ROOT);ROOT.location=(at[0],-at[2],at[1]);ASSETS[name]={'root':ROOT,'objects':[],'at':at}
 return ROOT
def add(ob,name,material,node='static'):
 ob.name=name;ob.parent=ROOT
 for c in list(ob.users_collection):c.objects.unlink(ob)
 COL.objects.link(ob);ob.data.materials.append(M[material]);ob['node']=node;ASSETS[ROOT.name[:-7]]['objects'].append(ob)
 return ob
def xyz(v):return (v[0],-v[2],v[1])
def mesh(name,verts,faces,m,node='static',bevel=0):
 me=bpy.data.meshes.new(name);me.from_pydata([xyz(p) for p in verts],[],faces);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new(name,me);add(o,name,m,node)
 if bevel:
  mod=o.modifiers.new('Soft crafted edges','BEVEL');mod.width=bevel;mod.segments=1
  mod=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def box(name,p,s,m,bevel=.035,node='static'):
 x,y,z=p;a,b,c=[v/2 for v in s]
 v=[(x+i*a,y+j*b,z+k*c) for i,j,k in [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]]
 return mesh(name,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(1,2,6,5),(0,4,7,3)],m,node,bevel)
def ball(name,p,s,m,node='static',seg=12,rings=6):
 vs=[];fs=[]
 for j in range(rings+1):
  ph=math.pi*j/rings
  for i in range(seg):
   th=math.tau*i/seg;vs.append((p[0]+s[0]*math.sin(ph)*math.cos(th),p[1]+s[1]*math.cos(ph),p[2]+s[2]*math.sin(ph)*math.sin(th)))
 for j in range(rings):
  for i in range(seg):fs.append((j*seg+i,j*seg+(i+1)%seg,(j+1)*seg+(i+1)%seg,(j+1)*seg+i))
 o=mesh(name,vs,fs,m,node)
 for f in o.data.polygons:f.use_smooth=True
 return o
def tube(name,a,b,r,m,node='static',n=8):
 av,bv=Vector(a),Vector(b);d=(bv-av).normalized();u=d.cross(Vector((0,1,0)))
 if u.length<.01:u=d.cross(Vector((1,0,0)))
 u.normalize();v=d.cross(u).normalized();vs=[]
 for c in [av,bv]:
  for i in range(n):vs.append(tuple(c+r*(u*math.cos(i*math.tau/n)+v*math.sin(i*math.tau/n))))
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,m,node)
def path(name,pts,r,m,node='static',n=6):
 for i in range(len(pts)-1):tube(name+str(i),pts[i],pts[i+1],r,m,node,n)
def ring(name,x,y,z,rx,ry,r,m):
 pts=[(x+rx*math.cos(i*math.tau/24),y+ry*math.sin(i*math.tau/24),z) for i in range(25)];path(name,pts,r,m,n=6)
def prism(name,xy,z,depth,m,bevel=.015,node='static'):
 n=len(xy);v=[(x,y,z+d) for d in [-depth/2,depth/2] for x,y in xy];f=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,v,f,m,node,bevel)
def gable_roof(w,d,eave,rise,m='roof',y0=2.25,z0=0):
 half=w/2; rows=5;cols=max(6,int(d/.42)); dd=d/cols
 for zz in [-d/2+.30+z0,d/2-.30+z0]:
  prism('Solid timber framed gable infill',[(-half+.23,y0-.12),(0,y0+rise-.15),(half-.23,y0-.12)],zz,.12,'plaster',.015)
 # Each tile is a real beveled clay slab, separate for editing and merged by material at runtime.
 for side in [-1,1]:
  for row in range(rows):
   x0=side*(row/rows*half);x1=side*((row+1)/rows*half+.045)
   ya=y0+rise*(1-abs(x0)/half)-row*.007;yb=y0+rise*(1-abs(x1)/half)+.07*(abs(x1)/half)**4-row*.007
   for j in range(cols):
    zz=-d/2+(j+.5)*dd+z0
    pp=[(x0,ya+.06),(x1,yb+.06),(x1,yb-.08),(x0,ya-.08)]
    prism('Overlapping roof tile',pp,zz,dd-.016,m if (row+j)%5 else m+'_light' if m+'_light' in M else m,.018)
 for zz in [-d/2+z0,d/2+z0]:
  path('Heavy shaped gable fascia',[(-half,y0+.07,zz),(0,y0+rise+.06,zz),(half,y0+.07,zz)],.085,'wood')
 tube('Rounded ridge cap',(0,y0+rise+.13,-d/2+z0),(0,y0+rise+.13,d/2+z0),.105,m,n=10)
def window(x,y,z,w=.65,h=.85,front=True):
 # Front-facing windows; side windows rotate an editable collection of meshes after generation.
 prior=len(ASSETS[ROOT.name[:-7]]['objects'])
 box('Warm window pane',(x,y,z),(w,h,.045),'window',.015,'emissive_windows')
 for xx in [x-w/2,x+w/2]:box('Window jamb',(xx,y,z+.045),(.075,h+.16,.11),'wood',.012)
 for yy in [y-h/2,y+h/2]:box('Window lintel sill',(x,yy,z+.045),(w+.16,.09,.14),'wood',.014)
 box('Window vertical muntin',(x,y,z+.06),(.045,h,.055),'wood',.008);box('Window crossbar',(x,y,z+.06),(w,.055,.055),'wood',.008)
 if not front:
  pivot=Vector(xyz((x,y,z)));rot=Matrix.Rotation(math.pi/2,4,'Z')
  for o in ASSETS[ROOT.name[:-7]]['objects'][prior:]:o.matrix_basis=Matrix.Translation(pivot)@rot@Matrix.Translation(-pivot)@o.matrix_basis
def door(x,z,y=.15,w=.95,h=1.5):
 box('Door shadow recess',(x,y+h/2,z),(w+.15,h+.12,.12),'charcoal')
 for side in [-1,1]:
  xx=x+side*w/4;box('Twin timber entrance leaf',(xx,y+h/2,z+.07),(w/2-.025,h,.09),'wood_light',.022)
  box('Door glass',(xx,y+h*.69,z+.125),(w/2-.13,h*.47,.023),'window',.015,'emissive_windows')
  box('Door lower inset',(xx,y+h*.21,z+.13),(w/2-.14,h*.27,.035),'wood',.009)
  tube('Brass door pull',(x+side*.065,y+h*.47,z+.17),(x+side*.065,y+h*.62,z+.17),.023,'gold')
 for xx in [x-w/2-.07,x+w/2+.07]:box('Door carved jamb',(xx,y+h/2,z+.10),(.11,h+.22,.18),'wood',.02)
 box('Entrance lintel',(x,y+h+.075,z+.1),(w+.3,.16,.19),'wood',.025)
def planter(x,z,w=.6):
 box('Timber planter',(x,.22,z),(w,.32,.44),'wood_light',.045)
 for q in [-1,1]:box('Planter band',(x,.15+q*.1,z+.235),(w+.05,.055,.05),'wood',.008)
 for i in range(3):
  xx=x+(i-1)*w*.27;ball('Leaf tuft',(xx,.49,z),(.23,.22,.22),'leaf_light')
  if i%2==0:
   for a in range(5):ball('Flower petals',(xx+.06*math.cos(a*math.tau/5),.73,z+.06*math.sin(a*math.tau/5)),(.055,.022,.045),'cream',seg=8,rings=4)
   ball('Flower heart',(xx,.753,z),(.025,.023,.025),'gold',seg=8,rings=4)
def lantern(x,y,z):
 tube('Lantern iron hanger',(x,y+.2,z-.1),(x,y+.2,z+.07),.032,'charcoal')
 box('Lantern glowing core',(x,y,z+.06),(.19,.28,.18),'lamp',.03,'emissive_lamps')
 for xx in [-.11,.11]:
  for zz in [-.04,.16]:tube('Lantern corner iron',(x+xx,y-.15,z+zz),(x+xx,y+.15,z+zz),.016,'charcoal')
 box('Lantern cap',(x,y+.18,z+.06),(.3,.08,.28),'charcoal',.04)
 box('Lantern foot',(x,y-.18,z+.06),(.25,.065,.24),'charcoal',.025)
def bench(x,z,w=1.2):
 for zz in [-.16,0,.16]:box('Bench seat slat',(x,.45,z+zz),(w,.075,.12),'wood_light',.02)
 for yy in [.69,.85]:box('Bench back slat',(x,yy,z-.23),(w,.12,.06),'wood_light',.018)
 for xx in [x-w*.35,x+w*.35]:
  tube('Bench support',(xx,.08,z-.22),(xx,.88,z-.22),.034,'charcoal');tube('Bench front leg',(xx,.05,z+.18),(xx,.46,z+.18),.034,'charcoal')
def awning(w,z,y,colors=('red','cream')):
 n=8
 for i in range(n):
  xx=-w/2+(i+.5)*w/n
  xa=xx-w/n/2;xb=xx+w/n/2
  mesh('Striped sloping awning',[(xa,y+.18,z-.32),(xb,y+.18,z-.32),(xb,y-.04,z+.32),(xa,y-.04,z+.32),(xa,y+.10,z-.32),(xb,y+.10,z-.32),(xb,y-.12,z+.32),(xa,y-.12,z+.32)],[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],colors[i%2],bevel=.02)
  # front rounded valance below the canopy
  box('Awning scalloped valance',(xx,y-.17,z+.32),(w/n,.27,.09),colors[i%2],.065)
def basehouse(w=3.8,d=2.8,h=2.25):
 box('Stone foundation',(0,.1,0),(w+.18,.2,d+.18),'stone_light',.07)
 box('Plastered building walls',(0,h/2+.16,0),(w,h,d),'plaster',.07)
 for x in [-w/2,w/2]:
  for z in [-d/2,d/2]:box('Exposed structural corner post',(x,h/2+.2,z),(.16,h+.15,.16),'wood',.035)
 for yy in [.4,h+.15]:box('Front timber beam',(0,yy,d/2+.055),(w+.15,.17,.15),'wood',.025)
 for z in [-d/2,d/2]:box('Side base beam',(0,.26,z),(w,.17,.16),'wood',.022)
 for x in [-w/2,w/2]:box('Side top timber',(x,h+.14,0),(.17,.15,d+.1),'wood',.025)
 box('Front entrance paving',(0,.065,d/2+.4),(w+.38,.13,.9),'stone_light',.05)
 return d/2+.12
def sign_arch(w,y,z,color='wood',trim='gold'):
 shape=[(-w/2,y),(-w/2,y+.52),(-w*.33,y+.60),(-w*.22,y+.82),(0,y+.96),(w*.22,y+.82),(w*.33,y+.60),(w/2,y+.52),(w/2,y)]
 prism('Sculpted arch sign surround',shape,z,.18,trim,.055)
 cx=sum(p[0] for p in shape)/len(shape);cy=y+.4
 inner=[(x*.92,cy+(yy-cy)*.82) for x,yy in shape];prism('Recessed arched sign face',inner,z+.11,.12,color,.045)
def cup(x,y,z,s=1):
 # Solid cup and toroidal handle: symbol modeled as relief, not texture.
 ball('Cup bowl relief',(x,y,z),(.20*s,.20*s,.10*s),'cream');box('Cup lip',(x,y+.16*s,z),(.39*s,.055*s,.16*s),'cream',.022)
 ring('Cup handle',x+.22*s,y+.03*s,z,.11*s,.12*s,.027*s,'cream');box('Cup saucer',(x,y-.19*s,z),(.5*s,.045*s,.19*s),'cream',.015)
 for dx in [-.06,.05]:path('Coffee steam',[(x+dx*s,y+.25*s,z),(x+(dx-.03)*s,y+.34*s,z),(x+dx*s,y+.43*s,z)],.014*s,'cream')
FACILITIES={'home':[-9,0,3],'cafe':[-9,0,-4],'arcade':[7,0,3],'farm':[7,0,-4],'bath':[0,0,-5]}

# HOME: warm plaster, crafted timber balcony and brackets, tiled gable roof.
asset('town_home',FACILITIES['home']);basehouse(4,2.9,2.55)
gable_roof(4.55,3.45,0,.98,y0=2.8)
door(-.65,1.59,h=1.5);window(.92,1.07,1.52,.72,.80);window(2.04,1.24,-.3,.75,.95,False)
for x in [-1.65,1.65]:
 box('Porch post',(x,1.1,1.91),(.13,2.12,.13),'wood',.02)
 path('Porch curved corbel',[(x,1.65,1.91),(x*.9,1.89,1.91),(x*.72,2.03,1.91)],.055,'wood_light')
box('Porch beam',(0,2.10,1.91),(3.65,.18,.16),'wood',.025)
for x in [-1.65,-1.25,1.2,1.65]:box('Porch railing baluster',(x,.62,1.95),(.065,.78,.065),'wood_light',.008)
for x in [-1.43,1.43]:box('Porch handrail',(x,1.02,1.95),(.85,.10,.12),'wood',.02)
for i in range(12):box('Porch deck planks',(-1.95+(i+.5)*3.9/12,.2,1.72),(.30,.10,.75),'wood_light',.01)
window(0,2.91,1.52,.55,.45);planter(-1.55,2.28,.58);planter(1.58,2.28,.6);lantern(.08,1.8,1.64)
bench(1.5,-1.75,1.1)

# CAFE: pink clay tile roof, small dormer, striped modest canopy, cup sign, plant pots.
asset('town_cafe',FACILITIES['cafe']);basehouse(3.85,2.7,2.05)
gable_roof(4.4,3.18,0,.9,'pink',2.3)
door(0,1.49,h=1.48);window(-1.25,1.05,1.43,.58,.83);window(1.25,1.05,1.43,.58,.83);window(1.98,1.12,-.25,.66,.87,False)
awning(3.3,1.67,1.99,('pink_light','cream'))
sign_arch(2.55,2.16,1.73);cup(0,2.61,1.93,.9)
for x in [-1.36,1.36]:lantern(x,2.22,1.70)
# chimney actual stacked bricks
for r in range(4):
 for c in range(2):box('Turquoise chimney masonry',(.98+(c-.5)*.24,3.0+r*.19,-.72),(.23,.185,.40),'teal_light',.02)
box('Chimney cap',( .98,3.69,-.72),(.68,.14,.61),'charcoal',.04)
planter(-1.53,2.1,.64);planter(1.53,2.1,.64);bench(2.42,.35,.95)

# ARCADE: stepped masonry, arched bulbs, raised mummy relief, striped awning.
asset('town_arcade',FACILITIES['arcade']);basehouse(3.8,2.8,2.22)
for yy,ww,dd in [(2.45,4.18,3.15),(2.61,3.93,2.91),(2.78,3.60,2.61)]:box('Stepped roof parapet',(0,yy,0),(ww,.17,dd),'stone' if yy==2.61 else 'wood_light',.045)
box('Flat tiled roof',(0,2.8,-.15),(3.5,.10,2.5),'roof',.02)
for x in [-1.65,-1.05,-.45,.15,.75,1.35]:box('Parapet coping joints',(x,2.9,-1.32),(.54,.16,.21),'stone_light',.018)
for yy in [.72,1.12,1.52,1.92]:
 for side in [-1,1]:
  for zz in [-.98,-.36,.26,.88]:box('Side brick quoin',(side*1.915,yy,zz),(.09,.15,.51),'wood_light',.012)
door(0,1.54,h=1.55);window(-1.29,1.05,1.47,.64,.95);window(1.29,1.05,1.47,.64,.95)
awning(3.7,1.71,2.08)
sign_arch(3.5,2.3,1.79,'red','gold')
for i in range(13):ball('Marquee bulb',(-1.58+i*.264,2.38,1.945),(.052,.052,.047),'lamp','emissive_lamps',8,4)
for x in [-1.7,1.7]:
 for y in [2.59,2.78]:ball('Marquee edge bulb',(x,y,1.945),(.052,.052,.047),'lamp','emissive_lamps',8,4)
# Mummy cat-head sculpted shallow relief. No image plane, facial wrap and glasses separate meshes.
ball('Mummy silhouette',(0,3.36,1.82),(.76,.62,.19),'cream')
for side in [-1,1]:
 prism('Mummy pointed ear',[(side*.36,3.74),(side*.77,4.03),(side*.73,3.42)],1.81,.25,'cream',.05)
 prism('Mummy inner ear',[(side*.48,3.73),(side*.69,3.92),(side*.65,3.56)],1.97,.035,'wood_light',.015)
for j in range(5):
 yy=3.04+j*.15;xx=math.sqrt(max(.0,1-((yy-3.36)/.64)**2))*.68
 path('Mummy individual wrap seam',[(-xx,yy+.05,1.998),(0,yy,2.03),(xx,yy-.05,1.998)],.015,'wood_light')
for x in [-.30,.30]:
 ball('Mummy dark eye field',(x,3.4,2.045),(.245,.26,.055),'wood');ring('Mummy gold spectacles',x,3.4,2.10,.25,.27,.044,'gold');ball('Mummy friendly eye gleam',(x-.05,3.49,2.11),(.06,.09,.025),'cream',seg=8,rings=5)
tube('Mummy spectacles bridge',(-.045,3.43,2.12),(.045,3.43,2.12),.024,'gold')
for x in [-.95,.95]:ball('Mummy paw on marquee',(x,2.96,1.98),(.23,.13,.11),'cream')
box('Roof ventilator',(1.01,3.04,-.51),(.65,.51,.57),'stone',.05)
for i in range(5):box('Ventilator slats',(.79+i*.11,3.06,-.215),(.035,.28,.018),'charcoal',.005)
planter(-1.56,2.24,.61);planter(1.56,2.24,.61)

# BATH: real timber frame, individually tiled roof, plain split noren, chimney, small rock water basin.
asset('town_bath',FACILITIES['bath']);basehouse(4.15,3.0,2.13)
gable_roof(4.72,3.55,0,1.13,'roof',2.38)
door(.63,1.66,h=1.48,w=.94);window(-1.13,1.12,1.62,.83,.89);window(2.15,1.23,-.28,.86,1.04,False)
for x in [-1.87,-.43,1.70]:box('Bath substantial front pillar',(x,1.20,1.65),(.18,2.12,.20),'wood_light',.025)
for i in range(10):box('Bath front lower timber boards',(-1.86+i*.40,.57,1.62),(.34,.55,.10),'wood_light',.01)
# entry canopy small pitched awning
for i in range(9):
 xx=-1.95+i*.48;prism('Entry canopy tile',[(xx-.25,2.30),(xx+.25,2.30),(xx+.25,2.14),(xx-.25,2.14)],1.76,.66,'roof_light' if i%3==0 else 'roof',.03)
box('Bath blank carved wood sign',(0,2.64,1.85),(2.72,.51,.16),'wood_gold',.09)
# The individual 013 building instruction explicitly permits this name only.
# Mesh lettering uses the locally installed Japanese font; no logo/image plane.
ft=bpy.data.curves.new('Bath Japanese sign lettering','FONT');ft.body='ネコクー温泉';ft.align_x='CENTER';ft.align_y='CENTER';ft.size=.345;ft.extrude=.006;ft.bevel_depth=.002;ft.bevel_resolution=0;ft.resolution_u=3
ft.font=bpy.data.fonts.load('C:/Windows/Fonts/meiryob.ttc')
letter=bpy.data.objects.new('Bath name real extruded lettering',ft);COL.objects.link(letter);letter.parent=ROOT;letter.location=xyz((0,2.64,1.945));letter.rotation_euler=(math.pi/2,0,0);ft.materials.append(M['wood']);letter['node']='static'
bpy.ops.object.select_all(action='DESELECT');letter.select_set(True);bpy.context.view_layer.objects.active=letter;bpy.ops.object.convert(target='MESH');ASSETS['town_bath']['objects'].append(bpy.context.object)
tube('Noren rod',(-.03,1.92,1.87),(1.29,1.92,1.87),.035,'wood')
for i in range(3):
 xx=.17+i*.43;prism('Split indigo cloth noren',[(xx-.2,1.86),(xx+.2,1.86),(xx+.2,1.22),(xx+.05,1.20),(xx-.2,1.23)],1.86,.025,'roof',.012)
for x in [-1.60,1.53]:lantern(x,2.02,1.99)
for r in range(4):box('Stone chimney course',(1.42,2.95+r*.22,-.76),(.47,.215,.50),'stone_light' if r%2 else 'stone',.025)
box('Chimney wide top',(1.42,3.8,-.76),(.67,.15,.68),'stone_light',.03)
box('Outdoor water trough',(2.38,.35,.84),(.8,.61,.85),'wood_light',.035);box('Visible fresh water',(2.38,.65,.84),(.66,.045,.71),'water',.04)
for i in range(7):
 a=i*math.tau/7;ball('Trough rounded stones',(2.38+.43*math.cos(a),.67,.84+.46*math.sin(a)),(.17,.18,.14),'stone',seg=8,rings=4)
planter(-2.14,1.93,.56);bench(-1.28,2.46,1.12)

# FARM: nine beds, asymmetric farm shed, gate, crate and water barrel; not a proxy building.
asset('town_farm',FACILITIES['farm'])
box('Farm yard',(0,.035,0),(4.7,.07,3.75),'sand',.1)
for x in [-1.4,-.45,.5]:
 for z in [-.82,.13,1.08]:
  box('Raised vegetable bed',(x,.16,z),(.80,.22,.72),'wood_light',.02);box('Tilled bed soil',(x,.30,z),(.69,.065,.62),'soil',.025)
  for k in [-.19,.19]:
   tube('Young crop stalk',(x+k,.31,z),(x+k,.69,z),.018,'leaf');ball('Crop leaf',(x+k-.07,.48,z),(.12,.04,.075),'leaf_light',seg=8,rings=4);ball('Crop leaf',(x+k+.07,.57,z),(.12,.04,.075),'leaf_light',seg=8,rings=4)
for x in [-2.25,-1.5,-.75,0,.75,1.5,2.25]:
 for z in [-1.76,1.76]:
  if z>0 and x==1.5:continue
  box('Farm fence post',(x,.45,z),(.1,.85,.1),'wood_light',.018)
for z in [-1.76,1.76]:
 for y in [.38,.66]:
  if z<0:box('Farm fence cross rail',(0,y,z),(4.5,.075,.07),'wood_light',.01)
  else:
   box('Farm front rail left',(-.73,y,z),(3.0,.075,.07),'wood_light',.01)
   box('Farm front rail right',(2.07,y,z),(.42,.075,.07),'wood_light',.01)
box('Shed back wall',(1.67,.83,-.70),(1.04,1.55,.10),'wood_light',.015)
for x in [1.12,2.22]:box('Shed side timber',(x,.83,-.29),(.10,1.55,.85),'wood_light',.025)
for x in [1.12,2.22]:box('Shed front upright',(x,.82,.17),(.10,1.57,.10),'wood',.025)
box('Farm shed sloped roof',(1.67,1.7,-.23),(1.48,.15,1.32),'teal',.05)
for i in range(5):box('Shed corrugation',(1.11+i*.28,1.80,-.23),(.065,.07,1.32),'teal_light',.02)
for x in [1.4,1.91]:box('Harvest crate',(x,.33,.04),(.40,.52,.43),'wood_gold',.025)
tube('Water barrel',(1.72,.08,1.06),(1.72,.71,1.06),.30,'wood_light',n=12)
for yy in [.18,.58]:
 for i in range(12):
  a=i*math.tau/12;b=(i+1)*math.tau/12;tube('Barrel metal hoop',(1.72+.305*math.cos(a),yy,1.06+.305*math.sin(a)),(1.72+.305*math.cos(b),yy,1.06+.305*math.sin(b)),.026,'steel')

# TRAIN built at local origin, wheel tread lowest point y=0; +X forward, movable along one track.
asset('town_train',[-8,.8975,-13.6])
for k,cx in enumerate([-1.20,1.20]):
 box('Car underframe',(cx,.30,0),(2.20,.20,.88),'charcoal',.05)
 box('Cream railcar body',(cx,.91,0),(2.15,1.04,1.04),'cream',.15)
 box('Teal waist stripe',(cx,.78,0),(2.18,.18,1.06),'teal',.025)
 box('Rounded teal roof',(cx,1.51,0),(2.3,.22,1.13),'teal',.12)
 for s in [-1,1]:
  for dx in [-.69,-.2,.32,.77]:
   box('Railcar dark window surround',(cx+dx,1.14,s*.532),(.39,.47,.045),'wood',.05)
   box('Railcar window',(cx+dx,1.16,s*.558),(.31,.37,.025),'glass',.04)
  box('Railcar sliding door',(cx-.17,.87,s*.565),(.49,1.0,.024),'teal_light',.028)
  box('Door upper glazing',(cx-.17,1.13,s*.583),(.33,.36,.025),'glass',.04)
 for dx in [-.70,.70]:
  for s in [-1,1]:tube('Steel wheel',(cx+dx,.20,s*.34),(cx+dx,.20,s*.54),.20,'charcoal',n=12)
 for dx in [-.63,.64]:box('Roof ventilation pod',(cx+dx,1.68,0),(.43,.16,.46),'stone_light',.055)
for xx in [-2.31,2.31]:
 box('Cab front window',(xx,1.11,0),(.027,.40,.76),'glass',.025)
 for zz in [-.31,.31]:ball('Train headlight',(xx,.76,zz),(.035,.075,.075),'lamp','emissive_lamps',8,4)
box('Intercar flexible gangway',(0,.80,0),(.28,.90,.65),'charcoal',.065)
tube('Coupler',(-.27,.35,0),(.27,.35,0),.065,'steel')

# TERRAIN / STATION. Continuous countryside instead of floating diorama pedestal.
asset('town_terrain',[0,0,0])
box('Continuous meadow ground',(0,-.28,0),(72,.55,66),'grass',.3)
# Gently rising north and west landscape as smooth low-poly hills; distant sea edge east.
for i in range(10):
 x=-34+i*7.5;z=-27-random.uniform(0,5);ball('Distant rounded mountain',(x,1.7,z),(6+random.random()*3,4+random.random()*4,7),'mountain',seg=12,rings=7)
box('Coastal sea',(32,-.05,7),(24,.12,70),'water',.12)
for i in range(15):ball('Coastal rolling bank',(20+random.uniform(-1,2),-.1,-27+i*4),(2.9,.8,3.3),'grass_light',seg=10,rings=5)
# Open road cross; all lot branches connect to it. Keep central pedestrian paths unobstructed.
box('Village main road',(0,.025,0),(34,.07,2.20),'asphalt',.04)
box('Station road',(0,.025,-5),(2.15,.07,24),'asphalt',.04)
for z in [-1.22,1.22]:box('Raised road shoulder',(0,.07,z),(34,.11,.24),'stone_light',.03)
for x in [-1.19,1.19]:box('North south road curb',(x,.07,-5),(.21,.1,24),'stone_light',.025)
for f,at in FACILITIES.items():
 x,y,z=at;end=z+2.15
 box('Facility footpath '+f,(x,.047,end/2),(1.15,.09,abs(end)+.15),'stone_light',.025)
 # connector from spine to building frontage
 box('Connected lane '+f,(x/2,.045,end),(abs(x)+1.10,.09,.95),'stone_light',.025)
for x in [-13.5,13.5]:
 box('Future lane spine',(x,.03,3),(1.05,.09,22),'sand',.025)
 box('Future cross connection',(x/2,.03,10),(abs(x)+1.1,.09,1.0),'sand',.025)
LOTS=[[-8,8],[0,8],[8,8],[-8,-9],[8,-9],[13,4.5]]
for j,(x,z) in enumerate(LOTS):
 box('Expandable plot '+str(j+1),(x,.035,z),(4.5,.055,3.5),'sand',.08)
 for xx in [-2.22,2.22]:
  for zz in [-1.72,1.72]:box('Plot boundary stake',(x+xx,.3,z+zz),(.1,.55,.1),'wood_light',.012)
 # actual connecting path not isolated ground marker
 box('Future plot access '+str(j+1),(x,.055,(z+1.75)/2),(1,.08,abs(z+1.75)),'sand',.015)
# Retaining wall: modest platform elevation only, no floating map edge.
box('Rail embankment',(0,.24,-13.6),(47,.52,4.0),'stone',.15)
for xx in range(-23,24):
 for yy in [.12,.43]:box('Embankment stone course',(xx,yy,-11.58),(.96,.29,.26),'stone_light' if xx%3==0 else 'stone',.07)
box('Rail ballast',(0,.57,-13.6),(48,.22,1.46),'stone_light',.10)
for x in range(-47,48):box('Timber rail sleeper',(x*.5,.72,-13.6),(.17,.12,1.51),'wood',.018)
for z in [-14.06,-13.14]:
 box('Single track rail',(0,.85,z),(48,.095,.09),'steel',.01)
box('One side station platform',(1, .62,-11.87),(9.7,1.04,1.77),'stone',.08)
box('Platform concrete top',(1,1.17,-11.87),(9.87,.18,1.9),'stone_light',.05)
for xx in [i*.40-3.70 for i in range(24)]:box('Platform edge safety paver',(xx,1.28,-12.69),(.36,.04,.21),'cream',.015)
# Roofed timber waiting shelter at platform; front faces rails, rotate roof/props overall? use both open sides.
for x in [-2.2,0,2.2]:
 for z in [-12.32,-11.36]:box('Station timber shelter column',(x,2.02,z),(.13,1.55,.13),'wood',.025)
for z in [-12.32,-11.36]:box('Station shelter longitudinal beam',(0,2.78,z),(4.65,.16,.17),'wood_light',.02)
# pitched roof built along X ridge (custom roof strips) rather than global roof helper
for side in [-1,1]:
 for row in range(4):
  za=-11.84+side*row*.2;zb=za+side*.23;ya=3.2-row*.1-row*.008;yb=ya-.115
  for col in range(11):
   xa=-2.55+col*.47; mesh('Station slate tile',[(xa,ya,za),(xa+.455,ya,za),(xa+.455,yb,zb),(xa,yb,zb),(xa,ya-.08,za),(xa+.455,ya-.08,za),(xa+.455,yb-.08,zb),(xa,yb-.08,zb)],[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],'roof_light' if col%4==0 else 'roof',bevel=.012)
tube('Station ridge cap',(-2.63,3.27,-11.84),(2.65,3.27,-11.84),.09,'roof',n=10)
# Bench at raised height using transform translate after ordinary construction
prior=len(ASSETS['town_terrain']['objects']);bench(0,-11.55,2.5)
for o in ASSETS['town_terrain']['objects'][prior:]:o.location.z+=1.26
for x in [-1.85,1.85]:
 box('Station lower windscreen',(x,1.80,-11.36),(.54,1.03,.10),'wood_light',.02)
 for yy in [1.60,1.89,2.17]:box('Shelter timber panel batten',(x,yy,-11.3),(.55,.035,.065),'wood',.008)
# platform stairs and railings facing central road
for i in range(6):box('Station access stair',(4.4,.11+i*.10,-9.03-i*.30),(1.38,.22+i*.20,.32),'stone_light',.025)
for side in [-1,1]:
 for i in [0,2,5]:tube('Stair handrail post',(4.4+side*.79,.25+i*.20,-9.02-i*.3),(4.4+side*.79,.95+i*.20,-9.02-i*.3),.025,'steel')
 tube('Stair handrail',(4.4+side*.79,.98,-9.03),(4.4+side*.79,2.00,-10.56),.033,'steel')
box('Station walking approach',(2.2,.04,-8.7),(4.4,.08,1.0),'sand',.02)
# Railway crossing edge on eastern end; stripes modeled.
for z in [-14.7,-12.5]:
 tube('Crossing post',(12,.0,z),(12,2.2,z),.075,'gold')
 for yy in [.3,.7,1.1,1.5]:tube('Crossing black stripe',(12,yy,z),(12,yy+.20,z),.077,'charcoal')
 for s in [-1,1]:tube('Railway crossbuck',(11.72,1.96+s*.25,z),(12.28,1.96-s*.25,z),.055,'gold')
 box('Crossing signal',(12,1.6,z),(.39,.18,.18),'charcoal',.04)
 for xx in [-.11,.11]:ball('Crossing red lamp',(12+xx,1.60,z+.11),(.06,.06,.04),'red',seg=8,rings=4)
# Japanese utility poles, sagging wires, non-obstructive decorative shoulder placement.
for x in [-16,-5,6,17]:
 tube('Rural utility pole',(x,0,-15.8),(x,4.2,-15.8),.10,'wood_light')
 tube('Utility crossarm',(x-.65,3.85,-15.8),(x+.65,3.85,-15.8),.055,'wood')
 for xx in [-.48,.48]:tube('Ceramic insulator',(x+xx,3.86,-15.8),(x+xx,4.03,-15.8),.065,'cream')
for x in [-16,-5,6]:
 for dz in [-.2,.2]:path('Sagging overhead wire',[(x+i*11/8,4.04-.35*math.sin(i*math.pi/8),-15.8+dz) for i in range(9)],.012,'charcoal',n=4)
def tree(x,z,scale=1):
 tube('Tree trunk',(x,0,z),(x,1.65*scale,z),.14*scale,'wood_light')
 for dx,dz,yy in [(-.42,0,1.6),(.4,.12,1.8),(0,-.3,2.1),(0,.3,1.85)]:ball('Rounded broadleaf canopy',(x+dx*scale,yy*scale,z+dz*scale),(.68*scale,.70*scale,.66*scale),'leaf_light' if dx<0 else 'leaf',seg=10,rings=6)
for x,z in [(-15,-7),(-14,4),(-14,10),(-4,-9),(12,-6),(13,11),(-6,12),(4,12),(-17,-14),(18,-15),(-11,-17),(7,-19),(14,-20),(-20,0),(-20,10),(17,3)]:tree(x,z,random.uniform(.75,1.2))
for j in range(32):
 x=random.choice([-1,1])*random.uniform(15,21);z=random.uniform(-19,15);ball('Roadside rounded boulder',(x,.22,z),(.3,.32,.4),'stone',seg=8,rings=4)
for x,z in [(-4,2),(3,2),(-3,-7),(3,-7),(-12,6),(12,6)]:
 tube('Street lamp post',(x,0,z),(x,2.45,z),.045,'charcoal');lantern(x,2.45,z)
# Scenic rice fields outside buildable lots
for cx,cz in [(-20,6),(-20,-5),(16,-7)]:
 box('Rural rice paddy soil',(cx,.015,cz),(3.9,.055,4.8),'soil',.03)
 for xx in [-1.8,1.8]:box('Raised paddy earth berm',(cx+xx,.08,cz),(.23,.17,4.9),'grass_light',.05)
 for r in range(7):
  for c in range(6):
   x=cx-1.35+c*.53;z=cz-2+r*.64
   for dx in [-.06,.07]:tube('Rice young shoot',(x,.04,z),(x+dx,.45,z+.05),.024,'leaf_light',n=5)
# Modest low fences and log pile, pasture fringe clear of central lanes
for x in range(-12,13,2):
 box('Southern wooden roadside fence',(x,.39,12.8),(.10,.72,.1),'wood_light',.015)
 if x<12:
  for y in [.30,.55]:box('Fence cross rail',(x+1,y,12.8),(2,.06,.065),'wood_light',.008)
for k in range(3):tube('Stored rounded firewood',(-14.8+k*.35,.22,-3.5),(-14.8+k*.35,.22,-2.3),.17,'wood_light',n=10)

# Build one non-overlapping walking-surface tessellation. Independent rectangular
# path slabs intersected coplanar and caused black rectangles in the first Cycles
# inspection. Replace every intersecting slab with disjoint exact-boundary cells.
prefixes=('Village main road','Station road','Facility footpath','Connected lane','Future lane spine','Future cross connection','Expandable plot','Future plot access','Station walking approach')
rects=[];old=[]
for o in list(ASSETS['town_terrain']['objects']):
 if o.name.startswith(prefixes):
  vv=[v.co for v in o.data.vertices];xmin=min(v.x for v in vv);xmax=max(v.x for v in vv);zmin=min(-v.y for v in vv);zmax=max(-v.y for v in vv)
  rects.append((xmin,xmax,zmin,zmax,o.data.materials[0].name));old.append(o)
xs=sorted(set(round(x,5) for r in rects for x in r[:2]));zs=sorted(set(round(z,5) for r in rects for z in r[2:4]));cells={};priority={'asphalt':0,'sand':1,'stone_light':2}
for i in range(len(xs)-1):
 for j in range(len(zs)-1):
  x=(xs[i]+xs[i+1])/2;z=(zs[j]+zs[j+1])/2;matches=[r for r in rects if r[0]-1e-5<=x<=r[1]+1e-5 and r[2]-1e-5<=z<=r[3]+1e-5]
  if matches:cells[i,j]=max(matches,key=lambda r:priority.get(r[4],0))[4]
for material in ['asphalt','sand','stone_light']:
 vs=[];fs=[]
 for (i,j),mm in cells.items():
  if mm!=material:continue
  a=len(vs);vs.extend([(xs[i],.092,zs[j]),(xs[i+1],.092,zs[j]),(xs[i+1],.092,zs[j+1]),(xs[i],.092,zs[j+1])]);fs.append((a,a+3,a+2,a+1))
 o=mesh('Continuous non-overlapping '+material+' walking surface',vs,fs,material)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=.00001);bmesh.ops.dissolve_limit(bm,angle_limit=.005,verts=bm.verts,edges=bm.edges,use_dissolve_boundaries=False);bm.to_mesh(o.data);bm.free()
 # Open road surface explicitly faces up; do not infer volume orientation.
 for poly in o.data.polygons:
  if poly.normal.z<0:poly.flip()
for o in old:ASSETS['town_terrain']['objects'].remove(o);bpy.data.objects.remove(o,do_unlink=True)

# Editable source organization; runtime export remains grouped by asset/material.
groups={n:bpy.data.collections.new(n) for n in ['01_TERRAIN','02_ROADS','03_STATION','04_RAILWAY','05_NATURE','06_PROPS','07_EMPTY_LOTS']}
for cc in groups.values():COL.children.link(cc)
for o in ASSETS['town_terrain']['objects']:
 n=o.name.lower()
 if any(w in n for w in ['station','platform','stair','shelter']):key='03_STATION'
 elif any(w in n for w in ['rail','sleeper','crossing','embankment']):key='04_RAILWAY'
 elif any(w in n for w in ['walking surface','road','curb','shoulder']):key='02_ROADS'
 elif 'boundary stake' in n:key='07_EMPTY_LOTS'
 elif any(w in n for w in ['tree','canopy','mountain','coastal','rice','paddy','boulder','meadow','sea']):key='05_NATURE'
 else:key='06_PROPS'
 COL.objects.unlink(o);groups[key].objects.link(o)

# Exports evaluated, triangulated, transform-flattened meshes, in Three +Y up/+Z front.
def export_asset(name,data):
 deps=bpy.context.evaluated_depsgraph_get();parts=[];points=[];tri=0;rootinv=data['root'].matrix_world.inverted()
 for ob in data['objects']:
  ev=ob.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();tr=rootinv@ob.matrix_world;nm=tr.to_3x3().inverted().transposed()
  p=[];ns=[]
  for face in me.loop_triangles:
   if face.area<1e-10:continue
   for vi in face.vertices:
    vv=tr@me.vertices[vi].co;nn=(nm@me.vertices[vi].normal).normalized();v=[round(vv.x,5),round(vv.z,5),round(-vv.y,5)];p.extend(v);ns.extend([round(nn.x,5),round(nn.z,5),round(-nn.y,5)]);points.append(v)
  mm=ob.data.materials[0];bs=mm.node_tree.nodes.get('Principled BSDF');c=list(bs.inputs['Base Color'].default_value)[:3]
  parts.append({'name':ob.name,'node':ob.get('node','static'),'positions':p,'normals':ns,'material':{'name':mm.name,'color':c,'roughness':.82,'metallic':0,'opacity':1}});tri+=len(p)//9;ev.to_mesh_clear()
 b={'min':[min(p[a] for p in points) for a in range(3)],'max':[max(p[a] for p in points) for a in range(3)]}
 anchors={'entrance':[0,.1,2.2]} if name.startswith('town_') and name not in ['town_terrain','town_train'] else {}
 if name=='town_home':anchors['entrance']=[-.65,.1,2.2]
 if name=='town_farm':anchors['entrance']=[1.35,.1,1.95]
 if name=='town_bath':anchors.update({'entrance':[.63,.1,2.2],'chimneySteam':[1.42,3.96,-.76]})
 if name=='town_train':anchors={'wheelContact':[0,0,0],'forward':[1,0,0]}
 obj={'id':name,'parts':parts,'anchors':anchors,'bounds':b,'triangleCount':tri};(OUT/(name+'.json')).write_text(json.dumps(obj,separators=(',',':')),encoding='utf8')
 return {'id':name,'json':name+'.json','worldOrigin':data['at'],'bounds':b,'triangleCount':tri,'objectCount':len(parts),'materialCount':len(set(p['material']['name'] for p in parts)),'nodes':sorted(set(p['node'] for p in parts))}
bpy.context.view_layer.update()
records=[export_asset(n,d) for n,d in ASSETS.items()]
# train wheels must sit on rails top in assembled inspection scene
ASSETS['town_train']['root'].location.z=.8975
manifest={'name':'MOB CHILL modeled country town','coordinateSystem':'Three +Y up +Z front; source Blender +Z up -Y front','production':'Original bpy modeled meshes. No image planes and no existing source blend modified.','referencesViewed':['001.png','009.png','011.png','013.png','017.png','素材について.txt','町について.txt'],'referenceAdoption':{'001':'Warm wood/plaster material language for sharehouse; image is an interior illustration, exterior interpreted.','009':'Stepped roof parapet, striped awning, arched marquee bulbs and sculpted mummy cat relief; omitted tiny posters/text.','011':'Pink individual clay tiles, modest striped canopy, arched cup sign, chimney, small windows and planters; simplified crowded terrace.','013':'Individual slate tiles, substantial timber frame, split indigo noren, chimney, porch and basin; no shopkeeper or interior duplication.','017':'Actual raised station, stairs, retaining wall, single railway, rice fields, broadleaf trees, power poles, future lots; continuous countryside replaces floating slab.'},'deviations':['Original town brief 200m field scaled to a walkable 34x29 town core with 72x66 surrounding landscape for current game; no attempt at a literal 200m simulation.','Buildings are game-sized cartoon interpretations, not pixel-perfect tracing of highly detailed reference illustrations.','Sign text omitted in keeping with town brief no-text rule; modeled icons identify facilities.','No train passengers, station names, shopkeepers or new gameplay systems.','Final phone performance and game lighting must be verified by integrator.'],'assets':records,'facilityPositions':FACILITIES,'entrances':{k:[v[0],.1,v[2]+2.2] for k,v in FACILITIES.items()},'emptyLots':[{'center':[x,0,z],'size':[4.5,3.5],'access':[x,0,z+1.75]} for x,z in LOTS],'rail':{'axis':'X','centerZ':-13.6,'railTopY':.8975,'trainOriginY':.8975,'rangeX':[-24,24]},'lightingNodes':{'emissive_windows':'warm window panes; runtime may set emissiveIntensity by day phase','emissive_lamps':'street lamps, fixture cores, marquee bulbs, train lamps'},'triangleCount':sum(a['triangleCount'] for a in records)}
manifest['entrances'].update({'home':[-9.65,.1,5.2],'farm':[8.35,.1,-2.05],'bath':[.63,.1,-2.8]})
manifest['deviations'][2]='Only the bath name ネコクー温泉 is real extruded mesh lettering per reference 013; no station text or added logos. Other facility signs use modeled identity cues.'
manifest['referenceAdoption']['013']+=' The specifically permitted Japanese bath name is extruded mesh text; no decorative cat/steam logos.'
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
# All source geometry plus semantic roots exported to GLB. Cameras/lights stay in .blend only.
bpy.ops.object.select_all(action='DESELECT')
for d in ASSETS.values():
 d['root'].select_set(True)
 for o in d['objects']:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'MOB_CHILL_TOWN.glb'),export_format='GLB',use_selection=True,export_apply=True)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.world.color=(.38,.44,.52);scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.46,.60,.75,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
scene.view_settings.view_transform='AgX'
bpy.ops.object.light_add(type='AREA',location=(2,-6,25));bpy.context.object.name='Large soft daylight';bpy.context.object.data.energy=2600;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=20
bpy.ops.object.light_add(type='SUN',location=(0,0,20));bpy.context.object.name='Warm afternoon sun';bpy.context.object.rotation_euler=(.45,-.5,-.5);bpy.context.object.data.energy=2;bpy.context.object.data.angle=.18
def camera(name,pos,target,scale):
 bpy.ops.object.camera_add(location=xyz(pos));cam=bpy.context.object;cam.name=name;cam.rotation_euler=(Vector(xyz(target))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale;scene.camera=cam;return cam
cam=camera('Town overview camera',(27,31,38),(0,.5,-2),43)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'MOB_CHILL_TOWN.blend'))
def render(name,pos,target,scale):
 camera(name,pos,target,scale);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
render('town_overview',(27,31,38),(0,.5,-2),43)
render('station_detail',(10,8,-4),(0,1.4,-12.1),14)
for an,d in ASSETS.items():
 for o in d['objects']:o.hide_render=(an!='town_terrain')
render('station_front',(0,3.7,-4.3),(0,2,-11.9),10.8)
for d in ASSETS.values():
 for o in d['objects']:o.hide_render=False
render('cafe_arcade_detail',(13,9,15),(0,1.5,1),23)
for an,d in ASSETS.items():
 for o in d['objects']:o.hide_render=(an not in ['town_bath','town_terrain'])
render('bath_detail',(6,5,3),(0,1.7,-5),8.7)
# Individual building renders with other asset geometry hidden for inspection.
for name in ['town_home','town_cafe','town_arcade','town_farm']:
 for an,d in ASSETS.items():
  for o in d['objects']:o.hide_render=(an not in [name,'town_terrain'])
 at=ASSETS[name]['at'];render(name+'_detail',(at[0]+6,5.8,at[2]+7),(at[0],1.5,at[2]),7)
for d in ASSETS.values():
 for o in d['objects']:o.hide_render=False
for an,d in ASSETS.items():
 for o in d['objects']:o.hide_render=(an not in ['town_train','town_terrain'])
render('train_detail',(-1,5,-7),(-8,1.6,-13.6),7.8)
for d in ASSETS.values():
 for o in d['objects']:o.hide_render=False
scene.camera=cam;bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'MOB_CHILL_TOWN.blend'))
print('TOWN COMPLETE',json.dumps({'triangles':manifest['triangleCount'],'assets':len(records)}))
