/* Character-specific speech at the shared output boundary, including old action code. */
(function(root){'use strict';
 const greetings={nekokoo:['オラがネコクーだぞ。','ひと休みするんだぞ。','カフェへ行くんだぞ。','オラも順番を待つんだぞ。','おいしいんだぞ！','また来るんだぞ。'],mita:['いらっしゃいませ！','たくさん見て行ってください。','良い天気ですね。','お元気ですか？','ありがとうございます♪','また来てくださいね♪']};
 function line(a,text){if(a?.key==='mita')return typeof text==='string'&&text?text:greetings.mita[0];if(a?.key!=='nekokoo')return text||'';
  if(typeof text!=='string'||!text.trim())return 'オラも楽しむんだぞ！';
  return text.replace(/ふふっ、|あら～、|ほぅ～、/g,'').replace(/拙者|僕|わたし|私/g,'オラ').replace(/でありました/g,'だったんだぞ').replace(/であります(?:ね)?/g,'だぞ').replace(/でござった(?:な～)?/g,'だったんだぞ').replace(/でござる(?:な～|ね)?/g,'だぞ').replace(/でやんす(?:ね)?/g,'だぞ').replace(/(?:だ)?ニョロ[～ー~]*/g,'んだぞ').replace(/ですね/g,'なんだぞ').replace(/ですよ/g,'だぞ').replace(/です/g,'だぞ').replace(/します(?:ね)?/g,'するんだぞ').replace(/しました/g,'したんだぞ').replace(/([いくぐすつぬぶむるた])だぞ/g,'$1んだぞ');
 }
 root.ChillVoice21={line,greetings};if(typeof module!=='undefined')module.exports=root.ChillVoice21;
})(typeof window==='undefined'?globalThis:window);
