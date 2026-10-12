/* Standalone farm aggregate. No game currency, bag policy or localStorage access. */
(function(root){
'use strict';
const clone=x=>JSON.parse(JSON.stringify(x));
const integer=x=>Number.isSafeInteger(x)&&x>=0;
const cropKeys=['wheat','corn','beans'];
const emptyPlot=()=>({crop:null,wateredAt:null,durationMs:null,yield:null});
const count=x=>integer(x)?x:0;
class FarmState {
  constructor(config={},saved=null){
    this.config={durations:{wheat:300000,corn:240000,beans:null,...config.durations},animalMs:null,harvestWeights:null,...config};
    this.config.durations={wheat:300000,corn:240000,beans:null,...config.durations};
    this.busy=false;
    this.restore(saved);
  }
  restore(saved){
    const s=saved&&saved.v===1?saved:{};
    this.state={v:1,revision:count(s.revision),clock:count(s.clock),plots:Array.from({length:24},(_,i)=>{
      const p=s.plots?.[i];if(!cropKeys.includes(p?.crop))return emptyPlot();
      const growing=integer(p.wateredAt)&&Number.isSafeInteger(p.durationMs)&&p.durationMs>0&&[1,2,3].includes(p.yield);
      return {crop:p.crop,wateredAt:growing?p.wateredAt:null,durationMs:growing?p.durationMs:null,yield:growing?p.yield:null};
    }),seeds:Object.fromEntries(cropKeys.map(k=>[k,count(s.seeds?.[k])])),storage:Object.fromEntries([...cropKeys,'egg','milk','dorayaki','omelet','soup'].map(k=>[k,count(s.storage?.[k])])),hen:{eggs:Math.min(3,count(s.hen?.eggs)),nextAt:integer(s.hen?.nextAt)?s.hen.nextAt:null},cow:{ready:!!s.cow?.ready,nextAt:integer(s.cow?.nextAt)?s.cow.nextAt:null}};
    // Preserve crops from the former 36-bed layout until a bed becomes available.
    this.state.pendingPlots=(s.plots?.slice(24)||[]).concat(s.pendingPlots||[]).filter(p=>cropKeys.includes(p?.crop)).map(p=>({...p}));
    this.refillPending();
    if(this.state.hen.eggs===3)this.state.hen.nextAt=null;
    if(this.state.cow.ready)this.state.cow.nextAt=null;
    this.state.hen2={eggs:Math.min(3,count(s.hen2?.eggs)),nextAt:integer(s.hen2?.nextAt)?s.hen2.nextAt:null};
    this.state.cow2={ready:!!s.cow2?.ready,nextAt:integer(s.cow2?.nextAt)?s.cow2.nextAt:null};
    for(const key of ['cow','cow2'])this.state[key].milk=[2,3,4].includes(s[key]?.milk)?s[key].milk:2+Math.floor(Math.random()*3);
  }
  refillPending(){for(let i=0;i<this.state.plots.length&&this.state.pendingPlots.length;i++)if(!this.state.plots[i].crop)this.state.plots[i]=this.state.pendingPlots.shift();}
  serialize(){return clone(this.state);}
  now(at){if(!integer(at))throw Error('A nonnegative integer wall-clock timestamp is required');return Math.max(at,this.state.clock);}
  period(){const n=this.config.animalMs;return Number.isSafeInteger(n)&&n>0?n:null;}
  settle(at){
    const s=this.state,t=this.now(at),ms=this.period();s.clock=t;
    if(!ms)return;
    for(const hen of [s.hen,s.hen2]){const s={hen};if(s.hen.eggs<3){
      if(s.hen.nextAt===null)s.hen.nextAt=t+ms;
      if(t>=s.hen.nextAt){const n=Math.min(3-s.hen.eggs,Math.floor((t-s.hen.nextAt)/ms)+1);s.hen.eggs+=n;s.hen.nextAt=s.hen.eggs===3?null:s.hen.nextAt+n*ms;}
    }}
    for(const cow of [s.cow,s.cow2])if(!cow.ready){if(cow.nextAt===null)cow.nextAt=t+ms;if(t>=cow.nextAt){cow.ready=true;cow.nextAt=null;}}
  }
  transact(at,save,change){
    if(this.busy||typeof save!=='function')return {ok:false,reason:'busy-or-no-persistence'};
    const before=this.serialize();this.busy=true;
    try {
      this.settle(at);const result=change();
      if(result?.ok===false){this.state=before;return result;}
      this.state.revision++;
      // Persist the entire farm aggregate atomically with any outer game state.
      if(save(this.serialize())!==true)throw Error('save-failed');
      return {ok:true,...result};
    } catch(e){this.state=before;return {ok:false,reason:e.message||'transaction-failed'};}
    finally{this.busy=false;}
  }
  advance(at,save){return this.transact(at,save,()=>({}));}
  plant(index,crop,at,save){return this.transact(at,save,()=>{
    const p=this.state.plots[index];if(!p||p.crop||!cropKeys.includes(crop)||this.state.seeds[crop]<1)return {ok:false,reason:'no-empty-plot-or-seed'};
    this.state.seeds[crop]--;this.state.plots[index]={...emptyPlot(),crop};return {};
  });}
  water(index,at,save,random=Math.random){return this.transact(at,save,()=>{
    const p=this.state.plots[index],duration=this.config.durations[p?.crop],w=this.config.harvestWeights;
    if(!p?.crop||p.wateredAt!==null)return {ok:false,reason:'not-dry'};
    if(!Number.isSafeInteger(duration)||duration<=0||!Array.isArray(w)||w.length!==3||w.some(n=>!Number.isFinite(n)||n<0)||w.reduce((a,b)=>a+b,0)<=0)return {ok:false,reason:'configuration-pending'};
    const r=random();if(!Number.isFinite(r)||r<0||r>=1)return {ok:false,reason:'invalid-random'};
    let n=r*w.reduce((a,b)=>a+b,0),yieldCount=3;for(let i=0;i<3;i++){n-=w[i];if(n<0){yieldCount=i+1;break;}}
    Object.assign(p,{wateredAt:this.state.clock,durationMs:duration,yield:yieldCount});return {};
  });}
  plot(index,at){const p=this.state.plots[index];if(!p?.crop)return {stage:0,empty:true};if(p.wateredAt===null)return {stage:0,crop:p.crop,dry:true};const elapsed=Math.max(0,this.now(at)-p.wateredAt),progress=Math.min(1,elapsed/p.durationMs);return {crop:p.crop,stage:Math.min(4,Math.floor(progress*5)),ready:progress===1,remainingMs:Math.max(0,p.durationMs-elapsed),progress};}
  collect(kind,index,at,save,accept){return this.transact(at,save,()=>{
    const s=this.state,hen=index===1?s.hen2:s.hen,cow=index===1?s.cow2:s.cow;let item,n;
    if(kind==='crop'){const p=s.plots[index];if(!this.plot(index,s.clock).ready)return {ok:false,reason:'not-ready'};item=p.crop;n=p.yield;}
    else if(kind==='egg'){item='egg';n=hen.eggs;if(!n)return {ok:false,reason:'not-ready'};}
    else if(kind==='milk'){item='milk';n=cow.milk;if(!cow.ready)return {ok:false,reason:'not-ready'};}
    else return {ok:false,reason:'invalid-kind'};
    // Slot/stack rules are intentionally supplied by the eventual inventory adapter.
    if(typeof accept!=='function'||accept(clone(s.storage),item,n)!==true)return {ok:false,reason:'storage-full-or-policy-pending'};
    if(!Number.isSafeInteger(s.storage[item]+n))return {ok:false,reason:'overflow'};
    s.storage[item]+=n;
    if(kind==='crop'){s.plots[index]=emptyPlot();this.refillPending();}
    else if(kind==='egg'){const full=hen.eggs===3;hen.eggs=0;if(full)hen.nextAt=this.period()?s.clock+this.period():null;}
    else {cow.ready=false;cow.nextAt=this.period()?s.clock+this.period():null;cow.milk=2+Math.floor(Math.random()*3);}
    return {item,count:n};
  });}
}
root.ChillFarmState=FarmState;
if(typeof module!=='undefined')module.exports=FarmState;
})(typeof window==='undefined'?globalThis:window);
