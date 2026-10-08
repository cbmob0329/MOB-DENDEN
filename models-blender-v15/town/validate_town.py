from pathlib import Path
import json, math, hashlib
P=Path(__file__).resolve().parent
manifest=json.loads((P/'manifest.json').read_text(encoding='utf8'))
result={'assets':[],'failures':[],'warnings':[]}
for rec in manifest['assets']:
 p=P/rec['json'];d=json.loads(p.read_text(encoding='utf8'));count=0;deg=0;opposed=0;normal_zero=0;groups=set()
 for part in d['parts']:
  pos=part['positions'];norm=part['normals'];assert len(pos)==len(norm) and len(pos)%9==0
  assert all(math.isfinite(x) for x in pos+norm)
  count+=len(pos)//9;groups.add((part['node'],part['material']['name']))
  for i in range(0,len(pos),9):
   a=pos[i:i+3];b=pos[i+3:i+6];c=pos[i+6:i+9]
   u=[b[j]-a[j] for j in range(3)];v=[c[j]-a[j] for j in range(3)]
   cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
   mag=math.sqrt(sum(t*t for t in cross))
   if mag<1e-10:deg+=1;continue
   n=[sum(norm[i+k+j] for k in [0,3,6])/3 for j in range(3)]
   if sum(t*t for t in n)<1e-6:normal_zero+=1
   if sum(cross[j]*n[j] for j in range(3))/mag<-.05:opposed+=1
 assert count==d['triangleCount']==rec['triangleCount']
 if opposed:result['failures'].append(f"{d['id']}: {opposed} triangles have normals opposed to winding")
 if deg:result['warnings'].append(f"{d['id']}: {deg} collapsed UV-sphere pole triangles; visually harmless but optional importer can omit zero-area faces")
 result['assets'].append({'id':d['id'],'triangles':count,'parts':len(d['parts']),'mergedNodeMaterialDraws':len(groups),'zeroAreaTriangles':deg,'opposedNormals':opposed,'zeroNormalsNondegenerate':normal_zero,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert len(manifest['emptyLots'])>=5
assert manifest['rail']['trainOriginY']==.8975
train=json.loads((P/'town_train.json').read_text())
assert abs(train['bounds']['min'][1])<.0001
result['status']='PASS' if not result['failures'] else 'FAIL'
(P/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
