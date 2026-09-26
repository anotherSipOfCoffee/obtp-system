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
    style=Rhino.DocObjects.DimensionStyle();style.Name=root;style.TextHeight=125;style.ArrowLength=60;style.DimensionScale=1
    sid=doc.DimStyles.Add(style);style_id=doc.DimStyles[sid].Id
    offsets={}
    for i,(name,view) in enumerate(scene['drawings']['views'].items()):
        ox=15000;oy=-i*8500;offsets[name]=(ox,oy)
        layer=Rhino.DocObjects.Layer();layer.Name=root+' / '+name;layer.Color=Color.Black;li=doc.Layers.Add(layer)
        def attr():
            a=Rhino.DocObjects.ObjectAttributes();a.LayerIndex=li;a.SetUserString('geometry_sha256',scene['geometry_sha256']);return a
        def pt(p):return Rhino.Geometry.Point3d(ox+p[0],oy+p[1],0)
        for p in view['polygons']:
            if len(p['points'])<3:continue
            curve=Rhino.Geometry.PolylineCurve([pt(q) for q in p['points']+[p['points'][0]]]);doc.Objects.AddCurve(curve,attr())
            if p['fill']=='#111111':
                for hatch in Rhino.Geometry.Hatch.Create(curve,0,0,1,doc.ModelAbsoluteTolerance) or []:doc.Objects.AddHatch(hatch,attr())
        for p in view['polylines']:doc.Objects.AddPolyline([pt(q) for q in p],attr())
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
    detail=page.AddDetailView('Planas 1:50',Rhino.Geometry.Point2d(25,90),Rhino.Geometry.Point2d(405,260),Rhino.Display.DefinedViewportProjection.Top)
    if detail:
        ox,oy=offsets['plan'];d=scene['dimensions'];target=Rhino.Geometry.Point3d(ox+(d['length_mm']+d['annex_length_mm'])/2,oy+d['width_mm']/2-400,0)
        detail.Viewport.SetCameraTarget(target,True);detail.DetailGeometry.SetScale(1,doc.ModelUnitSystem,50,doc.PageUnitSystem);detail.DetailGeometry.IsProjectionLocked=True;detail.CommitChanges()
    doc.Views.Redraw()
    return root
