from pathlib import Path
import base64, json, html, subprocess
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design'
C={'ink':'#282329','muted':'#746971','red':'#C72E4B','pink':'#F8E7EC','gold':'#B88724','lightgold':'#F6E7BF','white':'#FFFEFB','bg':'#F7F4EE','line':'#D8D0C6','blue':'#3D7A95','pale':'#E5F0F4','green':'#538A79','black':'#202025'}
FONT='Noto Sans CJK JP'
class Board:
 def __init__(self,w,h):
  self.w=w;self.h=h;self.e=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',f'<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8" fill="none" stroke="{C["blue"]}" stroke-width="1.3"/></marker></defs>'];self.rect(0,0,w,h,C['bg'])
 def add(self,s):self.e.append(s)
 def rect(self,x,y,w,h,fill='none',stroke='none',sw=1,rx=0,extra=''):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
 def line(self,x1,y1,x2,y2,col=None,sw=2,extra=''):self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col or C["line"]}" stroke-width="{sw}" {extra}/>')
 def text(self,x,y,t,size=28,col=None,weight=400,anchor='start',extra=''):self.add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{col or C["ink"]}" {extra}>{html.escape(t)}</text>')
 def lines(self,x,y,lines,size=28,col=None,gap=None,weight=400):
  for i,l in enumerate(lines):self.text(x,y+i*(gap or size*1.55),l,size,col,weight)
 def circle(self,x,y,r,fill='none',stroke='none',sw=1):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
 def poly(self,pts,fill='none',stroke='none',sw=1):self.add(f'<polygon points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
 def path(self,d,col=None,sw=3,extra=''):self.add(f'<path d="{d}" fill="none" stroke="{col or C["blue"]}" stroke-width="{sw}" {extra}/>')
 def number(self,x,y,n,fill=None):self.circle(x,y,25,fill or C['red']);self.text(x,y+10,str(n),27,'#fff',700,'middle')
 def header(self,num,title,sub):
  self.text(60,70,'SHOP-01  /  RESIDENT-01',22,C['red'],700)
  self.text(60,145,f'{num}  {title}',54,weight=700)
  self.text(60,202,sub,27,C['muted'])
  self.text(self.w-60,70,'設計案 v0.1  |  2026.10.11',22,C['muted'],anchor='end')
 def footer(self,txt):self.line(60,self.h-92,self.w-60,self.h-92);self.text(60,self.h-48,txt,23,C['muted'])
 def save(self,filename):
  p=OUT/f'{filename}.svg';p.write_text('\n'.join(self.e+['</svg>']),encoding='utf-8')
  subprocess.run(['inkscape',str(p),'--export-type=png',f'--export-filename={OUT/f"{filename}.png"}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

# Board 1 keeps the supplied image unchanged and labels the reference facts outside it.
b=Board(2200,1640);b.header('01','元キャラクターの固定条件','添付画像で確認できる形を優先する。側面・背面は、この画像だけでは確定できない。')
ref=next((ROOT/'reference').glob('*.jpeg'));enc=base64.b64encode(ref.read_bytes()).decode()
b.rect(60,252,1140,1140,'#fff',C['line'],2)
b.add(f'<image x="70" y="262" width="1120" height="1120" xlink:href="data:image/jpeg;base64,{enc}"/>')
b.text(70,1450,'原画像をそのまま掲載  /  正面寄りの斜め構図',25,C['muted'])
notes=[('大きく曲がったウサギ耳','二本とも幅広く、先端が丸い。','短い三角耳や猫耳に変えない。'),('黒い顔・口無し・金丸眼鏡','赤い虹彩と白いハイライト。','鼻・牙・口の追加はしない。'),('画像左の大きな赤金リボン','丸い金ボタンと黒いX状の糸。','耳・リボンを左右対称化しない。'),('白・赤・黒・金の重なる衣装','袖と裾のフリル、縫い目、金飾り。','丸い肩章／胸元寄りのRを残す。'),('両手で持つ銀色の縫い針','細長い針穴と尖った先。','剣の鍔や別の武器意匠は加えない。')]
for i,(t,l1,l2) in enumerate(notes):
 y=300+i*193;b.number(1280,y-10,i+1);b.text(1326,y,t,31,weight=700);b.lines(1326,y+53,[l1,l2],27,C['muted'],42)
b.text(1248,1307,'補完案として確認する部分',31,C['red'],700)
b.lines(1248,1360,['背面／厳密な側面／耳の厚み／眼鏡のつる','新しい尻尾・髪型・紋章・名前は足さない。','補完後は前・横・後を並べて確認する。'],27,gap=43)
b.footer('基準画像は一枚のみ。細部の描き込みより、耳・顔・眼鏡・リボン・針のシルエットを先に固定する。');b.save('01_reference_lock')

# Furniture coordinate data is the single source of truth for both plans.
f1=[(1,'衣服ラック 左',(.35,.70,1.05,2.60),1.25,'E'),(2,'衣服ラック 右',(6.95,.70,7.65,2.40),1.25,'W'),(3,'接客カウンター',(.60,3.80,2.70,4.50),.78,'N/S'),(4,'布と道具の収納',(.40,6.10,2.60,6.65),1.55,'S'),(5,'仕立て作業台',(3.60,5.85,4.90,6.65),.76,'S'),(6,'姿見',(2.20,.45,2.90,1.05),1.45,'N')]
f2=[(8,'ベッド',(.55,4.25,2.05,6.45),.42,'E'),(9,'衣装棚',(3.35,6.15,4.85,6.65),1.60,'S'),(10,'ソファ',(.55,2.10,2.35,2.85),.42,'S'),(11,'ローテーブル',(1.10,.60,1.90,1.20),.36,''),(12,'小机',(3.50,.45,4.80,1.15),.72,'N'),(13,'ミニキッチン',(5.80,.40,7.55,1.05),.76,'N')]
manifest={'revision':'0.1','coordinate_system':{'units':'m','up':'Z','front':'Y=0','back':'+Y'},'character':{'height_with_ears':1.4,'collision_diameter':.64,'visual_width_initial':1.05},'building':{'width':8,'depth':7,'wall':.2,'floor_to_floor':2.6,'ceiling_clear':2.4,'eave':5.4,'ridge':6.4,'roof_type':'soft_hipped','door_x':[3.2,4.8],'door_height':1.9},'stair':{'bounds':[5.2,3.6,7.8,6.8],'flight_width':1.2,'divider':.2,'rises':16,'rise':.1625,'treads_per_flight':7,'tread':.3,'landing':1.1},'furniture':[{'id':n,'floor':fl,'label_ja':label,'bounds_xy':list(bounds),'height':h,'use_side':side}for fl,rows in [(1,f1),(2,f2)]for n,label,bounds,h,side in rows]}
(OUT/'design_dimensions.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

# Exterior orthographic design, intentionally not claimed to be a Blender render.
b=Board(2200,1510);b.header('02','二階建て衣装屋の外観案','建物は新規の補完案。白い壁、赤い布ひさし、金の丸ボタンを軸にまとめる。')
s=101; ground=1010
for ox,dep,label in [(150,8,'正面  /  Y=0'),(1240,7,'右側面  /  X=8')]:
 def p(x,z):return ox+x*s,ground-z*s
 def r(x,z,w,h,fill,stroke=C['ink'],sw=2):
  px,py=p(x,z+h);b.rect(px,py,w*s,h*s,fill,stroke,sw)
 r(0,0,dep,5.4,C['white'],C['ink'],4);r(0,0,dep,.16,C['lightgold']);r(0,2.5,dep,.13,C['lightgold']);r(0,5.25,dep,.15,C['gold'])
 if dep==8:
  b.poly([p(-.28,5.4),p(3.1,6.4),p(4.9,6.4),p(8.28,5.4)],C['red'],C['ink'],4)
  for x in [.6,5.4]:
   r(x,.65,2,1.23,'#DDE9EB',C['gold'],5)
   b.line(*p(x+.98,.65),*p(x+.98,1.88),C['gold'],4)
   b.line(*p(x,1.15),*p(x+2,1.15),C['gold'],3)
  r(3.2,0,1.6,1.9,'#F4E9D7',C['red'],5)
  b.line(*p(4,0),*p(4,1.9),C['red'],4)
  for x in [3.87,4.13]:b.circle(*p(x,.83),10,C['gold'],C['ink'],2)
  for x in [1,5.3]:
   r(x,3.35,1.7,1.4,'#DDE9EB',C['gold'],5);b.line(*p(x+.85,3.35),*p(x+.85,4.75),C['gold'],3)
  r(.45,2.12,7.1,.38,C['red'],C['ink'],3)
  y=p(0,2.18)[1];b.line(*p(.65,2.18),*p(7.35,2.18),C['lightgold'],4,'stroke-dasharray="12 9"')
  b.circle(*p(4,3.17),35,C['red'],C['gold'],5);b.line(*p(3.86,2.95),*p(4.10,3.40),C['lightgold'],5);b.circle(*p(4.08,3.34),4,'none',C['lightgold'],2);b.path(f'M {p(4.08,3.32)[0]},{p(4.08,3.32)[1]} C {p(4.40,3.20)[0]},{p(4.40,3.20)[1]} {p(3.80,3.20)[0]},{p(3.80,3.20)[1]} {p(4.14,3.03)[0]},{p(4.14,3.03)[1]}',C['lightgold'],3)
  b.text(*p(4,5.55),'',20)
 else:
  b.poly([p(-.28,5.4),p(3.5,6.4),p(7.28,5.4)],C['red'],C['ink'],4)
  for z in [.68,3.38]:
   r(.75,z,1.65,1.32,'#DDE9EB',C['gold'],5);b.line(*p(1.57,z),*p(1.57,z+1.32),C['gold'],3)
  r(5.6,4.10,.85,.72,'#DDE9EB',C['gold'],4)
  b.line(*p(0,2.2),*p(-.32,2.2),C['red'],8)
 for z in [0,2.6,5.4,6.4]:
  x,y=p(dep+.2,z);b.line(ox-25,y,x+45,y,C['line'],1,'stroke-dasharray="6 8"')
  b.text(x+52,y+8,f'{z:.2f}',21,C['muted'])
 # horizontal dimension
 x0,y=p(0,-.35);x1,_=p(dep,-.35);b.line(x0,y,x1,y,C['blue'],2);b.line(x0,y-10,x0,y+10,C['blue'],2);b.line(x1,y-10,x1,y+10,C['blue'],2);b.text((x0+x1)/2,y+39,f'{dep:.2f} m',26,C['blue'],700,'middle')
 b.text(ox,1152,label,32,weight=700)
b.lines(150,1225,['入口 幅1.60m × 高さ1.90m','丸看板は針と糸の意匠。文字は入れない。'],26,gap=45)
b.lines(1240,1225,['丸みを付けた寄棟屋根 / 棟高6.40m','屋根・二階・手前の壁を分割して室内を見せる。'],26,gap=45)
for x,col,name in [(150,C['white'],'白い壁'),(400,C['red'],'赤い布と屋根'),(760,C['gold'],'金の縁とボタン')]:
 b.rect(x,1340,38,38,col,C['line'],2,5);b.text(x+55,1370,name,26)
b.footer('外観の意匠を確認するための正投影図。現実の建築用図面ではない。寸法と開口は室内図と照合する。');b.save('02_shop_exterior')

# Floor plans and circulation.
b=Board(2300,1780);b.header('03','一階の店舗と二階の住まい','家具は番号で整理。青は移動ルートの目安、緑の破線は家具を使うために空ける場所。')
S=117;YTOP=410
for floor,ox,rows,title in [(1,135,f1,'1F  接客・陳列・仕立て'),(2,1280,f2,'2F  本人の寝室・休憩・住居')]:
 b.text(ox,294,title,36,weight=700);b.text(ox,342,'室内 7.60 × 6.60m  /  階高 2.60m',26,C['muted'])
 def q(x,y):return ox+x*S,YTOP+(7-y)*S
 def box(bounds,fill,stroke='none',sw=2,extra=''):
  x0,y0,x1,y1=bounds;x,y=q(x0,y1);b.rect(x,y,(x1-x0)*S,(y1-y0)*S,fill,stroke,sw,0,extra)
 box((0,0,8,7),'#D5CDC1',C['ink'],4);box((.2,.2,7.8,6.8),C['white'])
 for x in range(1,8):b.line(*q(x,.2),*q(x,6.8),'#EAE5DC',1)
 for y in range(1,7):b.line(*q(.2,y),*q(7.8,y),'#EAE5DC',1)
 # circulation visual only; actual clearances checked separately
 if floor==1:
  box((3.2,.2,5.0,5.0),C['pale']);box((1.15,2.60,6.40,3.80),C['pale']);box((5.0,2.4,6.4,3.6),C['pale'])
  box((3.2,0,4.8,.24),C['white']);b.path(f'M {q(4,-.4)[0]},{q(4,-.4)[1]} L {q(4,2)[0]},{q(4,2)[1]} L {q(5.2,3.15)[0]},{q(5.2,3.15)[1]} L {q(5.8,3.0)[0]},{q(5.8,3.0)[1]}',C['blue'],5,'marker-end="url(#arrow)"')
  b.text(*q(4,-.68),'入口 1.60m',25,C['blue'],700,'middle')
 else:
  box((3.0,1.2,5.0,5.0),C['pale']);box((2.15,2.85,5.20,4.05),C['pale']);box((5.2,2.4,7.8,3.6),C['pale'])
  b.path(f'M {q(7.2,3.45)[0]},{q(7.2,3.45)[1]} L {q(7.2,2.9)[0]},{q(7.2,2.9)[1]} L {q(4.4,2.9)[0]},{q(4.4,2.9)[1]}',C['blue'],5,'marker-end="url(#arrow)"')
 # furniture service areas
 for n,label,bs,h,side in rows:
  x0,y0,x1,y1=bs
  if side=='E':a=(x1,y0,x1+.9,y1)
  elif side=='W':a=(x0-.9,y0,x0,y1)
  elif side=='N':a=(x0,y1,x1,y1+.9)
  elif side in ('S','N/S'):a=(x0,y0-.9,x1,y0)
  else:a=None
  if a:box(a,'none',C['green'],2.4,'stroke-dasharray="9 7"')
  if side=='N/S':box((x0,y1,x1,y1+1),'none',C['green'],2.4,'stroke-dasharray="9 7"')
  fill=C['pink'] if n in (1,2,8,10) else C['lightgold'];box(bs,fill,C['ink'],2.2)
  if n in (1,2):
   for yy in [y0+.25+i*.3 for i in range(int((y1-y0-.25)/.3))]:b.line(*q(x0+.12,yy),*q(x1-.12,yy),C['red'],4)
  if n==8:box((x0+.1,y1-.52,x1-.1,y1-.12),C['white'],C['line'],1)
  if n==10:box((x0+.1,y1-.22,x1-.1,y1-.05),C['red'])
  if n==13:
   box((x0+.15,y0+.15,x0+.65,y1-.1),'#DDE9EB',C['muted'],1)
  cx,cy=q((x0+x1)/2,(y0+y1)/2);b.number(cx,cy,n)
 # stairs: same shared plan, 7 treads per run and landing
 box((5.2,3.6,7.8,6.8),'#F0EADF',C['ink'],2)
 box((6.4,3.6,6.6,5.7),'#D5CDC1',C['ink'],1)
 for yy in [3.6+i*.3 for i in range(8)]:
  b.line(*q(5.2,yy),*q(6.4,yy),C['muted'],2);b.line(*q(6.6,yy),*q(7.8,yy),C['muted'],2)
 b.number(*q(6.5,6.25),7)
 if floor==1:
  b.path(f'M {q(5.8,3.8)[0]},{q(5.8,3.8)[1]} L {q(5.8,5.5)[0]},{q(5.8,5.5)[1]}',C['blue'],4,'marker-end="url(#arrow)"')
  b.text(*q(5.8,4.0),'UP',21,C['blue'],700,'middle')
 else:
  b.path(f'M {q(7.2,5.5)[0]},{q(7.2,5.5)[1]} L {q(7.2,3.8)[0]},{q(7.2,3.8)[1]}',C['blue'],4,'marker-end="url(#arrow)"')
  b.text(*q(7.2,4.0),'到着',21,C['blue'],700,'middle')
 # dimensions and orientation
 x0,y=q(0,7.23);x1,_=q(8,7.23);b.line(x0,y,x1,y,C['blue'],2);b.text((x0+x1)/2,y-12,'8.00m',24,C['blue'],700,'middle')
 for x in [0,8]:xx,yy=q(x,7.23);b.line(xx,yy-9,xx,yy+9,C['blue'],2)
 x,y0=q(-.33,0);_,y1=q(-.33,7);b.line(x,y0,x,y1,C['blue'],2);b.text(x-16,(y0+y1)/2,'7.00m',24,C['blue'],700,'middle',f'transform="rotate(-90 {x-16} {(y0+y1)/2})"')
 b.text(ox+8*S,YTOP-75,'奥 +Y',23,C['muted'],anchor='end')
 b.text(ox+8*S,YTOP+7*S+55,'正面 Y=0',23,C['muted'],anchor='end')
 # legends
 ly=1360
 for i,(n,label,bs,h,side) in enumerate(rows):
  xx=ox+(i%2)*470;yy=ly+(i//2)*68;b.number(xx+25,yy-9,n);b.text(xx+66,yy,label,28,weight=500)
 b.text(ox,1600,'07  階段は上下階で同じ位置',28,C['muted'])
 b.text(ox,1650,'空ける：主通路1.20m以上 / 使用面0.90m以上',25,C['green'])
b.footer('床面の配置案。家具の正確な座標・高さは制作指示書と design_dimensions.json に記載。階段前は常に空ける。');b.save('03_floor_plans')

# Scale + variant requirements. These are technical diagrams, not alternative character art.
b=Board(2200,1580);b.header('04','スケールと派生モデルの作り分け','共通の顔と耳を守りつつ、台座・材質・使い方を用途ごとに分ける。')
cols=[(60,'フィギュア',['耳高 140mm 案','MOB付き駒台座：直径92 × 厚6mm','元画像の両手針ポーズを優先','塗装樹脂・控えめな金属感'],'台座あり'),(790,'ぬいぐるみ',['耳高 240mm 案','金の布眼鏡／目とRは刺繍','耳の曲がりを布の折れで残す','銀灰色の柔らかい針小物'],'台座なし'),(1520,'ゲーム住人',['耳高 1.40m 案','歩行・着席・作業を個別確認','針は別部品で持つ／収納を切替','ドット量産は静止確認の後'],'台座なし')]
for x,t,ls,tag in cols:
 b.rect(x,264,660,330,C['white'],C['line'],2,10);b.text(x+28,319,t,35,weight=700);b.text(x+625,318,tag,24,C['red'],700,'end');b.lines(x+28,380,ls,26,gap=48)
b.text(60,696,'高さの基準  /  ゲーム内メートル',36,weight=700)
# simple height envelope
baseY=1260; sy=190; left=175
for h,label in [(0,'床'),(.42,'座面 0.42'),(.76,'作業台 0.76'),(1.40,'耳の上端 1.40'),(1.90,'扉の上端 1.90'),(2.40,'室内天井 2.40')]:
 yy=baseY-h*sy;b.line(80,yy,1000,yy,C['line'],2,'stroke-dasharray="8 7"' if h else '');b.text(710,yy-12,label,26,C['muted'])
# body envelope and ceiling/door diagram
b.rect(260,baseY-1.4*sy,1.05*sy,1.4*sy,C['pale'],C['blue'],3,0,'stroke-dasharray="10 6"')
b.rect(299,baseY-1.15*sy,.64*sy,1.15*sy,'none',C['blue'],4,55)
b.text(360,baseY-140,'寸法基準',27,C['blue'],700,'middle');b.text(360,baseY-98,'の包絡',27,C['blue'],700,'middle')
b.rect(515,baseY-.76*sy,145,.76*sy,C['lightgold'],C['gold'],3);b.text(588,baseY-55,'机',30,C['ink'],700,'middle')
b.text(80,1324,'耳とリボンの見た目幅は、初期目安1.05m。',26,C['muted'])
b.text(80,1372,'当たり判定だけで通れる判定にしない。',26,C['muted'])
# top down clearance diagram
b.text(1130,696,'歩行と家具の空き',36,weight=700)
b.rect(1140,785,980,400,C['white'],C['line'],2)
b.rect(1165,815,340,340,C['lightgold'],C['gold'],3);b.text(1335,930,'家具',31,C['ink'],700,'middle');b.text(1335,980,'占有範囲',27,C['muted'],400,'middle')
b.rect(1505,815,243,340,'none',C['green'],3,0,'stroke-dasharray="11 8"');b.text(1626,874,'使用面',26,C['green'],700,'middle');b.text(1626,919,'0.90m',27,C['green'],700,'middle')
b.circle(1860,1010,87,C['pale'],C['blue'],4);b.circle(1860,1010,141,'none',C['blue'],2)
b.text(1860,1002,'当たり判定',22,C['blue'],700,'middle');b.text(1860,1040,'直径0.64m',25,C['blue'],700,'middle')
b.lines(1130,1243,['主通路の有効幅 1.20m以上','補助通路1.10m / 階段1.20m以上','着席時は座面0.42mに骨盤を合わせ、靴を接地。','手を机へ置くテストまで行って寸法を確定。'],27,gap=47)
b.footer('寸法は制作開始時の提案値。キャラクターの形状プレビューと接触テストで確定し、全モデルへ一括反映する。');b.save('04_scale_and_variants')
print('Boards and manifest created.')
