"""PDF schedule from the canonical manufacturing identity; no second BOM."""
from pathlib import Path
from html import escape
from .manufacturing import analyse


def write(scene, path, revision):
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
    for field,title in [('primary_schedule','Elementų žiniaraštis / Part schedule'),('cladding_schedule','Fasado apdaila / Separate facade cladding schedule')]:
        if flow:flow.append(PageBreak())
        flow.extend([Paragraph('studio 9120',styles['Title']),Paragraph(title,styles['Heading2']),p(scene['config']['id']+' | '+scene['geometry_sha256'][:16]),Spacer(1,4*mm)])
        flow.append(p('PERŽIŪRA / REVIEW ONLY. Matmenys mm / Dimensions mm. Gamybinės jungtys, apdirbimas ir medžiagų klasės nepatvirtinti / Manufacturing details remain unverified.'))
        flow.append(p('Pagrindiniai kiekiai / Primary: %s types, %s pieces. Fasado apdaila / Cladding: %s types, %s pieces (excluded from primary totals).'%(counts['unique_manufactured_part_candidates'],counts['physical_pieces'],counts['cladding']['unique_types'],counts['cladding']['physical_pieces'])))
        flow.append(Spacer(1,4*mm))
        rows=[[p(x) for x in ['ID','Medžiaga / Material','Matmenys / Dimensions','Vnt. / Qty','Paskirtis / Role']]]
        for row in counts[field]:
            d=row['definition'];dims=' × '.join(f'{n:g}' for n in d['dimensions_mm'])
            if d['slope_y'] or d['top_slope_y']:dims+='; slope '+str(d['slope_y'])+'/'+str(d['top_slope_y'])
            rows.append([p(row['type_id']),p(d['material']),p(dims),p(row['pieces']),p(d.get('unresolved_application') or 'unspecified')])
        table=LongTable(rows,colWidths=[45*mm,32*mm,40*mm,15*mm,48*mm],repeatRows=1,hAlign='LEFT')
        table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8ece9')),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#cccccc')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        flow.append(table)
    def footer(c,doc):
        c.setFont('OBTP',7);c.drawString(15*mm,10*mm,'studio 9120 | '+revision[:12]+' | '+str(doc.page))
    SimpleDocTemplate(str(path),pagesize=(210*mm,297*mm),leftMargin=15*mm,rightMargin=15*mm,topMargin=15*mm,bottomMargin=18*mm,title='studio 9120 - part schedule',author='studio 9120').build(flow,onFirstPage=footer,onLaterPages=footer)
