// Run after node build.cjs. Distribution archives stay outside the repository.
const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
let JSZip;
try { JSZip = require('jszip'); } catch {
  JSZip = require(path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/jszip'));
}
const repo = __dirname;
const outputDir = path.join(os.homedir(), 'Documents', 'MOB-CHILL-LIFE-Distribution');
const name = 'MOB_CHILL_LIFE_V15_1.zip';
const output = path.join(outputDir, name);
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
async function main() {
  const html = fs.readFileSync(path.join(repo, 'dist-local', 'MOB_CHILL_LIFE.html'));
  if (!html.length) throw Error('Game HTML is empty');
  const seed = fs.existsSync(output) ? output : path.join(repo, name);
  const zip = await JSZip.loadAsync(fs.readFileSync(seed));
  zip.remove('verification-v20/package-proof.json');
  zip.remove('verification-v20/distribution-proof.json');
  // Refresh existing supporting files without dropping retained models or artwork.
  for (const entry of Object.keys(zip.files)) {
    if (!entry.startsWith('runtime-reference/') || zip.files[entry].dir) continue;
    const local = path.resolve(repo, entry.slice('runtime-reference/'.length));
    if (!local.startsWith(repo + path.sep)) throw Error('Invalid supporting path');
    if (fs.existsSync(local)) zip.file(entry, fs.readFileSync(local));
  }
  zip.file('MOB_CHILL_LIFE.html', html);
  zip.file('V20_RESIDENT_LIFE_REPORT.md', fs.readFileSync(path.join(repo, 'V20_RESIDENT_LIFE_REPORT.md')));
  const evidence = path.join(repo, 'verification-v20');
  for (const file of fs.readdirSync(evidence)) {
    if (file === 'package-proof.json' || file === 'distribution-proof.json') continue;
    const local = path.join(evidence, file);
    if (fs.statSync(local).isFile()) zip.file('verification-v20/' + file, fs.readFileSync(local));
  }
  zip.file('runtime-reference/package-distribution.cjs', fs.readFileSync(__filename));
  for (const file of ['voice-v21.js', 'spaces-v21.js', 'mob-play-v21.js', 'expansion-v21.js', 'expansion-v21.css', 'assets/mita-v21.js', 'assets/mita-v21/manifest.json', 'assets/mita-v21/poses-no-tail.png']) {
    zip.file('runtime-reference/' + file, fs.readFileSync(path.join(repo, file)));
  }
  zip.file('V21_EXPANSION_REPORT.md', fs.readFileSync(path.join(repo, 'V21_EXPANSION_REPORT.md')));
  for (const file of fs.readdirSync(path.join(repo, 'verification-v21'))) {
    if (file === 'package-proof.json') continue;
    const local = path.join(repo, 'verification-v21', file);
    if (fs.statSync(local).isFile()) zip.file('verification-v21/' + file, fs.readFileSync(local));
  }
  for (const file of ['shop-life-v22.js', 'assets/mita-v21/poses-walk-v22.png']) zip.file('runtime-reference/' + file, fs.readFileSync(path.join(repo, file)));
  zip.file('V22_SHOP_AND_SPRITES_REPORT.md', fs.readFileSync(path.join(repo, 'V22_SHOP_AND_SPRITES_REPORT.md')));
  for (const file of fs.readdirSync(path.join(repo, 'verification-v22'))) {
    if (file === 'package-proof.json') continue;
    const local = path.join(repo, 'verification-v22', file);
    if (fs.statSync(local).isFile()) zip.file('verification-v22/' + file, fs.readFileSync(local));
  }
  for (const file of ['player-v24.js', 'neighborhood-v24.js', 'life-v24.js', 'life-v24-features.js', 'residents-v23.js', 'tavern-v23.js', 'assets/residents-v23.js', 'assets/shop-figures-v23.js']) zip.file('runtime-reference/' + file, fs.readFileSync(path.join(repo, file)));
  for (const dir of ['assets/residents-v23', 'assets/shop-figures-v23']) for (const file of fs.readdirSync(path.join(repo, dir))) {
    const local = path.join(repo, dir, file);
    if (fs.statSync(local).isFile()) zip.file('runtime-reference/' + dir + '/' + file, fs.readFileSync(local));
  }
  zip.file('V23_RESIDENTS_AND_TAVERN_REPORT.md', fs.readFileSync(path.join(repo, 'V23_RESIDENTS_AND_TAVERN_REPORT.md')));
  for (const file of fs.readdirSync(path.join(repo, 'verification-v23'))) {
    if (file === 'package-proof.json') continue;
    const local = path.join(repo, 'verification-v23', file);
    if (fs.statSync(local).isFile()) zip.file('verification-v23/' + file, fs.readFileSync(local));
  }
  zip.file('README.md', fs.readFileSync(path.join(repo, 'README.md')));
  for (const file of fs.readdirSync(path.join(repo, 'verification-v24'))) {
    const local = path.join(repo, 'verification-v24', file);
    if (fs.statSync(local).isFile() && file !== 'package-proof.json') zip.file('verification-v24/' + file, fs.readFileSync(local));
  }
  const bytes = await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE', compressionOptions: { level: 6 } });
  const check = await JSZip.loadAsync(bytes);
  const packed = check.file('MOB_CHILL_LIFE.html');
  if (!packed || !(await packed.async('nodebuffer')).equals(html)) throw Error('Game HTML missing or mismatched');
  fs.mkdirSync(outputDir, { recursive: true });
  const pending = output + '.pending';
  fs.writeFileSync(pending, bytes);
  if (hash(fs.readFileSync(pending)) !== hash(bytes)) throw Error('Archive write mismatch');
  fs.renameSync(pending, output);
  const proof = { output, bytes: bytes.length, sha256: hash(bytes), htmlBytes: html.length, htmlSha256: hash(html), mainMatches: true };
  fs.writeFileSync(path.join(repo, 'verification-v23/package-proof.json'), JSON.stringify(proof, null, 2));
  console.log(JSON.stringify(proof, null, 2));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
