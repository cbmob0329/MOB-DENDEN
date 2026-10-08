import json, math, hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
out=[]
for name,width,depth in [('home_shell',11.5,9.3),('cafe_shell',10.8,8.4),('arcade_shell',10.8,8.4),('bath_interior',9,8.5)]:
 data=json.loads((root/(name+'.json')).read_text())
 assert data['id']==name
 assert len(data['parts'])>20
 count=0
 for p in data['parts']:
  assert len(p['positions'])==len(p['normals'])
  assert len(p['positions'])%9==0
  assert all(math.isfinite(v) for v in p['positions']+p['normals'])
  count+=len(p['positions'])//9
  if p['node']=='water':
   assert all(abs(y-.53)<.0001 for y in p['positions'][1::3])
   assert all(n>.99 for n in p['normals'][1::3])
  if p['material'].get('texture'):
   assert name=='bath_interior' and '004' in p['name']
   assert len(p['uv'])==len(p['positions'])//3*2
 assert count==data['triangleCount']
 assert data['bounds']['max'][0]-data['bounds']['min'][0] <= width+.015, data['bounds']
 assert data['bounds']['max'][2]-data['bounds']['min'][2] <= depth+.015, data['bounds']
 for ext in ['blend','glb']:
  p=root/(name+'.'+ext);assert p.stat().st_size>50000
 out.append({'asset':name,'triangles':count,'bounds':data['bounds'],'sha256':{ext:hashlib.sha256((root/(name+'.'+ext)).read_bytes()).hexdigest() for ext in ['blend','glb','json']}})
(root/'validation.json').write_text(json.dumps({'passed':True,'assets':out},indent=2))
print(json.dumps({'passed':True,'assets':[{'asset':a['asset'],'triangles':a['triangles']} for a in out]}))
