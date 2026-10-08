"""Lossless runtime cleanup: remove zero-area triangles from evaluated exports.
No visible surface, normal, material, source object or Blender render changes.
"""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
m=json.loads((P/'manifest.json').read_text(encoding='utf8'));removed=0
for rec in m['assets']:
 p=P/rec['json'];d=json.loads(p.read_text(encoding='utf8'));count=0
 for part in d['parts']:
  pos=part['positions'];norm=part['normals'];pp=[];nn=[]
  for i in range(0,len(pos),9):
   a=pos[i:i+3];b=pos[i+3:i+6];c=pos[i+6:i+9]
   u=[b[j]-a[j] for j in range(3)];v=[c[j]-a[j] for j in range(3)]
   q=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
   if sum(x*x for x in q)<1e-20:removed+=1;continue
   pp.extend(pos[i:i+9]);nn.extend(norm[i:i+9])
  part['positions']=pp;part['normals']=nn;count+=len(pp)//9
 d['triangleCount']=count;rec['triangleCount']=count;p.write_text(json.dumps(d,separators=(',',':')),encoding='utf8')
m['triangleCount']=sum(a['triangleCount'] for a in m['assets']);m['runtimeOptimization']='Zero-area pole/bevel triangles removed without altering visible geometry; source GLB retains editable evaluated geometry.'
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
print('Removed',removed,'zero-area triangles; visible triangles',m['triangleCount'])
