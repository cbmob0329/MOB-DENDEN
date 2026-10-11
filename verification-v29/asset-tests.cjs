const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
function load(file){const box={window:{}};vm.runInNewContext(fs.readFileSync(file,'utf8'),box);return JSON.parse(JSON.stringify(box.window));}
let images=0,frames=0,models=0;
function compare(original,runtime,path=''){
  if(!original||typeof original!=='object')return;
  if(original.url?.startsWith('data:image/')){
    assert.deepEqual(fs.readFileSync(runtime.url),Buffer.from(original.url.split(',')[1],'base64'),path+' native bytes');images++;
  }
  if(original.rects){assert.deepEqual(runtime.rects,original.rects,path+' rectangles');frames+=original.rects.length;}
  if(original.frames){assert.equal(runtime.frames.length,original.frames.length,path+' frame count');for(let i=0;i<original.frames.length;i++)assert.deepEqual(runtime.frames[i].rect,original.frames[i].rect,path+' frame bounds');frames+=original.frames.length;}
  for(const k of Object.keys(original))if(k!=='rects'&&k!=='frames')compare(original[k],runtime[k],path+'/'+k);
}
for(const file of ['residents-v23.js','white-v26.js','tailor-v28.js','mita-v21.js','town-action-assets-v19.js'])compare(load('assets/'+file),load('assets/runtime-v29/'+file),file);
const original=load('assets/blender-models.js').CHILL_BLENDER_DATA,runtime=load('assets/runtime-v29/blender-models.js').CHILL_BLENDER_DATA;
for(const [id,spec]of Object.entries(original)){let actual;vm.runInNewContext(fs.readFileSync(runtime[id].modelURL29,'utf8'),{ChillResources29:{acceptModel:(name,data)=>{assert.equal(name,id);actual=JSON.parse(JSON.stringify(data));}}});const hydrated=JSON.stringify(actual).replace(/assets\/runtime-v29\/media\/[a-f0-9]+\.png/g,p=>'data:image/png;base64,'+fs.readFileSync(p).toString('base64'));assert.equal(hydrated===JSON.stringify(spec),true,id+' complete geometry');models++;}
const white=load('assets/runtime-v29/white-v26.js').CHILL_WHITE26,tailor=load('assets/runtime-v29/tailor-v28.js').CHILL_TAILOR28;
assert.equal(Object.values(white).reduce((n,s)=>n+s.rects.length,0),48);assert.equal(white.dance.rects.length,16);assert.equal(Object.values(tailor.sheets).reduce((n,s)=>n+s.rects.length,0),36);
const town=load('assets/runtime-v29/town-action-assets-v19.js').CHILL_TOWN_ACTION_ASSETS19;assert(town.denden.frames.every(f=>f.grip29?.length===2));
const result={nativeImages:images,unchangedAuthoredFrameRects:frames,unchangedModels:models,whiteFrames:48,whiteDanceFrames:16,tailorFrames:36};
fs.writeFileSync('verification-v29/asset-results.json',JSON.stringify(result,null,2));console.log('PASS original image bytes, frame rectangles/counts, complete model geometry',result);
