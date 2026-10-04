from pathlib import Path
from PIL import Image
import re,json,base64,hashlib
root=Path(__file__).parent
j=json.loads((root/'assets/characters.js').read_text().split('=',1)[1].rstrip(';\n'))
expected=['idle','walk','walk2','sit','sleep','eat','read','windowlook','clean','garden','dance','chat']
r={'type':'static file and image inspection; not browser rendering','files':[]}
for who in ['denden','pink']:
 assert sorted(j[who])==sorted(expected)
 for pose in expected:
  p=root/'assets'/who/(pose+'.png'); b=p.read_bytes(); assert base64.b64decode(j[who][pose].split(',')[1])==b
  im=Image.open(p);assert im.mode=='RGBA' and im.size==(256,256);assert set(im.getchannel('A').getdata())<=set([0,255])
  bbox=im.getbbox();assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<256 and bbox[3]<=236
  r['files'].append({'character':who,'pose':pose,'size':list(im.size),'alphaBounds':bbox,'sha256':hashlib.sha256(b).hexdigest()})
h=(root/'hidamari-standalone.html').read_text()
r['standaloneBytes']=(root/'hidamari-standalone.html').stat().st_size
r['inlineScripts']=len(re.findall('<script>',h)); r['externalScriptTags']=re.findall(r'<script[^>]+src=',h);r['externalStylesheetTags']=re.findall(r'<link[^>]+stylesheet',h)
r['embeddedDataImages']=h.count('data:image/png;base64,')
assert r['inlineScripts']==3 and not r['externalScriptTags'] and not r['externalStylesheetTags'] and r['embeddedDataImages']==24
r['finalBrowserVisualQA']='NOT RUN: cloud browser blocked local file/HTTP access; command Chromium could not open a local socket.'
(root/'qa-final-static.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print('PASS:',len(r['files']),'PNG assets; standalone has',r['embeddedDataImages'],'embedded data images')
