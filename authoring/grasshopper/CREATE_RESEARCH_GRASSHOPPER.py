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
    controls={}
    controls['system']=choices('Construction system',[(0,'WikiHouse / pinned source'),(1,'Timber cassette specimen'),(2,'Experimental B / plate ribs')],1,40,100)
    controls['specimen']=choices('Cassette specimen',list(enumerate(['Wall','Floor','Roof','Opening','Corner','Floor-wall interface'])),0,40,180)
    controls['bays']=slider('Bays / count',3,2,6,40,270)
    controls['span']=choices('Cassette/B span / mm',[(n,str(n)) for n in [2400,3600,4800]],2400,40,330)
    controls['height']=choices('Cassette/B height / mm',[(n,str(n)) for n in [2100,2700]],2100,40,390)
    controls['sheet']=choices('Cassette sheet thickness / mm',[(n,str(n)) for n in [12,18]],12,40,450)
    controls['cassette_depth']=choices('Cassette wall frame depth / mm',[(n,str(n)) for n in [145,195,220]],195,40,510)
    controls['b_depth']=choices('B rib depth / mm',[(n,str(n)) for n in [180,240,300,360]],240,40,690)
    controls['pitch']=choices('B rib spacing / mm',[(n,str(n)) for n in [600,900,1200]],900,40,570)
    controls['thickness']=choices('B rib thickness / mm',[(n,str(n)) for n in [27,45,60,75]],45,40,630)
    controls['mode']=choices('WikiHouse/B inspection',[(0,'Assembly'),(1,'Object'),(2,'Interface')],0,600,100)
    controls['object_index']=slider('Object/interface index / see catalogue',0,0,50,600,180)
    controls['explode']=slider('Exploded inspection / percent',0,0,100,600,270)
    controls['insulation']=toggle('Show insulation cavities',True,600,330)
    controls['core']=toggle('Unique constituent colours',False,600,390)
    obj=script('03 Specimen geometry and measured quantities','research_specimen.py',[(k,Boolean if k in ('insulation','core') else Double) for k in controls],[(n,GH_ParamAccess.list) for n in ['geometry','materials']]+[('report',GH_ParamAccess.item),('catalogue',GH_ParamAccess.list),('schedule',GH_ParamAccess.list)],1200,100)
    for i,source in enumerate(controls.values()):obj.Params.Input[i].AddSource(source)
    report=panel('',1200,300,600,640);report.AddSource(obj.Params.Output[2])
    catalogue=panel('',1900,300,500,500);catalogue.AddSource(obj.Params.Output[3])
    schedule=panel('',2500,300,600,640);schedule.AddSource(obj.Params.Output[4])
    proxies=[p for p in Grasshopper.Instances.ComponentServer.ObjectProxies if p.Desc.Name=='Custom Preview' and p.Desc.Category=='Display' and not p.Obsolete]
    if len(proxies)!=1:raise RuntimeError('Expected one native Custom Preview component')
    preview=place(proxies[0].CreateInstance(),1900,100)
    preview.Params.Input[0].AddSource(obj.Params.Output[0]);preview.Params.Input[1].AddSource(obj.Params.Output[1]);obj.Hidden=True
    note=panel('RESEARCH ONLY / All dimensions in mm. No building presets, room programme or equipment. WikiHouse uses rigid pinned source parts and its object/interface catalogue. Cassette exposes wall, floor, roof, rough opening, corner and floor-wall specimens. B retains implemented ribs, panels, insulation and knee/base interfaces; B opening framing is not implemented. Counts are measured geometry; capacities, fastening, grades and supplier acceptance are unknown. Controls identify their applicable systems; unsupported values clear results. Cassette stud width is 45 mm; X/Y rhythm is 900/1200. Floor/roof joist depth is 220 mm. Depth control applies to cassette WALLS or B ribs.',40,850,1060,360)
    group('01 / SYSTEM AND SPECIMEN',[controls[k] for k in list(controls)[:10]]+[note],Color.FromArgb(220,232,221))
    group('02 / INSPECTION',[controls[k] for k in list(controls)[10:]],Color.FromArgb(218,228,235))
    group('03 / GEOMETRY, QUANTITIES AND ENGINEERING HOLDS',[obj,report,preview,catalogue,schedule],Color.FromArgb(233,226,207))
    # Never overwrite a definition the owner may have edited.
    name='OBTP_Research_Specimens_R27_'+datetime.now().strftime('%Y%m%d_%H%M%S')
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
