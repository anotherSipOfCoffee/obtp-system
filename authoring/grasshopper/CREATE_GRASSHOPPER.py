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
from System.Drawing import PointF, Color, SizeF

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
        obj.VariableParameterMaintenance();obj.SetSource(code)
        return place(obj,x,y)
    def group(name,objects,color):
        g=GH_Group();g.NickName=name;g.Colour=color;doc.AddObject(g,False)
        for obj in objects:g.AddObject(obj.InstanceGuid)
        return g
    presets=GH_ValueList();presets.NickName='Saved size / storage configuration';presets.ListMode=GH_ValueListMode.DropDown
    presets.ListItems.Clear()
    labels=['S / no storage','S / storage','M / no storage','M / storage','L / no storage','L / storage']
    for i,label in enumerate(labels):
        item=GH_ValueListItem(label,str(i));item.Selected=(i==2);presets.ListItems.Add(item)
    place(presets,40,60)
    controls={'preset_index':presets,'custom':toggle('Use custom parameters',False,40,110)}
    values=[('room_depth_steps',3,3,8),('sauna_length_steps',4,3,8),('hall_length_steps',3,2,8),
            ('storage_length_steps',2,2,4),('wall_height',2100,2100,2700),('partition_depth',90,90,120),
            ('door_width',900,600,1200),('door_height',1900,1600,2100),('sauna_door_offset',150,90,900),
            ('bench_depth',600,400,800),('bench_height',900,650,1100),('foot_bench_height',450,250,700)]
    for i,(n,v,lo,hi) in enumerate(values):
        if n in ['wall_height','partition_depth']:
            obj=GH_ValueList();obj.NickName=n;obj.ListMode=GH_ValueListMode.DropDown;obj.ListItems.Clear()
            for choice in ([2100,2700] if n=='wall_height' else [90,120]):
                entry=GH_ValueListItem(str(choice)+' mm',str(choice));entry.Selected=(choice==v);obj.ListItems.Add(entry)
            controls[n]=place(obj,40,190+i*45)
        else:controls[n]=slider(n,v,lo,hi,40,190+i*45)
    controls['storage']=toggle('Custom storage',False,40,750)
    controls['include_foundation']=toggle('Foundation study',True,40,795)
    roofs=GH_ValueList();roofs.NickName='Roof';roofs.ListMode=GH_ValueListMode.DropDown;roofs.ListItems.Clear()
    for i,label in enumerate(['Flat / membrane','Single slope / metal','Gable / metal']):
        item=GH_ValueListItem(label,str(i));item.Selected=(i==1);roofs.ListItems.Add(item)
    controls['roof_type']=place(roofs,40,850)
    terrace=GH_ValueList();terrace.NickName='Terrace depth / mm';terrace.ListMode=GH_ValueListMode.DropDown;terrace.ListItems.Clear()
    for depth,steps in [(1200,2)]:
        item=GH_ValueListItem(str(depth),str(steps));item.Selected=(steps==2);terrace.ListItems.Add(item)
    controls['terrace_steps']=place(terrace,40,895)
    win=GH_ValueList();win.NickName='Window width / mm';win.ListMode=GH_ValueListMode.DropDown;win.ListItems.Clear()
    for w in [580,880,1180]:
        item=GH_ValueListItem(str(w),str(w));item.Selected=(w==1180);win.ListItems.Add(item)
    controls['window_width']=place(win,40,940)
    facade=GH_ValueList();facade.NickName='Facade';facade.ListMode=GH_ValueListMode.DropDown;facade.ListItems.Clear()
    item=GH_ValueListItem('Vertical timber', '0');item.Selected=True;facade.ListItems.Add(item)
    controls['facade_type']=place(facade,40,985)
    systems=GH_ValueList();systems.NickName='Construction system';systems.ListMode=GH_ValueListMode.DropDown;systems.ListItems.Clear()
    system_item=GH_ValueListItem('OBTP Cassette', '0');system_item.Selected=True;systems.ListItems.Add(system_item)
    controls['system_type']=place(systems,40,1030)
    programs=GH_ValueList();programs.NickName='Program / Sauna or Studio';programs.ListMode=GH_ValueListMode.DropDown;programs.ListItems.Clear()
    for i,label in enumerate(['Sauna','Studio']):
        item=GH_ValueListItem(label,str(i));item.Selected=(i==0);programs.ListItems.Add(item)
    controls['program_type']=place(programs,40,1075)
    controls['studio_winter_closed']=toggle('Studio sliding doors closed',True,40,1120)
    inputs=[(k,Boolean if k in ['custom','storage','include_foundation','studio_winter_closed'] else Double) for k in controls]
    model=script('01 · Shared module','model.py',inputs,[('scene_json',GH_ParamAccess.item),('report',GH_ParamAccess.item)],420,240)
    for i,(key,_) in enumerate(inputs):model.Params.Input[i].AddSource(controls[key])
    GROUPS=local_module('preview_filter').GROUPS
    panels=toggle('Show panels',True,420,620);cut=toggle('Cut view',False,420,665);explode=slider('Explode display',0,0,100,420,710)
    only=GH_ValueList();only.NickName='Show only';only.ListMode=GH_ValueListMode.DropDown;only.ListItems.Clear()
    for i,label in enumerate(['All enabled groups']+[label for key,label in GROUPS]):
        item=GH_ValueListItem(label,str(i));item.Selected=(i==0);only.ListItems.Add(item)
    place(only,800,1750)
    part_controls=[toggle(label,True,800+(i//12)*420,1810+(i%12)*45) for i,(key,label) in enumerate(GROUPS)]
    preview=script('02 · Rhino preview','preview.py',[(n,t) for n,t in [('scene_json',String),('panels',Boolean),('cut',Boolean),('explode',Double),('only',Double)]]+[('show_'+key,Boolean) for key,label in GROUPS],
                   [('geometry',GH_ParamAccess.list),('part_ids',GH_ParamAccess.list)],800,250)
    for i,source in enumerate([model.Params.Output[0],panels,cut,explode,only]+part_controls):preview.Params.Input[i].AddSource(source)
    report=panel('',800,80);report.AddSource(model.Params.Output[1])
    export_toggle=toggle('Export review snapshot',False,800,620)
    export=script('03 · Checked export','export.py',[('scene_json',String),('run_export',Boolean)],[('receipt',GH_ParamAccess.item)],1120,250)
    export.Params.Input[0].AddSource(model.Params.Output[0]);export.Params.Input[1].AddSource(export_toggle)
    receipt=panel('',1400,250);receipt.AddSource(export.Params.Output[0])
    group('A · Saved presets and custom dimensions / mm / 600 mm steps',list(controls.values()),Color.FromArgb(220,232,221))
    group('B · Shared Python generator',[model],Color.FromArgb(233,226,207))
    group('C · Inspection only',[preview,panels,cut,explode],Color.FromArgb(218,228,235))
    group('C2 · Part visibility / Show only overrides switches',[only]+part_controls,Color.FromArgb(218,228,235))
    group('D · Manual export / does not publish website',[export,export_toggle,receipt],Color.FromArgb(235,222,218))
    # Analysis preparation shares the detailed scene, not the display/cut geometry.
    analysis_inputs=local_module('analysis').inputs
    settings=panel(json.dumps(analysis_inputs(),indent=2),420,1150)
    run_analysis=toggle('Export analysis preparation',False,800,1100)
    analysis=script('04 · Detailed analysis preparation','analysis.py',
        [('scene_json',String),('inputs_json',String),('run_export',Boolean)],
        [(n,GH_ParamAccess.item) for n in ['preflight_json','geometry_report','solver_report','results_report','diagrams_report','receipt']],800,1250)
    for i,source in enumerate([model.Params.Output[0],settings,run_analysis]):analysis.Params.Input[i].AddSource(source)
    audit=panel('',1120,1100);audit.AddSource(analysis.Params.Output[1])
    setup=panel('',1520,1100);setup.AddSource(analysis.Params.Output[2])
    results=panel('',1920,1100);results.AddSource(analysis.Params.Output[3])
    diagrams=panel('',1120,1500);diagrams.AddSource(analysis.Params.Output[4])
    analysis_receipt=panel('',1520,1500);analysis_receipt.AddSource(analysis.Params.Output[5])
    group('E1 · Geometry extraction / detailed model',[analysis,audit],Color.FromArgb(218,228,235))
    group('E2 · Materials, site and operating inputs / null means required',[settings],Color.FromArgb(233,226,207))
    group('E3 · Solver setup requirements / not executed',[setup],Color.FromArgb(235,222,218))
    group('E4 · Results status / no invented values',[results],Color.FromArgb(235,222,218))
    group('E5 · Material section diagrams',[diagrams],Color.FromArgb(218,228,235))
    group('E6 · Report export / local only',[run_analysis,analysis_receipt],Color.FromArgb(220,232,221))
    # Never overwrite a definition the owner may have edited.
    name='OBTP_Module_R10_'+datetime.now().strftime('%Y%m%d_%H%M%S')
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

