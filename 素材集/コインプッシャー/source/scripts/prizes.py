"""Chunky low-poly coin-pusher collectibles. Blender 4.3+; meters; +Z up.

build_prizes() returns {asset_id: [root_empty, meshes..., lid_pivot...] }.
Every asset is centered at world origin with its lowest point at Z=0.
Move/export its ROOT as a hierarchy. Chest lids rotate around local X; -105° opens.
No modifiers, curve geometry, external textures, cameras, or lights are retained.
"""
import bpy, math
from mathutils import Vector

P = 'MOBP_'

def _mat(name, color, metallic=0.0, roughness=.36):
    name=P+name
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metallic
    bs.inputs['Roughness'].default_value=roughness
    return m

def _mesh(name, verts, faces, mat, parent=None, smooth=False):
    me=bpy.data.meshes.new(P+name+'_mesh'); me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(P+name,me); bpy.context.collection.objects.link(ob)
    if mat: me.materials.append(mat)
    if parent: ob.parent=parent
    for p in me.polygons:p.use_smooth=smooth
    return ob

def _root(name, reward=None):
    ob=bpy.data.objects.new(P+name+'_ROOT',None); bpy.context.collection.objects.link(ob)
    ob.empty_display_type='PLAIN_AXES'; ob.empty_display_size=.014
    ob['asset_id']=name; ob['is_asset_root']=True; ob['units']='meters'; ob['origin']='bottom center'
    if reward is not None: ob['reward']=reward; ob['reward_coins']=reward
    return ob

def _apply(ob):
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active=ob
    for mod in list(ob.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    # All non-root mesh origins sit at their parent's origin; their vertices carry placement.
    if ob.location.length:
        delta=ob.location.copy()
        for v in ob.data.vertices:v.co+=delta
        ob.location=(0,0,0)
    ob.select_set(False)
    return ob

def _cube(name, dims, loc, mat, parent, bevel=.002, segments=1):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    ob=bpy.context.object; ob.name=P+name; ob.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mo=ob.modifiers.new('Soft manufactured edges','BEVEL'); mo.width=bevel;mo.segments=segments
    ob.data.materials.append(mat)
    _apply(ob); ob.parent=parent
    return ob

def _lathe(name, rings, n, mat, parent, cap=True, phase=0., smooth=True):
    vs=[(r*math.cos(2*math.pi*i/n+phase),r*math.sin(2*math.pi*i/n+phase),z) for r,z in rings for i in range(n)]
    fs=[]
    for j in range(len(rings)-1):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    if cap:fs.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))])
    ob=_mesh(name,vs,fs,mat,parent,smooth)
    if cap:
        ob.data.polygons[-1].use_smooth=False; ob.data.polygons[-2].use_smooth=False
    return ob

def _tube(name, points, radius, sides, mat, parent, closed=False):
    vs=[]; n=len(points)
    for i,pt in enumerate(points):
        p=Vector(pt); tangent=Vector(points[(i+1)%n])-Vector(points[(i-1)%n]) if closed else (Vector(points[min(n-1,i+1)])-Vector(points[max(0,i-1)]))
        tangent.normalize(); ref=Vector((0,0,1))
        if abs(tangent.dot(ref))>.95:ref=Vector((0,1,0))
        a=tangent.cross(ref).normalized();b=tangent.cross(a).normalized()
        vs.extend(tuple(p+radius*(a*math.cos(2*math.pi*k/sides)+b*math.sin(2*math.pi*k/sides))) for k in range(sides))
    fs=[]
    for i in range(n if closed else n-1):
        for k in range(sides):fs.append((i*sides+k,i*sides+(k+1)%sides,((i+1)%n)*sides+(k+1)%sides,((i+1)%n)*sides+k))
    if not closed:fs.extend([tuple(reversed(range(sides))),tuple((n-1)*sides+k for k in range(sides))])
    return _mesh(name,vs,fs,mat,parent,True)

def _letter(letter, finish, mat, side):
    key='letter_'+letter+'_'+finish; root=_root(key,100)
    cu=bpy.data.curves.new(P+key+'_font','FONT');cu.body=letter;cu.align_x='CENTER';cu.size=1
    try:cu.font=bpy.data.fonts.load('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',check_existing=True)
    except RuntimeError:pass
    cu.extrude=.095;cu.bevel_depth=.023;cu.bevel_resolution=2;cu.resolution_u=4
    ob=bpy.data.objects.new(P+key,cu);bpy.context.collection.objects.link(ob)
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
    bpy.ops.object.convert(target='MESH');ob=bpy.context.object
    # Font's Y becomes upright Z. The letter's front points toward -Y.
    vertices=[Vector((v.co.x,-v.co.z,v.co.y)) for v in ob.data.vertices]
    zmin=min(v.z for v in vertices); zmax=max(v.z for v in vertices)
    xmin=min(v.x for v in vertices); xmax=max(v.x for v in vertices)
    ymin=min(v.y for v in vertices); ymax=max(v.y for v in vertices)
    s=.085/(zmax-zmin)
    for v,co in zip(ob.data.vertices,vertices):v.co=((co.x-(xmin+xmax)/2)*s,(co.y-(ymin+ymax)/2)*s,(co.z-zmin)*s)
    ob.data.materials.append(mat);ob.data.materials.append(side);ob.data.update()
    for p in ob.data.polygons:
        p.material_index=0 if abs(p.normal.y)>.8 else 1
        p.use_smooth=abs(p.normal.y)<.99
    ob.parent=root;ob['reward']=100;ob['reward_coins']=100;ob['glyph']=letter;ob['finish']=finish
    return key,[root,ob]

def _coin(gold,light):
    key='coin'; root=_root(key,1)
    # 14 sides / 4 edge rings: 108 triangles including filled faces.
    ob=_lathe('coin_body',[(.0246,0),(.026,.0012),(.026,.0038),(.0246,.00488)],14,gold,root)
    ob['radius_m']=.026;ob['thickness_m']=.005
    # A near-zero relief face in the metal, intentionally without sidewalls.
    # All glyphs are simple meshes: 10 + 12 + 18 = 40 triangles. Total = 148.
    h=.010; base=-h/2; z=.005
    def poly(name,xy):return _mesh(name,[(x,y,z) for x,y in xy],[tuple(range(len(xy)))],light,root)
    m=[(-.019,base),(-.019,base+h),(-.0167,base+h),(-.0139,base+.0052),(-.0111,base+h),(-.0088,base+h),(-.0088,base),(-.011,base),(-.011,base+.0064),(-.0139,base+.0018),(-.0168,base+.0064),(-.0168,base)]
    mo=poly('coin_M_relief',m)
    # Eight-corner outer ring and four-corner aperture; four sides use three triangles each.
    outer=[(-.005,base+.002),(-.003,base),( .002,base),(.004,base+.002),(.004,base+.008),(.002,base+h),(-.003,base+h),(-.005,base+.008)]
    inner=[(-.0027,base+.0022),(.0017,base+.0022),(.0017,base+.0078),(-.0027,base+.0078)]
    vs=outer+inner; faces=[]
    # Bottom, right, top, left bands; each four/five-point polygon triangulates predictably.
    faces=[(0,1,2,9,8),(2,3,4,10,9),(4,5,6,11,10),(6,7,0,8,11)]
    oo=_mesh('coin_O_relief',[(x,y,z) for x,y in vs],faces,light,root)
    # B is assembled from a stem and two angular hollow bowls (18 triangles).
    bverts=[];bfaces=[]
    def bpoly(coords):
        start=len(bverts);bverts.extend((x,y,z) for x,y in coords);bfaces.append(tuple(range(start,len(bverts))))
    bpoly([(.008,base),(.0102,base),(.0102,base+h),(.008,base+h)])
    for by in (base,base+.005):
        bpoly([(.0102,by),(.016,by),(.0182,by+.0015),(.0182,by+.0035),(.016,by+.005),(.0102,by+.005),(.0102,by+.0032),(.0155,by+.0032),(.0155,by+.0018),(.0102,by+.0018)])
    bo=_mesh('coin_B_relief',bverts,bfaces,light,root)
    root['face_detail']='MOB shallow mesh relief';root['nominal_triangle_budget']=160
    return key,[root,ob,mo,oo,bo]

def _dorayaki(baked,edge,filling,toast):
    key='dorayaki';root=_root(key,80);obs=[root]
    lower=_lathe('dorayaki_lower_pancake',[(.032,0),(.048,.003),(.054,.010),(.053,.015),(.047,.020)],20,edge,root)
    lower.data.materials.append(baked)
    for p in lower.data.polygons:
        if p.center.z<.010:p.material_index=1
    obs.append(lower)
    obs.append(_lathe('dorayaki_redbean_filling',[(.046,.017),(.052,.020),(.050,.025),(.045,.027)],20,filling,root))
    upper=_lathe('dorayaki_upper_pancake',[(.047,.024),(.054,.029),(.051,.038),(.043,.045),(.026,.050),(.009,.052)],20,baked,root)
    upper.data.materials.append(edge)
    for p in upper.data.polygons:
        if p.center.z<.032:p.material_index=1
    obs.append(upper)
    for i,(x,y,r) in enumerate([(-.016,.011,.0045),(.012,.019,.0035),(.024,-.006,.003),(-.020,-.021,.003)]):
        # Small toasted freckles follow the dome and are raised only 0.1 mm.
        xy=[]
        for j in range(7):
            px=x+r*math.cos(2*math.pi*j/7);py=y+r*.7*math.sin(2*math.pi*j/7);rr=math.hypot(px,py)
            if rr<.009:zz=.052
            elif rr<.026:zz=.052-(rr-.009)/.017*.002
            elif rr<.043:zz=.050-(rr-.026)/.017*.005
            else:zz=.045-(rr-.043)/.008*.007
            xy.append((px,py,zz+.00022))
        obs.append(_mesh('dorayaki_toast_'+str(i),xy,[tuple(range(7))],toast,root))
    root['reward']=80;root['reward_coins']=80
    return key,obs

def _bag(cloth,shade,rope,gold):
    key='coin_bag';root=_root(key);obs=[root]
    rings=[(.018,0),(.033,.006),(.043,.025),(.044,.045),(.035,.064),(.018,.077),(.017,.083),(.024,.094)]
    body=_lathe('coin_bag_cloth',rings,16,cloth,root,False,phase=math.pi/16)
    # Organic compressed sack: broad cheeks, a pinched neck, and gentle pleats.
    for v in body.data.vertices:
        a=math.atan2(v.co.y,v.co.x);z=v.co.z
        if z>.063:v.co.x*=1+.06*math.cos(a*8);v.co.y*=1+.06*math.cos(a*8)
        else:v.co.y*=.82
    body.data.update();obs.append(body)
    obs.append(_mesh('coin_bag_bottom',[(.018*math.cos(i*2*math.pi/16),.018*.82*math.sin(i*2*math.pi/16),0) for i in range(16)],[tuple(reversed(range(16)))],cloth,root))
    # Dark open mouth makes the protruding gold coins read clearly.
    obs.append(_lathe('coin_bag_opening',[(.019,.090),(.019,.0905)],16,shade,root))
    points=[(.019*math.cos(2*math.pi*i/16),.019*math.sin(2*math.pi*i/16),.0795) for i in range(16)]
    obs.append(_tube('coin_bag_drawstring',points,.0025,5,rope,root,True))
    for side in (-1,1):
        pts=[(side*(.002+.011*(1-math.cos(2*math.pi*i/9))),-.020-.006*math.sin(2*math.pi*i/9),.080+.008*math.sin(2*math.pi*i/9)) for i in range(9)]
        obs.append(_tube('coin_bag_bow_'+str(side),pts,.002,5,rope,root,True))
    obs.append(_tube('coin_bag_tie_tail_L',[(-.003,-.021,.079),(-.008,-.027,.068),(-.013,-.027,.064)],.0022,5,rope,root))
    obs.append(_tube('coin_bag_tie_tail_R',[(.003,-.022,.079),(.012,-.025,.066),(.010,-.023,.061)],.0022,5,rope,root))
    # Three peeking coins share the same restrained gold finish.
    for i,(x,y,z,angle) in enumerate([(-.012,.0,.091,-.28),(.004,.004,.094,.18),(.012,-.003,.090,.4)]):
        coin=_lathe('coin_bag_gold_'+str(i),[(.010,0),(.011,.0007),(.011,.0028),(.010,.0035)],12,gold,root)
        for v in coin.data.vertices:
            p=v.co.copy();v.co=(p.x+x,p.y*math.cos(angle)-p.z*math.sin(angle)+y,p.y*math.sin(angle)+p.z*math.cos(angle)+z)
        obs.append(coin)
    # A simple golden circular sewn badge; no text or unrelated branding.
    vs=[(.013*math.cos(2*math.pi*i/12),-.0368,.037+.013*math.sin(2*math.pi*i/12)) for i in range(12)]
    obs.append(_mesh('coin_bag_round_badge',vs,[tuple(reversed(range(12)))],gold,root))
    return key,obs

def _arch_shell(name,x0,x1,ydepth,zbase,rise,thick,n,mat,parent):
    # Half-elliptical lid profile, extruded in X with a thin inner shell.
    profile=[(-ydepth/2*math.cos(math.pi*i/n),zbase+rise*math.sin(math.pi*i/n)) for i in range(n+1)]
    inner=[(y*.91,z-thick) for y,z in profile]
    vs=[]
    for x in (x0,x1):
        vs.extend((x,y,z) for y,z in profile);vs.extend((x,y,z) for y,z in inner)
    m=n+1;fs=[]
    for i in range(n):
        fs.extend([(i,i+1,2*m+i+1,2*m+i),(m+i,3*m+i,3*m+i+1,m+i+1)])
    for i in (0,n):fs.append((i,2*m+i,3*m+i,m+i))
    for b in (0,2*m):
        for i in range(n):fs.append((b+i,b+m+i,b+m+i+1,b+i+1))
    return _mesh(name,vs,fs,mat,parent)

def _chest(kind,wood,wooddark,metal,metaldark,inner,goldbody=None):
    key=kind+'_chest';root=_root(key);obs=[root]
    w=.12;d=.084;h=.049;t=.006
    bodymat=wood if kind=='wood' else (goldbody or metal)
    edgemat=metal if kind=='wood' else metaldark
    # Open box: five actual beveled panels, dark interior revealed on opening.
    obs.append(_cube(key+'_bottom',(w-.006,d-.006,.009),(0,0,.0045),inner,root,.002,1))
    obs.append(_cube(key+'_front',(w,t,h-.004),(0,-d/2+t/2,(h+.004)/2),bodymat,root,.002,1))
    obs.append(_cube(key+'_back',(w,t,h-.004),(0,d/2-t/2,(h+.004)/2),bodymat,root,.002,1))
    obs.append(_cube(key+'_left',(t,d-t*2,h-.004),(-w/2+t/2,0,(h+.004)/2),bodymat,root,.002,1))
    obs.append(_cube(key+'_right',(t,d-t*2,h-.004),(w/2-t/2,0,(h+.004)/2),bodymat,root,.002,1))
    # Two broad straps; front and back panels, with their curved lid extensions.
    for x in (-.039,.039):
        for y in (-d/2-.0006,d/2+.0006):
            obs.append(_cube(key+'_body_strap_'+str(x)+'_'+str(y),(.010,.0024,h-.006),(x,y,.026),edgemat,root,.0009,1))
    # Lower band strengthens the silhouette and keeps the chests toy-like.
    for y in (-d/2-.0004,d/2+.0004):
        obs.append(_cube(key+'_lower_rail_'+str(y),(w+.002,.003,.005),(0,y,.007),edgemat,root,.0008,1))
    if kind=='wood':
        # Very shallow dark joints suggest wide hand-crafted planks without tiny grain.
        for x in (-.019,.018):
            obs.append(_cube(key+'_plank_joint_'+str(x),(.0009,.00035,.032),(x,-d/2-.002,.030),wooddark,root,0))
    pivot=bpy.data.objects.new(P+key+'_LID_PIVOT',None);bpy.context.collection.objects.link(pivot)
    pivot.parent=root;pivot.location=(0,d/2,h);pivot.empty_display_type='SINGLE_ARROW';pivot.empty_display_size=.015
    pivot['pivot_role']='lid hinge';pivot['open_rotation_x_degrees']=-105.;pivot['closed_rotation_x_degrees']=0.
    obs.append(pivot)
    # Objects are built in root coordinates, then shifted to pivot-local coordinates.
    lid=_arch_shell(key+'_arched_lid',-.061,.061,d+.003,h,.032,.005,10,bodymat,pivot)
    obs.append(lid)
    for x in (-.039,.039):
        obs.append(_arch_shell(key+'_lid_band_'+str(x),x-.005,x+.005,d+.005,h+.0014,.033,.0024,10,edgemat,pivot))
    # Solid wooden/golden semicircular end panels, with broad beveled-looking edge bands.
    for side in (-1,1):
        x=side*.0607
        prof=[(x,-(d+.003)/2*math.cos(math.pi*i/10),h+.032*math.sin(math.pi*i/10)) for i in range(11)]
        obs.append(_mesh(key+'_lid_end_'+str(side),prof,[tuple(range(11))],bodymat,pivot))
    # Front latch hangs from the moving lid; latch keeper stays on the body.
    latch=_cube(key+'_lid_latch',(.016,.005,.020),(0,-d/2-.004,h-.005),edgemat,pivot,.002,1);obs.append(latch)
    obs.append(_cube(key+'_latch_keeper',(.010,.007,.010),(0,-d/2-.005,.033),metaldark,root,.0015,1))
    obs.append(_cube(key+'_key_slot',(.0025,.0006,.004),(0,-d/2-.0088,.033),inner,root,.0005,1))
    # Round-looking square rivets, grouped on the two front straps.
    for x in (-.039,.039):
        for z in (.015,.040):
            obs.append(_cube(key+'_rivet_'+str(x)+'_'+str(z),(.0045,.002,.0045),(x,-d/2-.0026,z),metal,root,.001,1))
    for ob in obs:
        if ob.parent==pivot and ob.type=='MESH':
            for v in ob.data.vertices:v.co-=Vector(pivot.location)
    return key,obs

def _triangles(ob):
    if ob.type!='MESH':return 0
    ob.data.calc_loop_triangles();return len(ob.data.loop_triangles)

def build_prizes():
    gold=_mat('warm_gold',(.86,.46,.065),.72,.26)
    brightgold=_mat('chest_bright_yellow_gold',(1.0,.78,.025),.32,.30)
    light=_mat('coin_relief_gold',(1.0,.73,.22),.66,.28)
    bronze=_mat('antique_gold_shadow',(.36,.15,.032),.58,.36)
    wood=_mat('honey_wood',(.43,.18,.053),.05,.48)
    wooddark=_mat('plank_grooves',(.16,.055,.018),0,.6)
    inner=_mat('chest_interior',(.085,.038,.019),0,.6)
    baked=_mat('dorayaki_caramel',(.74,.34,.095),0,.63)
    edge=_mat('dorayaki_soft_edge',(1.,.70,.34),0,.7)
    filling=_mat('dorayaki_redbean',(.20,.055,.045),0,.62)
    toast=_mat('dorayaki_toast',(.45,.15,.031),0,.7)
    cloth=_mat('bag_canvas',(.75,.43,.15),0,.76)
    clothdark=_mat('bag_inner',(.19,.073,.018),0,.85)
    rope=_mat('red_drawstring',(.56,.032,.027),0,.65)
    assets={}
    colors={'red':((.86,.045,.050),(.53,.015,.028)),'blue':((.040,.34,.94),(.015,.12,.55)),'green':((.045,.68,.26),(.015,.34,.10))}
    for finish,(front,side) in colors.items():
        fm=_mat('letter_'+finish,front,.12,.3);sm=_mat('letter_'+finish+'_edge',side,.15,.32)
        for letter in 'MOB':
            k,v=_letter(letter,finish,fm,sm);assets[k]=v
    for result in [_coin(gold,light),_dorayaki(baked,edge,filling,toast),_bag(cloth,clothdark,rope,gold),_chest('wood',wood,wooddark,gold,bronze,inner),_chest('gold',wood,wooddark,gold,bronze,inner,brightgold)]:assets[result[0]]=result[1]
    for key,obs in assets.items():
        count=sum(_triangles(ob) for ob in obs)
        obs[0]['triangle_count']=count
        obs[0]['asset_category']='prize' if key!='coin' else 'coin'
        for ob in obs:
            ob['asset_id']=key
            if ob.type=='MESH':ob['triangle_count']=_triangles(ob)
        if count>=2000:raise RuntimeError(f'{key}: {count} triangles exceeds prize budget')
        if key=='coin' and count>=160:raise RuntimeError(f'Coin triangle budget exceeded: {count}')
    return assets
