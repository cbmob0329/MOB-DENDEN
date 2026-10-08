import os,json,math,hashlib
root=os.path.dirname(__file__)
report=[]
for id in ['gacha','capsule','ufo','race','race_course','kart']:
 d=json.load(open(os.path.join(root,id+'.json'),encoding='utf8'));n=0
 for p in d['parts']:
  assert len(p['positions'])%9==0 and len(p['normals'])==len(p['positions'])
  assert all(math.isfinite(v) for v in p['positions']+p['normals'])
  assert 0<=p['material']['opacity']<=1
  if 'uv' in p:assert len(p['uv'])==len(p['positions'])*2/3
  n+=len(p['positions'])//9
 assert n==d['triangleCount']
 if id=='ufo':
  assert d['anchors']['prizeFloor'][1]==1.05
  assert d['anchors']['chuteCenter']==[-1.225,1.05,.9]
  assert {'roof','glass','claw','finger_0','finger_1','finger_2'}.issubset({p['node'] for p in d['parts']})
 if id=='race':assert {'screen_left','screen_right'}.issubset({p['node'] for p in d['parts']})
 report.append({'id':id,'triangles':n,'parts':len(d['parts']),'glb_bytes':os.path.getsize(os.path.join(root,id+'.glb')),'json_sha256':hashlib.sha256(open(os.path.join(root,id+'.json'),'rb').read()).hexdigest()})
json.dump({'status':'PASS','checks':'finite triangulated geometry, normals/UV lengths, material alpha, counts, screen nodes, UFO exact physics floor/hole and semantic roof/claw nodes','assets':report},open(os.path.join(root,'validation.json'),'w'),indent=2)
print(json.dumps(report))
