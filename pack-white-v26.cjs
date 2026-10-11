const fs=require('fs'),path=require('path'),base=path.join(__dirname,'assets/white-v26');
const sheets={};for(const name of ['actions','dance','life']){const data=fs.readFileSync(path.join(base,name+'.png'));sheets[name]={url:'data:image/png;base64,'+data.toString('base64'),columns:4,rows:4};}
fs.writeFileSync(path.join(__dirname,'assets/white-v26.js'),'window.CHILL_WHITE26='+JSON.stringify(sheets)+';\n');
console.log('Packed Mob White: 48 sprite frames');
