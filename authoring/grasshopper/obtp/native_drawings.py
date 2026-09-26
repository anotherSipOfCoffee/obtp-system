"""RhinoCommon-native annotation/layout stage; executed inside Rhino only.
Uses the same measured points exported to the website/PDF. No text-only fake dimensions.
"""
def bake(scene):
    import Rhino
    import System
    from System.Drawing import Color
    from .drawings import dimension_lines
    doc=Rhino.RhinoDoc.ActiveDoc
    root='OBTP '+scene['config']['id']+' '+scene['geometry_sha256'][:8]
    style=Rhino.DocObjects.DimensionStyle();style.Name=root;style.TextHeight=62.5;style.ArrowLength=30;style.DimensionScale=1
    sid=doc.DimStyles.Add(style);style_id=doc.DimStyles[sid].Id
    hp=Rhino.DocObjects.HatchPattern.Defaults.Hatch1
    found=doc.HatchPatterns.FindName(hp.Name)
    hatch_index=found.Index if found else doc.HatchPatterns.Add(hp)
    offsets={}
    for i,(name,view) in enumerate(scene['drawings']['views'].items()):
        if name in ['concept-plan','window-jamb']:continue
        ox=15000;oy=-i*8500;offsets[name]=(ox,oy)
        layer=Rhino.DocObjects.Layer();layer.Name=root+' / '+name;layer.Color=Color.Black;li=doc.Layers.Add(layer)
        def attr():
            a=Rhino.DocObjects.ObjectAttributes();a.LayerIndex=li;a.SetUserString('geometry_sha256',scene['geometry_sha256']);return a
        def pt(p):return Rhino.Geometry.Point3d(ox+p[0],oy+p[1],0)
        for p in view['polygons']:
            if len(p['points'])<3:continue
            curve=Rhino.Geometry.PolylineCurve([pt(q) for q in p['points']+[p['points'][0]]]);doc.Objects.AddCurve(curve,attr())
            if p.get('cut') and p.get('material') in ['timber','plywood','lining-wood','cladding-wood','deck-wood'] and hatch_index>=0:
                for hatch in Rhino.Geometry.Hatch.Create(curve,hatch_index,0,12 if p['material']=='plywood' else 30,doc.ModelAbsoluteTolerance) or []:doc.Objects.AddHatch(hatch,attr())
            if p.get('cut') and p.get('material')=='mineral-wool':
                import math
                x0=min(q[0] for q in p['points']);x1=max(q[0] for q in p['points']);y0=min(q[1] for q in p['points']);y1=max(q[1] for q in p['points']);horizontal=x1-x0>=y1-y0
                lo,hi=(x0,x1) if horizontal else (y0,y1);a,b=(y0,y1) if horizontal else (x0,x1);stride=max(30,min(150,(b-a)*.65));count=max(2,int((hi-lo)/5));wave=[]
                for j in range(count+1):
                    t=lo+(hi-lo)*j/count;v=(a+b)/2+(b-a)*.43*math.sin((t-lo)/stride*2*math.pi);wave.append(pt((t,v) if horizontal else (v,t)))
                doc.Objects.AddPolyline(wave,attr())
        for p in view['polylines']:doc.Objects.AddPolyline([pt(q) for q in p],attr())
        for label in view.get('labels',[]):
            text=Rhino.Geometry.TextEntity();text.Plane=Rhino.Geometry.Plane(pt(label['at']),Rhino.Geometry.Vector3d.ZAxis);text.PlainText=label['text'];text.TextHeight=100;doc.Objects.AddText(text,attr())
        for dim in view['dimensions']:
            _,location,_=dimension_lines(dim);a,b=dim['a'],dim['b']
            # Rotate vertical dimension plane; extension-point separation is measured by Rhino.
            vertical=dim['axis']==1
            plane=Rhino.Geometry.Plane(Rhino.Geometry.Point3d(ox,oy,0),Rhino.Geometry.Vector3d(0,1,0) if vertical else Rhino.Geometry.Vector3d(1,0,0),Rhino.Geometry.Vector3d(-1,0,0) if vertical else Rhino.Geometry.Vector3d(0,1,0))
            def uv(p):return Rhino.Geometry.Point2d(p[1],-p[0]) if vertical else Rhino.Geometry.Point2d(*p)
            d=Rhino.Geometry.LinearDimension(plane,uv(a),uv(b),uv(location));d.DimensionStyleId=style_id
            doc.Objects.AddLinearDimension(d,attr())
    page=doc.Views.AddPageView(root+' / A3 plan',420,297)
    # Paper layout title block uses the same 180 x 45 mm geometry as PDF.
    def paper_attr():
        a=Rhino.DocObjects.ObjectAttributes();a.Space=Rhino.DocObjects.ActiveSpace.PageSpace;a.ViewportId=page.MainViewport.Id;return a
    def rectangle(x,y,w,h):
        ps=[Rhino.Geometry.Point3d(a,b,0) for a,b in [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]];doc.Objects.AddPolyline(ps,paper_attr())
    rectangle(20,10,390,277);rectangle(230,10,180,45)
    for y in [25,40]:doc.Objects.AddLine(Rhino.Geometry.Point3d(230,y,0),Rhino.Geometry.Point3d(410,y,0),paper_attr())
    text=Rhino.Geometry.TextEntity();text.Plane=Rhino.Geometry.Plane(Rhino.Geometry.Point3d(233,46,0),Rhino.Geometry.Vector3d.ZAxis);text.PlainText='OBTP / '+scene['config']['id']+' / STUDIJA';text.TextHeight=3;doc.Objects.AddText(text,paper_attr())
    detail=page.AddDetailView('Planas 1:25',Rhino.Geometry.Point2d(25,90),Rhino.Geometry.Point2d(405,260),Rhino.Display.DefinedViewportProjection.Top)
    if detail:
        ox,oy=offsets['plan'];d=scene['dimensions'];target=Rhino.Geometry.Point3d(ox+(d['length_mm']+d['annex_length_mm'])/2,oy+d['width_mm']/2-400,0)
        detail.Viewport.SetCameraTarget(target,True);detail.DetailGeometry.SetScale(1,doc.ModelUnitSystem,25,doc.PageUnitSystem);detail.DetailGeometry.IsProjectionLocked=True;detail.CommitChanges()
    doc.Views.Redraw()
    return root
