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
    values=[('room_depth_steps',2,2,8),('sauna_length_steps',3,3,8),('hall_length_steps',3,2,8),
            ('storage_length_steps',1,1,4),('wall_height',2100,2100,2700),('partition_depth',90,90,120),
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
    for i,label in enumerate(['Plokščias / membrane','Single slope / metal']):
        item=GH_ValueListItem(label,str(i));item.Selected=(i==1);roofs.ListItems.Add(item)
    controls['roof_type']=place(roofs,40,850)
    win=GH_ValueList();win.NickName='Window width / mm';win.ListMode=GH_ValueListMode.DropDown;win.ListItems.Clear()
    for w in [580,880,1180]:
        item=GH_ValueListItem(str(w),str(w));item.Selected=(w==1180);win.ListItems.Add(item)
    controls['window_width']=place(win,40,940)
    programs=GH_ValueList();programs.NickName='Program / Sauna or Studio';programs.ListMode=GH_ValueListMode.DropDown;programs.ListItems.Clear()
    for i,label in enumerate(['Sauna','Studio']):
        item=GH_ValueListItem(label,str(i));item.Selected=(i==0);programs.ListItems.Add(item)
    controls['program_type']=place(programs,40,1075)
    controls['studio_winter_closed']=toggle('Studio sliding doors closed',True,40,1120)
    foundations=GH_ValueList();foundations.ListMode=GH_ValueListMode.DropDown
    foundations.CreateAttributes();foundations.Name='Foundation';foundations.NickName='Foundation';foundations.ListItems.Clear()
    foundations.ListItems.Add(GH_ValueListItem('Timber support frame on piles', '0'))
    foundations.ListItems.Add(GH_ValueListItem('Concrete pile grillage study', '1'))
    foundations.ListItems[0].Selected=True
    controls['foundation_type']=place(foundations,40,1180)
    inputs=[(k,Boolean if k in ['custom','storage','include_foundation','studio_winter_closed'] else Double) for k in controls]
    model=script('01 · Shared module','model.py',inputs,[('scene_json',GH_ParamAccess.item),('report',GH_ParamAccess.item)],420,240)
    for i,(key,_) in enumerate(inputs):model.Params.Input[i].AddSource(controls[key])
    preview=script('02 · Rhino preview','preview.py',[('scene_json',String),('assembly_stage',Double),('core_frame',Double)],
                   [(n,GH_ParamAccess.list) for n in ['geometry','part_ids','materials','type_ids','legend']]+[('preview_status',GH_ParamAccess.item)],800,250)
    preview.Params.Input[0].AddSource(model.Params.Output[0])
    stage_control=slider('Assembly progress / 0 empty - 100 complete',100,0,100,420,520)
    core_control=slider('Core frame / 0 complete - 1 unique part colours',0,0,1,420,565)
    preview.Params.Input[1].AddSource(stage_control)
    preview.Params.Input[2].AddSource(core_control)
    proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies
             if p.Desc.Name=='Custom Preview' and p.Desc.Category=='Display' and not p.Obsolete]
    if len(proxies)!=1:raise RuntimeError('Expected one native Custom Preview component; found '+str(len(proxies)))
    coloured=place(proxies[0].CreateInstance(),1120,500)
    coloured.Params.Input[0].AddSource(preview.Params.Output[0])
    coloured.Params.Input[1].AddSource(preview.Params.Output[2])
    preview.Hidden=True # Avoid the default GH preview masking the type materials.
    preview_note=panel('',1120,620);preview_note.AddSource(preview.Params.Output[5])
    type_legend=panel('',1520,500);type_legend.AddSource(preview.Params.Output[4])
    report=panel('',800,80);report.AddSource(model.Params.Output[1])
    export_toggle=toggle('Export model + drawings (PDF disabled)',False,800,620)
    export=script('03 · Checked export','export.py',[('scene_json',String),('run_export',Boolean)],[('receipt',GH_ParamAccess.item)],1120,250)
    export.Params.Input[0].AddSource(model.Params.Output[0]);export.Params.Input[1].AddSource(export_toggle)
    receipt=panel('',1400,250);receipt.AddSource(export.Params.Output[0])
    group('A · Saved presets and custom dimensions / mm / 900 mm X / 1200 mm Y cells',list(controls.values()),Color.FromArgb(220,232,221))
    group('B · Shared Python generator',[model],Color.FromArgb(233,226,207))
    group('C · Complete model preview',[preview,stage_control,core_control,coloured,preview_note,type_legend],Color.FromArgb(218,228,235))
    group('D · Checked model export / PDF disabled',[export,export_toggle,receipt],Color.FromArgb(235,222,218))
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
    name='OBTP_Module_R21_'+datetime.now().strftime('%Y%m%d_%H%M%S')
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

