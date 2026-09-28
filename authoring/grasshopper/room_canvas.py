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


def main(mode="combined"):
    if mode not in ("combined","layout","structure","detailing"):raise ValueError("Unknown canvas mode")
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
        if stage is not None:code=code.replace("STAGE='programme'",'STAGE='+repr(stage)).replace("KIND='adjacency'",'KIND='+repr(stage))
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
        g=GH_Group();g.CreateAttributes();g.NickName="OBTP / "+name;g.Colour=color;doc.AddObject(g,False)
        for obj in objects:g.AddObject(obj.InstanceGuid)
        return g
    def choices(name,labels,default,x,y):
        obj=GH_ValueList();obj.NickName=name;obj.ListMode=GH_ValueListMode.DropDown;obj.ListItems.Clear()
        for number,label in labels:
            entry=GH_ValueListItem(label,str(number));entry.Selected=(number==default);obj.ListItems.Add(entry)
        return place(obj,x,y)
    core=local_module('room_config')
    def exchange(stage,source,x,y):
        path=panel(str(ROOT/'handoffs'/(stage+'.json')),x,y,440,65)
        load=toggle('Read saved '+stage,False,x,y+95)
        save=toggle('Write current '+stage,False,x,y+155)
        io=script(stage.upper()+' / import or export','config_exchange.py',[('upstream',String),('file_path',String),('read_file',Boolean),('write_file',Boolean)],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item)],x,y+250,stage=stage)
        if source is not None:io.Params.Input[0].AddSource(source.Params.Output[0])
        io.Params.Input[1].AddSource(path);io.Params.Input[2].AddSource(load);io.Params.Input[3].AddSource(save)
        report=panel('',x,y+410,440,150);report.AddSource(io.Params.Output[1])
        note=panel('Live upstream wire takes priority. Without a wire, enable Read saved. Writing requires valid live input and never overwrites the import. Turn Write off after saving. Connect data_json directly when combining stages on one canvas.',x,y+610,440,150)
        group(stage.upper()+' / FILE HANDOFF',[path,load,save,io,report,note],Color.FromArgb(220,230,235))
        return io
    if mode in ("combined","layout"):
        presets=local_module('room_presets')
        typ=choices('Building preset',list(enumerate(presets.TYPES)),0,40,70)
        size=choices('Size',list(enumerate(presets.SIZES)),1,40,150)
        extension=toggle('Extension / Yes or No',True,40,230)
        window=choices('Window / structural host and frame',[(0,'900 host / 580 frame'),(1,'1800 host / 1180 frame')],1,40,310)
        plan=script('A / Preset layout','config_stage.py',[('building_type',Double),('size',Double),('extension',Boolean),('window',Double)],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('rows',GH_ParamAccess.list)],550,100,stage='preset')
        for i,obj in enumerate([typ,size,extension,window]):plan.Params.Input[i].AddSource(obj)
        status=panel('',1000,100,420,180);status.AddSource(plan.Params.Output[1])
        plan_show=toggle('Plan preview',True,40,390)
        preview=script('Plan preview','config_preview.py',[('data_json',String),('show',Boolean)],[('geometry',GH_ParamAccess.list),('labels',GH_ParamAccess.list),('label_points',GH_ParamAccess.list),('report',GH_ParamAccess.item)],550,400)
        preview.Params.Input[0].AddSource(plan.Params.Output[0]);preview.Params.Input[1].AddSource(plan_show)
        objects=[typ,size,extension,window,plan,status,plan_show,preview]
        proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies if p.Desc.Name=='Text Tag 3D']
        if proxies:
            tag=proxies[0].CreateInstance();ports={p.Name.lower():p for p in tag.Params.Input}
            loc=next((v for k,v in ports.items() if k in ('location','locations')),None);txt=next((v for k,v in ports.items() if k in ('text','tag')),None)
            if loc is not None and txt is not None:
                place(tag,1000,400);loc.AddSource(preview.Params.Output[2]);txt.AddSource(preview.Params.Output[1]);objects.append(tag)
                if 'size' in ports:
                    labelsize=slider('Label size / mm',85,30,150,40,470);ports['size'].AddSource(labelsize);objects.append(labelsize)
        group('A / PRESET AND PLAN',[*objects],Color.FromArgb(222,234,220))
        exchange("plan",plan,2500,1950)
    else:
        plan=exchange("plan",None,2000,1950) if mode=="structure" else None
    if mode in ("combined","structure"):
        controls={'system':choices('B1 / System',[(0,'Cassette')],0,2700,700),'roof_type':choices('B2 / Roof',[(0,'Plokščias / drainage slope'),(1,'Single slope')],0,2700,770),'foundation_type':choices('B2 / Foundation study',[(0,'Timber rails on piles'),(1,'Concrete grillage study')],0,2700,840)}
        skeleton=script('B / Plan-derived cassette skeleton','config_stage.py',[('upstream',String)]+[(k,Double) for k in controls],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('rows',GH_ParamAccess.list)],2750,200,stage='skeleton')
        skeleton.Params.Input[0].AddSource(plan.Params.Output[0])
        for i,obj in enumerate(controls.values(),1):skeleton.Params.Input[i].AddSource(obj)
        skeleton_report=panel('',2700,360,460,240);skeleton_report.AddSource(skeleton.Params.Output[1])
        skeleton_show=toggle('Preview skeleton only',False,2700,1030)
        skeleton_preview=script('Skeleton preview','config_preview.py',[('data_json',String),('show',Boolean)],[('geometry',GH_ParamAccess.list),('labels',GH_ParamAccess.list),('label_points',GH_ParamAccess.list),('report',GH_ParamAccess.item)],2700,1150)
        skeleton_preview.Params.Input[0].AddSource(skeleton.Params.Output[0]);skeleton_preview.Params.Input[1].AddSource(skeleton_show)
        group('B / STRUCTURE · candidate geometry, capacities unresolved',[skeleton,skeleton_report,skeleton_show,skeleton_preview]+list(controls.values()),Color.FromArgb(237,224,210))
        exchange("skeleton",skeleton,3000,1950)
    elif mode=="detailing":
        skeleton=exchange("skeleton",None,2700,1950)
    if mode in ("combined","detailing"):
        det={'terrace':toggle('Terrace / 1200 mm',True,3400,700),'paneling':choices('Panel build-up',[(0,'Structural panels'),(1,'Panels + insulation'),(2,'Panels + insulation + lining')],2,3400,800)}
        detail=script('C / Detail the current layout','config_stage.py',[('upstream',String)]+[(k,Boolean if k=='terrace' else Double) for k in det],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('rows',GH_ParamAccess.list)],3450,200,stage='detail')
        detail.Params.Input[0].AddSource(skeleton.Params.Output[0])
        for i,obj in enumerate(det.values(),1):detail.Params.Input[i].AddSource(obj)
        detail_report=panel('',3400,360,460,280);detail_report.AddSource(detail.Params.Output[1])
        note=panel('Façade is included. Terrace depth is 1200 mm. Sauna extension contains the integrated storage/shower/bench. Studio extension adds its second block; without it the centre has two windows. Living studio is a provisional study.',3400,1200,460,240)
        group('C / DETAILING',[detail,detail_report,note]+list(det.values()),Color.FromArgb(226,233,222))
        assembly=script('D / Assembly sequence','assembly_checkpoint.py',[('scene_json',String),('assembly_stage',Double)],[('display_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('steps',GH_ParamAccess.list)],4100,200)
        assembly.Params.Input[0].AddSource(detail.Params.Output[0]);progress=slider('Assembly progress',100,0,100,4050,370);assembly.Params.Input[1].AddSource(progress)
        scope=choices('Final preview',[(0,'Structure + panels'),(1,'Building without facade'),(2,'Complete with facade')],2,4050,440);colours=toggle('Unique part colours',False,4050,510)
        preview=script('Final material preview','final_preview.py',[('display_json',String),('preview_scope',Double),('type_colours',Boolean),('assembly_filter',String)],[(n,GH_ParamAccess.list) for n in ['geometry','part_ids','materials','type_ids','legend']]+[('preview_status',GH_ParamAccess.item)],4100,640)
        preview.Params.Input[0].AddSource(assembly.Params.Output[0]);preview.Params.Input[1].AddSource(scope);preview.Params.Input[2].AddSource(colours)
        proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies if p.Desc.Name=='Custom Preview' and p.Desc.Category=='Display' and not p.Obsolete]
        if len(proxies)!=1:raise RuntimeError('Native Custom Preview not available')
        display=place(proxies[0].CreateInstance(),4650,640);display.Params.Input[0].AddSource(preview.Params.Output[0]);display.Params.Input[1].AddSource(preview.Params.Output[2]);preview.Hidden=True
        status=panel('',4050,850,460,240);status.AddSource(preview.Params.Output[5]);steps=panel('',4650,850,460,350);steps.AddSource(assembly.Params.Output[2])
        run=toggle('Export complete model / no PDF',False,4050,1250)
        export=script('Export room configuration','config_export.py',[('scene_json',String),('run_export',Boolean)],[('receipt',GH_ParamAccess.item)],4100,1370)
        export.Params.Input[0].AddSource(detail.Params.Output[0]);export.Params.Input[1].AddSource(run);receipt=panel('',4650,1300,460,240);receipt.AddSource(export.Params.Output[0])
        group('D / DISPLAY AND EXPORT · never changes source quantities',[assembly,progress,scope,colours,preview,display,status,steps,run,export,receipt],Color.FromArgb(228,220,237))
        exchange("scene",detail,4000,1950)
        destination=panel(str(ROOT/'documents'),5000,100,420,65)
        rates=panel(str(ROOT/'material-rates.json'),5000,210,420,65)
        generate=toggle('Generate layouts + PDF / turn off after use',False,5000,320)
        documents=script('E / Drawings, CNC review and material costs','config_documents.py',[('scene_json',String),('destination',String),('rates_path',String),('generate',Boolean)],[('receipt',GH_ParamAccess.item)],5500,100)
        for i,source in enumerate([detail.Params.Output[0],destination,rates,generate]):documents.Params.Input[i].AddSource(source)
        receipt=panel('',6000,100,420,220);receipt.AddSource(documents.Params.Output[0])
        group('E / DOCUMENTS',[destination,rates,generate,documents,receipt],Color.FromArgb(228,225,218))
    name='OBTP_'+mode.title()+'_R30_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if mode in ('structure','detailing'):
        offset=1900 if mode=='structure' else 2600
        for obj in doc.Objects:
            if isinstance(obj,GH_Group):continue
            p=obj.Attributes.Pivot;obj.Attributes.Pivot=PointF(p.X-offset,p.Y)
    local_module('canvas_tidy').tidy(doc)
    path=ROOT/(name+'.gh')
    if not GH_DocumentIO(doc).SaveQuiet(str(path)):raise IOError('Could not write native GH definition')
    doc.FilePath=str(path);Grasshopper.Instances.DocumentServer.AddDocument(doc);Grasshopper.Instances.ActiveCanvas.Document=doc
    doc.Enabled=True;doc.NewSolution(False)
    print('Created '+str(path))

try:main(globals().get("CANVAS_MODE","combined"))
except Exception:
    error=traceback.format_exc();(ROOT/'setup-room-config-error.txt').write_text(error,encoding='utf-8');print(error);raise
