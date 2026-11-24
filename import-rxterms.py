"""Build the offline catalog from an official RxTerms monthly ZIP. No third-party packages needed.
Usage: python3 import-rxterms.py /path/to/RxTermsYYYYMM.zip
"""
import csv,io,json,zipfile,sys,hashlib,re
from pathlib import Path
archive=Path(sys.argv[1]);release=re.search(r'RxTerms(\d{6})',archive.name).group(1);z=zipfile.ZipFile(archive)
name=next(n for n in z.namelist() if Path(n).name=='RxTerms'+release+'.txt')
rows=list(csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig')),delimiter='|'))
groups={};excluded=0
for r in rows:
 if r['IS_RETIRED'] or r['SUPPRESS_FOR'] or r['TTY'] not in ('SCD','SBD'):
  excluded+=1;continue
 key=r['DISPLAY_NAME'];g=groups.setdefault(key,{'name':key,'brand':r['BRAND_NAME'],'route':r['ROUTE'],'aliases':[],'variants':[]})
 for alias in r['DISPLAY_NAME_SYNONYM'].split(';'):
  if alias.strip() and alias.strip() not in g['aliases']:g['aliases'].append(alias.strip())
 # Keep original full descriptions: combination strength order cannot safely be inferred from shorthand.
 g['variants'].append({'rxcui':r['RXCUI'],'genericRxcui':r['GENERIC_RXCUI'],'form':r['RXN_DOSE_FORM'],'strength':r['STRENGTH'],'name':r['FULL_NAME'],'generic':r['FULL_GENERIC_NAME']})
result={'source':'NLM RxTerms','release':release,'sourceUrl':'https://data.lhncbc.nlm.nih.gov/public/rxterms/release/'+archive.name,'documentation':'https://lhncbc.nlm.nih.gov/MOR/RxTerms/','sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'sourceRows':len(rows),'excludedRows':excluded,'scope':'Active, unsuppressed SCD/SBD records. Packs excluded. Listed U.S. strengths and forms; not guaranteed local stock, approval status or recommended treatment doses.','groups':sorted(groups.values(),key=lambda g:g['name'].lower())}
root=Path(__file__).parent;payload=json.dumps(result,separators=(',',':'),ensure_ascii=False);(root/'rxterms-catalog.json').write_text(payload+'\n')
index=root/'index.html';s=index.read_text();tag='<script id="rxterms-catalog-data" type="application/json">'+payload.replace('<','\\u003c')+'</script>'
if 'id="rxterms-catalog-data"' in s:s=re.sub(r'<script id="rxterms-catalog-data" type="application/json">.*?</script>',lambda _:tag,s,flags=re.S)
else:s=s.replace("<script>\n'use strict';",tag+"<script>\n'use strict';",1)
# Refresh the mental-health name-group mappings when that optional directory is installed.
mh_path=root/'mental-health-medications.json'
if mh_path.exists():
 mh=json.loads(mh_path.read_text())
 def normalized(value):return ' '+re.sub(r'[^a-z0-9]+',' ',value.lower()).strip()+' '
 cached=[(g,[normalized(v['generic']) for v in g['variants']],normalized(g['brand'])) for g in result['groups']]
 for med in mh['medications']:
  med['rxGroups']=[g['name'] for g,names,brand in cached if any(any(all(normalized(part) in name for part in term.split('/')) for name in names) for term in med['terms']) or any(normalized(alias) in brand for alias in med['aliases'])]
 for med in mh['medications']:
  med['rxGroups']=[name for name in med['rxGroups'] if not any(term.lower() in name.lower() for term in med.get('excludeGroupTerms',[]))]
 mh['rxTermsRelease']=release;mh_path.write_text(json.dumps(mh,indent=2)+'\n')
 mh_tag='<script id="mental-health-medications-data" type="application/json">'+json.dumps(mh,separators=(',',':')).replace('<','\\u003c')+'</script>'
 s=re.sub(r'<script id="mental-health-medications-data" type="application/json">.*?</script>',lambda _:mh_tag,s,flags=re.S)
index.write_text(s);print(len(groups),'groups,',sum(len(g['variants']) for g in groups.values()),'strength/form records')
