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
        g=GH_Group();g.NickName=name;g.Colour=color;doc.AddObject(g,False)
        for obj in objects:g.AddObject(obj.InstanceGuid)
        return g
    def choices(name,labels,default,x,y):
        obj=GH_ValueList();obj.NickName=name;obj.ListMode=GH_ValueListMode.DropDown;obj.ListItems.Clear()
        for number,label in labels:
            entry=GH_ValueListItem(label,str(number));entry.Selected=(number==default);obj.ListItems.Add(entry)
        return place(obj,x,y)
    core=local_module('room_config')
    typ=choices('0 / BUILDING TYPE',list(enumerate(core.TYPES)),0,40,70)
    room_lists=[]
    for i,default in enumerate([7,0,2]):room_lists.append(choices('Room function '+str(i+1),[(j,x[0]) for j,x in enumerate(core.FUNCTIONS)],default,40,240+i*70))
    rooms=script('1 / Collect room functions','config_stage.py',[('building_type',Double),('functions',Double)],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('rows',GH_ParamAccess.list)],400,200,stage='programme')
    rooms.Params.Input[0].AddSource(typ);rooms.Params.Input[1].Access=GH_ParamAccess.list
    for obj in room_lists:rooms.Params.Input[1].AddSource(obj)
    room_report=panel('',40,530,620,180);room_report.AddSource(rooms.Params.Output[2])
    room_note=panel('ONE VALUE LIST = ONE ROOM. Duplicate a function list and Shift-connect it to functions. Maximum 6 connected lists. Wire order assigns stable R01..R06 IDs; repeated functions are distinct rooms. Removing/reordering wires changes IDs: review pair rules afterward.',40,760,620,170)
    group('A0–A1 / TYPE AND ROOM FUNCTIONS',[typ,rooms,room_report,room_note]+room_lists,Color.FromArgb(222,234,220))
    adj=script('2 / Shared-edge rules','config_stage.py',[('upstream',String),('rules',String)],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('rows',GH_ParamAccess.list)],850,200,stage='adjacency')
    adj.Params.Input[0].AddSource(rooms.Params.Output[0]);adj.Params.Input[1].Access=GH_ParamAccess.list
    boundary=script('3 / Boundary treatments','config_stage.py',[('upstream',String),('rules',String)],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('rows',GH_ParamAccess.list)],1450,200,stage='boundaries')
    boundary.Params.Input[0].AddSource(adj.Params.Output[0]);boundary.Params.Input[1].Access=GH_ParamAccess.list
    for kind,target,x,labels,default in [('adjacency',adj,800,[(0,'May share edge'),(1,'Must share edge'),(2,'Cannot share edge')],1),('boundary',boundary,1400,[(0,'Totally open'),(1,'Partition with opening'),(2,'Closed partition')],1)]:
        a=choices('Room A',[(i,'R%02d'%i) for i in range(1,7)],1,x,700)
        b=choices('Room B',[(i,'R%02d'%i) for i in range(1,7)],2,x,770)
        relation=choices('Relationship',labels,default,x,840)
        rule=script('Pair rule / duplicate this group','config_pair.py',[('room_a',Double),('room_b',Double),('relation',Double)],[('rule',GH_ParamAccess.item)],x,980,stage=kind)
        for j,obj in enumerate([a,b,relation]):rule.Params.Input[j].AddSource(obj)
        target.Params.Input[1].AddSource(rule.Params.Output[0])
        note=panel('Duplicate the three selectors + Pair rule to add a constraint. Shift-connect its output to rules. Disconnect rules referring to removed rooms. Unspecified adjacency = may; neighbouring rooms default to partition with opening. Closed partitions get exterior access.',x,1120,440,220)
        status=panel('',x,360,440,250);status.AddSource(target.Params.Output[1])
        group('A2 / ADJACENCY' if kind=='adjacency' else 'A3 / BOUNDARY TYPE',[target,a,b,relation,rule,note,status],Color.FromArgb(231,228,212))
    dims={'length_cells':slider('Overall X cells / 900 mm',8,3,14,2000,750),'width_cells':slider('Overall Y cells / 1200 mm',2,2,3,2000,820),'arrangement':slider('Arrangement / valid range in report',0,0,7,2000,890),'entrance_side':choices('Main entrance edge',[(i,v) for i,v in enumerate(core.SIDES)],0,2000,960),'summer_passage':toggle('Studio summer passage / two double doors',False,2000,1030)}
    plan=script('4 / Resolve room plan','config_stage.py',[('upstream',String)]+[(k,Boolean if k=='summer_passage' else Double) for k in dims],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('rows',GH_ParamAccess.list)],2050,200,stage='plan')
    plan.Params.Input[0].AddSource(boundary.Params.Output[0])
    for i,obj in enumerate(dims.values(),1):plan.Params.Input[i].AddSource(obj)
    plan_report=panel('',2000,360,460,280);plan_report.AddSource(plan.Params.Output[1])
    plan_show=toggle('Preview room plan + connection graph',True,2000,1410)
    plan_preview=script('Plan / graph preview','config_preview.py',[('data_json',String),('show',Boolean)],[('geometry',GH_ParamAccess.list),('labels',GH_ParamAccess.list),('label_points',GH_ParamAccess.list),('report',GH_ParamAccess.item)],2000,1500)
    plan_preview.Params.Input[0].AddSource(plan.Params.Output[0]);plan_preview.Params.Input[1].AddSource(plan_show)
    plan_rows=panel('',2000,1160,460,200);plan_rows.AddSource(plan.Params.Output[2])
    tags=[]
    proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies if p.Desc.Name=='Text Tag 3D']
    if proxies:
        tag=proxies[0].CreateInstance();ports={p.Name.lower():p for p in tag.Params.Input}
        loc=next((v for k,v in ports.items() if k in ('location','locations')),None);txt=next((v for k,v in ports.items() if k in ('text','tag')),None)
        if loc is not None and txt is not None:
            place(tag,2200,1660);loc.AddSource(plan_preview.Params.Output[2]);txt.AddSource(plan_preview.Params.Output[1]);tags.append(tag)
            if 'size' in ports:
                size=slider('Room label size / mm',85,30,150,2000,1800);ports['size'].AddSource(size);tags.append(size)
    group('A4 / PLAN RESULT · usable without structure',[plan,plan_report,plan_rows,plan_preview,plan_show]+list(dims.values())+tags,Color.FromArgb(224,230,237))
    controls={'system':choices('B1 / System',[(0,'Cassette')],0,2700,700),'roof_type':choices('B2 / Roof',[(0,'Plokščias / drainage slope'),(1,'Single slope')],0,2700,770),'foundation_type':choices('B2 / Foundation study',[(0,'Timber rails on piles'),(1,'Concrete grillage study')],0,2700,840)}
    skeleton=script('B / Plan-derived cassette skeleton','config_stage.py',[('upstream',String)]+[(k,Double) for k in controls],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('rows',GH_ParamAccess.list)],2750,200,stage='skeleton')
    skeleton.Params.Input[0].AddSource(plan.Params.Output[0])
    for i,obj in enumerate(controls.values(),1):skeleton.Params.Input[i].AddSource(obj)
    skeleton_report=panel('',2700,360,460,240);skeleton_report.AddSource(skeleton.Params.Output[1])
    skeleton_show=toggle('Preview skeleton only',False,2700,1030)
    skeleton_preview=script('Skeleton preview','config_preview.py',[('data_json',String),('show',Boolean)],[('geometry',GH_ParamAccess.list),('labels',GH_ParamAccess.list),('label_points',GH_ParamAccess.list),('report',GH_ParamAccess.item)],2700,1150)
    skeleton_preview.Params.Input[0].AddSource(skeleton.Params.Output[0]);skeleton_preview.Params.Input[1].AddSource(skeleton_show)
    group('B / STRUCTURE · candidate geometry, capacities unresolved',[skeleton,skeleton_report,skeleton_show,skeleton_preview]+list(controls.values()),Color.FromArgb(237,224,210))
    det={'terrace':choices('C1 / Terrace',list(enumerate(local_module('room_detail').TERRACES)),1,3400,700),'return_end':choices('Return end / west or east for long entrance',[(0,'West / front for short entrance'),(1,'East / back for short entrance')],0,3400,770),'outdoor_shower':toggle('Sauna / outdoor shower reservation',False,3400,840),'outdoor_bench':toggle('Sauna / outdoor bench',False,3400,910),'paneling':choices('C2 / Panel build-up',[(0,'Structural panels'),(1,'Panels + cavity insulation'),(2,'Panels + insulation + timber lining')],1,3400,1010),'facade':toggle('C3 / Facade finish',True,3400,1080)}
    detail=script('C / Detail the current layout','config_stage.py',[('upstream',String)]+[(k,Boolean if k in ('outdoor_shower','outdoor_bench','facade') else Double) for k in det],[('data_json',GH_ParamAccess.item),('report',GH_ParamAccess.item),('rows',GH_ParamAccess.list)],3450,200,stage='detail')
    detail.Params.Input[0].AddSource(skeleton.Params.Output[0])
    for i,obj in enumerate(det.values(),1):detail.Params.Input[i].AddSource(obj)
    detail_report=panel('',3400,360,460,280);detail_report.AddSource(detail.Params.Output[1])
    note=panel('U = both long sides + one short return; entrance edge is always included. Outdoor features are compact terrace reservations, not additional full-width rooms. Summer passage changes openings, so its switch is in A4. Panel choices are geometric studies; supplier/weather/wet-area details are unresolved.',3400,1200,460,240)
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
    name='OBTP_Room_Configurator_R28_'+datetime.now().strftime('%Y%m%d_%H%M%S')
    path=ROOT/(name+'.gh')
    if not GH_DocumentIO(doc).SaveQuiet(str(path)):raise IOError('Could not write native GH definition')
    doc.FilePath=str(path);Grasshopper.Instances.DocumentServer.AddDocument(doc);Grasshopper.Instances.ActiveCanvas.Document=doc
    doc.Enabled=True;doc.NewSolution(False)
    print('Created '+str(path))

try:main()
except Exception:
    error=traceback.format_exc();(ROOT/'setup-room-config-error.txt').write_text(error,encoding='utf-8');print(error);raise
