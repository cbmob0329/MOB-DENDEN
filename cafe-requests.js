(function(){'use strict';CHILL_HEART_CONFIG.wish=1;CHILL_HEART_CONFIG.arcade=1;const Base=ChillCafe,kinds=['dorayaki','omelet','soup'],names={dorayaki:'どら焼き',omelet:'卵焼き',soup:'コーンスープ'};
window.ChillCafe=class extends Base {
 constructor(c){super(c);this.requestClock=0;this.requestSerial=0;this.requests={};const reserve=this.ledger.reserve.bind(this.ledger),consume=this.ledger.consume.bind(this.ledger);
 this.ledger.reserve=(seat,actor,save)=>{const guest=c.actors[actor];if(!guest||guest.cafeMode!=='seated'||this.ledger.orders[seat])return false;let r=this.requests[actor];if(!r){const wish=kinds[Math.floor(Math.random()*kinds.length)];r=this.requests[actor]={wish,kind:wish,phase:'ask',until:this.requestClock+2,tried:[],id:++this.requestSerial,disappointed:false};c.speak(guest,actor===4?names[wish]+'をいただきたいでござる！':actor===0?names[wish]+'がいいでやんす～。':actor===1?names[wish]+'が食べたいであります！':names[wish]+'がいいニョロ～',4,true);return false;}if(this.requestClock<r.until)return false;
 if(r.phase==='empty'){if(Object.values(this.ledger.stock).some(n=>n>0)){r.tried=[];r.phase='alternative';r.until=this.requestClock+1;}return false;}
 if(r.phase==='alternative'){let next=kinds.find(k=>!r.tried.includes(k)&&this.ledger.stock[k]>0);if(!next){r.phase='empty';r.until=this.requestClock+10;if(!r.disappointed){r.disappointed=true;this.collections.disappoint(actor);c.speak(guest,actor===4?'またの機会にするでござる。':actor===0?'ほぅ～、また今度にするでやんす。':actor===1?'また今度にするであります。':'残念だニョロ～',4,true);}return false;}r.kind=next;r.phase='ask';r.until=this.requestClock+2;const text=actor===4?'では、'+names[next]+'を頼むでござる！':actor===0?'じゃあ、'+names[next]+'がいいでやんす！':actor===1?'では、'+names[next]+'でお願いします！':'ニョロ～・・'+names[next]+'はあるニョロ？';c.speak(guest,text,4,true);return false;}
 if(this.ledger.stock[r.kind]<=0){if(!r.tried.includes(r.kind))r.tried.push(r.kind);c.speak(c.actors[3],'ごめんなさい、今品切れなの、、',4,true);r.phase='alternative';r.until=this.requestClock+2;return false;}
 const ok=reserve(seat,actor,save,{kind:r.kind,firstWish:r.kind===r.wish,requestId:r.id});if(ok){r.phase='reserved';c.speak(c.actors[3],'少々お待ちください！',4,true);}return ok;
 };
 this.ledger.consume=(seat,actor,save)=>{const order=this.ledger.orders[seat],ok=consume(seat,actor,save);if(ok&&order?.firstWish&&Math.random()<.8)this.reward('cafe-wish:'+order.requestId,c.actors[actor],'wish');return ok;};
 }
 reward(id,a,type){if((type==='fun'||type==='wish'||type==='arcade')&&this.collections&&Math.random()>[0,.25,.5,1,1,1][this.collections.state.mood[a.id]])return false;return super.reward(id,a,type);}
 serialize(){return {...super.serialize(),requestSerial:this.requestSerial||0};}
 restore(s){super.restore(s);this.requests={};this.requestSerial=Number.isSafeInteger(s?.requestSerial)?s.requestSerial:0;}
 update(a,dt){if(a.id===3)this.requestClock+=dt;if(a.id<3&&a.cafeMode!=='seated'&&this.requests?.[a.id]?.phase!=='reserved')delete this.requests?.[a.id];if(a.id<3&&!['seated','eating','satisfied','seating'].includes(a.cafeMode))delete this.requests?.[a.id];return super.update(a,dt);}
 afterRender(){super.afterRender();for(let a of this.c.actors){if(this.requests?.[a.id]?.phase==='empty'&&a.room===this.view&&a.cafeMode==='seated'){a.effect.textContent='〰';a.effect.style.opacity=1;}}}
};
})();
