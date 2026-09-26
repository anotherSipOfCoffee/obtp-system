"""R12 model-linked A3 schedules and assembly review layouts.
Same page recipes feed native Rhino layouts and explicitly labelled offline proofs.
"""
import copy,hashlib,json,math
from collections import defaultdict
from .export import vertices
from .drawings import hull,dimension
from .ssp_sheets import bounds
WOOD=('timber','plywood','lining-wood','cladding-wood','deck-wood')
NAMES={'timber':'Karkaso mediena','plywood':'Fanera','lining-wood':'Vidaus apdaila','cladding-wood':'Fasadas / apvadai','deck-wood':'Terasos mediena'}
FAMILY={'floor':'Grindys','roof':'Stogas','walls':'Sienos','partitions':'Pertvaros','foundation':'Pamatai / atramos','terrace':'Terasa','facade':'Fasadas','interior':'Vidaus apdaila','ceiling':'Lubos'}

def volume(a):
    x,y,z=a['size'];return x*y*(z+a.get('top_slope_y',0)*y/2)/1e9

def axon(parts,highlight=None):
    polys=[]
    def project(v):x,y,z=v;return [.8660254*(x-y),z-.5*(x+y)]
    for a in parts:
        vs=vertices(a)
        for i,face in enumerate(((1,2,6,5),(2,3,7,6),(4,5,6,7))):
            points=[project(vs[k]) for k in face]
            polys.append(dict(id=a['id'],points=points,material=a['material'],cut=False,
              fill=('#ffffff' if highlight is None or a['id'] in highlight else '#eeeeee'), depth=((3 if '/seam-' in a['id'] or a['id'].startswith('ridge-cap/') else 2 if a['id'].startswith('weather-roof-') and '/cover' in a['id'] else 1 if a['id'].startswith('weather-roof-') and '/deck-' in a['id'] else 0),sum(vs[k][2] for k in face)/len(face),sum(vs[k][0]+vs[k][1] for k in face)/len(face))))
    polys.sort(key=lambda p:p['depth'])
    return dict(polygons=polys,polylines=[],labels=[],dimensions=[])

def page(name,code):return dict(name=name,code=code,texts=[],lines=[],details=[])
def text(p,x,y,t,size=2.5):p['texts'].append(dict(at=[x,y],text=str(t),size=size))
def line(p,x,y,X,Y):p['lines'].append([[x,y],[X,Y]])
def rect(p,x,y,w,h):
    for a,b,c,d in [(x,y,x+w,y),(x+w,y,x+w,y+h),(x+w,y+h,x,y+h),(x,y+h,x,y)]:line(p,a,b,c,d)
def slot(p,name,v,box,scales=(10,20,25,50,75,100,150,200)):
    b=bounds(v);w=box[2]-box[0];h=box[3]-box[1]
    scale=next((s for s in scales if (b[2]-b[0])/s<w and (b[3]-b[1])/s<h),None)
    if scale is None:raise ValueError('Drawing does not fit '+name)
    p['details'].append(dict(name=name,view=v,box=box,scale=scale,center=[(b[0]+b[2])/2,(b[1]+b[3])/2]))
    return scale

def finish(scene,sheets,kind):
    for i,p in enumerate(sheets):
        p.update(number=i+1,total=len(sheets));rect(p,15,10,395,277)
        text(p,22,277,'obtp. / '+('studija' if scene['config']['program_type'] else 'pirtis')+' '+scene['config']['size'],4.5)
        text(p,22,267,p['name'],4)
        rect(p,230,10,180,36)
        for y in (22,34):line(p,230,y,410,y)
        line(p,365,10,365,34);line(p,390,10,390,34)
        text(p,234,39,'PERŽIŪRA / NE STATYBAI',3)
        text(p,234,27,p['code']+' / GH-R12',2.7);text(p,369,27,'Lapas',2);text(p,394,27,'Lapų',2)
        text(p,234,15,'2026-09-26 / '+scene['geometry_sha256'][:16],2.3);text(p,370,15,i+1);text(p,396,15,len(sheets))
        text(p,22,20,'Matmenys mm. Kiekiai pagal modelį; gamybinės jungtys nepatvirtintos.',2)
    return dict(schema='obtp-document-layouts/1',kind=kind,geometry_sha256=scene['geometry_sha256'],page_mm=[420,297],sheets=sheets)

def openings(scene):
    groups={}
    byid={p['id']:p for p in scene['parts']}
    for item in scene['object_library']['instances']:
        ids=item['part_ids']
        if not (item['definition']=='obtp.door.study' or any(x.startswith(('window/','studio-slider-')) for x in ids)):continue
        parts=[byid[x] for x in ids]
        lo=[min(v[k] for a in parts for v in vertices(a)) for k in range(3)];hi=[max(v[k] for a in parts for v in vertices(a)) for k in range(3)]
        axis=0 if hi[0]-lo[0]>hi[1]-lo[1] else 1
        width=hi[axis]-lo[axis];height=hi[2]-lo[2]
        typ='Langas' if any(x.startswith('window/') for x in ids) else 'Stumdomos durys' if any(x.startswith('studio-slider-') for x in ids) else 'Durys'
        sig=(typ,round(width,3),round(height,3),item.get('placement',{}).get('plan_angle_rad'))
        row=groups.setdefault(sig,dict(parts=parts,instances=[],width=width,height=height,axis=axis,lo=lo,type=typ));row['instances'].append(item['id']);row['product']=item.get('product',{})
    sheets=[]
    for n,row in enumerate(groups.values()):
        if n%8==0:
            p=page('Langų ir durų žiniaraštis','LD-'+str(len(sheets)+1).zfill(2));sheets.append(p)
            for x in (22,218):
                for X in [x,x+23,x+104,x+151,x+181]:line(p,X,59,X,256)
                line(p,x,256,x+181,256);line(p,x,245,x+181,245)
                for X,t in [(x+2,'Žymuo'),(x+26,'Vaizdas'),(x+107,'Gabaritai, mm'),(x+154,'Kiekis')]:text(p,X,249,t,2.2)
        x=22 if n%8<4 else 218;y=245-(n%4)*46
        code=('L' if row['type']=='Langas' else 'D')+'-'+hashlib.sha256(str((row['type'],row['width'],row['height'],row['instances'][0])).encode()).hexdigest()[:5].upper()
        text(p,x+2,y-10,code,2.4);text(p,x+107,y-13,f"{row['width']:.0f} × {row['height']:.0f}",2.3);text(p,x+157,y-13,len(row['instances']),2.6)
        text(p,x+107,y-23,row['type'],2.2);text(p,x+107,y-32,'Varstymas: tikslinti',1.9)
        polys=[]
        for a in row['parts']:
            pts=hull([[v[row['axis']]-row['lo'][row['axis']],v[2]-row['lo'][2]] for v in vertices(a)])
            polys.append(dict(id=a['id'],points=pts,material=a['material'],cut=False))
        v=dict(polygons=polys,polylines=[],labels=[],dimensions=[dimension([0,0],[row['width'],0],-120),dimension([row['width'],0],[row['width'],row['height']],120)])
        slot(p,code,v,[x+25,y-43,x+102,y-2],(50,75,100));line(p,x,y-46,x+181,y-46)
    text(sheets[-1],22,51,'Gaminio gabaritai nėra angos matmenys. Varstymo kryptį, stiklą ir tvirtinimą suderinti su tiekėju.',2.4)
    p=page('Langų ir durų tiekėjai / kainos','LD-P');sheets.append(p)
    for j,row in enumerate(groups.values()):
        data=row['product'];y=246-j*28
        code=('L' if row['type']=='Langas' else 'D')+'-'+hashlib.sha256(str((row['type'],row['width'],row['height'],row['instances'][0])).encode()).hexdigest()[:5].upper()
        text(p,25,y,code+' / '+data.get('project_id','Neparinkta'),2.5)
        text(p,25,y-7,data.get('supplier','')+' / '+data.get('product',''),2.5)
        text(p,25,y-14,'Gamintojo kodas: '+str(data.get('manufacturer_code') or 'pagal individualų užsakymą'),2.2)
        price=data.get('price_eur');text(p,270,y,(f'{price:.2f} EUR / vnt.' if price is not None else 'Kaina: pagal pasiūlymą'),2.7)
        text(p,270,y-8,'Vnt.: '+str(len(row['instances'])),2.5)
        text(p,25,y-22,'Patikra: '+data.get('checked','')+' · '+('gaminio gabaritas' if data.get('frame_mm') else 'projektinis gabaritas; tiekėjas tikslina'),2)
        line(p,25,y-25,395,y-25)
    if any(r['product'].get('price_eur') is not None for r in groups.values()):text(p,25,63,'344 EUR: SaunaBee / D91902M. PVM bazę ir pristatymą Lietuvoje patikslinti.',2.5)
    text(p,25,55,'Trūkstamos kainos nėra 0 EUR. Pilna angų užpildų suma neskaičiuojama be pasiūlymų.',2.5)
    return finish(scene,sheets,'openings')

def component_groups(scene):
    groups={}
    for a in scene['parts']:
        if a['material'] not in WOOD:continue
        # Exact recipe orientation and slopes retained; no shape equivalence inferred.
        from .optimisation import signature
        sig=signature(a)
        code='K-'+hashlib.sha256(repr(sig).encode()).hexdigest()[:6].upper()
        row=groups.setdefault(code,dict(code=code,example=a,parts=[],m3=0));row['parts'].append(a['id']);row['m3']+=volume(a)
    return sorted(groups.values(),key=lambda g:(WOOD.index(g['example']['material']),g['example']['family'],g['code']))

def estimate(scene):
    # Market benchmarks are not certified product selections. Explicit allowances.
    timber=sum(volume(a) for a in scene['parts'] if a['material']=='timber')
    ply=sum(volume(a) for a in scene['parts'] if a['material']=='plywood')
    sheets=[a for a in scene['parts'] if a['material']=='plywood']
    outline=sum(2*sum(sorted(a['size'])[1:])/1000 for a in sheets)
    # Sensitivity scenario: not a CAM runtime. Includes 2 passes, 2m/min, 2min handling/sheet.
    hours=outline*2/2/60+len(sheets)*2/60
    mat=timber*450*1.10+ply*(23.63/.018)*1.15
    cnc=hours*30+4*50
    return dict(timber_m3=timber,plywood_m3=ply,material_eur=mat,cnc_hours_scenario=hours,cnc_eur=cnc,total_ex_vat=mat+cnc,total_with_vat=(mat+cnc)*1.21,
      scope='Structural timber and plywood only. Excludes finishes, insulation, openings, concrete, connectors, installation and transport.',
      rates={'timber_eur_m3_ex_vat':450,'plywood_eur_m3_ex_vat':23.63/.018,'cnc_eur_hour_assumed_ex_vat':30,'preparation_eur_hour_assumed_ex_vat':50},
      holds=['Timber rate benchmark C24 45x195; grade/stock for actual sections unconfirmed.','Plywood 18mm rate is a proxy for other thicknesses; structural suitability unconfirmed.','10% timber and 15% plywood allowances are assumptions, not nesting results.','CNC runtime is a sensitivity scenario, not simulated toolpaths; supplier tax basis needs confirmation.','Long members need suitable timber processing, not the cited 2x3m sheet router.'])

def components(scene):
    rows=component_groups(scene);sheets=[]
    for n,row in enumerate(rows):
        if n%10==0:
            p=page('Medinių elementų žiniaraštis','K-'+str(len(sheets)+1).zfill(2));sheets.append(p)
            for x in (22,218):
                for X in (x,x+28,x+100,x+151,x+181):line(p,X,55,X,256)
                line(p,x,256,x+181,256);line(p,x,245,x+181,245)
                for X,t in [(x+2,'Indeksas'),(x+31,'Aksonometrija'),(x+102,'Matmenys, mm'),(x+153,'Vnt. / m³')]:text(p,X,249,t,2.1)
        x=22 if n%10<5 else 218;y=245-(n%5)*38;a=row['example']
        text(p,x+2,y-11,row['code'],2.2)
        dims=sorted(a['size']);text(p,x+102,y-10,' × '.join(f'{d:.0f}' for d in dims),2.1)
        text(p,x+102,y-20,NAMES[a['material']],2);text(p,x+102,y-29,FAMILY.get(a['family'],a['family']),2)
        text(p,x+154,y-11,len(row['parts']),2.4);text(p,x+154,y-23,f"{row['m3']:.4f}",2.2)
        q=dict(a,origin=[0,0,0]);sc=slot(p,row['code'],axon([q]),[x+30,y-35,x+98,y-2]);text(p,x+31,y-35,'1:'+str(sc),1.8)
        line(p,x,y-38,x+181,y-38)
    p=page('Kiekių ir kainos suvestinė','K-SUM');sheets.append(p)
    y=246
    text(p,25,y,'Elementų tipas',3);text(p,180,y,'Vnt.',3);text(p,230,y,'Modelio tūris, m³',3)
    for mat in WOOD:
        y-=13;items=[a for a in scene['parts'] if a['material']==mat]
        text(p,25,y,NAMES[mat]);text(p,180,y,len(items));text(p,230,y,f'{sum(volume(a) for a in items):.4f}');line(p,25,y-4,395,y-4)
    y-=15;text(p,25,y,'IŠ VISO MEDIENOS IR FANEROS',3);text(p,180,y,sum(len(g['parts']) for g in rows));text(p,230,y,f"{scene['metrics']['total_wood_m3']:.4f}",3)
    e=estimate(scene);y-=20
    for title,val in [('Karkaso medžiagos + atliekų prielaida',f"{e['material_eur']:.0f} EUR"),('CNC scenarijus + failų paruošimas',f"{e['cnc_eur']:.0f} EUR"),('Scenarijaus suma be PVM',f"{e['total_ex_vat']:.0f} EUR"),('Scenarijaus suma su 21% PVM',f"{e['total_with_vat']:.0f} EUR")]:
        text(p,25,y,title,2.7);text(p,250,y,val,3);y-=11
    text(p,25,y-2,'Tai karkaso ir faneros biudžeto scenarijus, ne viso pastato kaina ar tiekėjo pasiūlymas.',2.4)
    text(p,25,y-12,'Apdaila, vata, langai, durys, pamatai, jungtys, pristatymas ir montavimas neįkainoti.',2.2)
    p=page('Kiekiai pagal elementų grupes','K-TYPES');sheets.append(p)
    text(p,25,246,'Elementų grupė',3);text(p,205,246,'Vnt.',3);text(p,270,246,'Medienos tūris, m³',3)
    families=sorted(set(a['family'] for a in scene['parts'] if a['material'] in WOOD))
    for j,family in enumerate(families):
        items=[a for a in scene['parts'] if a['family']==family and a['material'] in WOOD];y=230-j*14
        text(p,25,y,FAMILY.get(family,family));text(p,205,y,len(items));text(p,270,y,f'{sum(volume(a) for a in items):.4f}');line(p,25,y-4,395,y-4)
    text(p,25,65,'Tik mediena ir fanera. Mineralinė vata, stiklas, betonas ir kiti gaminiai neįtraukti.',2.5)
    p=page('Kainodaros pagrindas ir apribojimai','K-COST');sheets.append(p)
    notes=[
      'Rinkos patikra: 2026-09-26. Sumos apvalintos iki EUR; modelio tūriai iki 0,0001 m³.',
      'Lentvario Mediena: C24 45×195×6000 - 544,50 EUR/m³ su PVM; bazė 450 EUR/m³ be PVM.',
      'Faneros pardavimas: beržinė 18 mm BB/CP - 23,63 EUR/m² + PVM. Kitų storių kaina - tūrio analogas.',
      'Lazertechas: CNC nuo 30 EUR/val. InSky: failų paruošimas 50 EUR/val.; mokesčių bazę patikslinti.',
      'Prielaidos: mediena +10%, fanera +15%. Tai rezervas, ne optimizuotas ruošinių išdėstymas.',
      f"CNC scenarijus: {e['cnc_hours_scenario']:.1f} val.; 2 ėjimai, 2 m/min, 2 min/detalei + 4 val. paruošimui.",
      'Šie laikai nėra CAM skaičiavimas. Jie skirti biudžeto jautrumui parodyti ir pakeičiami gavus pasiūlymą.',
      'Ne visos karkaso dalys frezuojamos: tiesūs tašai gali būti pjaunami pjūklu ar medienos centru.',
      'Ilgi ir aukšti elementai netelpa į 2×3 m / 200 mm CNC pavyzdį. Reikia atskiro gamybos maršruto.',
      'Kiekis - modelio detalių tūrių suma. Susikirtimų auditas atskiras; tai nėra užsakymo kiekis.',
      'Indeksas priklauso nuo geometrijos ir medžiagos; egzempliorių ID pateikti JSON / CSV faile.',
      'Šaltiniai: lentvariomediena.lt/straipsniai/c18-c24-mediena-lietuvoje',
      'faneros-pardavimas.lt/berzine-fanera/ • lazer.lt/cnc-frezavimas/ • insky.lt/cnc-frezavimas/'
    ]
    for j,t in enumerate(notes):text(p,25,244-j*13,t,2.6)
    from .optimisation import analyse
    opt=analyse(scene);p=page('Elementų racionalizavimo analizė','K-OPT');sheets.append(p)
    rows=[('Fizinės medinės detalės',opt['physical_wood_parts']),('Tipai pagal modelio orientaciją',opt['orientation_specific_types']),('Tipai suvienodinus stačiakampių tašų orientaciją',opt['normalised_types']),('Sumažintas geometrinių tipų skaičius',opt['fewer_geometric_types']),('6000 mm ruošiniai / 3 mm pjūvio prielaida',opt['stock_bars']),('Ruošinių panaudojimas, % (su pjūviais)',opt['stock_utilisation_percent'])]
    for j,(label,value) in enumerate(rows):text(p,25,241-j*17,label,3);text(p,345,241-j*17,value,3);line(p,25,235-j*17,395,235-j*17)
    for j,t in enumerate(['Geometriniai tipai sujungiami nekeičiant konstrukcijos matmenų ar detalių kiekio.',
      'Ruošinių studija: pirmiausia išdėstomos ilgiausios detalės. Tai euristika, ne optimalumo įrodymas.',
      'Medienos klasę, pluošto kryptį, jungtis, galų apipjovimą ir įrangą tikrina gamintojas.',
      'Fraktalinis skaidymas savaime nemažina sąnaudų: daugiau dalijimų gali reikšti daugiau jungčių.',
      'Nepašalintos porinės statramsčių ar kasetės kraštų detalės: tam reikia konstrukcinio vertinimo.',
      'Ilgesnės pamatų sijos išlaiko tarpines atramas; sujungimai palikti ties atramų ašimis.']):text(p,25,116-j*10,t,2.5)
    return finish(scene,sheets,'components')

STAGES=[('Pamatai ir bendra atramų ašių sistema','foundation','Patikrinti gruntą, altitudes, atramų laikomąją galią ir inkarų projektą. Be patvirtinimo nemontuoti.'),
('Grindų ir terasos karkasas','floor-frame','Tikrinamos įstrižainės, atrėmimai ir aukščiai. Laikinas stabilumas turi būti užtikrintas.'),
('Grindų šiltinimas ir paklotas','floor-skin','Patikrinti drėgmę ir apatinę apsaugą; prieš uždengiant apžiūrėti jungtis ir komunikacijas.'),
('Sienų ir pertvarų karkasas','wall-frame','Kelti pagal indeksus. Laikinai įstrižinti. Jungčių tvirtinimo schema dar turi būti suprojektuota.'),
('Sienų šiltinimas ir apkalos','wall-skin','Vata užpildo karkaso ertmes; angos lieka laisvos. Oro ir garų sluoksniai turi būti tęstiniai.'),
('Lubų ir stogo konstrukcija','roof','Patikrinti atrėmimus, konsoles ir stogo nuolydį. Neužpildyti numatyto vėdinimo tarpo.'),
('Langai, durys ir išorės apdaila','outside','Suderinti angų tarpus, sandarinimą ir vandens nuvedimą. Stoglangių šiame modelyje nėra.'),
('Vidaus apdaila ir patikra','finish','Tik po paslėptų darbų patikros. Krosnies, elektros, vėdinimo ir priešgaisriniai sprendiniai atskiri.')]

def stage(a):
    f=a['family'];m=a['material'];id=a['id']
    if f=='foundation':return 0
    if f in ('floor','terrace') and m in ('timber','deck-wood') and '/board-' not in id:return 1
    if f=='floor' or id.startswith('insulation-floor'):return 2
    if f in ('walls','partitions') and m=='timber':return 3
    if f in ('walls','partitions') and m=='plywood' or (f=='insulation' and not id.startswith(('insulation-floor','insulation-ceiling'))):return 4
    if f in ('roof','ceiling') or id.startswith('insulation-ceiling'):return 5
    if f in ('facade','terrace') or m in ('glass','object') and f!='furniture':return 6
    return 7

def assembly(scene):
    sheets=[]
    p=page('Surinkimo gairės / turinys','M-00');sheets.append(p)
    text(p,25,244,'Eiga paremta modelio grupėmis. Tai surinkimo studija, ne patvirtinta darbų technologija.',3)
    rect(p,25,108,370,120)
    for i,(title,_,note) in enumerate(STAGES):
        y=218-i*14;text(p,30,y,title,3);text(p,365,y,f'M-{i+1:02}');line(p,25,y-5,395,y-5)
    for j,t in enumerate(['Prieš gamybą: konstruktorius patvirtina jungtis, laikiną stabilumą ir kėlimo planą.',
                         'Tvirtinimo detalių kiekiai ir suveržimo momentai neišgalvoti - jie dar nepateikti.',
                         'Baltai rodoma nauja stadija, pilkai - jau surinkta dalis. Vaizdai iš to paties modelio.']):text(p,25,91-j*12,t,2.7)
    for i,(title,_,note) in enumerate(STAGES):
        p=page(f'{i+1:02} / '+title,f'M-{i+1:02}');sheets.append(p)
        current=[a for a in scene['parts'] if stage(a)==i];previous=[a for a in scene['parts'] if stage(a)<i]
        # A clear stage-only exploded overview and context view; geometry remains unchanged.
        highlight={a['id'] for a in current}
        slot(p,'Surinkta iki šios stadijos',axon(previous+current,highlight),[25,77,272,250],(50,75,100,150,200))
        slot(p,'Pridedami elementai',axon(current),[282,130,400,245],(50,75,100,150,200))
        text(p,282,121,'Pridedamos detalės: '+str(len(current)),2.8)
        text(p,25,66,note,2.3)
        groups=component_groups(dict(scene,parts=current))
        codes=[g['code'] for g in groups]
        for j in range(min(4,math.ceil(len(codes)/5))):text(p,282,110-j*8,', '.join(codes[j*5:j*5+5]),1.9)
        if len(codes)>20:text(p,282,75,'Visi indeksai - kiekių byloje.',2)
    return finish(scene,sheets,'assembly')

def documents(scene):return {'openings':openings(scene),'components':components(scene),'assembly':assembly(scene)}
