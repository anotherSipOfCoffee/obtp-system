#! python 3
"""Run once in Rhino 8 ScriptEditor (Python 3), with Grasshopper open.
Creates a native editable .gh beside this script, without touching existing documents.
Requires the modern Python3Component.Create API; unsupported Rhino builds fail explicitly.
"""
from datetime import datetime
from pathlib import Path
import json
import traceback
import clr
import Rhino
import Grasshopper
from Grasshopper.Kernel import GH_Document, GH_DocumentIO, GH_ParamAccess
from Grasshopper.Kernel.Special import GH_NumberSlider, GH_BooleanToggle, GH_ValueList, GH_ValueListItem, GH_ValueListMode, GH_Panel, GH_Group
from Grasshopper.GUI.Base import GH_SliderAccuracy
from System import Decimal, Double, Boolean, String
from System.Drawing import PointF, Color, SizeF, RectangleF

ROOT=Path(__file__).resolve().parent


def local_module(module):
    """Resolve this download explicitly, even with an older obtp already cached."""
    import hashlib
    import importlib
    import importlib.util
    import sys
    package_root=ROOT/'obtp'
    target=package_root/(module+'.py')
    if not target.is_file():
        raise FileNotFoundError('Missing '+str(target)+'. Extract the complete source ZIP before running setup.')
    name='_obtp_setup_'+hashlib.sha256(str(package_root.resolve()).encode()).hexdigest()[:16]
    if name not in sys.modules:
        spec=importlib.util.spec_from_file_location(name,package_root/'__init__.py',submodule_search_locations=[str(package_root)])
        package=importlib.util.module_from_spec(spec)
        sys.modules[name]=package
        try:spec.loader.exec_module(package)
        except Exception:
            del sys.modules[name]
            raise
    return importlib.import_module(name+'.'+module)


def main():
    if Rhino.RhinoDoc.ActiveDoc is None or Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem != Rhino.UnitSystem.Millimeters:
        raise ValueError('Open a millimetre Rhino document first; this script never rescales your document.')
    if Grasshopper.Instances.ActiveCanvas is None:
        raise RuntimeError('Open Grasshopper first, then run this script again.')
    # Resolve only the already loaded Rhino script component assembly.
    from System import AppDomain
    assemblies=[a for a in AppDomain.CurrentDomain.GetAssemblies() if a.GetName().Name=='RhinoCodePluginGH']
    if not assemblies:
        raise RuntimeError('Drop a Python 3 Script component onto a blank GH canvas once to initialize it, then rerun setup.')
    clr.AddReference(assemblies[0].Location)
    from RhinoCodePluginGH.Components import Python3Component
    from RhinoCodePluginGH.Parameters import ScriptVariableParam
    if not hasattr(Python3Component,'Create'):
        raise RuntimeError('This Rhino build lacks the script creation API. Install a current Rhino 8 service release. See README fallback.')
    doc=GH_Document()
    def place(obj,x,y):
        obj.CreateAttributes();obj.Attributes.Pivot=PointF(x,y);doc.AddObject(obj,False);return obj
    def slider(name,value,minimum,maximum,x,y):
        obj=GH_NumberSlider();obj.CreateAttributes();obj.NickName=name
        obj.Slider.Type=GH_SliderAccuracy.Integer
        obj.Slider.Minimum=Decimal(minimum);obj.Slider.Maximum=Decimal(maximum)
        obj.SetSliderValue(Decimal(value));return place(obj,x,y)
    def toggle(name,value,x,y):
        obj=GH_BooleanToggle();obj.NickName=name;obj.Value=value;return place(obj,x,y)
    def panel(text,x,y,width=350,height=200):
        obj=GH_Panel();obj.UserText=text;place(obj,x,y)
        obj.Attributes.Bounds=RectangleF(x,y,width,height)
        return obj
    def script(name,file,inputs,outputs,x,y,stage=None):
        code=(ROOT/'components'/file).read_text(encoding='utf-8')
        if stage is not None:code=code.replace("STAGE_NAME='structure'",'STAGE_NAME='+repr(stage))
        obj=Python3Component.Create(name,code)
        obj.UsingStandardOutputParam=False
        for p in list(obj.Params.Input):obj.Params.UnregisterInputParameter(p)
        for p in list(obj.Params.Output):obj.Params.UnregisterOutputParameter(p)
        for n,t in inputs:
            p=ScriptVariableParam(n);p.PrettyName=n;p.ToolTip=n.replace('_',' ');p.Optional=True;p.Access=GH_ParamAccess.item
            # Keep the native default hint; components explicitly normalize inputs.
            # Select(System.Type) is unavailable in some Rhino 8 builds.
            p.CreateAttributes();obj.Params.RegisterInputParam(p)
        for n,access in outputs:
            p=ScriptVariableParam(n);p.Access=access;p.CreateAttributes();obj.Params.RegisterOutputParam(p)
        # Source is already assigned by Create(name, code). Some Rhino 8 builds
        # do not expose SetSource; changing ports only needs maintenance.
        obj.VariableParameterMaintenance()
        return place(obj,x,y)
    def group(name,objects,color):
        g=GH_Group();g.NickName=name;g.Colour=color;doc.AddObject(g,False)
        for obj in objects:g.AddObject(obj.InstanceGuid)
        return g
    def choices(name,labels,default,x,y):
        obj=GH_ValueList();obj.NickName=name;obj.ListMode=GH_ValueListMode.DropDown;obj.ListItems.Clear()
        for number,label in labels:
            entry=GH_ValueListItem(label,str(number));entry.Selected=(number==default);obj.ListItems.Add(entry)
        return place(obj,x,y)
    labels=list(local_module('sauna_workflow').PRESETS)
    controls={'preset_index':choices('Preset / saved or custom',list(enumerate(labels)),2,40,80)}
    controls['base_preset']=choices('Custom starting preset',list(enumerate(['S open','S storage','M open','M storage','L open','L storage'])),2,40,150)
    controls['use_overrides']=toggle('Use custom overrides / False = RESET',False,40,210)
    for i,(key,label) in enumerate([('sauna','Sauna active'),('entrance','Entrance active'),('outdoor','Outdoor active')]):
        controls[key]=toggle(label,True,40,300+i*50)
    for i,(key,label) in enumerate([('sauna_cells','Sauna length change'),('entrance_cells','Entrance length change'),('outdoor_cells','Outdoor length change'),('work_cells','Studio work length change'),('centre_cells','Studio centre length change'),('preparation_cells','Studio preparation length change')]):
        controls[key+'_delta']=slider(label+' / 900 mm cells from base',0,-1,1,40,500+i*55)
    edge_choices=[(0,'None'),(1,'Adjacent'),(2,'Internal passage'),(3,'External access')]
    for i,(key,label,default) in enumerate([('sauna_entrance','Sauna to entrance',2),('entrance_outdoor','Entrance to outdoor',3),('sauna_outdoor','Sauna to outdoor',0)]):
        controls[key]=choices(label,edge_choices,default,40,950+i*55)
    controls['arrangement']=slider('Sauna strip order / check valid range in Layout',0,0,5,40,1150)
    controls['roof_type']=choices('Roof',[(0,'Plokščias / membrane'),(1,'Single slope / metal')],1,500,650)
    controls['window_width']=choices('Window frame / mm',[(w,str(w)) for w in [580,880,1180]],1180,500,710)
    controls['window_shift']=choices('Window adjacent bay',[(v,str(v)) for v in [-1,0,1]],0,500,770)
    controls['wall_height']=choices('Wall height / mm',[(h,str(h)) for h in [2100,2700]],2100,500,830)
    controls['foundation_type']=choices('Foundation study',[(0,'Timber on piles'),(1,'Concrete grillage')],0,500,890)
    controls['include_foundation']=toggle('Include foundation study',True,500,950)
    preset=script('01 Preset and programme','sauna_preset.py',[(k,Boolean if k in ('sauna','entrance','outdoor','include_foundation','use_overrides') else Double) for k in controls],[('workflow_json',GH_ParamAccess.item),('report',GH_ParamAccess.item)],500,100)
    for i,obj in enumerate(controls.values()):preset.Params.Input[i].AddSource(obj)
    preset_report=panel('',500,270,430,280);preset_report.AddSource(preset.Params.Output[1])
    purpose=panel('01 INPUTS / Select a saved building or Custom. Custom starts from the selected S/M/L preset; False uses base dimensions and room programme; delta sliders retain their displayed offsets. Room controls apply to Sauna; Studio retains work-centre-preparation. Integer cell increments; typed inputs receive the same validation. Dependent fit/area failures stop the pipeline. All capacity and connection claims remain unresolved.',40,1270,900,200)
    group('01 / PRESET, PROGRAMME AND RELATIONSHIPS',list(controls.values())+[preset,preset_report,purpose],Color.FromArgb(220,232,221))
    layout=script('02 Layout and dimensional coordination','room_layout.py',[('workflow_json',String)],[('plan_json',GH_ParamAccess.item),('geometry',GH_ParamAccess.list),('materials',GH_ParamAccess.list),('labels',GH_ParamAccess.list),('label_points',GH_ParamAccess.list),('report',GH_ParamAccess.item)],1100,100)
    layout.Params.Input[0].AddSource(preset.Params.Output[0])
    plan_report=panel('',1100,280,440,380);plan_report.AddSource(layout.Params.Output[5])
    proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies if p.Desc.Name=='Custom Preview' and p.Desc.Category=='Display' and not p.Obsolete]
    if len(proxies)!=1:raise RuntimeError('Expected one native Custom Preview component')
    layout_colour=place(proxies[0].CreateInstance(),1100,750)
    layout_colour.Params.Input[0].AddSource(layout.Params.Output[1]);layout_colour.Params.Input[1].AddSource(layout.Params.Output[2]);layout.Hidden=True
    labels_panel=panel('',1100,850,440,240);labels_panel.AddSource(layout.Params.Output[3])
    tag_objects=[]
    tag_proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies if p.Desc.Name=='Text Tag 3D']
    if tag_proxies:
        tag=tag_proxies[0].CreateInstance();ports={p.Name.lower():p for p in tag.Params.Input}
        location=next((v for k,v in ports.items() if k in ('location','locations')),None)
        text_port=next((v for k,v in ports.items() if k in ('text','tag')),None)
        if location is not None and text_port is not None:
            place(tag,1100,1170);location.AddSource(layout.Params.Output[4]);text_port.AddSource(layout.Params.Output[3]);tag_objects.append(tag)
            if 'size' in ports:
                label_size=slider('Plan label size / mm',100,30,200,1100,1240);ports['size'].AddSource(label_size);tag_objects.append(label_size)
    group('02 / PLAN · boundaries, rooms and relationships',[layout,plan_report,layout_colour,labels_panel]+tag_objects,Color.FromArgb(233,226,207))
    def stage(key,title,sources,x,y,purpose):
        obj=script(title,'construction_stage.py',[(n,String) for n,source in sources],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('details',GH_ParamAccess.list)],x,y,stage=key)
        for i,(n,source) in enumerate(sources):obj.Params.Input[i].AddSource(source)
        status=panel('',x,y+150,440,130);status.AddSource(obj.Params.Output[1])
        note=panel(purpose,x,y+320,440,100)
        show=toggle('Preview '+key,False,x,y+470)
        view=script('Preview / '+key,'stage_preview.py',[('data_json',String),('show',Boolean)],[('geometry',GH_ParamAccess.list),('part_ids',GH_ParamAccess.list),('report',GH_ParamAccess.item)],x,y+550)
        view.Params.Input[0].AddSource(obj.Params.Output[0]);view.Params.Input[1].AddSource(show)
        group(title,[obj,status,note,show,view],Color.FromArgb(230,229,220))
        return obj
    structure=stage('structure','03 Opening hosts and structural arrangement',[('plan_json',layout.Params.Output[0])],1700,100,'Derives wall runs, opening hosts, corners, junctions and slab boundaries from the strip plan. Details output lists dimensions and unresolved connections; preview shows wall envelopes.')
    src=structure.Params.Output[0]
    floor=stage('floor','04a Floor cassettes',[('structure_json',src)],2300,100,'Manufactures floor joists, blocking, partition trimmers and plywood from plan boundaries. Width is the candidate bearing span; no capacity assertion.')
    roof=stage('roof','04b Roof cassettes',[('structure_json',src)],2300,900,'Independent roof-cassette generation. Studio centre uses header-seat deductions. Weather roof is generated in stage 08.')
    walls=stage('walls','04c Wall cassettes and opening products',[('structure_json',src)],2300,1700,'Manufactures actual cassette constituents, terminal pieces, opening framing and programme objects. Window fitting allowances retained.')
    merged=stage('framing','05 Coordinated frame',[('structure_json',src),('floor_json',floor.Params.Output[0]),('roof_json',roof.Params.Output[0]),('walls_json',walls.Params.Output[0])],2900,100,'Checks that independent branches belong to this exact plan, then combines their parts. No branch rebuilds another branch.')
    previous=merged
    for key,title,x,y,description in [
      ('surfaces','06 Panels, lining and finishes',3500,100,'Adds seasonal glazing, room lining, ceiling finish and facade finish. Structural skins were generated with their cassettes.'),
      ('terrace','07 Coordinated terrace',3500,900,'Generates deck, edge members and supported butt joints from the same building envelope; 1200 mm front coordination strip; programme-specific side return.'),
      ('weather','08 Weather roof',4100,900,'Generates pitched or flat weather roof, bearing frames and canopy. Cantilever, roof uplift and covering acceptance remain unresolved.'),
      ('foundation','09 Foundation arrangement',4700,900,'Generates coordinated support nodes and selected foundation study. Soil, pile resistance and connection capacities remain unknown.'),
      ('insulation','10 Insulation cavities',4700,100,'Derives insulation blanks around the actual framing and openings. Thermal and moisture performance are not certified.'),
      ('complete','11 Complete model, drawings and quantities',5300,100,'Finalizes IDs, drawings and canonical quantities. Facade boards retain a separate schedule. Every export takes this complete scene.')]:
        previous=stage(key,title,[('structure_json',src),('previous_json',previous.Params.Output[0])],x,y,description)
    cassette=previous
    assembly=script('CP4 · Assembly sequence','assembly_checkpoint.py',[('scene_json',String),('assembly_stage',Double)],
      [('display_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('steps',GH_ParamAccess.list)],6250,100)
    assembly.Params.Input[0].AddSource(cassette.Params.Output[0])
    stage_control=slider('ASSEMBLY PROGRESS / 0 empty - 100 complete',100,0,100,6250,220)
    assembly.Params.Input[1].AddSource(stage_control)
    assembly_report=panel('',6250,300,400,180);assembly_report.AddSource(assembly.Params.Output[1])
    step_list=panel('',6250,530,400,400);step_list.AddSource(assembly.Params.Output[2])
    preview=script('CP5 · Final 3D preview','final_preview.py',[('display_json',String),('preview_scope',Double),('type_colours',Boolean),('assembly_filter',String)],
      [(n,GH_ParamAccess.list) for n in ['geometry','part_ids','materials','type_ids','legend']]+[('preview_status',GH_ParamAccess.item)],6850,100)
    preview.Params.Input[0].AddSource(assembly.Params.Output[0])
    scope_control=choices('FINAL VIEW',[(0,'Structure + panels'),(1,'Building / no facade boards'),(2,'Complete / with cladding')],2,6850,220)
    colour_control=toggle('Colour by unique part type',False,6850,270)
    assembly_filter=panel('',6850,380,400,70);assembly_filter.NickName='ISOLATE ASSEMBLY / blank = all; exact CP3 ID'
    for i,obj in enumerate([scope_control,colour_control,assembly_filter],1):preview.Params.Input[i].AddSource(obj)
    proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies if p.Desc.Name=='Custom Preview' and p.Desc.Category=='Display' and not p.Obsolete]
    if len(proxies)!=1:raise RuntimeError('Expected one native Custom Preview component')
    coloured=place(proxies[0].CreateInstance(),7400,100)
    coloured.Params.Input[0].AddSource(preview.Params.Output[0]);coloured.Params.Input[1].AddSource(preview.Params.Output[2]);preview.Hidden=True
    preview_note=panel('',6850,530,400,230);preview_note.AddSource(preview.Params.Output[5])
    type_legend=panel('',7400,530,400,400);type_legend.AddSource(preview.Params.Output[4])
    inspector=script('CP3 · Inspect rooms / openings / assemblies / parts','inspect_checkpoints.py',[('scene_json',String)],
      [('report',GH_ParamAccess.item)]+[(n,GH_ParamAccess.list) for n in ['rooms','openings','assembly_ids','assembly_rows','part_rows','checks']],5650,1200)
    inspector.Params.Input[0].AddSource(cassette.Params.Output[0])
    audit_report=panel('',5650,1420,400,300);audit_report.AddSource(inspector.Params.Output[0])
    assembly_ids=panel('',6250,1200,400,520);assembly_ids.AddSource(inspector.Params.Output[3])
    audit_note=panel('CHECKPOINT OUTPUTS: connect a Panel to rooms, openings, assembly_rows, part_rows or checks. Change variety through CP1 controls; direct JSON edits fail validation. Copy an assembly ID to CP5 to isolate it. Blank restores all.',5650,1780,950,130)
    export_toggle=toggle('Export model + drawings (PDF disabled)',False,6850,1200)
    export=script('06 · Checked export','export.py',[('scene_json',String),('run_export',Boolean)],[('receipt',GH_ParamAccess.item)],6850,1300)
    export.Params.Input[0].AddSource(cassette.Params.Output[0]);export.Params.Input[1].AddSource(export_toggle)
    receipt=panel('',7400,1200,400,350);receipt.AddSource(export.Params.Output[0])
    group('12 / ASSEMBLY · laydown, raising, cladding last',[assembly,stage_control,assembly_report,step_list],Color.FromArgb(224,218,235))
    group('13 / FINAL PREVIEW · display-only',[preview,scope_control,colour_control,assembly_filter,coloured,preview_note,type_legend],Color.FromArgb(218,228,235))
    group('14 / DIAGNOSTICS AND EXPORT',[inspector,audit_report,assembly_ids,audit_note,export,export_toggle,receipt],Color.FromArgb(237,235,212))
    settings=panel(json.dumps(local_module('analysis').inputs(),indent=2),40,3000,400,500)
    run_analysis=toggle('Export analysis preparation',False,550,3000)
    analysis=script('Analysis preparation','analysis.py',[('scene_json',String),('inputs_json',String),('run_export',Boolean)],
      [(n,GH_ParamAccess.item) for n in ['preflight_json','geometry_report','solver_report','results_report','diagrams_report','receipt']],550,3100)
    for i,source in enumerate([cassette.Params.Output[0],settings,run_analysis]):analysis.Params.Input[i].AddSource(source)
    analysis_panels=[]
    for i in range(1,6):
        item=panel('',1050+(i-1)*480,3000,400,500);item.AddSource(analysis.Params.Output[i]);analysis_panels.append(item)
    group('ANALYSIS / preparation only · capacities and solver acceptance unresolved',[settings,run_analysis,analysis]+analysis_panels,Color.FromArgb(220,232,221))
    # Never overwrite a definition the owner may have edited.
    name='OBTP_Plan_Cassette_R27_'+datetime.now().strftime('%Y%m%d_%H%M%S')
    path=ROOT/(name+'.gh')
    if not GH_DocumentIO(doc).SaveQuiet(str(path)):raise IOError('Could not write native GH definition')
    doc.FilePath=str(path)
    Grasshopper.Instances.DocumentServer.AddDocument(doc)
    Grasshopper.Instances.ActiveCanvas.Document=doc
    doc.Enabled=True;doc.NewSolution(False)
    receipt_data=dict(rhino_version=str(Rhino.RhinoApp.Version),definition=path.name,
                      status='Definition created; inspect GH runtime messages before acceptance')
    (ROOT/'setup-receipt.json').write_text(json.dumps(receipt_data,indent=2))
    print('Created and opened '+str(path))

try:main()
except Exception:
    error=traceback.format_exc()
    (ROOT/'setup-error.txt').write_text(error,encoding='utf-8')
    print(error)
    raise

