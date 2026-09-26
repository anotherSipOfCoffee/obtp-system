"""Standalone review with exact baseline/current model meshes, plans and counts."""
import base64,gzip,json,sys,io,tarfile,tempfile,subprocess
from pathlib import Path
from compare_manufacturing import module,ROOT,REPO,PINS
from obtp.export import browser_scene


def opening_diagram(before,after):
    from html import escape
    drawing=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 620" role="img" aria-label="Opening framing before and after optimization">','<rect width="920" height="620" fill="white"/>']
    for col,(scene,title) in enumerate([(before,'Before: separate infill and full top'),(after,'After: matching side plates')]):
        parts=[a for a in scene['parts'] if a['assembly']=='front-window/opening' and a['material']=='timber']
        x0=min(a['origin'][0] for a in parts);z0=min(a['origin'][2] for a in parts)
        width=max(a['origin'][0]+a['size'][0] for a in parts)-x0
        height=max(a['origin'][2]+a['size'][2] for a in parts)-z0
        scale=min(400/width,490/height);left=col*460+30;bottom=550
        drawing.append(f'<text x="{left}" y="32" font-family="Arial" font-size="18">{title}</text>')
        for a in parts:
            x,z=a['origin'][0]-x0,a['origin'][2]-z0;w,h=a['size'][0],a['size'][2]
            color='#85c6b4' if 'plate-' in a['id'] else '#ddbd8d'
            drawing.append(f'<rect x="{left+x*scale}" y="{bottom-(z+h)*scale}" width="{w*scale}" height="{h*scale}" fill="{color}" stroke="#333" stroke-width="0.7"><title>{escape(a["id"])}: {w:g} × {h:g} mm elevation</title></rect>')
        drawing.append(f'<text x="{left}" y="580" font-family="Arial" font-size="14">Same opening and footprint; sheathing omitted for clarity.</text>')
    drawing.append('<text x="30" y="608" font-family="Arial" font-size="14">Green: plates. Tan: studs and lintel. Geometry study; capacities and connections unverified.</text></svg>')
    return ''.join(drawing)


def cut_diagram(before,after):
    from html import escape
    rows=[(before,'lining-back/board-10-','Before: one back-wall lining course',60),(after,'lining-back/board-10-','After: shared extension and end cuts',160),(before,'weather-bearing-0-0/top','Before: roof bearing top rail',280),(after,'weather-bearing-0-0/top','After: repeated rails with joint seats',380)]
    drawing=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 470" role="img" aria-label="Measured before and after cut lengths">','<rect width="920" height="470" fill="white"/>']
    for scene,prefix,label,y in rows:
        parts=sorted([a for a in scene['parts'] if a['id'].startswith(prefix)],key=lambda a:a['origin'][0])
        lo=min(a['origin'][0] for a in parts);hi=max(a['origin'][0]+a['size'][0] for a in parts);scale=840/(hi-lo)
        drawing.append(f'<text x="35" y="{y-12}" font-family="Arial" font-size="17">{label}</text>')
        for a in parts:
            x=35+(a['origin'][0]-lo)*scale;w=a['size'][0]*scale
            drawing.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" fill="#a9cdbf" stroke="#344d44"/><text x="{x+w/2}" y="{y+20}" text-anchor="middle" font-family="Arial" font-size="15">{a["size"][0]:g}</text>')
    drawing.append('<text x="35" y="452" font-family="Arial" font-size="14">Lengths in mm, taken from the model. Gaps retained; strip heights enlarged for legibility.</text></svg>')
    return ''.join(drawing)


def render(destination,baseline_root=None):
    if baseline_root is None:
        with tempfile.TemporaryDirectory() as temp:
            for name,sha in PINS.items():
                target=Path(temp)/name;target.mkdir()
                data=subprocess.check_output(['git','-C',str(REPO),'archive',sha,'authoring/grasshopper'])
                with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(target,filter='data')
            return render(destination,temp)
    out=Path(destination);report=json.loads(gzip.decompress((out/'manufacturing-comparison.json.gz').read_bytes()))
    models={'original':module(Path(baseline_root)/'original/authoring/grasshopper','visual_original'),
            'cells':module(Path(baseline_root)/'cells/authoring/grasshopper','visual_cells'),
            'revised':module(ROOT,'visual_revised')}
    data={}
    for program in range(2):
        for name,m in models.items():
            s=m.build(m.parameters(2,program_type=program,roof_type=0))
            data[('studio' if program else 'sauna')+'-'+name]=base64.b64encode(gzip.compress(json.dumps(browser_scene(s),separators=(',',':')).encode(),mtime=0)).decode()
    previous=module(Path(baseline_root)/'pre_opening/authoring/grasshopper','visual_pre_opening')
    diagram=opening_diagram(previous.build(previous.parameters(2,roof_type=0)),models['revised'].build(models['revised'].parameters(2,roof_type=0)))
    (out/'opening-detail.svg').write_text(diagram)
    corrected=module(Path(baseline_root)/'pre_kit_corrected/authoring/grasshopper','visual_corrected')
    cuts=cut_diagram(corrected.build(corrected.parameters(2,roof_type=0)),models['revised'].build(models['revised'].parameters(2,roof_type=0)))
    (out/'kit-cut-comparison.svg').write_text(cuts)
    script=(REPO/'dist/mesh-view.js').read_text()
    cards=[]
    for program in ['sauna','studio']:
        for name,label in [('original','Original'),('cells','First cell system'),('revised','Revised')]:
            key=program+'-'+name
            plan=(out/(key+'-plan.svg')).read_text()
            cards.append(f'<article><h3>{program.title()} · {label}</h3><canvas id="{key}"></canvas><details><summary>Model-derived plan</summary>{plan}</details></article>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>studio 9120 — System review</title>
<style>*{box-sizing:border-box}body{margin:0 auto;max-width:1600px;padding:28px;font:16px/1.5 Arial,sans-serif;color:#252525;background:#fff}h1{font-size:32px;font-weight:500}h2{margin-top:36px}p{max-width:1050px}button{font:inherit;padding:8px 14px;margin-right:8px;background:white;border:1px solid #999;cursor:pointer}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}article{border:1px solid #ccc;padding:12px;min-width:0}h3{font-size:18px;font-weight:500}canvas{width:100%;height:330px}svg{width:100%;height:auto}table{border-collapse:collapse;width:100%;margin:20px 0}td,th{border-bottom:1px solid #ddd;padding:8px;text-align:left}.scroll{overflow-x:auto}.note{padding:14px;background:#f0f3f5}summary{cursor:pointer}small{color:#555}@media(max-width:850px){.grid{grid-template-columns:1fr}body{padding:16px}}</style>
<h1>studio 9120 — construction-system review</h1>
<p class="note"><b>The 75% target was not achieved.</b> These are provisional manufacturing candidate types, not certified interchangeable parts. The same counting rules and façade-board exclusion apply to all three snapshots. No release for construction is implied.</p>
<p>216 supported selections: 72 Sauna and 144 Studio configurations. Catalogue totals are unions of types; piece totals mean one of every selection. Façade finish boards remain visible. Battens, trims, insulation and object representations remain in primary counts.</p>
<div id="totals"></div><h2>Architecture and terrace direction</h2><p>M / no storage / flat roof / 1180 mm window / timber foundation. Drag or scroll each view. Plans are drawn from the same geometry. The revised Sauna is 2400 mm wide, down from 3600 mm in the first cell system; Studio remains 2400 mm.</p>
<button id="full">Complete model</button><button id="deck">Terrace and floor</button><button id="rotate">Rotate all views</button><p id="status" role="status">Loading model comparison…</p><div class="grid">CARDS</div>
<h2>Same-footprint control</h2><p>Finished interior area uses the same finish deductions in all three snapshots; the original Sauna’s historical gross-inside metric is normalized in this audit.</p><div id="control"></div><h2>Effect of excluding façade boards</h2><p>This exclusion is applied equally before calculating design improvements; it does not contribute to the reduction percentages.</p><div id="exclusion"></div>
<h2>Repeated cuts, same architecture</h2><p>The geometry-repairs-only row isolates corrected intersections from the repeated-cut recipes. Ordinary bays and opening positions are retained. Long roof rails use 900 mm cuts with actual studs at their joints; facade battens use supported 1800 mm cuts. Interior lining keeps constant short runs and reuses 900/1800 mm extensions with recurring room-end cuts. Every constituent and added support remains counted.</p>CUT_DIAGRAM<h2>Retained opening detail</h2>OPENING_DIAGRAM<h2>What changed</h2><ul><li>Shared 2400 mm width aligns floor and roof lengths across both buildings. The 900 × 1200 planning grid and room sequence remain.</li><li>Foundation bearings normally repeat at 1800 × 1200 mm, with explicit terminal bays. Beam cuts end at actual supports.</li><li>Terrace boards run in X throughout both complete terraces, with supported joints and a maximum 1800 mm cut length. Continuous return joists close the corner with the same 5 mm board gap.</li><li>Opening side frames use matching top/bottom plates. The centre top plate reuses standard 900/1200 mm cuts where the opening width matches. Jack studs retain direct bearing under the lintel. The pre_opening row isolates this change at identical building dimensions.</li><li>Studio’s firewood-niche floor retains two continuous joists and six packing pieces on the shared foundation; all eight added pieces are counted.</li><li>One normal Grasshopper preview replaces the many object-type switches. Single-option GH controls are removed; PDF export remains disabled.</li><li>Immutable Git baseline snapshots replace duplicated baseline generation in the website export. Source hashes guard against stale comparisons.</li></ul>
<p>Terminal widths remain explicit exceptions: 705 mm at deducted corners and 588 mm at Studio’s niche. Extending a 900 mm member through a corner would require overlap or distinct machining; it is not counted as reuse.</p><h2>Tradeoffs and rejected experiment</h2><p>The reduced Sauna width removes 1200 mm of room depth relative to the first cell system; it is still 210 mm wider than the original structural shell. Foundation supports decrease, while shorter terrace boards and framed opening infill increase some piece counts. Studio's typical part diversity slightly increases relative to the first cell system. The same-footprint and geometry-repairs-only comparisons separate resizing, repairs and repeated cuts. Fewer catalogue types can require more physical pieces; the table reports both.</p><p>A 900 mm interior-board experiment increased typical building piece counts by about 400 and added many joints. Its added pieces and joints were excessive. The adopted recipe preserves short constant lengths and splits only selected variable runs, with supported joints.</p>
<h2>Prefabrication and unresolved engineering</h2><p>Repeated floor/roof strips and solid wall frames are candidates for jig-built subassemblies. Assembly counts describe geometric groups, not certified lifting units. No mass, crew-size capacity or crane-free installation has been verified: larger floor/roof groups should be assembled from loose parts or smaller subassemblies until handling is assessed.</p><p>Material grades, profiles, grain, machining, handedness, connector locations and fastener schedules remain incomplete. Foundation capacity, longer support spacing, roof uplift/cantilevers, opening headers, bracing, moisture layers, heater/fire clearances, glazing and native Rhino/GH acceptance remain unresolved. Modelled product subparts are placeholders; unmodelled fasteners, tapes and seals have unknown counts in every version. No category was excluded to hide these gaps.</p>
<small id="pins"></small><script>RENDERER</script><script>
const report=REPORT,encoded=DATA,views=[];
const fmt=n=>Number.isInteger(n)?n:n.toFixed(2);const table=(heads,rows)=>'<div class="scroll"><table><thead><tr>'+heads.map(x=>'<th>'+x+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map(x=>'<td>'+x+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';
const versions=['original','cells','pre_opening','pre_kit','pre_kit_corrected','revised_same_footprint','revised'];
const labels={original:'Original',cells:'First cells',pre_opening:'Before opening revision',pre_kit:'Before shared cuts',pre_kit_corrected:'Geometry repairs only',revised_same_footprint:'Current at first-cell footprint',revised:'Current shared cuts'};
document.getElementById('totals').innerHTML=table(['Catalogue','Sauna types','Studio types','Combined types'],versions.map(v=>[labels[v],...['sauna','studio','combined'].map(p=>report.catalogue[v][p].unique_manufactured_part_candidates)]));
const defaults=report.rows.filter(r=>r.key.includes('-m-open-r0-w1180-b0-winter'));
document.getElementById('control').innerHTML=table(['Building / version','Candidate types','Pieces','Cladding pieces','Assemblies: types / installed','Usable m²','Wood m³'],defaults.flatMap(r=>versions.map(v=>{const a=r.versions[v];return[r.program+' / '+labels[v],a.unique_manufactured_part_candidates,a.physical_pieces,a.cladding.physical_pieces,a.unique_assembly_candidates+' / '+a.assemblies_installed,fmt(a.usable_area_m2),fmt(a.wood_m3)];})));
document.getElementById('exclusion').innerHTML=table(['Building / version','Types including façade','Primary types','Exclusion effect','Cladding pieces'],defaults.flatMap(r=>['original','cells','revised'].map(v=>{const a=r.versions[v];return[r.program+' / '+labels[v],a.unique_types_including_cladding,a.unique_manufactured_part_candidates,a.cladding_exclusion_type_effect,a.cladding.physical_pieces];})));
document.getElementById('pins').textContent='Original: '+report.baseline_commits.original+' · First cells: '+report.baseline_commits.cells;
(async()=>{for(const [id,base64]of Object.entries(encoded)){const bytes=Uint8Array.from(atob(base64),c=>c.charCodeAt(0));const text=await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).text();const scene=JSON.parse(text);const view=new SourceMeshView(document.getElementById(id));view.arctic=true;view.angle=-Math.PI/4;view.elev=.55;scene.models.forEach(m=>view.register(m));view.setScene(scene.items);views.push({view,scene});}document.getElementById('status').textContent='All six source-model comparisons loaded.';window.REVIEW_READY=true;})().catch(e=>document.getElementById('status').textContent=e.message);
document.getElementById('full').onclick=()=>views.forEach(({view,scene})=>view.setScene(scene.items));document.getElementById('deck').onclick=()=>views.forEach(({view,scene})=>view.setScene(scene.items.filter(i=>['terrace','floor','foundation'].includes(i.stage))));document.getElementById('rotate').onclick=()=>views.forEach(({view})=>{view.angle+=Math.PI/2;view.draw();});
</script></html>'''
    compact=dict(report);compact['rows']=[r for r in report['rows'] if '-m-open-r0-w1180-b0-winter' in r['key']]
    html=html.replace('CUT_DIAGRAM',cuts).replace('OPENING_DIAGRAM',diagram).replace('CARDS',''.join(cards)).replace('RENDERER',script).replace('REPORT',json.dumps(compact,separators=(',',':'))).replace('DATA',json.dumps(data,separators=(',',':')))
    (out/'index.html').write_text(html)
    print('Standalone model review:',out/'index.html')

if __name__=='__main__':render(sys.argv[1])
