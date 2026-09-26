"""Portable review package; does not claim Rhino-native PDF execution."""
import sys,json,csv,zipfile
from pathlib import Path
from obtp.model import build,parameters
from obtp.documentation import documents,component_groups,estimate
from obtp.ssp_sheets import prepare
from obtp.ssp_preview import pdf
from obtp.export import file3dm
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
for program,index,roof in [(1,2,0),(0,3,1)]:
 s=build(parameters(index,program_type=program,roof_type=roof));stem='Studio_M' if program else 'Sauna_M_Storage'
 (out/(stem+'-scene.json')).write_text(json.dumps(s,ensure_ascii=False),encoding='utf-8')
 for kind,recipe in documents(s).items():
  pdf(recipe,out/(stem+'-'+kind+'.pdf'))
  (out/(stem+'-'+kind+'-layouts.json')).write_text(json.dumps(recipe,ensure_ascii=False),encoding='utf-8')
 pdf(prepare(s),out/(stem+'-drawings.pdf'))
 rows=component_groups(s)
 with (out/(stem+'-components.csv')).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['index','family','material','count','volume_m3','source_part_ids','geometry_hash'])
  for r in rows:w.writerow([r['code'],r['example']['family'],r['example']['material'],len(r['parts']),r['m3'],';'.join(r['parts']),s['geometry_sha256']])
 (out/(stem+'-cost.json')).write_text(json.dumps(estimate(s),indent=2))
 file3dm([s],out/(stem+'.3dm'))
 print(stem,len(s['parts']),len(rows),flush=True)
