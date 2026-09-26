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
    def brand(file,label,x,y,w=40,h=12):
        asset=Path(__file__).resolve().parents[1]/'suppliers'/'assets'/file
        if asset.exists():
            from reportlab.lib.utils import ImageReader
            im=ImageReader(str(asset));iw,ih=im.getSize();scale=min(w/iw,h/ih)
            c.drawImage(im,x,y,width=iw*scale,height=ih*scale,mask='auto')
        else:text(x,y,label,4)

    studio=scene['config'].get('program_type',0)==1
    product_name='Modulinė studija' if studio else 'Modulinė pirtis'
    def title(n,name,scale):
        c.setFillColor('#111111');c.setStrokeColor('#111111')
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
        text(233,43,'Gaminio techninė byla / ne statybai',2.3)
        text(322,51,'Gaminio pavadinimas',1.8)
        text(322,44,product_name+' '+scene['config']['size'],3)
        for yy,label in [(36.5,'PV'),(31.5,'PDV'),(26.5,'Parengė')]:text(246,yy,label,2)
        text(231,21,'Kalba',1.8);text(233,13,'LT',2.5)
        text(248,19,'Užsakovas / vieta: tikslinama',2.2)
        text(248,13,'Modelio versija '+scene['version'],2.2)
        text(322,36.5,'Brėžinio pavadinimas',1.8)
        text(322,30,name[:45],2 if len(name)>30 else 2.5)
        text(396,36.5,'Laida',1.8);text(400,29,'0',2.5)
        text(322,21,'Dokumento žymuo',1.8)
        text(322,16,'OBTP-'+scene['config']['id'].upper()+'-'+str(n).zfill(2),1.8)
        text(322,12,'M '+scale+' / A3',2)
        text(381,21,'Lapas',1.8);text(396,21,'Lapų',1.8)
        text(386,13,n,2.5);text(400,13,9,2.5)
        text(25,15,'Modelis '+scene['geometry_sha256'][:16]+' | 2026-09-26',2)
    def page():c.showPage();c.scale(mm,mm)
    def hatch(points,material):
        # Paper-space patterns, clipped to the exact model intersection polygon.
        # Timber / plywood / fibrous insulation / concrete remain distinguishable.
        if material not in ['timber','plywood','lining-wood','cladding-wood','deck-wood','mineral-wool','concrete-study']:return
        c.saveState();path=c.beginPath();path.moveTo(*points[0])
        for q in points[1:]:path.lineTo(*q)
        path.close();c.clipPath(path,stroke=0,fill=0)
        x0=min(q[0] for q in points);x1=max(q[0] for q in points);y0=min(q[1] for q in points);y1=max(q[1] for q in points)
        c.setStrokeColor('#777777');c.setLineWidth(.09)
        import math
        if material=='mineral-wool':
            # Continuous fibrous batt symbol, with loop depth governed by cavity.
            horizontal=(x1-x0)>=(y1-y0)
            lo,hi=(x0,x1) if horizontal else (y0,y1);v0,v1=(y0,y1) if horizontal else (x0,x1)
            stride=min(6,max(2,(v1-v0)*.65));amp=(v1-v0)*.43;mid=(v0+v1)/2
            pp=c.beginPath()
            for i in range(int((hi-lo)/.15)+2):
                t=min(hi,lo+i*.15);v=mid+amp*math.sin((t-lo)/stride*2*math.pi);q=(t,v) if horizontal else (v,t)
                if i:pp.lineTo(*q)
                else:pp.moveTo(*q)
            c.drawPath(pp)
        elif material=='concrete-study':
            c.setFillColor('#777777')
            for i in range(math.floor(x0/2),math.ceil(x1/2)+1):
                for j in range(math.floor(y0/2),math.ceil(y1/2)+1):c.circle(i*2+(j%2)*.7,j*2,.13,fill=1,stroke=0)
        else:
            spacing=1.0 if material=='plywood' else 2.5
            for i in range(math.floor((x0-y1)/spacing),math.ceil((x1-y0)/spacing)+1):
                t=i*spacing;line((t+y0,y0),(t+y1,y1))
        c.restoreState()
    def view(name,ox,oy,scale):
        v=scene['drawings']['views'][name];s=1/scale
        def point(p):return ox+p[0]*s,oy+p[1]*s
        c.saveState()
        if v.get('crop'):
            x,y,X,Y=v['crop'];clip=c.beginPath();clip.rect(*point((x,y)),(X-x)*s,(Y-y)*s);c.clipPath(clip,stroke=0,fill=0)
        for a in v['polygons']:
            if not a['points']:continue
            pts=[point(q) for q in a['points']];pp=c.beginPath();pp.moveTo(*pts[0])
            for q in pts[1:]:pp.lineTo(*q)
            pp.close();cut=a.get('cut');mat=a.get('material','object')
            c.setFillColor('#f1f1f1' if mat=='glass' else '#ffffff');c.setStrokeColor('#171717' if cut else '#777777');c.setLineWidth(.35 if cut else .13);c.drawPath(pp,fill=1,stroke=1)
            if cut:hatch(pts,mat)
        c.restoreState()
        c.setFillColor('#000000');c.setStrokeColor('#333333');c.setLineWidth(.18)
        for a in v['polylines']:
            for p,q in zip(a,a[1:]):line(point(p),point(q))
        for a in v.get('guides',[]):
            c.setDash([3,1]);c.setStrokeColor('#777777');c.setLineWidth(.13);line(point(a['points'][0]),point(a['points'][1]));c.setDash();x,y=point(a['points'][0]);text(x+2,y+2,a['label'],2.3)
        for a in v.get('labels',[]):
            x,y=point(a['at']);c.setFont('OBTP',3);c.drawCentredString(x,y,a['text'])
        for d in v['dimensions']:
            lines,pt,label=dimension_lines(d);c.setLineWidth(.13)
            for a,b in lines:line(point(a),point(b))
            for p in lines[-1]:
                x,y=point(p);line((x-1,y-1),(x+1,y+1))
            x,y=point(pt)
            c.saveState();c.setFillColor('#ffffff');c.rect(x-1,y+.5,len(label)*1.65+3,3.7,fill=1,stroke=0);c.setFillColor('#111111');text(x+1,y+1,label,2.5);c.restoreState()
    def legend(x,y):
        for i,(mat,label) in enumerate([('timber','Mediena'),('plywood','Fanera'),('mineral-wool','Mineralinė vata'),('concrete-study','Betono atramos')]):
            yy=y-i*8;c.setFillColor('#ffffff');c.setStrokeColor('#333333');c.setLineWidth(.2);c.rect(x,yy,12,5,fill=1,stroke=1);hatch([(x,yy),(x+12,yy),(x+12,yy+5),(x,yy+5)],mat);c.setFillColor('#111111');text(x+16,yy+1,label,2.5)
    def leader(anchor,elbow,label):
        c.setLineWidth(.18);c.setStrokeColor('#555555');line(anchor,elbow);line(elbow,(elbow[0]+50,elbow[1]));text(elbow[0]+2,elbow[1]+2,label,2.5)
    title(1,'Konstrukcinis planas','1:25');view('plan',55,135,25)
    v=scene['drawings'];L=scene['dimensions']['length_mm']+scene['dimensions']['annex_length_mm'];W=scene['dimensions']['width_mm']
    for m in v['cut_markers']:
        c.setDash([5,1,1,1]);c.setLineWidth(.25)
        if m['axis']==0:
            x=55+m['position']/25;line((x,129),(x,135+W/25+10));text(x+2,125,m['name'])
        else:
            y=135+m['position']/25;line((44,y),(55+L/25+10,y));text(29,y+3,m['name'])
        c.setDash()
    cfg=scene['config'];roof=['Plokščias','Vienšlaitis','Dvišlaitis'][cfg['roof_type']]
    text(25,73,('Studija ' if studio else 'Pirtis ')+cfg['size']+'  /  '+roof+' stogas  /  terasa 1200 mm  /  '+(('su lentynomis' if cfg['storage'] else 'be lentynų') if studio else ('su sandėliuku' if cfg['storage'] else 'be sandėliuko')),3)
    text(25,65,'Kirtimo aukštis: 1100 mm virš grindų. Matmenys mm. Konstrukcijų sluoksniai pagal 3D modelį.',2.5)
    legend(25,51)
    page();title(2,'Pjūvis A-A / skersinis','1:25');view('section-a',95,70,25)
    leader((95+W/50,70+(scene['dimensions']['floor_top_mm']+cfg['wall_height']+110)/25),(230,181),'220 mm šiltinama perdanga')
    leader((95+W/50,70+(scene['dimensions']['floor_top_mm']+cfg['wall_height']+500)/25),(230,205),'Vėdinama šalta pastogė')
    text(230,165,'Šiltinimas tarp sijų; ne visas stogo tūris.',2.5)
    text(230,158,'Vėdinimo ir sandarinimo mazgai tikslinami.',2.5)
    legend(280,130)
    text(25,48,'Aukščiai nuo modelio ±0,000. Grindų viršus +0,238. Šildymo ir vėdinimo sprendiniai tikslinami.',2.5)
    page();title(3,'Pjūvis B-B / išilginis','1:25');view('section-b',55,70,25)
    text(25,55,'Pjūvio medžiagos iš modelio. Toliau esančios interjero dalys - plona pilka linija.',2.5)
    legend(25,43)
    page();title(4,'L1 / lango žiniaraštis','1:10')
    view('window',45,77,10);view('window-section',205,77,10)
    brand('pihla.png','PIHLA',265,234,40,15);text(265,225,'Varma Kiinteä / lango kandidatas' if studio else 'Varma Kiinteä / pirties lango kandidatas',3)
    text(200,269,'L1 / vertikalus pjūvis',2.5)
    rows=['Kiekis: 1 vnt. / nevarstomas','Rėmas: '+str(cfg['window_width'])+' × '+str(cfg['door_height']-20)+' mm','Konstrukcinė anga: '+str(cfg['window_width']+20)+' × '+str(cfg['door_height'])+' mm','Rėmo gylis: 170 mm; plotis: 51 mm','Montavimo tarpas: 10 mm kiekviename krašte','Trigubas stiklo paketas; vidinis stiklas grūdintas','Stiklo storį ir tiekimą patvirtina gamintojas']
    for i,t in enumerate(rows):text(265,204-i*8,t,2.8)
    text(265,139,'Montavimo tarpas - OBTP derinimo prielaida.',2.5)
    text(265,131,'Angos apačia ir viršus sutampa su durų anga.',2.5)
    text(265,119,'www.pihla.fi/product/saunan-ikkuna/',2.5)
    c.linkURL('https://www.pihla.fi/product/saunan-ikkuna/',(265,115,400,123),relative=1)
    page();title(5,'D1 / lango vertikalūs mazgai','1:2 / -')
    for name,y,label in [('window-head',170,'D1a / viršus'),('window-sill',73,'D1b / apačia')]:
        crop=v['views'][name]['crop'];view(name,35-crop[0]/2,y-crop[1]/2,2)
        text(35,y+(crop[3]-crop[1])/2+3,label+' / 1:2',3)
    text(25,67,'Vertikalūs pjūviai iš 3D modelio. Supaprastintas rėmo profilis.',2.3)
    text(25,61,'Sandarinimas, skardinimas ir tvirtinimas dar nesuderinti. Ne gamybai.',2.3)
    text(25,55,'Gamintojo profilis: pg.emmi.fi/l/tZjpVv-cnSLX',2.3)
    c.linkURL('https://pg.emmi.fi/l/tZjpVv-cnSLX',(25,52,220,59),relative=1)
    for x,label in [(235,'D2 / Durų mazgas'),(323,'D3 / Sienų kampas')]:
        c.setLineWidth(.2);c.rect(x,90,80,160);text(x+3,254,label,3)
    text(235,79,'Rezervuota suderintiems konstrukcijų mazgams.',2.3)
    page();title(6,'Gamintojai ir duomenų šaltiniai','-')
    text(25,252,'Konstrukcinė sistema: OBTP Cassette / numatytasis variantas',3.5)
    text(25,242,'Gamintojų žymos nurodo gaminio ar dokumentacijos šaltinį, ne patvirtintą viso pastato komplektą.',2.7)
    from .suppliers import attach
    suppliers=scene.get('supplier_spec') or attach(scene)
    for i,record in enumerate(suppliers['products']):
        y=214-i*28
        if record.get('logo'):brand(record['logo'].replace('.svg','.png'),record['supplier'],25,y-3,40,12)
        else:text(25,y,record['supplier'],4)
        text(78,y+5,record['category_lt']+' / '+record['product'],3)
        text(78,y-2,record['status_lt'],2.5)
        text(78,y-9,record['scope_lt'],2.4)
        c.linkURL(record['url'],(25,y-12,402,y+13),relative=1)
    text(25,68,'Alternatyvos tyrimas: Hunton. Pirties sluoksniai, jungtys ir tiekimas Lietuvoje dar nesuderinti.',2.5)
    text(25,60,'Karkaso, izoliacijos, durų ir kitų nepriskirtų gaminių tiekėjai dar nepatvirtinti.',2.5)
    from .analysis import prepare
    analysis=prepare(scene)
    page();title(7,'Analizė / modelis ir šiluminiai mazgai','1:50')
    text(25,254,'PARUOŠIMAS ATLIKTAS. SKAITINIAI SKAIČIAVIMAI NEATLIKTI.',3.5)
    view('section-a',95,120,50);legend(280,215)
    text(220,249,'Pjūvis iš detalaus konstrukcinio modelio',3)
    notes=[
      'Medžiagų ribos paimtos iš tų pačių dalių kaip brėžiniuose.',
      'Šiluminį domeną dar reikia suskaidyti ir patikrinti.',
      'Tikrinami mazgai: siena-grindys, siena-stogas, kampai,',
      'angos, kasečių jungtys ir inžinerinių sistemų pravedimai.',
      'Taškiniai šilumos tilteliai vertinami atskiru 3D modeliu.',
      'U, psi, chi ir paviršiaus temperatūros dar nenustatytos.',
      'Šilumos nuostoliai ir kondensacijos rizika neapskaičiuoti.']
    for i,t in enumerate(notes):text(220,158-i*8,t,2.7)
    text(25,76,'Duomenų vientisumas: '+str(analysis['audit']['source_parts'])+' dalių; unikalūs ID; teigiami baigtiniai prizmių matmenys.',2.7)
    text(25,68,'Tai nėra persidengimų, sandarumo, tinklo konvergencijos ar konstrukcinio tinkamumo patikra.',2.5)
    text(25,60,'Analizės šaltinis: '+analysis['source_sha256'][:32],2.5)
    page();title(8,'Analizė / šildymo ir džiūvimo etapai','-')
    text(25,253,'Trys nuoseklūs etapai / temperatūros kreivė dar neapskaičiuota',3.5)
    stages=[('01 / Prieš šildymą',['Krosnelė išjungta.','Reikia pradinės temperatūros,','drėgmės ir lauko sąlygų.']),
            ('02 / Šildymas ir naudojimas',['Kandidatas: Harvia Spirit SP90E.','Vardinė galia 9 kW; faktinį darbą','lemia valdiklis ir naudojimas.']),
            ('03 / Vėsimas ir džiūvimas',['Krosnelė išjungta.','Pradinė būsena iš antro etapo.','Reikia vėdinimo ir drėgmės duomenų.'])]
    if studio:
        stages=[('01 / Nenaudojama',['Pradinė temperatūra ir drėgmė','dar nenurodytos.','Šildymo sistema neparinkta.']),('02 / Darbo laikas',['Reikia žmonių, įrangos ir','vėdinimo grafikų.','Šilumos poreikis neskaičiuotas.']),('03 / Po darbo',['Reikia temperatūros režimo','ir vėdinimo duomenų.','Džiūvimas neapskaičiuotas.'])]
    for i,(label,lines) in enumerate(stages):
        x=25+i*128;c.setLineWidth(.25);c.rect(x,177,118,58);text(x+5,224,label,3)
        for j,t in enumerate(lines):text(x+5,211-j*9,t,2.6)
    if studio:
        for i,t in enumerate(['Studija skirta kūrybai, pasiruošimui ir medžiagoms laikyti; ne gyvenimui.',
          'Dengta vidurinė erdvė yra lauko zona ir įtraukiama į konservatyvią ploto ribą.',
          'Šildymas, vėdinimas, garų kontrolė ir langų charakteristikos dar neparinkti.',
          'Skaitiniai šilumos nuostoliai, paviršiaus temperatūros ir drėgminė būklė neapskaičiuoti.',
          'Paskirtį, sklypo sąlygas ir SLD poreikį būtina įvertinti konkrečiam projektui.']):text(25,153-i*11,t,2.9)
    else:
        for i,t in enumerate([
          'Stacionarus THERM mazgo skaičiavimas neparodo įšilimo trukmės ar džiūvimo.',
          'Pereinamajam procesui reikia medžiagų šiluminės talpos, valdymo, vėdinimo ir drėgmės šaltinių.',
          'Krosnelė yra parinkimo kandidatas. Modelio tūris dar nėra suderintas su jos montavimo instrukcija.',
          'Krosnelės gabaritai: 385 x 334 x 687 mm. Gamintojo nurodomas patalpos tūris: 8-14 m³.',
          'Patikrinti įstiklinimo įtaką parinkimui, saugius atstumus, tvirtinimą ir elektros įvadą.',
          'Šaltinis: harvia.com / HSPE904M. Medžiagų kandidatai ir metodai pateikti analysis/README.md.',
          'Ši byla aprašo gaminį; ji nepakeičia konkretaus sklypo statinio projekto.']):text(25,153-i*11,t,2.9)
    page();title(9,'Analizė / konstrukcijos ir vėjas','-')
    text(25,253,'Konstrukcijų analizė nebaigta. Vėjo ir sniego vertinimas pristabdytas.',3.5)
    rows=[
      ('Modelio dalys',str(analysis['audit']['structural_candidates'])+' konstrukcinių dalių kandidatų; strypų ir plokštelių schema nepatvirtinta.'),
      ('Jungtys',str(analysis['audit']['unresolved_interfaces'])+' sąsajų be patvirtintos laikomosios galios; standumas nepriskirtas.'),
      ('Atramos','Reikia grunto, atramų ir inkarų sprendinių. Modelio betono tūriai yra studija.'),
      ('Apkrovos','Nuolatinės ir naudojimo apkrovos nepatvirtintos. Vėjas ir sniegas šiuo etapu nevertinami.'),
      ('Vietovė','Lietuva; numatomas lygus sklypas. Konkretūs vietovės duomenys nepriskirti.'),
      ('Vėjas ir sniegas','Pristabdyta užsakovo sprendimu. Tai nereiškia nulinių apkrovų.'),
      ('Rezultatai','Įrąžos, įtempiai, įlinkiai, reakcijos ir jungčių apkrovos dar neapskaičiuoti.'),
      ('Patikros','Pusiausvyra, reakcijų sumos, mechanizmai ir konvergencija dar nepatikrinti.')]
    for i,(label,body) in enumerate(rows):
        y=229-i*18;text(25,y,label,3);text(88,y,body,2.65);c.setStrokeColor('#cccccc');line((25,y-6),(400,y-6));c.setStrokeColor('#111111')
    text(25,72,'Ne statybai. Tai nėra konstrukcijų patvirtinimas ar STR atitikties deklaracija.',3)
    text(25,62,'Skaitinių rezultatų diagramos įtraukiamos tik po patikrinto, šiai modelio laidai priskirto skaičiavimo.',2.5)
    c.save()
