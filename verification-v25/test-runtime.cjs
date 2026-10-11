const path=require('path');
try{module.exports=require('playwright');}catch{module.exports=require(process.env.PLAYWRIGHT_PATH||path.join(process.env.USERPROFILE||process.env.HOME,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));}
