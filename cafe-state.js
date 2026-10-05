/* Persisted ownership: pantry -> cafe stock -> order -> consumed. */
(()=>{'use strict';
const kinds=['dorayaki','omelet','soup'],copy=x=>JSON.parse(JSON.stringify(x));
class CafeLedger{
 constructor(){this.stock=Object.fromEntries(kinds.map(k=>[k,0]));this.orders={};this.eaten=0;}
 serialize(){return {v:1,stock:{...this.stock},orders:copy(this.orders),eaten:this.eaten};}
 restore(s){this.stock=Object.fromEntries(kinds.map(k=>[k,Number.isSafeInteger(s?.stock?.[k])&&s.stock[k]>=0?s.stock[k]:0]));this.orders={};this.eaten=Number.isSafeInteger(s?.eaten)&&s.eaten>=0?s.eaten:0;
 // A reload releases physical reservations. Unconsumed dishes still have one owner.
 for(const o of Object.values(s?.orders||{}))if(kinds.includes(o.kind))this.stock[o.kind]++;
 }
 transaction(save,fn){const before=this.serialize();fn();if(save())return true;this.stock=before.stock;this.orders=before.orders;this.eaten=before.eaten;return false;}
 deposit(pantry,kind,n,save){if(!kinds.includes(kind)||!Number.isSafeInteger(n)||n<1||pantry[kind]<n)return false;const old=pantry[kind];pantry[kind]-=n;if(this.transaction(save,()=>this.stock[kind]+=n))return true;pantry[kind]=old;return false;}
 reserve(seat,actor,save){if(this.orders[seat])return false;let kind=kinds.find(k=>this.stock[k]>0);if(!kind)return false;return this.transaction(save,()=>{this.stock[kind]--;this.orders[seat]={actor,kind};});}
 release(seat,save){let o=this.orders[seat];if(!o)return true;return this.transaction(save,()=>{this.stock[o.kind]++;delete this.orders[seat];});}
 consume(seat,actor,save){let o=this.orders[seat];if(!o||o.actor!==actor)return false;return this.transaction(save,()=>{delete this.orders[seat];this.eaten++;});}
}
window.CafeLedger=CafeLedger;
})();
