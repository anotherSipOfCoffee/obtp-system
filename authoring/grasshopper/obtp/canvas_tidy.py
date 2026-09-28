"""Deterministic group lanes. Only OBTP-tagged groups/objects are repositioned."""
def tidy(doc):
 from System.Drawing import PointF
 from Grasshopper.Kernel.Special import GH_Group,GH_Panel
 groups=[g for g in doc.Objects if isinstance(g,GH_Group) and g.NickName.startswith('OBTP / ')]
 x=60
 for group in groups:
  members=[doc.FindObject(guid,False) for guid in group.ObjectIDs]
  members=[o for o in members if o is not None and not isinstance(o,GH_Group)]
  lanes=[[],[],[]]
  for obj in members:
   if isinstance(obj,GH_Panel):lane=2 if obj.SourceCount else 0
   elif hasattr(obj,'Params'):lane=1
   else:lane=0
   lanes[lane].append(obj)
  for lane,objects in enumerate(lanes):
   y=100
   for obj in objects:
    bounds=obj.Attributes.Bounds
    obj.Attributes.Pivot=PointF(x+lane*560,y)
    obj.Attributes.ExpireLayout()
    ports=max(obj.Params.Input.Count,obj.Params.Output.Count) if hasattr(obj,'Params') else 0
    y+=max(160,bounds.Height+90,100+ports*36)
  group.Attributes.ExpireLayout()
  x+=1800
 return len(groups)
