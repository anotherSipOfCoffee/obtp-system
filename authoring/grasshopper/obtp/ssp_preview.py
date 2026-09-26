"""Offline proof renderer. Never presented as a Rhino-printed PDF."""
from pathlib import Path
import math
from .drawings import dimension_lines

def pdf(recipe,path):
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.units import mm
    font=next(p for p in [Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),Path('C:/Windows/Fonts/arial.ttf')] if p.exists())
    if 'OBTP' not in pdfmetrics.getRegisteredFontNames():pdfmetrics.registerFont(TTFont('OBTP',str(font)))
    c=canvas.Canvas(str(path),pagesize=(420*mm,297*mm));c.setTitle('OBTP R12 - offline layout proof');c.setAuthor('OBTP')
    def text(x,y,t,size):c.setFillColor('#111111');c.setFont('OBTP',size);c.drawString(x,y,str(t))
    for sheet in recipe['sheets']:
        c.scale(mm,mm);c.setStrokeColor('#222222');c.setLineWidth(.2)
        for a,b in sheet['lines']:c.line(*a,*b)
        for a in sheet['texts']:text(*a['at'],a['text'],a['size'])
        for detail in sheet['details']:
            v=detail['view'];x,y,X,Y=detail['box'];scale=detail['scale'];cx,cy=detail['center']
            def pt(p):return ((x+X)/2+(p[0]-cx)/scale,(y+Y)/2+(p[1]-cy)/scale)
            c.saveState();clip=c.beginPath();clip.rect(x,y,X-x,Y-y);c.clipPath(clip,stroke=0,fill=0)
            for poly in v['polygons']:
                pts=[pt(p) for p in poly['points']];path=c.beginPath();path.moveTo(*pts[0])
                for q in pts[1:]:path.lineTo(*q)
                path.close();c.setFillColor(poly.get('fill','#eeeeee' if poly['material']=='glass' else '#ffffff') if not poly.get('cut') else '#ffffff');c.setStrokeColor('#222222');c.setLineWidth(.30 if poly.get('cut') else .12);c.drawPath(path,fill=1,stroke=1)
                if poly.get('cut') and poly['material'] in ['timber','plywood','lining-wood','cladding-wood','deck-wood','mineral-wool']:
                    c.saveState();c.clipPath(path,stroke=0,fill=0);c.setStrokeColor('#888888');c.setLineWidth(.08)
                    a=min(q[0] for q in pts);b=max(q[0] for q in pts);l=min(q[1] for q in pts);h=max(q[1] for q in pts)
                    if poly['material']=='mineral-wool':
                        horizontal=b-a>=h-l;lo,hi=(a,b) if horizontal else (l,h);v0,v1=(l,h) if horizontal else (a,b)
                        wave=c.beginPath();stride=max(2,min(6,(v1-v0)*.65))
                        for j in range(int((hi-lo)/.15)+2):
                            t=min(hi,lo+j*.15);q=(v0+v1)/2+(v1-v0)*.43*math.sin((t-lo)/stride*2*math.pi);u,w=(t,q) if horizontal else (q,t)
                            if j:wave.lineTo(u,w)
                            else:wave.moveTo(u,w)
                        c.drawPath(wave)
                    else:
                        spacing=1 if poly['material']=='plywood' else 2.5
                        for i in range(math.floor((a-h)/spacing),math.ceil((b-l)/spacing)+1):c.line(i*spacing+l,l,i*spacing+h,h)
                    c.restoreState()
            c.setStrokeColor('#222222');c.setLineWidth(.18)
            for guide in v.get('guides',[]):
                c.setDash([4,1,1,1]);c.setLineWidth(.1)
                for a,b in zip(guide['points'],guide['points'][1:]):c.line(*pt(a),*pt(b))
                c.setDash();c.setLineWidth(.18)
            for line in v['polylines']:
                for a,b in zip(line,line[1:]):c.line(*pt(a),*pt(b))
            for label in v.get('labels',[]):text(*pt(label['at']),label['text'],2.5)
            for dim in v['dimensions']:
                lines,at,label=dimension_lines(dim)
                for a,b in lines:c.line(*pt(a),*pt(b))
                for a in lines[-1]:
                    u,w=pt(a);c.line(u-1,w-1,u+1,w+1)
                u,w=pt(at);c.setFillColor('#ffffff');c.rect(u-1,w+.3,len(label)*1.6+2,3.5,fill=1,stroke=0);text(u,w+1,label,2.5)
            c.restoreState()
        text(25,10.8,'Maketo peržiūra / ne Rhino spausdinys',1.7)
        c.showPage()
    c.save()
