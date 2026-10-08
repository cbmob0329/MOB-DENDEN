import bpy, bmesh, math, random, json, base64, sys
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).resolve().parent
REF=OUT if (OUT/'004.png').exists() else OUT.parents[1]/'素材集'
random.seed(21)
M={}
def mat(n,c,em=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.78
 if em:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=em
 M[n]=m;return m
def xyz(v):return (v[0],-v[2],v[1])
def finish(o,n,m,node='static'):
 o.name=n;o.data.materials.append(m);o['runtime_node']=node;return o
def box(n,p,s,m,b=.03,node='static'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=xyz(p));o=bpy.context.object;o.dimensions=(s[0],s[2],s[1]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if b:
  mod=o.modifiers.new('soft crafted edges','BEVEL');mod.width=b;mod.segments=2
  mod=o.modifiers.new('weighted corner normals','WEIGHTED_NORMAL')
 return finish(o,n,m,node)
def curve(n,pts,r,m,node='static'):
 cu=bpy.data.curves.new(n,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=r;cu.bevel_resolution=2
 sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for q,p in zip(sp.points,pts):q.co=(*xyz(p),1)
 o=bpy.data.objects.new(n,cu);bpy.context.collection.objects.link(o);return finish(o,n,m,node)
def bracket(x,back,sign):
 shape=[(0,2.97),(.9,2.97),(.9,2.85),(.70,2.79),(.51,2.66),(.35,2.48),(.23,2.26),(0,2.26)]
 vs=[xyz((x+sign*q,h,back+dep)) for dep in [.17,.34] for q,h in shape];N=len(shape)
 fs=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 me=bpy.data.meshes.new('curved solid timber support');me.from_pydata(vs,[],fs)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new('carved curved timber bracket',me);bpy.context.collection.objects.link(o);finish(o,o.name,M['oak'])
 mod=o.modifiers.new('carved eased edges','BEVEL');mod.width=.035;mod.segments=2
def cyl(n,p,r,d,m,vertices=16):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d,location=xyz(p));o=bpy.context.object
 mod=o.modifiers.new('rounded lip','BEVEL');mod.width=.025;mod.segments=2
 return finish(o,n,m)
def ring(n,p,r,minor,m):
 bpy.ops.mesh.primitive_torus_add(major_segments=24,minor_segments=6,location=xyz(p),major_radius=r,minor_radius=minor)
 return finish(bpy.context.object,n,m)
def reset():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 M.clear()
 for n,c in {'wood':(.25,.095,.032),'oak':(.48,.235,.085),'honey':(.65,.36,.15),'dark':(.075,.043,.028),'cream':(.72,.57,.37),'plaster':(.79,.65,.43),'gold':(.64,.37,.10),'iron':(.065,.07,.075),'light':(1,.65,.24),'glass':(.23,.45,.54),'red':(.45,.10,.105),'purple':(.27,.22,.29),'tile':(.68,.56,.40),'stone':(.32,.30,.27),'water':(.14,.53,.47),'leaf':(.16,.31,.045),'navy':(.045,.073,.14)}.items():mat(n,c,1.1 if n=='light' else 0)
def lamp(x,y,z):
 box('lantern wall mount',(x,y,z+.01),(.27,.6,.14),M['dark'])
 box('lantern warm glass',(x,y,z+.14),(.23,.40,.22),M['light'],.025,'lamps')
 for dx in [-.15,.15]:box('lantern frame',(x+dx,y,z+.15),(.055,.56,.29),M['iron'])
 for dy in [-.28,.28]:box('lantern cap',(x,y+dy,z+.15),(.40,.07,.34),M['iron'])
def frame_window(cx,back):
 box('window night glass',(cx,2,back+.12),(2.05,1.35,.04),M['glass'],.01,'windows')
 for x in [cx-1.12,cx,cx+1.12]:box('window oak stile',(x,2,back+.18),(.12,1.6,.18),M['wood'])
 for y in [1.2,2,2.8]:box('window oak rail',(cx,y,back+.18),(2.35,.12,.20),M['wood'])
 box('deep window sill',(cx,1.16,back+.28),(2.58,.15,.52),M['oak'])
def shell(w,d,kind):
 back=-d/2+.25;left=-w/2+.25
 box('foundation',(0,-.16,0),(w,.30,d),M['dark'],.09)
 if kind!='arcade':
  for j in range(16):
   z=-d/2+(j+.5)*d/16
   cuts=[-w/2]+[x for x in [-w/2+k*w/4+(w/8 if j%2 else 0) for k in range(5)] if -w/2<x<w/2]+[w/2]
   for k in range(len(cuts)-1):
    x=(cuts[k]+cuts[k+1])/2;sx=cuts[k+1]-cuts[k]
    box('individual oak floorboard',(x,-.003,z),(sx-.018,.09,d/16-.019),M[['oak','honey','wood'][random.choices([0,1,2],[6,3,1])[0]]],.018)
    if (j+k)%3==0:
     for off in [-.12,.06]:curve('subtle carved floor grain',[(x-sx*.35+t*sx*.70,.045,z+off+.012*math.sin(t*7)) for t in [i/6 for i in range(7)]],.005,M['wood'])
 else:
  for j in range(12):
   for k in range(15):box('checker ceramic tile',(-w/2+(k+.5)*w/15,-.005,-d/2+(j+.5)*d/12),(w/15-.012,.10,d/12-.012),M['tile' if (j+k)%2 else 'purple'],.015)
 # walls split around real home window; no front/right occlusion
 if kind!='home':box('back plaster wall',(0,1.55,back),(w-.25,3.1,.18),M['plaster'])
 box('left plaster wall',(left,1.55,0),(.18,3.1,d-.25),M['plaster'])
 if kind=='home':
  cx=-2.3
  for lo,hi in [(-w/2,cx-1.15),(cx+1.15,w/2)]:box('wall beside window',((lo+hi)/2,1.55,back),(hi-lo,3.1,.18),M['plaster'])
  for cy,sy in [(.56,1.12),(2.975,.25)]:box('wall below above window',(cx,cy,back),(2.3,sy,.18),M['plaster'])
  frame_window(cx,back)
 for y in [.12,.86,3.02]:
  box('back timber molding',(0,y,back+.14),(w,.15,.19),M['wood'])
  box('left timber molding',(left+.14,y,0),(.19,.15,d),M['wood'])
 for x in [-w/2+.3,0,w/2-.3]:
  box('back sculpted timber column',(x,1.55,back+.22),(.24,3.1,.24),M['wood'])
  for y in [.25,2.8]:box('column carved collar',(x,y,back+.23),(.37,.18,.32),M['oak'])
  for sign in [-1,1]:
   if kind!='arcade' and abs(x+sign*.9)<w/2:bracket(x,back,sign)
 if kind=='cafe':
  for i in range(30):box('cafe oak wainscot plank',(-w/2+(i+.5)*w/30,.44,back+.12),(w/30-.012,.66,.04),M['oak' if i%3 else 'wood'],.012)
 if kind in ['cafe','arcade']:
  # paired windows intentionally in back shell clear of existing counter
  frame_window(2.65,back)
 for x in [-w/2+.75,w/2-.75]:lamp(x,2.10,back+.22)
 if kind=='arcade':
  for j in range(42):
   for row in range(2):box('retro wall checker',(-w/2+(j+.5)*w/42,.49+row*.18,back+.12),(w/42-.008,.175,.035),M['cream' if (j+row)%2 else 'dark'],.003)
  for y in [.85,2.90]:box('retro red ribbon',(0,y,back+.24),(w,.11,.12),M['red'])
  box('cornice glow',(0,2.95,back+.28),(w-.4,.035,.035),M['light'],.01,'lamps')
  for j in range(32):
   for row in range(2):box('side retro wall checker',(left+.12,.49+row*.18,-d/2+(j+.5)*d/32),(.035,.175,d/32-.008),M['cream' if (j+row)%2 else 'dark'],.003)
  for y in [.85,2.90]:box('side retro red ribbon',(left+.24,y,0),(.12,.11,d),M['red'])
  box('side cornice glow',(left+.28,2.95,0),(.035,.035,d-.4),M['light'],.01,'lamps')
  for z in [-d/2+.4,0,d/2-.4]:
   box('arcade side column',(left+.20,1.5,z),(.27,3,.27),M['cream'])
   for y in [.2,2.90]:box('arcade column capital',(left+.20,y,z),(.40,.20,.40),M['dark'])
 return back
def bath():
 w,d=9,8.5;back=-4.0;left=-4.25
 box('bath foundation',(0,-.16,0),(w,.30,d),M['dark'],.10)
 for i in range(10):
  for j in range(10):
   mm=M['stone'] if (i+j)%3 else M['tile']
   box('slate floor tile',(-4.5+(i+.5)*.9,-.01,-4.25+(j+.5)*.85),(.878,.12,.829),mm,.035)
 for i in range(25):box('vertical cedar back plank',(-4.32+i*.36,1.6,back),(.345,3.2,.18),M['oak' if i%3 else 'honey'],.025)
 for i in range(23):box('vertical cedar side plank',(left,1.6,-4.0+i*.36),(.18,3.2,.345),M['oak' if i%3 else 'honey'],.025)
 for y in [.2,1.0,3.12]:
  box('cedar back horizontal beam',(0,y,back+.17),(8.9,.18,.24),M['wood'])
  box('cedar side horizontal beam',(left+.17,y,0),(.24,.18,8.5),M['wood'])
 for x in [-4.2,-1.65,1.65,4.15]:box('bath structural post',(x,1.6,back+.20),(.20,3.2,.24),M['wood'])
 # rounded rectangular basin: actual curved strip with interior walls
 def path(rx,rz,r):
  pts=[]
  for cx,cz,start in [(rx-r,rz-r,0),(-rx+r,rz-r,90),(-rx+r,-rz+r,180),(rx-r,-rz+r,270)]:
   for i in range(7):
    a=math.radians(start+i*90/6);pts.append((cx+r*math.cos(a),cz+r*math.sin(a)))
  return pts
 outer=path(2.65,2.15,.52);inner=path(2.25,1.76,.44)
 verts=[]
 for pts,h in [(outer,.05),(outer,.62),(inner,.62),(inner,.15)]:verts += [xyz((x,h,z-.05)) for x,z in pts]
 N=len(outer);faces=[]
 for level in range(3):
  for i in range(N):faces.append((level*N+i,level*N+(i+1)%N,(level+1)*N+(i+1)%N,(level+1)*N+i))
 me=bpy.data.meshes.new('hollow rounded basin');me.from_pydata(verts,[],[tuple(reversed(f)) for f in faces]);o=bpy.data.objects.new('continuous hollow stone basin',me);bpy.context.collection.objects.link(o);finish(o,o.name,M['stone'])
 # equal arc-length hand-cut rim stones instead of long straight slabs
 lengths=[math.dist(outer[i],outer[(i+1)%N]) for i in range(N)];total=sum(lengths);nrocks=30;sample=[]
 for j in range(nrocks):
  dist=j*total/nrocks
  for i,ll in enumerate(lengths):
   if dist<=ll:
    t=dist/ll;a,b=outer[i],outer[(i+1)%N];sample.append((a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t));break
   dist-=ll
 for i in range(nrocks):
  a=sample[i];b=sample[(i+1)%nrocks];cx=(a[0]+b[0])/2;cz=(a[1]+b[1])/2-.05
  length=math.dist(a,b)
  o=box('faceted individual rim stone',(cx,.45+random.uniform(-.025,.025),cz),(length-.025,.43,.44),M['tile' if i%7==0 else 'stone'],.10)
  for v in o.data.vertices:v.co += Vector((random.uniform(-.027,.027),random.uniform(-.027,.027),random.uniform(-.024,.024)))
  o.rotation_euler[2]=-math.atan2(b[1]-a[1],b[0]-a[0])
 # water face separate semantic node
 pts=path(2.27,1.78,.43);me=bpy.data.meshes.new('water mesh');me.from_pydata([xyz((x,.53,z-.05)) for x,z in pts],[],[tuple(reversed(range(len(pts))))]);o=bpy.data.objects.new('water',me);bpy.context.collection.objects.link(o);finish(o,'water',M['water'],'water')
 # spout at rear right
 for h in [.23,.67,1.10]:box('stacked spout stone',(1.7,h,-2.35),(.76,.44,.66),M['stone'],.09)
 box('dark spout opening',(1.7,.94,-1.985),(.33,.22,.03),M['dark'],.025)
 box('stone spout lower lip',(1.7,.80,-1.90),(.45,.09,.39),M['tile'])
 curve('flowing inlet water',[(1.7,.87,-1.8),(1.7,.72,-1.63),(1.7,.54,-1.56)],.07,M['water'],'waterfall')
 for x in [-3.45,3.45]:lamp(x,2.24,back+.15)
 # 004 artwork: only permitted image plane inside modeled substantial frame
 m=mat('supplied landscape mural',(1,1,1));img=bpy.data.images.load(str(REF/'004.png'));img.pack();tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=img;m.node_tree.links.new(tex.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
 m['source_image']=str(REF/'004.png')
 me=bpy.data.meshes.new('mural UV surface');me.from_pydata([xyz((-2.1,1.20,back+.40)),xyz((2.1,1.20,back+.40)),xyz((2.1,2.80,back+.40)),xyz((-2.1,2.80,back+.40))],[],[(0,1,2,3)]);me.uv_layers.new()
 # 941x1672 source -> 4.2:1.6 display: crop vertically without stretching
 vspan=(941/1672)/(4.2/1.6);vlo=.56-vspan/2;vhi=.56+vspan/2
 for l,uv in zip(me.uv_layers.active.data,[(0,vlo),(1,vlo),(1,vhi),(0,vhi)]):l.uv=uv
 o=bpy.data.objects.new('004 framed landscape',me);bpy.context.collection.objects.link(o);finish(o,o.name,m)
 for x in [-2.17,2.17]:box('picture carved side',(x,2.0,back+.46),(.14,1.88,.16),M['gold'])
 for y in [1.13,2.87]:box('picture carved rail',(0,y,back+.46),(4.48,.14,.16),M['gold'])
 # washing furniture beside far left wall; X +/-3 passage stays clear
 for z in [-2.7,-.8,1.10]:
  x=-3.8
  box('wood washing stool seat',(x,.43,z),(.54,.13,.43),M['honey'],.06)
  for dx in [-.18,.18]:box('stool splayed leg',(x+dx,.21,z),(.10,.39,.32),M['wood'])
  # bucket tapered staves, open interior
  for j in range(14):
   a=j*math.tau/14
   o=box('bucket oak stave',(x+.19*math.cos(a),.68,z+.19*math.sin(a)),(.085,.30,.047),M['honey' if j%2 else 'oak'],.015);o.rotation_euler[2]=-a+math.pi/2
  for h in [.57,.79]:ring('bucket metal hoop',(x,h,z),.205,.018,M['iron'])
  cyl('bucket inside bottom',(x,.545,z),.18,.03,M['wood'])
  # side-wall shower bent pipe using actual curves
  curve('shower pipe',[(-4.06,.68,z),(-4.06,1.42,z),(-3.93,1.57,z),(-3.77,1.49,z)],.024,M['iron'])
  box('shower head',(-3.76,1.48,z),(.13,.065,.16),M['iron'],.03)
  box('washing soap shelf',(-4.0,.82,z-.29),(.40,.075,.35),M['honey'])
  for k in range(2):
   cyl('wash bottle',(-3.94,.95,z-.34+k*.12),.045,.19,M['leaf' if k else 'gold'],12)
   cyl('wash bottle pump',(-3.94,1.06,z-.34+k*.12),.025,.035,M['iron'],12)
 # cloth entry low visual interference upper only, sides beyond opening
 for x in [-1.0,1.0]:box('entry noren pillar',(x,1.25,3.3),(.13,2.5,.16),M['wood'])
 box('entry noren lintel',(0,2.48,3.3),(2.22,.13,.18),M['wood'])
 for x in [-.72,-.24,.24,.72]:
  pts=[]
  for j in range(9):pts.append((x-.23+j*.46/8,1.82+.018*math.sin(j),3.30+.05*math.cos(j)))
  vs=[xyz(p) for p in pts]+[xyz((p[0],2.43,p[2])) for p in pts];fs=[(j,j+1,10+j,9+j) for j in range(8)]
  me=bpy.data.meshes.new('cloth folds');me.from_pydata(vs,[],fs);o=bpy.data.objects.new('indigo entry split curtain',me);bpy.context.collection.objects.link(o);finish(o,o.name,M['navy'],'entry_curtain')
def export(asset,anchors):
 curves=[o for o in bpy.context.scene.objects if o.type in ['CURVE','FONT']]
 if curves:
  bpy.ops.object.select_all(action='DESELECT')
  for o in curves:o.select_set(True)
  bpy.context.view_layer.objects.active=curves[0];bpy.ops.object.convert(target='MESH')
 meshes=[o for o in bpy.context.scene.objects if o.type in ['MESH','CURVE','FONT']]
 parts=[];lo=[1e9]*3;hi=[-1e9]*3;tri=0
 deps=bpy.context.evaluated_depsgraph_get()
 for o in meshes:
  ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();groups={}
  for t in me.loop_triangles:groups.setdefault(t.material_index,[]).append(t)
  for mi,ts in groups.items():
   m=o.data.materials[min(mi,len(o.data.materials)-1)];p=m.node_tree.nodes.get('Principled BSDF');pos=[];nor=[];uv=[]
   for t in ts:
    for vi,li in zip(t.vertices,t.loops):
     v=o.matrix_world@me.vertices[vi].co;n=o.matrix_world.to_3x3()@me.corner_normals[li].vector;n.normalize();v=[v.x,v.z,-v.y];n=[n.x,n.z,-n.y]
     pos+= [round(f,5) for f in v];nor+=[round(f,5) for f in n]
     for k in range(3):lo[k]=min(lo[k],v[k]);hi[k]=max(hi[k],v[k])
     if me.uv_layers.active:uv+=list(me.uv_layers.active.data[li].uv)
   material={'name':m.name,'color':list(p.inputs['Base Color'].default_value)[:3],'roughness':p.inputs['Roughness'].default_value,'metallic':0,'opacity':1}
   if m.get('source_image'):material['texture']='data:image/png;base64,'+base64.b64encode(Path(m['source_image']).read_bytes()).decode()
   part={'name':o.name,'node':o.get('runtime_node','static'),'positions':pos,'normals':nor,'material':material}
   if uv:part['uv']=uv
   parts.append(part);tri+=len(ts)
  ev.to_mesh_clear()
 data={'id':asset,'parts':parts,'anchors':anchors,'bounds':{'min':lo,'max':hi},'triangleCount':tri}
 (OUT/(asset+'.json')).write_text(json.dumps(data,separators=(',',':')))
 bpy.ops.object.select_all(action='DESELECT')
 for o in meshes:o.select_set(True)
 bpy.ops.export_scene.gltf(filepath=str(OUT/(asset+'.glb')),use_selection=True,export_format='GLB',export_apply=True)
 return {'id':asset,'triangleCount':tri,'objects':len(meshes),'materials':len({p['material']['name'] for p in parts}),'bounds':data['bounds'],'anchors':anchors}
def render(asset,detail=False):
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24
 scene.world.color=(.3,.3,.3)
 for loc,power,size in [((1,-3,10),1600,8),((-5,-2,7),1100,6),((3,4,7),1000,5)]:
  bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add(location=(11,-15,13) if not detail else (7,-9,7));cam=bpy.context.object;target=Vector((0,0,1) if not detail else (0,.2,.7));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=16 if not detail else 10.5;scene.camera=cam
 scene.render.resolution_x=1400;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
 scene.view_settings.view_transform='AgX';scene.view_settings.exposure=-.45;scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/(asset+('_detail' if detail else '_render')+'.png'))
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(asset+'.blend')))
 bpy.ops.render.render(write_still=True)
allm=[]
for name,w,d,kind in [('home_shell',11.5,9.3,'home'),('cafe_shell',10.8,8.4,'cafe'),('arcade_shell',10.8,8.4,'arcade'),('bath_interior',9,8.5,'bath')]:
 if '--' in sys.argv and name not in sys.argv[sys.argv.index('--')+1:]:continue
 reset()
 if kind=='bath':bath()
 else:shell(w,d,kind)
 anchors={'floor':[0,0,0]}
 if kind=='bath':anchors.update({'water':[0,.53,-.05],'entry':[0,0,3.3],'seat0':[-1.2,.55,-1.3],'seat1':[1.2,.55,-1.3],'seat2':[-1.2,.55,1.3],'seat3':[1.2,.55,1.3]})
 if kind=='home':anchors['window']=[-2.3,2,-4.2]
 allm.append(export(name,anchors));render(name)
 if kind=='bath':render(name,True)
if '--' in sys.argv and (OUT/'manifest.json').exists():
 old=json.loads((OUT/'manifest.json').read_text());allm=[a for a in old['assets'] if a['id'] not in {x['id'] for x in allm}]+allm
(OUT/'manifest.json').write_text(json.dumps({'assets':allm,'method':'Original Blender bpy modeled meshes, modifiers and curves; no structural image boards. Only user supplied mural 004 is textured.','referencesViewed':['001','002','003','004','010','011','012','013'],'adoption':{'home':'001 warm timber plank floor, timber borders and curved brackets; no floor mascot embossed to preserve existing furniture','cafe':'002/011 warm wood shell and lanterns, deliberately no extra luxury furnishings','arcade':'010 checker tiled floor, low checker wall band, red trim, cornice light and timber columns; 003 sci-fi style intentionally not mixed','bath':'012 plank walls, stone rounded basin, washing stools buckets shower fixtures lanterns and separate water; 004 4.2x1.6 landscape UV crop preserving pixel aspect; 013 split indigo curtain'},'deviations':['No ceiling/front wall/right wall to preserve game camera visibility','Furniture remains runtime-owned and is absent from shell renders','Bath room and basin dimensions follow existing game coordinates rather than guide dimensions','Steam and dynamic lighting are runtime additions','No NPCs modeled in this interiors scope']},indent=2))

