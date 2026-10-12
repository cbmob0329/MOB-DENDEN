const fs=require('fs'),vm=require('vm'),crypto=require('crypto'),path=require('path');
const root=__dirname,box={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'assets/tailor-goods-v35.js'),'utf8'),box);
const manifest=JSON.parse(fs.readFileSync(path.join(root,'assets/tailor-approved-v36/manifest.json'),'utf8'));
const seen=new Set();
const items=box.window.CHILL_TAILOR_GOODS35.map(old=>{
 const id=old.id.split('-'),entry=manifest.find(r=>r.number===id[1]&&r.category===old.type&&r.name===old.model);
 if(!entry)throw Error('Missing approved artwork: '+old.id);
 const data=fs.readFileSync(path.join(root,'assets/tailor-approved-v36',entry.file));
 const hash=crypto.createHash('sha256').update(data).digest('hex');
 if(hash!==entry.sha256)throw Error('Artwork checksum mismatch: '+old.id);
 const file='assets/runtime-v29/media/'+hash.slice(0,24)+'.png';fs.writeFileSync(path.join(root,file),data);seen.add(old.id);
 return {...old,url:file,artworkVersion:36};
});
if(items.length!==115||seen.size!==115)throw Error('Expected 115 unique products');
fs.writeFileSync(path.join(root,'assets/tailor-goods-v35.js'),'window.CHILL_TAILOR_GOODS35='+JSON.stringify(items)+';window.CHILL_TAILOR_OUTFITS35='+JSON.stringify(box.window.CHILL_TAILOR_OUTFITS35)+';');
console.log('115 approved original artworks packed; product IDs, types and prices preserved');
