// Run from any directory after installing the pinned test dependencies.
const fs=require('fs'),path=require('path'),z=require('zlib'),{execFileSync}=require('child_process');
const runtime=path.resolve(__dirname,'../../jlpt-n5-n4-test-runtime'),src=runtime+'/node_modules/@sparticuz/chromium/bin',out=runtime+'/browser';fs.mkdirSync(out,{recursive:true});
for(const name of fs.readdirSync(src)){if(!name.endsWith('.br'))continue;const target=out+'/'+name.slice(0,-3);fs.writeFileSync(target,z.brotliDecompressSync(fs.readFileSync(src+'/'+name)));if(name.endsWith('.tar.br'))execFileSync('tar',['--no-same-owner','-xf',target,'-C',out]);}
fs.chmodSync(out+'/chromium',0o755);
