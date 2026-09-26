"""Core SSP draft sheet recipe shared by Rhino layouts and offline proof.
No site is invented. This is not a signed or construction-ready project.
"""
import copy
import textwrap
from .drawings import dimension, dimension_lines, hull
from .export import vertices

REVISION='SSP-R03'

def elevation(scene,axis,positive):
    k=1-axis;polygons=[]
    for part in scene['parts']:
        if part['family']=='furniture':continue
        vs=vertices(part);points=hull([[(-1 if positive else 1)*v[k],v[2]] for v in vs])
        if len(points)<3:continue
        polygons.append(dict(id=part['id'],points=points,depth=sum(v[axis] for v in vs)/8,
          material=part['material'],cut=False,fill='#eeeeee' if part['material']=='glass' else '#ffffff'))
    polygons.sort(key=lambda p:p['depth'],reverse=not positive)
    # Draw far faces first. White polygon fills mask deeper projected parts.
    lo=min(q[0] for p in polygons for q in p['points']);hi=max(q[0] for p in polygons for q in p['points'])
    return dict(polygons=polygons,polylines=[],labels=[],dimensions=[dimension([lo,0],[hi,0],-220)],
      source_geometry_sha256=scene['geometry_sha256'],projection='orthographic-depth-sorted')

def bounds(view):
    pts=[q for p in view['polygons'] for q in p['points']]+[q for p in view['polylines'] for q in p]
    for dim in view['dimensions']:
        lines,pt,_=dimension_lines(dim);pts.extend(q for line in lines for q in line);pts.append(pt)
    return [min(p[k] for p in pts)-120 for k in (0,1)]+[max(p[k] for p in pts)+120 for k in (0,1)]

def prepare(scene):
    studio=scene['config'].get('program_type',0)==1
    product='Modulinė studija' if studio else 'Modulinė pirtis'
    cfg=scene['config'];m=scene['metrics'];sheets=[]
    def sheet(name,code):
        p=dict(name=name,code=code,texts=[],lines=[],details=[]);sheets.append(p);return p
    def text(p,x,y,value,size=3):p['texts'].append(dict(at=[x,y],text=str(value),size=size))
    def paragraph(p,x,y,value,width=116,size=3):
        for line in textwrap.wrap(value,width=width,break_long_words=False,break_on_hyphens=False):
            text(p,x,y,line,size);y-=size*1.6
        return y-5
    def view(p,name,v,box,scales):
        v=copy.deepcopy(v);b=bounds(v)
        scale=next((a for a in scales if (b[2]-b[0])/a<=box[2]-box[0] and (b[3]-b[1])/a<=box[3]-box[1]),None)
        if scale is None:raise ValueError('Drawing does not fit A3 at permitted scale: '+name)
        center=[(b[0]+b[2])/2,(b[1]+b[3])/2]
        p['details'].append(dict(name=name,view=v,box=box,scale=scale,center=center))
    p=sheet('Antraštinis lapas','BD-01')
    text(p,30,230,product.upper()+' '+cfg['size'],9)
    text(p,30,210,'SUPAPRASTINTO STATYBOS PROJEKTO RUOŠINYS',5)
    y=187
    for value in ['Naujos statybos sumanymas / OBTP medinis karkasas',
        'Statybos vieta: Lietuva; konkretus sklypas nepateiktas.',
        'Statytojas (užsakovas): nepateikta.',
        'Projektuotojas ir projekto vadovas: nepaskirti.',
        'Paskirties kodas ir statinio kategorija: tikslinama pagal naudojimą ir sklypą.',
        'Laida R03 / 2026-09-26 / '+scene['version'],
        'Nepasirašytas ruošinys. Ne statybai ir ne teikimui institucijoms.']:
        y=paragraph(p,30,y,value,102,3.5)
    paragraph(p,30,87,'Sklypo planas, teisiniai duomenys ir inžinerinių sprendinių patvirtinimas dar nepateikti. '
       'Šis egzempliorius skirtas dokumento struktūrai ir modelio brėžiniams peržiūrėti.',108,3)
    p=sheet('Bendrieji duomenys / dokumentų sudėtis','BD-02')
    rows=[('BD-01','Antraštinis lapas'),('BD-02','Dokumentų sudėtis ir rengimo pagrindas'),('BD-03','Aiškinamasis raštas ir rodikliai'),('BD-04','Konstrukcijų ir sistemų aprašas'),('SA-01','Planas'),('SA-02 / SA-03','Pjūviai A-A ir B-B'),('SA-04 / SA-05','Fasadai')]
    text(p,28,250,'PAVADINIMAS',3);text(p,323,250,'INDEKSAS',3)
    p['lines'] += [[[25,240],[398,240]],[[315,163],[315,258]],[[25,258],[398,258]]]
    for i,(code,name) in enumerate(rows):
        y=232-i*10;text(p,28,y,name,2.8);text(p,323,y,code,2.6);p['lines'].append([[25,y-4],[398,y-4]])
    y=paragraph(p,25,155,'Rengimo pagrindas: užsakovo užduotis ir parametrinis OBTP GH-R11 modelis. '
      'Statybos įstatymo 24 straipsnis; STR 1.04.04:2017 „Statinio projektavimas, projekto ekspertizė“.',116)
    y=paragraph(p,25,y,'Sudėtis remiasi supaprastinto projekto bendrųjų duomenų, aiškinamojo rašto, '
      'sklypo plano, architektūrinių brėžinių, konstrukcijų ir inžinerinių sistemų aprašo struktūra. '
      'Galiojančią STR redakciją, sudėtį ir įforminimą galutinai patikrina projekto rengėjas.',116)
    y=paragraph(p,25,y,'Sklypo planas šioje laidoje neparengtas. Jo negalima pakeisti bendru pastato planu. '
      'Reikia sklypo identifikacijos, aktualaus matavimų pagrindo, ribų, altitudžių, apribojimų, '
      'pastato vietos, tinklų ir privalomų sutikimų.',116)
    text(p,25,70,'Norminiai šaltiniai: infolex.lt/ta/77961:str24; vtpsi.lrv.lt (STR sąrašas).',2.6)
    text(p,25,63,'Tiekėjų katalogas, analizės priedai ir neprivalomi gaminio mazgai neįtraukti.',2.6)
    p=sheet('Aiškinamasis raštas / rodikliai','BD-03')
    use=('Kūrybinis darbas, pomėgiai, medžiagų paruošimas ir laikymas. Centrinė patalpa numatyta '
       'šildyti žiemą; vasarą ji atveriama stumdomomis durimis. Malkų niša atvira.' if studio else
       'Pirties patalpa, mažas prieangis ir lauko dušas. Sandėliukas - pagal pasirinktą variantą.')
    paragraph(p,25,248,use+' Gyvenamosios ir miegamųjų programos nėra.',116)
    rows=[('Pagrindinių sienų gabaritas',f"{scene['dimensions']['length_mm']} × {scene['dimensions']['width_mm']} mm"),
      ('Konservatyvi modelio ploto riba',f"{m['building_area_bound_m2']:.2f} m²"),
      ('Uždaro tūrio išorinio ploto metrika',f"{m['enclosed_finished_area_m2']:.2f} m²"),
      ('Modelio vidaus ploto įvertis',f"{m['main_clear_floor_less_partition_m2']:.2f} m²"),
      ('Aukštis nuo modelio nulio',f"{m['height_mm']/1000:.3f} m"),
      ('Didžiausias modelio atrėmimo linijų tarpas',f"{m['max_bearing_line_span_mm']/1000:.3f} m")]
    for i,(a,b) in enumerate(rows):
        y=210-i*14;text(p,25,y,a);text(p,250,y,b);p['lines'].append([[25,y-5],[398,y-5]])
    y=paragraph(p,25,113,'Rodikliai gauti iš modelio. Tai nėra kadastriniai plotai, teisinis aukštis ar '
      'konstrukcijų laikomosios galios patvirtinimas. Bendrasis ir užstatymo plotai, tūris, '
      'tankis ir intensyvumas turi būti nustatyti pritaikant projektą sklypui.',116)
    paragraph(p,25,y,'Energinio naudingumo reikalavimų taikymas ir rodikliai nenustatyti. '
      'Plotis, aukštis ir atrėmimo tarpai savaime nesuteikia teisės statyti be SLD.',116)
    p=sheet('Konstrukcijų ir inžinerinių sistemų aprašas','BD-04')
    y=248
    blocks=[('Konstrukcijos','Medinių kasečių grindys ir sienos; 600 mm koordinavimo modulis. '
      'Karkasas, apkalos ir šiltinimas vaizduojami pagal detalų modelį. Medienos klasė, jungtys, '
      'standumas, inkarai ir pamatų sprendiniai dar nepatvirtinti.'),
      ('Stogas ir atitvaros','Stogo, grindų ir sienų sluoksniai parodyti modelio pjūviuose. '
      'Konsolių be kolonų laikomoji galia, sandarumas, garų kontrolė ir vandens nuvedimas '
      'dar nepatikrinti. Fasadas - vertikali medinė apdaila.'),
      ('Angos','Durų ir langų geometrija yra derinimo modelis. Galutiniai gaminiai, saugus stiklas, '
      'šiluminės savybės, montavimo tarpai ir tvirtinimo mazgai tikslinami.'),
      ('Šildymas ir gaisrinė sauga',('Krosnelės Morsø 1442 korpusas - vietos rezervas. Dūmtraukis, '
       'grindų apsauga, saugūs atstumai, degimo oras ir vėdinimas neprojektuoti.' if studio else
       'Krosnelės kandidatas Harvia Spirit SP90E. Galia, saugūs atstumai, tvirtinimas ir '
       'vėdinimas turi būti patikrinti pagal galutinį patalpos tūrį ir gamintojo instrukcijas.')),
      ('Inžinerinės sistemos','Elektros grandinės, apsaugos, įžeminimas, vandens ir nuotekų '
       'įvadai dar neprojektuoti. Sklypo tinklų sąlygos nepateiktos.'),
      ('Neužbaigti sprendiniai','Vėjo ir sniego vertinimas pristabdytas; tai nėra nulinės apkrovos. '
       'Šiluminiai ir konstrukciniai skaičiavimai neatlikti. Prieš naudojant projektą statybai '
       'būtinas sklypo pritaikymas, inžinerinis pagrindimas ir atsakingų rengėjų parašai.')]
    for title,body in blocks:
        text(p,25,y,title,3.3);y=paragraph(p,25,y-7,body,116,3)-3
    for key,name,code in [('plan','Planas','SA-01'),('section-a','Pjūvis A-A','SA-02'),('section-b','Pjūvis B-B','SA-03')]:
        p=sheet(name,code);v=copy.deepcopy(scene['drawings']['views'][key])
        if key=='plan':
            # Source-linked section markers supplement the same model-derived plan.
            L=scene['dimensions']['length_mm'];W=scene['dimensions']['width_mm']
            for marker in scene['drawings']['cut_markers']:
                pos=marker['position']
                line=[[pos,-160],[pos,W+160]] if marker['axis']==0 else [[-160,pos],[L+160,pos]]
                v['polylines'].append(line);v.setdefault('labels',[]).append(dict(at=line[0],text=marker['name']))
        view(p,name,v,[25,65,405,258] if key=='plan' else [25,57,405,260],[10,25,50])
        text(p,25,49,'Matmenys mm. Medžiagų ribos iš detalaus modelio.',2.5)
        text(p,25,44,'Modelio nulis nėra sklypo altitudė.',2.5)
    for axis,title,code in [(1,'Išilginiai fasadai','SA-04'),(0,'Galiniai fasadai','SA-05')]:
        p=sheet(title,code)
        for positive,box,label in [(False,[25,162,405,248],('Y− / įėjimo pusė' if axis==1 else 'X− / trumpasis galas')),
                                   (True,[25,65,405,151],('Y+ / priešinga pusė' if axis==1 else 'X+ / trumpasis galas'))]:
            view(p,label,elevation(scene,axis,positive),box,[50,100]);text(p,25,box[3]+4,label,3)
        text(p,25,59,'Ortografinės modelio projekcijos. Sklypo orientacija ir reljefas nenustatyti.',2.5)
    for i,p in enumerate(sheets):
        p['number']=i+1;p['total']=len(sheets)
        text(p,25,278,'obtp. / studio',5);text(p,25,266,p['name'],4)
        text(p,25,16,'RUOŠINYS / '+scene['geometry_sha256'][:16],2)
        for x,y,w,h in [(20,10,390,277),(230,10,180,45)]:
            p['lines'] += [[[x,y],[x+w,y]],[[x+w,y],[x+w,y+h]],[[x+w,y+h],[x,y+h]],[[x,y+h],[x,y]]]
        p['lines'] += [[[230,25],[410,25]],[[230,40],[410,40]],[[320,10],[320,55]],[[380,10],[380,25]],[[395,10],[395,40]]]
        for x,y,t,z in [(233,48,'SSP / PROJEKTO RUOŠINYS',3),(233,43,'Ne statybai. Nepasirašyta.',2.4),
          (322,48,product+' '+cfg['size'],2.8),(233,34,'PV / PDV: nepaskirti',2.4),(233,28,'Sklypas / užsakovas: nepateikta',2.2),
          (322,34,p['name'][:36],1.9),(397,34,'R03',2.2),(233,19,'LT / 2026-09-26',2.4),(233,13,REVISION+' / '+scene['version'],2.4),
          (322,19,'OBTP-'+p['code'],2.4),(322,13,'A3 / '+('1:'+str(p['details'][0]['scale']) if p['details'] else '-'),2.4),
          (382,19,'Lapas',1.8),(397,19,'Lapų',1.8),(384,13,i+1,2.4),(399,13,len(sheets),2.4)]:text(p,x,y,t,z)
    return dict(schema='obtp-ssp-layouts/1',revision=REVISION,geometry_sha256=scene['geometry_sha256'],
      status='draft-missing-site-and-engineering',page_mm=[420,297],sheets=sheets,
      omitted_required=['site-plan-and-site-specific-data'],native_execution='not-executed')
