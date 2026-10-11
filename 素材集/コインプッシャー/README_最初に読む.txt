MOB CHILL LIFE コインプッシャー素材集
最初に読む

赤金と青金の3Dコインプッシャー、景品、10種のリール図柄、Astra向け実装仕様をまとめています。
筐体と景品は実際のBlenderメッシュです。ゲーム用GLBもあるため、この素材を使うためにユーザーのPCへBlenderを入れる必要はありません。

使い方
1 このZIPを展開します。
2 展開した「コインプッシャー」フォルダを、素材置き場へ置いてください。
   推奨例:
   C:\Users\user\Documents\GitHub\MOB DENDEN\素材集\コインプッシャー
   このフォルダの存在は未確認です。必要なら作成する場所の例です。
   同名の既存フォルダがある場合は、上書きせず別名かバックアップを使ってください。
3 Astraへ「Astra_START_HERE_JA.txt」を渡し、同じフォルダの全仕様とモデルを読んで組み込むよう依頼します。

重要
フォルダに置くだけではゲームへ自動で反映されません。この納品はモデルと実装資料です。
既存プロジェクトのコード変更、物理エンジンへの接続、スマホでの動作確認はまだ行っていません。
index.htmlなど既存のゲームファイルを、この素材で丸ごと置き換えないでください。

中身
Astra_START_HERE_JA.txt
  Astraへ最初に渡す短い依頼文

source/
  MOB_CHILL_LIFE_coin_pusher.blend  2台の筐体と可動部の編集原本
  prize_library.blend              コインとM/O/B・どら焼き等の編集原本
  slot_symbols.blend               全10種のリール図柄の編集原本
  scripts/                        制作スクリプトの参考ソース

gameassets/
  exports/                        筐体、マスコット、実体景品のGLB
  symbols/                        リール10種類のGLBと透過PNG

previews/
  01_two_cabinets.png              2台の外観
  02_mechanism_cutaway.png         内部機構
  03_front.png                    正面
  04_side.png                     側面
  05_top.png                      上面
  06_ten_slot_symbols.png          リール10種類
  07_prizes.png                   コインと景品

docs/
  MOB_CHILL_LIFE_Astra_Implementation_JA.txt  全体仕様と受け入れテスト
  coin_pusher_config.proposal.json           抽選・払い出し等の初期調整案
  asset_bindings.proposal.json               仕様IDと実ファイルの対応
  Asset_README_JA.md                         モデルの詳細と接続上の注意
  assets_manifest.json                      寸法・アンカー・物理用補助
  Config_Validation_JA.txt                   設定値の静的検証結果
  Package_Validation_JA.txt                  ZIP内容と参照の検証結果
  SHA256SUMS.txt                            同梱ファイルの照合用ハッシュ

ゲーム用GLBの選択
・cabinet_red.glb、cabinet_blue.glb: 通常はこちらを使います。展示コインを除いた単体筐体です。
・two_cabinets.glb: 並べて確認する展示用です。展示コインを含みます。
・gold_sunglasses_mascot.glb: 上部マスコット単体です。
・coin.glb、letter_M/O/B_各色.glb、dorayaki.glb: 実体コイン・景品です。
・coin_bag.glb、wood_chest.glb、gold_chest.glb: 演出にも使える袋・宝箱です。

リールのモブデンデンとモブピンクは、提供画像を使った顔アップのテクスチャ表示です。
この2図柄はテクスチャ付き平面、他8図柄は3Dメッシュです。筐体と実体景品の3D構造とは別です。
画像はGLBとBLENDへ埋め込まれているため、制作時の外部ファイルパスを用意しなくても納品素材を開けます。

Blenderで編集する場合
制作に使用したバージョンはBlender 4.3.2です。互換性は利用するBlenderで確認してください。
source/scriptsは制作ソースの参考です。制作環境のパスを含み、ユーザーのPCでそのまま一括再生成できる保証はありません。
完成したBLEND/GLBを使う場合に、これらのスクリプトを実行する必要はありません。

仕様の注意
ハート1個→メダル10枚、5灯でも回転待ちを打ち切らないこと、1000枚を実体で分割生成することなどを詳しく記載しています。
確率、デンデン/ピンクの枚数、景品の受取方法の解釈、住民の盤面分離は、確定要件と区別して提案として書いています。
現金購入、換金、課金、景品ショップは入っていません。

