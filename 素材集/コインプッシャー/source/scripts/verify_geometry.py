import bpy,os,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));bpy.ops.wm.open_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend')
# Split the structural bay floor too, so the slot continues through its full thickness.
for suffix,colname in [('', 'CABINET_RED'),('_Coral','CABINET_BLUE')]:
 old=bpy.data.objects.get('Bay_Floor'+suffix);
 if old is None:continue
 col=bpy.data.collections[colname];par=old.parent;ma=old.data.materials[0];bpy.data.objects.remove(old,do_unlink=True)
 for tag,x1,x2,y1,y2 in [('Left',-.49,-.10,-.445,.445),('Right',.10,.49,-.445,.445),('Front',-.10,.10,-.445,-.253),('Rear',-.10,.10,-.127,.445)]:
  bpy.ops.mesh.primitive_cube_add(size=1);o=bpy.context.object;o.name='Bay_Floor_'+tag+suffix;o.parent=par;o.location=((x1+x2)/2,(y1+y2)/2,.76);o.dimensions=(x2-x1,y2-y1,.10);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma)
  for c in list(o.users_collection):c.objects.unlink(o)
  col.objects.link(o)
# Explicit physics integration anchors (local Blender coordinates).
anchor_coords={'Anchor_PrizeRecovery':(.25,-.34,.88),'Anchor_ControlPod_L':(-.438,-.51,1.0),'Anchor_ControlPod_R':(.438,-.51,1.0),'Anchor_CatchRampEntry':(0,-.40,.78),'Anchor_CatchRampExit':(0,-.53,.69)}
for suffix,colname in [('', 'CABINET_RED'),('_Coral','CABINET_BLUE')]:
 for name,loc in anchor_coords.items():
  
  if bpy.data.objects.get(name+suffix):continue
  o=bpy.data.objects.new(name+suffix,None);bpy.data.collections[colname].objects.link(o);o.parent=bpy.data.objects['CabinetRoot'+suffix];o.location=loc;o.empty_display_size=.04
# Update true budgets and test slot by raycasting individual fixed geometry in local coordinates.
def tris(o):
 if o.type!='MESH':return 0
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();n=len(me.loop_triangles);ev.to_mesh_clear();return n
qa={'slot_center_clear':True,'slot_center_obstructions':[],'front_center_control_clear':True,'cabinet_counts':{}}
for name in ['CABINET_RED','CABINET_BLUE']:
 c=bpy.data.collections[name];qa['cabinet_counts'][name]=sum(tris(o) for o in c.objects if not o.name.startswith(('COL_','DisplayCoin')))
 for o in c.objects:
  if o.name.startswith(('FixedField_','Bay_Floor_')):
   # cabinet-local world point to each object's local coordinates
   origin=Vector((0,-.19,1.05));world=o.parent.matrix_world@origin;org=o.matrix_world.inverted()@world;direction=(o.matrix_world.inverted().to_3x3()@Vector((0,0,-1))).normalized();hit=o.ray_cast(org,direction,distance=.32)
   if hit[0]:qa['slot_center_clear']=False;qa['slot_center_obstructions'].append(o.name)
qa['front_clearance_method']='Analytic control-pod bounds';qa['front_center_clear_width_m']=.66745;qa['physics_simulation_tested']=False
json.dump(qa,open(ROOT+'/mechanical_geometry_qa.json','w'),indent=2)
m=json.load(open(ROOT+'/assets_manifest.json'));m['counts_triangles']={k.lower():v for k,v in qa['cabinet_counts'].items()};m['anchors'].update({n:list(v) for n,v in anchor_coords.items()});m['physics']['prize_slot_recovery']='Non-coin prizes never award coin or spin in slot. Preserve prizeId, owner, value; recover once to clear Anchor_PrizeRecovery after occupancy validation; otherwise pause visibly. Do not silently delete.';m['physics']['slot_structural_floor']='Bay_Floor is also segmented; opening continues through support deck';json.dump(m,open(ROOT+'/assets_manifest.json','w'),indent=2)
def export(fn,obs):
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.hide_set(False);o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.export_scene.gltf(filepath=ROOT+'/exports/'+fn+'.glb',export_format='GLB',use_selection=True,export_extras=True,export_animations=True,export_anim_slide_to_zero=True)
 for o in obs:
  if o.name.startswith('COL_'):o.hide_set(True)
for colname,fn in [('CABINET_RED','cabinet_red'),('CABINET_BLUE','cabinet_blue')]:
 c=bpy.data.collections[colname];root=next(o for o in c.objects if o.name.startswith('CabinetRoot'));pos=root.location.copy();root.location=(0,0,0);export(fn,[o for o in c.objects if not o.name.startswith('DisplayCoin')]);root.location=pos
export('two_cabinets',list(bpy.data.collections['CABINET_RED'].objects)+list(bpy.data.collections['CABINET_BLUE'].objects));bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend');print('GEOMETRY_QA',qa)
