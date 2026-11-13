const fs=require('node:fs');const vm=require('node:vm');const assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/index.html','utf8');const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];new vm.Script(script);
const extract=script.slice(script.indexOf('function extractEvidence'),script.indexOf('function resetReview'));
const validate=script.slice(script.indexOf('function validateLibrary'),script.indexOf('function exportTemplate'));
const ctx=vm.createContext({});vm.runInContext(extract+'\n'+validate,ctx);
const items=[{id:'mood',phrases:['low mood']},{id:'psychosis',phrases:['hallucinations']},{id:'activation',phrases:['racing thoughts']},{id:'fear',phrases:['fear']}];
let r=ctx.extractEvidence('Patient reports low mood. Patient denies hallucinations. Father had racing thoughts.',items);
assert.equal(r.mood.length,1);assert.equal(r.psychosis[0].classification,'unclassified');assert.equal(r.activation[0].classification,'unclassified');assert.equal(r.fear.length,0);
assert.equal(ctx.extractEvidence('Fearful but no fear.',items).fear.length,1);
assert.equal(ctx.extractEvidence('Fearful.',items).fear.length,0);
assert.equal(ctx.extractEvidence('test a+b?', [{id:'x',phrases:['a+b']}]).x.length,1);
assert.equal(ctx.extractEvidence('No text matches.',items).mood.length,0);
const valid={name:'Example',version:'1',source:'Authorized source',items:[{id:'a',label:'Example',phrases:['test']}]};assert.equal(ctx.validateLibrary(valid),valid);
for(const bad of [{}, {...valid,items:[]}, {...valid,items:[...valid.items,...valid.items]}, {...valid,items:[{id:'x',label:'x',phrases:['']}]}, {...valid,items:[{id:'x',label:'x',phrases:[' '.repeat(4)]}]}])assert.throws(()=>ctx.validateLibrary(bad));
const proto=ctx.extractEvidence('test',[{id:'__proto__',phrases:['test']}]);assert.equal(proto['__proto__'].length,1);
console.log('Passed: script syntax, evidence boundaries/literals, unclassified contextual hits, missing evidence, import validation, prototype-safe evidence keys.');

const data=JSON.parse(html.match(/<script type="application\/json" id="knowledge-data">([\s\S]*?)<\/script>/)[1]);
assert.equal(data.sources.length,10);assert.equal(data.cards.length,72);assert.equal(data.products.length,6);
const sourceIds=new Set(data.sources.map(s=>s.id));const ids=new Set();
for(const card of data.cards){assert(!ids.has(card.id));ids.add(card.id);assert(sourceIds.has(card.source));assert(card.areas.length);const source=data.sources.find(s=>s.id===card.source);for(const p of card.pages)assert(p>=1&&p<=source.pages);assert(card.bullets.every(b=>b.trim()));}
for(const product of data.products){assert(product.strengths&&product.indication&&product.form&&product.sig&&product.cautions);assert(product.url.startsWith('https://'));}
assert(data.cards.filter(c=>c.status==='Primary-source update').length===10);
const searchCtx=vm.createContext({});const searchCode=script.slice(script.indexOf('function matchesReference'),script.indexOf('function refreshReference'));vm.runInContext(searchCode,searchCtx);
assert(searchCtx.matchesReference('Sertraline Zoloft SSRI','zoloft ssri'));assert(!searchCtx.matchesReference('Sertraline Zoloft','zolpidem'));
for(const area of ['diagnoses','medications','supplements','therapies','education']){assert(html.includes('reference-results-'+area));assert(data.cards.some(c=>c.areas.includes(area)));}
assert.equal(JSON.stringify(data),JSON.stringify(JSON.parse(fs.readFileSync(__dirname+'/knowledge.json','utf8'))));
console.log('Passed: ten-source provenance, page references, 72 cards, six distinct product regimens, correction tags, search matching, five topic destinations, and embedded/JSON data consistency.');
