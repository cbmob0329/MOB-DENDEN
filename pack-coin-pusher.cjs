// Embed supplied GLBs/PNGs for both the existing file:// build and standalone build.
const fs=require('fs'),path=require('path');
const base=path.join(__dirname,'素材集','コインプッシャー'),models={},symbols={};
for(const name of fs.readdirSync(path.join(base,'gameassets/exports'))){
 if(!name.endsWith('.glb')||name==='two_cabinets.glb')continue;
 models[name.slice(0,-4)]=fs.readFileSync(path.join(base,'gameassets/exports',name)).toString('base64');
}
const names={mob_red:'redMOB',mob_blue:'blueMOB',mob_green:'greenMOB',seven:'7',denden:'Denden',pink:'Pink',coin_bag:'coinbag',wood_chest:'woodchest',gold_chest:'goldchest',dorayaki:'dorayaki'};
for(const [id,name]of Object.entries(names))symbols[id]='data:image/png;base64,'+fs.readFileSync(path.join(base,'gameassets/symbols','symbol_'+name+'.png')).toString('base64');
const config=JSON.parse(fs.readFileSync(path.join(base,'docs/coin_pusher_config.proposal.json'),'utf8'));
fs.writeFileSync(path.join(__dirname,'assets/coin-pusher.js'),'window.CHILL_PUSHER_ASSETS='+JSON.stringify({models,symbols,config})+';\n');
console.log('Packed',Object.keys(models).length,'GLBs and',Object.keys(symbols).length,'symbols');
