from pathlib import Path
import json, math
from collections import deque
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'design_dimensions.json').read_text())
errors=[]
# Rectangle overlaps and outer-wall limits.
for fl in [1,2]:
 rows=[f for f in m['furniture'] if f['floor']==fl]
 for f in rows:
  x0,y0,x1,y1=f['bounds_xy']
  if not(.2<=x0<x1<=7.8 and .2<=y0<y1<=6.8):errors.append(f'floor {fl} item {f["id"]}: out of bounds')
 for i,a in enumerate(rows):
  for b in rows[i+1:]:
   A=a['bounds_xy'];B=b['bounds_xy']
   if min(A[2],B[2])>max(A[0],B[0]) and min(A[3],B[3])>max(A[1],B[1]):errors.append(f'overlap {a["id"]}/{b["id"]}')
s=m['stair']; assert math.isclose(s['rises']*s['rise'],m['building']['floor_to_floor']);assert math.isclose(2*s['flight_width']+s['divider'],s['bounds'][2]-s['bounds'][0]);assert math.isclose(s['treads_per_flight']*s['tread']+s['landing'],s['bounds'][3]-s['bounds'][1])
# 2D preliminary navigation; height-aware simplification, not Blender physics.
step=.05
results=[]
start={1:(4,0.85),2:(7.2,2.95)}
targets={1:[('左ラック',(1.65,1.7)),('右ラック',(6.35,1.55)),('接客の客側',(1.65,3.15)),('接客の店主側',(1.65,5.1)),('布収納',(1.5,5.5)),('仕立て台',(4.25,5.25)),('姿見',(2.55,1.65)),('階段下',(5.8,3.0))],2:[('ベッド横',(2.65,5.25)),('衣装棚',(4.1,5.55)),('ソファ前',(1.45,1.65)),('ローテーブル横',(2.50,0.90)),('小机前',(4.15,1.75)),('キッチン前',(6.7,1.65))]}
def rect_dist(p,bs):
 x,y=p;x0,y0,x1,y1=bs;return math.hypot(max(x0-x,0,x-x1),max(y0-y,0,y-y1))
for fl in [1,2]:
 obs=[(f['bounds_xy'],.525 if f['height']>=1.05 else .32) for f in m['furniture'] if f['floor']==fl]+[(s['bounds'],.525)]
 def free(i,j):
  x,y=i*step,j*step
  # 1.05m envelope for high parts vs walls. No corridor needs transparent clipping.
  if x<.725-1e-6 or x>7.275+1e-6 or y<.725-1e-6 or y>6.275+1e-6:return False
  return all(rect_dist((x,y),bs)>=r-1e-6 for bs,r in obs)
 src=tuple(round(a/step)for a in start[fl]);seen={src};queue=deque([src])
 assert free(*src)
 while queue:
  i,j=queue.popleft()
  for ni,nj in [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]:
   if (ni,nj) not in seen and free(ni,nj):seen.add((ni,nj));queue.append((ni,nj))
 for label,pos in targets[fl]:
  dst=tuple(round(a/step)for a in pos);ok=dst in seen
  results.append({'floor':fl,'target':label,'point_xy':pos,'connected':ok})
  if not ok:errors.append(f'floor{fl} route {label} blocked')
report={'kind':'design-only 2D geometric precheck','grid_m':step,'wall_and_tall_furniture_envelope_radius_m':.525,'low_furniture_collision_radius_m':.32,'stair_arithmetic':True,'furniture_overlaps':False if not any('overlap' in x for x in errors) else True,'routes':results,'errors':errors,'limitations':['Does not check posed mesh, dynamic ears, skirt, needle or 3D head clearance.','Stairs traversability and actual furniture contact must be checked in Blender after modeling.']}
(root/'qa/design_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
