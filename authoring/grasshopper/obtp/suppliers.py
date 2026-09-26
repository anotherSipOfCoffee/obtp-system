"""Supplier provenance, distinct from geometry and engineering acceptance.
An alternative system must have its own verified geometry adapter before selection.
"""
import copy
SYSTEMS = [
 {'id':0,'key':'obtp-cassette','label':'OBTP Cassette','enabled':True,'default':True,
  'supplier':'OBTP','status':'project-study','reason_lt':None},
 {'id':1,'key':'hunton','label':'Hunton','enabled':False,'default':False,
  'supplier':'Hunton','status':'research-candidate','logo':'hunton.png',
  'url':'https://www.hunton.no/produkter/gulv/hunton-konstruksjon/',
  'reason_lt':'Ruošiama: reikia suderinti pirties sluoksnius, jungtis ir tiekimą Lietuvoje.'}]

PRODUCTS = [
 {'id':'window-pihla','category_lt':'Langas','category_en':'Window','supplier':'Pihla','product':'Varma Kiinteä / sauna',
  'status':'dimensional-candidate','status_lt':'Parinkimo kandidatas','status_en':'Product candidate','logo':'pihla.png',
  'url':'https://www.pihla.fi/product/saunan-ikkuna/',
  'scope_lt':'Modelio rėmas 170 mm. Stiklo paketas, tarpai ir montavimo mazgas dar derinami.',
  'scope_en':'170 mm model frame. Glazing, installation gaps and junction design remain to be confirmed.'},
 {'id':'heater-harvia','category_lt':'Krosnelė','category_en':'Heater','supplier':'Harvia','product':'Spirit SP90E / HSPE904M',
  'status':'research-candidate','status_lt':'Parinkimo kandidatas','status_en':'Product candidate','logo':'harvia.svg',
  'url':'https://www.harvia.com/en/products/HSPE904M/spirit-sp90e-90-kw-black',
  'scope_lt':'9 kW kandidatas. 3D modelyje dar rodomas bendrinis krosnelės tūris.',
  'scope_en':'9 kW candidate. The 3D model still shows a generic heater placeholder.'},
 {'id':'vapour-harvia','category_lt':'Garų izoliacija','category_en':'Vapour control','supplier':'Harvia','product':'SAS10001 / SAS10002',
  'status':'specification-candidate','status_lt':'Specifikacijos kandidatas','status_en':'Specification candidate','logo':'harvia.svg',
  'url':'https://www.harvia.com/en/products/SAS10001/aluminium-paper-12530-m2',
  'scope_lt':'Aliuminio popierius ir siūlių juosta. Pravedimų bei jungčių sprendiniai tikslinami.',
  'scope_en':'Aluminium paper and seam tape. Penetration and junction details remain unresolved.'},
 {'id':'lining-thermory','category_lt':'Pirties apdaila ir gultai','category_en':'Sauna lining and benches','supplier':'Thermory','product':'Installation guides',
  'status':'reference-only','status_lt':'Montavimo gairių šaltinis','status_en':'Installation reference','logo':None,
  'url':'https://thermory.com/wp-content/uploads/2023/01/Thermory_Installation_Guide_Sauna-wall-panels_A4_0123_ENG.pdf',
  'scope_lt':'Montavimo principai; konkretūs modelio profiliai nėra parinkti Thermory gaminiai.',
  'scope_en':'Installation principles; the model profiles are not selected Thermory products.'},
 {'id':'roof-ruukki','category_lt':'Šlaitinio stogo danga','category_en':'Pitched roof covering','supplier':'Ruukki','product':'Classic C',
  'status':'dimensional-reference','status_lt':'Matmenų ir nuolydžio šaltinis','status_en':'Geometry reference','logo':None,
  'url':'https://www.ruukki.com/ltu/stogai/produktai-stogams/stogo-dangos-lakstai/stogo-dangos-produktai/parnu-classic-c',
  'scope_lt':'475 mm dengiamasis plotis, 32 mm siūlė. Pilnas stogo mazgas dar nesuderintas.',
  'scope_en':'475 mm cover width and 32 mm seam. Complete roof assembly remains unresolved.'}]


def catalogue():
    return copy.deepcopy({'schema':'obtp-suppliers/1','systems':SYSTEMS,'products':PRODUCTS,
                          'reviewed':'2026-09-26','default_system':0})


def require_system(identifier):
    selected=next((x for x in SYSTEMS if x['id']==identifier),None)
    if not selected:raise ValueError('Unknown construction system')
    if not selected['enabled']:raise ValueError('Supplier system is not implemented or coordinated: '+selected['label'])
    return copy.deepcopy(selected)


def attach(scene):
    """Link current parts to reference records without relabelling generic materials."""
    data=catalogue();data['active_system']=require_system(scene['config'].get('system_type',0))
    data['products']=[p for p in data['products'] if scene['config']['roof_type']!=0 or p['id']!='roof-ruukki']
    if scene['config'].get('program_type',0)==1:
        data['products']=[p for p in data['products'] if p['id'] in ('window-pihla','roof-ruukki')]
        for record in data['products']:
            if record['id']=='window-pihla':
                record['product']='Varma Kiinteä / fixed window reference'
                record['scope_lt']='Bendro modelio 170 mm rėmas. Studijai tinkamas įstiklinimas ir montavimo mazgas dar tikslinami.'
                record['scope_en']='Shared 170 mm frame reference. Studio glazing and installation detail remain unselected.'
    def match(product,p):
        if product=='window-pihla':return p['id'].startswith('window/')
        if product=='heater-harvia':return p['id'].startswith('heater/')
        if product=='lining-thermory':return p['family'] in ('interior','ceiling') or p['id'].startswith('bench-')
        if product=='roof-ruukki':return p['material']=='roof-metal'
        return False
    for record in data['products']:
        record['source_part_ids']=[p['id'] for p in scene['parts'] if match(record['id'],p)]
    data['unassigned_types']=['structural timber and plywood','mineral wool product/thickness schedule',
       'external cladding profile','doors','decking','waterproof floor finish','foundations and anchors',
       'joint fastener schedules','ventilation','outdoor shower']+(['flat roof membrane'] if scene['config']['roof_type']==0 else [])
    return data
