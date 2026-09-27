"""PDF schedule from the canonical manufacturing identity; no second BOM."""
from pathlib import Path
from html import escape
from .manufacturing import analyse, schedule, cladding
from .documentation import axon

def included(part):
    return part['material'] in ('timber','plywood','mineral-wool','concrete-study') and not cladding(part)


def write(scene, path, revision, include_cladding=True):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    font=next(p for p in [Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),Path('C:/Windows/Fonts/arial.ttf')] if p.exists())
    if 'OBTP' not in pdfmetrics.getRegisteredFontNames():pdfmetrics.registerFont(TTFont('OBTP',str(font)))
    styles=getSampleStyleSheet()
    for st in styles.byName.values():st.fontName='OBTP'
    styles['Normal'].fontSize=8;styles['Normal'].leading=11
    def p(s):return Paragraph(escape(str(s)),styles['Normal'])
    counts=analyse(scene,True);flow=[]
    selected=[a for a in scene['parts'] if included(a)]
    counts['primary_schedule']=schedule(selected)
    byid={a['id']:a for a in scene['parts']}
    from reportlab.graphics.shapes import Drawing, Polygon
    def thumbnail(part):
        drawing=Drawing(29*mm,19*mm)
        polys=axon([part])['polygons']
        points=[v for face in polys for v in face['points']]
        lo=[min(v[k] for v in points) for k in (0,1)]
        hi=[max(v[k] for v in points) for k in (0,1)]
        scale=min(27*mm/max(1,hi[0]-lo[0]),17*mm/max(1,hi[1]-lo[1]))
        for i,face in enumerate(polys):
            xy=[c for v in face['points'] for c in ((v[0]-lo[0])*scale+mm,(v[1]-lo[1])*scale+mm)]
            drawing.add(Polygon(xy,fillColor=colors.HexColor(['#ded6c5','#c6bda9','#efe9dd'][i%3]),strokeColor=colors.HexColor('#555555'),strokeWidth=.35))
        return drawing
    sections=[('primary_schedule','Elementų žiniaraštis / Part schedule')]
    if include_cladding:sections.append(('cladding_schedule','Fasado apdaila / Separate facade cladding schedule'))
    for field,title in sections:
        if flow:flow.append(PageBreak())
        flow.extend([Paragraph('studio 9120',styles['Title']),Paragraph(title,styles['Heading2']),p(scene['config']['id']+' | '+scene['geometry_sha256'][:16]),Spacer(1,4*mm)])
        flow.append(p('PERŽIŪRA / REVIEW ONLY. Matmenys mm / Dimensions mm. Gamybinės jungtys, apdirbimas ir medžiagų klasės nepatvirtinti / Manufacturing details remain unverified.'))
        flow.append(p('Pagrindiniai kiekiai / Primary: %s types, %s pieces. Fasado apdaila / Cladding: %s types, %s pieces (excluded from primary totals).'%(counts['unique_manufactured_part_candidates'],counts['physical_pieces'],counts['cladding']['unique_types'],counts['cladding']['physical_pieces'])))
        flow.append(p('This schedule: core structure, panels and insulation only. Full-model audit totals above also retain finishes, equipment and all other non-facade parts.'))
        flow.append(p('Scheduled: '+str(len(counts[field]))+' types / '+str(sum(r['pieces'] for r in counts[field]))+' pieces. Axonometric views are individually scaled.'))
        flow.append(Spacer(1,4*mm))
        rows=[[p(x) for x in ['ID / Material','Aksonometrija','Matmenys / Dimensions','Vnt. / Qty','Paskirtis / Role']]]
        for row in counts[field]:
            d=row['definition'];dims=' × '.join(f'{n:g}' for n in d['dimensions_mm'])
            if d['slope_y'] or d['top_slope_y']:dims+='; slope '+str(d['slope_y'])+'/'+str(d['top_slope_y'])
            rows.append([p(row['type_id']+' / '+d['material']),thumbnail(byid[row['instances'][0]]),p(dims),p(row['pieces']),p(d.get('unresolved_application') or 'unspecified')])
        table=LongTable(rows,colWidths=[43*mm,32*mm,39*mm,13*mm,53*mm],repeatRows=1,hAlign='LEFT')
        table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8ece9')),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#cccccc')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        flow.append(table)
    def footer(c,doc):
        c.setFont('OBTP',7);c.drawString(15*mm,10*mm,'studio 9120 | '+revision[:12]+' | '+str(doc.page))
    SimpleDocTemplate(str(path),pagesize=(210*mm,297*mm),leftMargin=15*mm,rightMargin=15*mm,topMargin=15*mm,bottomMargin=18*mm,title='studio 9120 - part schedule',author='studio 9120').build(flow,onFirstPage=footer,onLaterPages=footer)
