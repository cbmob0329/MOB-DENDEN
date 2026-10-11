import bpy,os,json,struct
ROOT=os.path.dirname(os.path.abspath(__file__));bpy.ops.wm.open_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend')
for o in bpy.data.objects:
 if o.name.endswith('_Coral'):o.name=o.name[:-6]+'_Blue'
ma=bpy.data.materials.get('Accent • watermelon coral')
if ma:ma.name='Accent • deep blue'
# Match the hidden convenience prize library to the separately delivered corrected gold chest.
m=bpy.data.materials.new('MOBP_chest_bright_yellow_gold');m.use_nodes=True;m.diffuse_color=(1,.78,.025,1);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(1,.78,.025,1);p.inputs['Metallic'].default_value=.32;p.inputs['Roughness'].default_value=.30
for o in bpy.data.objects:
 if o.type=='MESH' and o.get('asset_id')=='gold_chest':
  for slot in o.material_slots:
   if slot.material and slot.material.name=='MOBP_warm_gold':slot.link='OBJECT';slot.material=m
# A stored default with clean blended glass; glTF alpha remains .065.
bpy.data.materials['Glass • clear front'].surface_render_method='BLENDED'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/MOB_CHILL_LIFE_coin_pusher.blend')
# GLB nodes are index-addressed, so canonicalizing display names preserves geometry, hierarchy and channels.
for fn in ['cabinet_blue','two_cabinets']:
 path=ROOT+'/exports/'+fn+'.glb';b=open(path,'rb').read();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n]);tail=b[20+n:]
 for key in ['nodes','meshes','materials','animations']:
  for item in j.get(key,[]):
   if 'name' in item:
    item['name']=item['name'].replace('_Coral','' if fn=='cabinet_blue' else '_Blue').replace('watermelon coral','deep blue')
 raw=json.dumps(j,separators=(',',':'),ensure_ascii=False).encode();raw+=b' '*((-len(raw))%4);out=struct.pack('<4sII',b'glTF',2,20+len(raw)+len(tail))+struct.pack('<I4s',len(raw),b'JSON')+raw+tail;open(path,'wb').write(out)
manifest=json.load(open(ROOT+'/assets_manifest.json'));manifest['node_naming']={'standalone_cabinets':'Both use canonical unsuffixed node names, e.g. PusherPlate_MOVING, Anchor_PrizeRecovery','combined_and_blend':'Red canonical; blue suffixed _Blue'};json.dump(manifest,open(ROOT+'/assets_manifest.json','w'),ensure_ascii=False,indent=2)
print('NORMALIZATION_COMPLETE')
