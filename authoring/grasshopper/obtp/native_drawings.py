"""Rhino 8: core SSP layouts -> Rhino PDF. No ReportLab fallback.
Run from explicit GH export. Native runtime acceptance is still required.
"""
import json
from pathlib import Path
from datetime import datetime
from .drawings import dimension_lines
from .ssp_sheets import prepare


def print_layouts(pages,path):
    import Rhino
    if not pages:raise ValueError('No SSP layouts to print')
    pdf=Rhino.FileIO.FilePdf.Create()
    for page in pages:
        page.SetPageAsActive();page.Redraw()
        settings=Rhino.Display.ViewCaptureSettings(page,300.0)
        settings.RasterMode=False
        settings.DrawBackground=False
        pdf.AddPage(settings)
    path=Path(path);temp=path.with_name(path.stem+'.pending.pdf')
    if not pdf.Write(str(temp)) or not temp.exists() or temp.stat().st_size==0:
        raise IOError('Rhino PDF write failed; no completed PDF receipt')
    temp.replace(path)
    return str(path)


def bake(scene,destination=None,recipe=None):
    import Rhino
    import System
    from System.Drawing import Color
    doc=Rhino.RhinoDoc.ActiveDoc
    if doc is None:raise RuntimeError('Open a Rhino document first')
    if doc.ModelUnitSystem!=Rhino.UnitSystem.Millimeters or doc.PageUnitSystem!=Rhino.UnitSystem.Millimeters:
        raise ValueError('SSP export requires model and layout units in millimetres; no automatic rescaling')
    recipe=recipe or prepare(scene)
    run=datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    kind=recipe.get('kind','SSP')
    root='OBTP '+kind+' '+scene['config']['id']+' '+run
    pages=[];details=[];owned_layers=[]
    def layer(name):
        l=Rhino.DocObjects.Layer();l.Name=name;l.Color=Color.Black;l.PlotColor=Color.Black;l.PlotWeight=.18
        # Keep new export geometry out of pre-existing user/OBTP layout details.
        for old_page in doc.Views.GetPageViews():
            for old_detail in old_page.GetDetailViews():
                l.SetPerViewportVisible(old_detail.Viewport.Id,False)
        index=doc.Layers.Add(l)
        if index<0:raise RuntimeError('Could not add layer '+name)
        owned_layers.append(index);return index
    paper_layer=layer(root+' PAPER')
    def attr(li,page=None,order=0,weight=.18,part_id=None):
        a=Rhino.DocObjects.ObjectAttributes();a.LayerIndex=li;a.DisplayOrder=order
        a.PlotWeightSource=Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject;a.PlotWeight=weight
        a.SetUserString('obtp_ssp_run',run);a.SetUserString('geometry_sha256',scene['geometry_sha256'])
        if part_id:a.SetUserString('obtp_id',part_id)
        if page:
            a.Space=Rhino.DocObjects.ActiveSpace.PageSpace;a.ViewportId=page.MainViewport.Id
        return a
    def point(q):return Rhino.Geometry.Point3d(q[0],q[1],0)
    def text(q,value,height,a):
        t=Rhino.Geometry.TextEntity();t.Plane=Rhino.Geometry.Plane(point(q),Rhino.Geometry.Vector3d.ZAxis)
        t.PlainText=str(value);t.TextHeight=height
        doc.Objects.AddText(t,a)
    solid=Rhino.DocObjects.HatchPattern.Defaults.Solid
    found=doc.HatchPatterns.FindName(solid.Name);solid_index=found.Index if found else doc.HatchPatterns.Add(solid)
    diag=Rhino.DocObjects.HatchPattern.Defaults.Hatch1
    found=doc.HatchPatterns.FindName(diag.Name);diag_index=found.Index if found else doc.HatchPatterns.Add(diag)
    previous=doc.Views.ActiveView
    for sheet in recipe['sheets']:
        page=doc.Views.AddPageView(root+' '+str(sheet['number']).zfill(2)+' '+sheet['code'],420,297)
        if page is None:raise RuntimeError('Could not create Rhino page')
        pages.append(page)
        for a,b in sheet['lines']:doc.Objects.AddLine(point(a),point(b),attr(paper_layer,page))
        for a in sheet['texts']:text(a['at'],a['text'],a['size'],attr(paper_layer,page))
        for slot in sheet['details']:
            li=layer(root+' '+sheet['code']+' '+slot['name']);offset=[25000, -len(details)*20000]
            def pt(q):return point([q[0]+offset[0],q[1]+offset[1]])
            v=slot['view'];scale=slot['scale']
            for i,p in enumerate(v['polygons']):
                curve=Rhino.Geometry.PolylineCurve([pt(q) for q in p['points']+[p['points'][0]]])
                # Solid fill masks geometry behind, consistently with offline projection proof.
                a=attr(li,order=i*3,part_id=p['id']);a.ColorSource=Rhino.DocObjects.ObjectColorSource.ColorFromObject
                a.ObjectColor=Color.LightGray if p.get('fill')=='#eeeeee' or p['material']=='glass' else Color.White
                a.PlotColorSource=Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject;a.PlotColor=a.ObjectColor
                for h in Rhino.Geometry.Hatch.Create(curve,solid_index,0,1,doc.ModelAbsoluteTolerance) or []:doc.Objects.AddHatch(h,a)
                if p.get('cut') and p['material'] in ['timber','plywood','lining-wood','cladding-wood','deck-wood']:
                    for h in Rhino.Geometry.Hatch.Create(curve,diag_index,0,scale*(1 if p['material']=='plywood' else 2.5),doc.ModelAbsoluteTolerance) or []:
                        doc.Objects.AddHatch(h,attr(li,order=i*3+1,weight=.08,part_id=p['id']))
                if p.get('cut') and p['material']=='mineral-wool':
                    import math
                    x0=min(q[0] for q in p['points']);x1=max(q[0] for q in p['points']);y0=min(q[1] for q in p['points']);y1=max(q[1] for q in p['points'])
                    horizontal=x1-x0>=y1-y0;lo,hi=(x0,x1) if horizontal else (y0,y1);u,w=(y0,y1) if horizontal else (x0,x1)
                    stride=max(2*scale,min(6*scale,(w-u)*.65));count=max(2,int((hi-lo)/(scale*.15)));wave=[]
                    for j in range(count+1):
                        t=lo+(hi-lo)*j/count;val=(u+w)/2+(w-u)*.43*math.sin((t-lo)/stride*2*math.pi)
                        wave.append(pt((t,val) if horizontal else (val,t)))
                    doc.Objects.AddPolyline(wave,attr(li,order=i*3+1,weight=.08,part_id=p['id']))
                doc.Objects.AddCurve(curve,attr(li,order=i*3+2,weight=.30 if p.get('cut') else .12,part_id=p['id']))
            top=len(v['polygons'])*3+10
            for guide in v.get('guides',[]):
                for aa,bb in zip(guide['points'],guide['points'][1:]):
                    # Dash-dot geometry is independent of document linetype names.
                    import math
                    length=math.dist(aa,bb);t=0
                    while t<length:
                        for draw,step in [(True,4*scale),(False,scale),(True,scale),(False,scale)]:
                            end=min(length,t+step)
                            if draw:doc.Objects.AddLine(pt([aa[k]+(bb[k]-aa[k])*t/length for k in range(2)]),pt([aa[k]+(bb[k]-aa[k])*end/length for k in range(2)]),attr(li,order=top,weight=.1))
                            t=end
            for line in v['polylines']:doc.Objects.AddPolyline([pt(q) for q in line],attr(li,order=top))
            for a in v.get('labels',[]):text([a['at'][0]+offset[0],a['at'][1]+offset[1]],a['text'],2.5*scale,attr(li,order=top))
            style=Rhino.DocObjects.DimensionStyle();style.Name=root+' '+sheet['code']+' '+slot['name'];style.TextHeight=2.5*scale;style.ArrowLength=scale;style.DimensionScale=1
            style_idx=doc.DimStyles.Add(style);style_id=doc.DimStyles[style_idx].Id
            for dim in v['dimensions']:
                _,location,_=dimension_lines(dim);vertical=dim['axis']==1
                plane=Rhino.Geometry.Plane(point(offset),Rhino.Geometry.Vector3d(0,1,0) if vertical else Rhino.Geometry.Vector3d(1,0,0),Rhino.Geometry.Vector3d(-1,0,0) if vertical else Rhino.Geometry.Vector3d(0,1,0))
                def uv(q):return Rhino.Geometry.Point2d(q[1],-q[0]) if vertical else Rhino.Geometry.Point2d(*q)
                entity=Rhino.Geometry.LinearDimension(plane,uv(dim['a']),uv(dim['b']),uv(location));entity.DimensionStyleId=style_id
                doc.Objects.AddLinearDimension(entity,attr(li,order=top))
            x,y,X,Y=slot['box']
            detail=page.AddDetailView(slot['name'],Rhino.Geometry.Point2d(x,y),Rhino.Geometry.Point2d(X,Y),Rhino.Display.DefinedViewportProjection.Top)
            if detail is None:raise RuntimeError('Could not create detail')
            detail.Viewport.DisplayMode=Rhino.Display.DisplayModeDescription.FindByName('Wireframe')
            detail.Viewport.ShowGrid=False;detail.Viewport.ShowGridAxes=False;detail.Viewport.ShowWorldAxes=False
            target=point([offset[0]+slot['center'][0],offset[1]+slot['center'][1]])
            detail.Viewport.SetCameraTarget(target,True);detail.CommitViewportChanges()
            # Model 25 mm = paper 1 mm, NOT the reversed 1 : 25 arguments.
            if not detail.DetailGeometry.SetScale(scale,doc.ModelUnitSystem,1.0,doc.PageUnitSystem):raise RuntimeError('Detail scale failed')
            detail.DetailGeometry.IsProjectionLocked=True;detail.CommitChanges()
            da=detail.Attributes.Duplicate();da.LayerIndex=paper_layer;da.PlotWeightSource=Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject;da.PlotWeight=-1
            doc.Objects.ModifyAttributes(detail.Id,da,True)
            details.append((detail,li))
    # Isolate every detail after ALL drawing layers exist. Do not hide user objects globally.
    for detail,li in details:
        for l in doc.Layers:
            if l.IsDeleted:continue
            l.SetPerViewportVisible(detail.Viewport.Id,l.Index==li);l.CommitChanges()
    doc.Views.Redraw()
    receipt=dict(status='layouts-created',root=root,geometry_sha256=scene['geometry_sha256'],
        pages=[p.PageName for p in pages],pdf=None,
        note='Layouts are in the active Rhino document. Save that document to retain editable layouts; the separate geometry-only 3dm has no layouts.')
    doc.Strings.SetString('OBTP/SSP/latest_pages',json.dumps(receipt['pages']))
    if destination is not None:
        destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
        try:
            receipt['pdf']=print_layouts(pages,destination/(scene['config']['id']+'-'+kind+'-R11.pdf'))
            receipt['status']='rhino-layout-pdf-written'
        except Exception as error:
            receipt['status']='native-pdf-failed';receipt['error']=str(error)
            (destination/(kind+'-layout-receipt.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
            raise
        (destination/(kind+'-layout-receipt.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
    if previous:doc.Views.ActiveView=previous
    return receipt
