"""A3 landscape vector review sheets. Measurements arrive from drawings.py."""
from pathlib import Path
from .drawings import dimension_lines

def pdf(scene,path):
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.units import mm
    font=next((p for p in [Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),Path('C:/Windows/Fonts/arial.ttf')] if p.exists()),None)
    if font is None:raise RuntimeError('Install DejaVu Sans or Arial for Lithuanian PDF text')
    if 'OBTP' not in pdfmetrics.getRegisteredFontNames():pdfmetrics.registerFont(TTFont('OBTP',str(font)))
    c=canvas.Canvas(str(path),pagesize=(420*mm,297*mm));c.setTitle('OBTP / '+scene['config']['id']);c.setAuthor('OBTP');c.scale(mm,mm)
    def text(x,y,t,size=2.5):c.setFont('OBTP',size);c.drawString(x,y,str(t))
    def line(a,b):c.line(*a,*b)
    def title(n,name,scale):
        c.setLineWidth(.25);c.rect(20,10,390,277);text(25,278,'obtp. / studio',5);text(25,269,name,4)
        # 180 x 45 mm construction-drawing arrangement documented by VIKO,
        # figure 6, LST 1516-based teaching template; professional fields left blank.
        x,y=230,10;c.rect(x,y,180,45)
        for yy in [25,40]:line((230,yy),(410,yy))
        line((320,10),(320,55))
        for yy in [30,35]:line((230,yy),(320,yy))
        for xx in [245,265,290,305]:line((xx,25),(xx,40))
        line((245,10),(245,25));line((230,20),(245,20))
        line((395,25),(395,40));line((395,35),(410,35))
        for xx in [380,395]:line((xx,10),(xx,25))
        line((380,20),(410,20))
        text(233,48,'obtp. / studio',4)
        text(233,43,'Projektavimo studija / ne statybai',2.3)
        text(322,51,'Statinio projekto pavadinimas',1.8)
        text(322,44,'Modulinė pirtis '+scene['config']['size'],3)
        for yy,label in [(36.5,'PV'),(31.5,'PDV'),(26.5,'Parengė')]:text(246,yy,label,2)
        text(231,21,'Kalba',1.8);text(233,13,'LT',2.5)
        text(248,19,'Užsakovas / vieta: tikslinama',2.2)
        text(248,13,'Modelio versija R04',2.2)
        text(322,36.5,'Brėžinio pavadinimas',1.8)
        text(322,30,name[:45],2 if len(name)>30 else 2.5)
        text(396,36.5,'Laida',1.8);text(400,29,'0',2.5)
        text(322,21,'Dokumento žymuo',1.8)
        text(322,16,'OBTP-'+scene['config']['id'].upper()+'-'+str(n).zfill(2),1.8)
        text(322,12,'M '+scale+' / A3',2)
        text(381,21,'Lapas',1.8);text(396,21,'Lapų',1.8)
        text(386,13,n,2.5);text(400,13,4,2.5)
        text(25,27,'Parengė / tikrino: ____________________',2.5)
        text(25,21,'Užsakovas / vieta: ____________________',2.5)
        text(25,15,'Modelis '+scene['geometry_sha256'][:16]+' | 2026-09-26',2)
    def page():c.showPage();c.scale(mm,mm)
    def view(name,ox,oy,scale):
        v=scene['drawings']['views'][name];s=1/scale
        def point(p):return ox+p[0]*s,oy+p[1]*s
        for a in v['polygons']:
            if not a['points']:continue
            pp=c.beginPath();pp.moveTo(*point(a['points'][0]))
            for p in a['points'][1:]:pp.lineTo(*point(p))
            pp.close();c.setFillColor(a['fill']);c.setStrokeColor('#333333');c.setLineWidth(.12 if a['fill']!='#111111' else .18);c.drawPath(pp,fill=1,stroke=1)
        c.setFillColor('#000000');c.setStrokeColor('#111111');c.setLineWidth(.18)
        for a in v['polylines']:
            for p,q in zip(a,a[1:]):line(point(p),point(q))
        for a in v.get('labels',[]):
            x,y=point(a['at']);c.setFont('OBTP',2.3);c.drawCentredString(x,y,a['text'])
        for d in v['dimensions']:
            lines,pt,label=dimension_lines(d);c.setLineWidth(.13)
            for a,b in lines:line(point(a),point(b))
            for p in lines[-1]:
                x,y=point(p);line((x-1,y-1),(x+1,y+1))
            x,y=point(pt);text(x+1,y+1,label,2.5)
    title(1,'Planas','1:50');view('plan',65,150,50)
    v=scene['drawings'];L=scene['dimensions']['length_mm']+scene['dimensions']['annex_length_mm'];W=scene['dimensions']['width_mm']
    for m in v['cut_markers']:
        c.setDash(3,1);c.setLineWidth(.2)
        if m['axis']==0:
            x=65+m['position']/50;line((x,143),(x,150+W/50+7));text(x+2,140,m['name'])
        else:
            y=150+m['position']/50;line((58,y),(65+L/50+7,y));text(45,y+5,m['name'])
        c.setDash()
    text(250,237,'Pasirinkta konfigūracija',4)
    cfg=scene['config'];roof=['Plokščias','Vienšlaitis','Dvišlaitis'][cfg['roof_type']]
    for i,t in enumerate(['Dydis: '+cfg['size'],'Sandėliukas: '+('taip' if cfg['storage'] else 'ne'),'Stogas: '+roof,'Terasa: '+str(cfg['terrace_steps']*600)+' mm','Langas: '+str(cfg['window_width'])+' × '+str(cfg['door_height'])+' mm','Fasadas: vertikalios dailylentės']):text(250,225-i*8,t,3)
    text(25,83,'Planas 1 100 mm virš grindų. Juoda - kertamos sienos. Matmenys pagal konstrukcijos paviršius.',2.5)
    text(25,76,'Durų ir lauko suolo simboliai iš užsakovo DXF; pirties suolai projektuojami iš 3D.',2.5)
    page();title(2,'Pjūviai A-A ir B-B','1:50')
    view('section-a',55,130,50);view('section-b',215,130,50)
    text(50,252,'A-A / skersinis pjūvis',3);text(215,252,'B-B / išilginis pjūvis',3)
    text(25,85,'Pjūviai ir matmenys iš to paties 3D modelio. Aukščiai nuo modelio ±0,000.',2.5)
    text(25,77,'Šiltinimo ir stogo mazgai - tikrinamas sprendinys. Krosnelė ir vėdinimas dar neparinkti.',2.5)
    page();title(3,'L1 / lango žiniaraštis','1:10')
    view('window',45,76,10);view('window-plan',235,205,10)
    text(235,223,'L1 / horizontalus pjūvis',3)
    for i,t in enumerate(['Kiekis: 1 vnt.','Angos plotis: '+str(cfg['window_width'])+' mm','Angos aukštis: '+str(cfg['door_height'])+' mm','Apačia: grindų lygis','Viršus: sutampa su durų viršumi','Rėmas ir stiklas: tikslinami','Varstymas: neparinktas']):text(235,175-i*8,t,3)
    c.setFillColor('#d71920');c.rect(235,91,32,9,fill=1,stroke=0);c.setFillColor('#ffffff');text(238,93,'VELUX',5);c.setFillColor('#000000')
    text(272,95,'Nuoroda / reference',2.5);text(235,85,'Gamintojas šiam fasado langui neparinktas.',2.3)
    page();title(4,'Detalės / vieta būsimiems mazgams','-')
    for i,label in enumerate(['D1 / Lango mazgas','D2 / Durų mazgas','D3 / Sienų kampas']):
        x=25+i*127;c.setLineWidth(.2);c.rect(x,100,120,150);text(x+4,254,label,3)
    text(25,86,'Detalės nepateiktos. Rėmeliai rezervuoti suderintiems konstrukcijų mazgams.',2.5)
    text(25,77,'Pagrindinis įrašas: 180 × 45 mm, pagal VIKO LST 1516 pagrįstą pavyzdį; projektas nepatvirtintas.',2.5)
    c.save()
