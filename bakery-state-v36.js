/* Bread has one owner: oven -> cooling rack -> warmer/bag -> guest -> eaten. */
(function(root){'use strict';
const copy=x=>JSON.parse(JSON.stringify(x)),valid=n=>Number.isSafeInteger(n)&&n>=0;
const recipes={koppe:{name:'コッペパン',cost:{wheat:1}},anpan:{name:'あんぱん',cost:{wheat:1,beans:1}},cheese:{name:'チーズパン',cost:{wheat:1,milk:1}}};
class BakeryState36{
 constructor(hooks){this.hooks=hooks;this.restore();}
 restore(raw){this.state={v:1,open:raw?.open!==false,oven:null,ready:[],stock:{koppe:0,anpan:0,cheese:0},cups:0,visits:{},eaten:raw?.eaten||0};const s=this.state;
 for(const k of Object.keys(recipes))s.stock[k]=valid(raw?.stock?.[k])?raw.stock[k]:0;
 s.cups=valid(raw?.cups)?Math.min(60,raw.cups):0;
 const batch=b=>b&&recipes[b.kind]&&valid(b.n)&&b.n>0&&b.n<=4&&Number.isFinite(b.endsAt);
 if(batch(raw?.oven))s.oven=copy(raw.oven);s.ready=(raw?.ready||[]).filter(batch).map(copy);
 // An interrupted meal returns its unconsumed bread and drink exactly once.
 for(const v of Object.values(raw?.visits||{})){if(!v.consumed&&recipes[v.kind]){if(this.total()<30)s.stock[v.kind]++;else s.ready.push({kind:v.kind,n:1,endsAt:0});}if(v.cup&&!v.consumed)s.cups=Math.min(60,s.cups+1);}
 }
 serialize(){return copy(this.state);}
 transaction(fn){if(this.busy)return{ok:false,reason:'busy'};const before=this.serialize(),pantry=copy(this.hooks.pantry()),extra=this.hooks.backup?.();this.busy=true;try{const r=fn();if(r?.ok===false){this.state=before;return r;}if(!this.hooks.save())throw Error('save');return{ok:true,...r};}catch{this.state=before;Object.assign(this.hooks.pantry(),pantry);this.hooks.rollback?.(extra);return{ok:false,reason:'save'};}finally{this.busy=false;}}
 total(){return Object.values(this.state.stock).reduce((a,b)=>a+b,0);}
 bake(kind,n,now=Date.now()){return this.transaction(()=>{const r=recipes[kind],p=this.hooks.pantry();if(!r||!valid(n)||n<1||n>4)return{ok:false,reason:'quantity'};if(this.state.oven)return{ok:false,reason:'oven'};if(Object.entries(r.cost).some(([k,v])=>(p[k]||0)<v*n))return{ok:false,reason:'ingredients'};for(const[k,v]of Object.entries(r.cost))p[k]-=v*n;this.state.oven={kind,n,startedAt:now,endsAt:now+180000};});}
 tick(now=Date.now()){const b=this.state.oven;if(!b||now<b.endsAt)return false;return this.transaction(()=>{this.state.ready.push(b);this.state.oven=null;}).ok;}
 collect(index,to='warmer'){return this.transaction(()=>{const b=this.state.ready[index];if(!b)return{ok:false,reason:'empty'};if(to==='warmer'){if(this.total()+b.n>30)return{ok:false,reason:'capacity'};this.state.stock[b.kind]+=b.n;}else{if(!this.hooks.canAdd(to,b.kind,b.n))return{ok:false,reason:'bag'};this.hooks.add(to,b.kind,b.n);}this.state.ready.splice(index,1);});}
 deposit(kind,n){return this.transaction(()=>{const p=this.hooks.pantry();if(!recipes[kind]||!valid(n)||n<1||(p[kind]||0)<n)return{ok:false,reason:'empty'};if(this.total()+n>30)return{ok:false,reason:'capacity'};p[kind]-=n;this.state.stock[kind]+=n;});}
 take(kind,to){return this.transaction(()=>{if(!(this.state.stock[kind]>0))return{ok:false,reason:'empty'};if(!this.hooks.canAdd(to,kind,1))return{ok:false,reason:'bag'};this.state.stock[kind]--;this.hooks.add(to,kind,1);});}
 fill(n){return this.transaction(()=>{const p=this.hooks.pantry();if(!valid(n)||n<1||(p.milk||0)<n)return{ok:false,reason:'ingredients'};if(this.state.cups+n*3>60)return{ok:false,reason:'tank'};p.milk-=n;this.state.cups+=n*3;});}
 reserve(v){return this.transaction(()=>{if(!this.state.open||this.state.visits[v.actor]||Object.values(this.state.visits).some(x=>x.seat===v.seat))return{ok:false,reason:'seat'};if(!(this.state.stock[v.kind]>0))return{ok:false,reason:'empty'};this.state.stock[v.kind]--;this.state.visits[v.actor]=copy(v);});}
 drink(id){return this.transaction(()=>{const v=this.state.visits[id];if(!v||v.cup||this.state.cups<1)return{ok:false,reason:'empty'};v.cup=true;this.state.cups--;});}
 eat(id){return this.transaction(()=>{const v=this.state.visits[id];if(!v||v.consumed)return{ok:false,reason:'eaten'};v.consumed=true;this.state.eaten++;this.hooks.credit?.(id);});}
}
BakeryState36.recipes=recipes;root.ChillBakeryState36=BakeryState36;if(typeof module!=='undefined')module.exports=BakeryState36;
})(typeof window==='undefined'?globalThis:window);
