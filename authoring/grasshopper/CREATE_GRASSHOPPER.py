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
    def script(name,file,inputs,outputs,x,y):
        code=(ROOT/'components'/file).read_text(encoding='utf-8')
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
    controls={'preset_index':choices('BUILDING PRESET / Sauna, Custom Sauna, Studio',list(enumerate(labels)),2,40,60)}
    for i,(key,label) in enumerate([('sauna','Custom / sauna room'),('entrance','Custom / entrance room'),('outdoor','Custom / outdoor zone')]):
        controls[key]=toggle(label,True,40,180+i*45)
    for i,(key,label,value_,lo,hi) in enumerate([('sauna_cells','Custom / sauna length / 900 mm cells',3,3,8),('entrance_cells','Custom / entrance length / 900 mm cells',3,2,8),('outdoor_cells','Custom / outdoor length / 900 mm cells',1,1,4),('depth_cells','Custom / depth / 1200 mm cells',2,2,4)]):
        controls[key]=slider(label,value_,lo,hi,40,340+i*45)
    edge_choices=[(0,'No relationship'),(1,'Adjacent'),(2,'Internal passage'),(3,'External access route')]
    for i,(key,label,default) in enumerate([('sauna_entrance','Custom / sauna to entrance',2),('entrance_outdoor','Custom / entrance to outdoor',3),('sauna_outdoor','Custom / sauna to outdoor',0)]):
        controls[key]=choices(label,edge_choices,default,40,560+i*45)
    controls['arrangement']=slider('Custom / arrangement / valid range in plan report',0,0,5,40,740)
    controls['roof_type']=choices('Roof',[(0,'Plokščias / membrane'),(1,'Single slope / metal')],1,450,600)
    controls['window_width']=choices('Window frame width / mm',[(w,str(w)) for w in [580,880,1180]],1180,450,645)
    controls['wall_height']=choices('Wall height / mm',[(h,str(h)) for h in [2100,2700]],2100,450,690)
    controls['foundation_type']=choices('Foundation',[(0,'Timber support frame on piles'),(1,'Concrete pile grillage study')],0,450,735)
    controls['include_foundation']=toggle('Include foundation study',True,450,780)
    preset=script('CP1 · Preset + parameters','sauna_preset.py',[(k,Boolean if k in ('sauna','entrance','outdoor','include_foundation') else Double) for k in controls],
      [('workflow_json',GH_ParamAccess.item),('report',GH_ParamAccess.item)],450,100)
    for i,obj in enumerate(controls.values()):preset.Params.Input[i].AddSource(obj)
    preset_report=panel('',450,220,400,250);preset_report.AddSource(preset.Params.Output[1])
    layout=script('CP2 · Layout plan','room_layout.py',[('workflow_json',String)],
      [('plan_json',GH_ParamAccess.item),('geometry',GH_ParamAccess.list),('materials',GH_ParamAccess.list),('labels',GH_ParamAccess.list),('label_points',GH_ParamAccess.list),('report',GH_ParamAccess.item)],1000,100)
    layout.Params.Input[0].AddSource(preset.Params.Output[0])
    plan_report=panel('',1000,240,400,350);plan_report.AddSource(layout.Params.Output[5])
    cassette=script('CP3 · Cassette construction','sauna_cassette.py',[('plan_json',String)],
      [('scene_json',GH_ParamAccess.item),('report',GH_ParamAccess.item)],1550,100)
    cassette.Params.Input[0].AddSource(layout.Params.Output[0])
    cassette_report=panel('',1550,240,400,300);cassette_report.AddSource(cassette.Params.Output[1])
    assembly=script('CP4 · Assembly sequence','assembly_checkpoint.py',[('scene_json',String),('assembly_stage',Double)],
      [('display_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('steps',GH_ParamAccess.list)],2100,100)
    assembly.Params.Input[0].AddSource(cassette.Params.Output[0])
    stage_control=slider('ASSEMBLY PROGRESS / 0 empty - 100 complete',100,0,100,2100,220)
    assembly.Params.Input[1].AddSource(stage_control)
    assembly_report=panel('',2100,300,400,180);assembly_report.AddSource(assembly.Params.Output[1])
    step_list=panel('',2100,530,400,400);step_list.AddSource(assembly.Params.Output[2])
    preview=script('CP5 · Final 3D preview','final_preview.py',[('display_json',String),('preview_scope',Double),('type_colours',Boolean),('assembly_filter',String)],
      [(n,GH_ParamAccess.list) for n in ['geometry','part_ids','materials','type_ids','legend']]+[('preview_status',GH_ParamAccess.item)],2700,100)
    preview.Params.Input[0].AddSource(assembly.Params.Output[0])
    scope_control=choices('FINAL VIEW',[(0,'Structure + panels'),(1,'Building / no facade boards'),(2,'Complete / with cladding')],2,2700,220)
    colour_control=toggle('Colour by unique part type',False,2700,270)
    assembly_filter=panel('',2700,380,400,70);assembly_filter.NickName='ISOLATE ASSEMBLY / blank = all; exact CP3 ID'
    for i,obj in enumerate([scope_control,colour_control,assembly_filter],1):preview.Params.Input[i].AddSource(obj)
    proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies if p.Desc.Name=='Custom Preview' and p.Desc.Category=='Display' and not p.Obsolete]
    if len(proxies)!=1:raise RuntimeError('Expected one native Custom Preview component')
    coloured=place(proxies[0].CreateInstance(),3200,100)
    coloured.Params.Input[0].AddSource(preview.Params.Output[0]);coloured.Params.Input[1].AddSource(preview.Params.Output[2]);preview.Hidden=True
    preview_note=panel('',2700,530,400,230);preview_note.AddSource(preview.Params.Output[5])
    type_legend=panel('',3200,530,400,400);type_legend.AddSource(preview.Params.Output[4])
    layout_colour=place(proxies[0].CreateInstance(),1000,650)
    layout_colour.Params.Input[0].AddSource(layout.Params.Output[1]);layout_colour.Params.Input[1].AddSource(layout.Params.Output[2]);layout.Hidden=True
    label_report=panel('',1000,730,400,200);label_report.AddSource(layout.Params.Output[3])
    tag_objects=[]
    tag_proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies if p.Desc.Name=='Text Tag 3D']
    if tag_proxies:
        tag=tag_proxies[0].CreateInstance();ports={p.Name.lower():p for p in tag.Params.Input}
        location=next((v for k,v in ports.items() if k in ('location','locations')),None)
        text_port=next((v for k,v in ports.items() if k in ('text','tag')),None)
        if location is not None and text_port is not None:
            place(tag,1000,1030);location.AddSource(layout.Params.Output[4]);text_port.AddSource(layout.Params.Output[3]);tag_objects.append(tag)
            if 'size' in ports:
                label_size=slider('Plan label size / mm',100,30,200,1000,1100);ports['size'].AddSource(label_size);tag_objects.append(label_size)
    inspector=script('CP3 · Inspect rooms / openings / assemblies / parts','inspect_checkpoints.py',[('scene_json',String)],
      [('report',GH_ParamAccess.item)]+[(n,GH_ParamAccess.list) for n in ['rooms','openings','assembly_ids','assembly_rows','part_rows','checks']],1550,1200)
    inspector.Params.Input[0].AddSource(cassette.Params.Output[0])
    audit_report=panel('',1550,1420,400,300);audit_report.AddSource(inspector.Params.Output[0])
    assembly_ids=panel('',2100,1200,400,520);assembly_ids.AddSource(inspector.Params.Output[3])
    audit_note=panel('CHECKPOINT OUTPUTS: connect a Panel to rooms, openings, assembly_rows, part_rows or checks. Change variety through CP1 controls; direct JSON edits fail validation. Copy an assembly ID to CP5 to isolate it. Blank restores all.',1550,1780,950,130)
    export_toggle=toggle('Export model + drawings (PDF disabled)',False,2700,1200)
    export=script('06 · Checked export','export.py',[('scene_json',String),('run_export',Boolean)],[('receipt',GH_ParamAccess.item)],2700,1300)
    export.Params.Input[0].AddSource(cassette.Params.Output[0]);export.Params.Input[1].AddSource(export_toggle)
    receipt=panel('',3200,1200,400,350);receipt.AddSource(export.Params.Output[0])
    group('01 / PRESET + PARAMETERS · Custom controls apply only to Custom Sauna',list(controls.values())+[preset,preset_report],Color.FromArgb(220,232,221))
    group('02 / PLAN · inspect geometry, room labels and validity',[layout,plan_report,layout_colour,label_report]+tag_objects,Color.FromArgb(233,226,207))
    group('03 / CONSTRUCTION · authoritative complete scene',[cassette,cassette_report],Color.FromArgb(237,223,211))
    group('04 / ASSEMBLY · connected wall laydown, raising and cladding last',[assembly,stage_control,assembly_report,step_list],Color.FromArgb(224,218,235))
    group('05 / FINAL PREVIEW · scope, type colours and optional isolation',[preview,scope_control,colour_control,assembly_filter,coloured,preview_note,type_legend],Color.FromArgb(218,228,235))
    group('DIAGNOSTICS / CP3 · inspect without modifying source',[inspector,audit_report,assembly_ids,audit_note],Color.FromArgb(237,235,212))
    group('EXPORT / complete source, independent of preview filters',[export,export_toggle,receipt],Color.FromArgb(235,222,218))
    settings=panel(json.dumps(local_module('analysis').inputs(),indent=2),40,2200,400,500)
    run_analysis=toggle('Export analysis preparation',False,550,2200)
    analysis=script('Analysis preparation','analysis.py',[('scene_json',String),('inputs_json',String),('run_export',Boolean)],
      [(n,GH_ParamAccess.item) for n in ['preflight_json','geometry_report','solver_report','results_report','diagrams_report','receipt']],550,2300)
    for i,source in enumerate([cassette.Params.Output[0],settings,run_analysis]):analysis.Params.Input[i].AddSource(source)
    analysis_panels=[]
    for i in range(1,6):
        item=panel('',1050+(i-1)*480,2200,400,500);item.AddSource(analysis.Params.Output[i]);analysis_panels.append(item)
    group('ANALYSIS / preparation only · capacities and solver acceptance unresolved',[settings,run_analysis,analysis]+analysis_panels,Color.FromArgb(220,232,221))
    # Never overwrite a definition the owner may have edited.
    name='OBTP_Cassette_Checkpoints_R26_'+datetime.now().strftime('%Y%m%d_%H%M%S')
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

