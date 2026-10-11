import bpy,json,math
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(OUT/'shop_spatial_blockout_v01.blend'))
def bounds(name):
 o=bpy.data.objects[name];v=[o.matrix_world@Vector(p)for p in o.bound_box];return [[min(p[i]for p in v)for i in range(3)],[max(p[i]for p in v)for i in range(3)]]
def close(a,b):return abs(a-b)<1e-5
checks={}
checks['lower_flight_has_7_treads']=all(f'Lower_tread_{i}'in bpy.data.objects for i in range(1,8))
checks['upper_flight_has_7_treads']=all(f'Upper_tread_{i}'in bpy.data.objects for i in range(1,8))
checks['half_landing_height_1_3']=close(bounds('Half_landing')[1][2],1.3)
checks['upper_floor_height_2_6']=close(bounds('Floor_02_front')[1][2],2.6)
checks['rise_height_0_1625']=all(close(bounds(f'Lower_tread_{i}')[1][2],i*.1625)for i in range(1,8)) and all(close(bounds(f'Upper_tread_{i}')[1][2],1.3+i*.1625)for i in range(1,8))
checks['lower_flies_north']=bounds('Lower_tread_7')[0][1]>bounds('Lower_tread_1')[0][1]
checks['upper_returns_south']=bounds('Upper_tread_7')[0][1]<bounds('Upper_tread_1')[0][1]
checks['clear_flight_width_1_2']=all(close(bounds(n)[1][0]-bounds(n)[0][0],1.2)for n in ['Lower_tread_1','Upper_tread_1'])
checks['floor_01_is_8_by_7']=close(bounds('Floor_01')[1][0]-bounds('Floor_01')[0][0],8) and close(bounds('Floor_01')[1][1]-bounds('Floor_01')[0][1],7)
checks['floor_02_opening_not_filled']=all(not(min(bounds(n)[1][0],7.8)>max(bounds(n)[0][0],5.2)+1e-5 and min(bounds(n)[1][1],6.8)>max(bounds(n)[0][1],3.6)+1e-5)for n in ['Floor_02_front','Floor_02_left','Floor_02_back','Floor_02_right'])
checks['meter_scale']=close(bpy.context.scene.unit_settings.scale_length,1.0)
report={'kind':'Actual Blender 4.3.2 file reopened and geometry checked','checks':checks,'all_pass':all(checks.values()),'object_count':len(bpy.data.objects),'limitations':'Spatial blockout only; no resident mesh or rig, finished materials, full apertures, actual path following, or furniture-contact animation yet.'}
(OUT/'qa/blender_geometry_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
if not report['all_pass']:raise SystemExit(1)
