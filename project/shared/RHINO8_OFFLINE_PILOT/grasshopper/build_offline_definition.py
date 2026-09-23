# Run in a licensed Windows Rhino session using RunPythonScript, after opening Grasshopper.
# Builds a native .gh definition using the installed SDK rather than hand-written GHX XML.
# AUTHORED, NOT RUNTIME-VALIDATED HERE. Stops rather than producing a fake .gh file.
import os
import json
import clr
import System
import System.Drawing
import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg
clr.AddReference("Grasshopper")
clr.AddReference("GH_IO")
import Grasshopper as gh
from Grasshopper.Kernel import GH_Document, GH_ParamAccess
from Grasshopper.Kernel.Parameters import Param_String, Param_GenericObject
from Grasshopper.Kernel.Special import GH_Group
from Grasshopper.Kernel.Types import GH_String
from GH_IO.Serialization import GH_Archive

script_path = rs.OpenFileName("Select supplied house_mesh.py", "Python (*.py)|*.py||")
if not script_path:
    raise Exception("No script selected")
request_path = os.path.join(os.path.dirname(script_path), "..", "examples", "reference.request.json")
if not os.path.isfile(request_path):
    raise Exception("Extract the complete kit; examples/reference.request.json is required")
output_path = rs.SaveFileName("Save OBTP native Grasshopper definition", "Grasshopper (*.gh)|*.gh||", os.path.dirname(script_path), "obtp_component_library.gh")
if not output_path:
    raise Exception("No output selected")

doc = GH_Document()
component = gh.Instances.ComponentServer.EmitObject(System.Guid("410755B1-224A-4C1E-A407-BF32FB45EA7E"))
if component is None or not hasattr(component, "Code"):
    raise Exception("Legacy GhPython component unavailable; see manual assembly instructions")
component.CreateAttributes()
component.Attributes.Pivot = System.Drawing.PointF(350, 150)
doc.AddObject(component, False)
component.HiddenCodeInput = True
component.Code = open(script_path, "r").read()
component.Params.Input[0].NickName = "house_json"
component.Params.Input[0].Name = "house_json"
component.Params.Input[0].Access = GH_ParamAccess.item
component.Params.Input[1].Optional = True
component.Params.Output[component.Params.Output.Count-1].NickName = "mesh_json"
component.Params.Output[component.Params.Output.Count-1].Name = "mesh_json"
mesh_output = component.Params.Output[component.Params.Output.Count-1]
geo_output = Param_GenericObject()
geo_output.Name = geo_output.NickName = "geometry"
component.Params.RegisterOutputParam(geo_output)
component.Params.OnParametersChanged()

incoming = Param_String()
incoming.Name = incoming.NickName = "House JSON"
incoming.CreateAttributes()
incoming.Attributes.Pivot = System.Drawing.PointF(100, 150)
incoming.SetPersistentData(GH_String(open(request_path, "r").read()))
doc.AddObject(incoming, False)
component.Params.Input[0].AddSource(incoming)
outgoing = Param_String()
outgoing.Name = outgoing.NickName = "Mesh JSON"
outgoing.CreateAttributes()
outgoing.Attributes.Pivot = System.Drawing.PointF(650, 150)
outgoing.AddSource(mesh_output)
doc.AddObject(outgoing, False)
for name, param in [("RH_IN:house_json", incoming), ("RH_OUT:mesh_json", outgoing)]:
    group = GH_Group()
    group.NickName = name
    doc.AddObject(group, False)
    group.AddObject(param.InstanceGuid)

doc.Enabled = True
doc.NewSolution(False)
output_items = list(outgoing.VolatileData.AllData(True))
if len(output_items) != 1:
    raise Exception("Reference solve did not produce one JSON output; inspect Grasshopper errors")
packet = json.loads(str(output_items[0].Value))
if packet.get("producer") != "RhinoCommon via Grasshopper" or not packet.get("objects"):
    raise Exception("Reference solve returned an unexpected payload")
archive = GH_Archive()
if not archive.AppendObject(doc, "Definition"):
    raise Exception("Could not archive Grasshopper definition")
if not archive.WriteToFile(output_path, True, False):
    raise Exception("Could not write Grasshopper definition")
with open(output_path + ".reference-mesh.json", "w") as handle:
    json.dump(packet, handle)
gh.Instances.DocumentServer.AddDocument(doc)
if gh.Instances.ActiveCanvas is not None:
    gh.Instances.ActiveCanvas.Document = doc
# A successful real GH solve is required before writing an offline kit.
request = json.loads(open(request_path, "r").read())
if packet.get("requestKey") != request["requestKey"]:
    raise Exception("Returned mesh request identity mismatch")
if set(x["id"] for x in packet["objects"]) != set(x["id"] for x in request["components"]):
    raise Exception("Returned mesh asset identities differ")
kit = {"schema": "obtp-offline-kit/1", "units": "m", "producer": packet["producer"],
       "runtime": packet["runtime"], "scriptVersion": packet["scriptVersion"],
       "requestKey": packet["requestKey"], "assets": packet["objects"],
       "variants": request["variants"]}
geometry_items = list(geo_output.VolatileData.AllData(True))
if len(geometry_items) != len(request["components"]):
    raise Exception("GH Brep output count mismatch; no offline kit released")
by_id = {}
for item, spec in zip(geometry_items, request["components"]):
    value = item.Value
    if not isinstance(value, rg.Brep) or not value.IsValid:
        raise Exception("Invalid CAD asset: " + spec["id"])
    by_id[spec["id"]] = value
for variant in request["variants"]:
    cad = Rhino.FileIO.File3dm()
    cad.Settings.ModelUnitSystem = Rhino.UnitSystem.Meters
    cad.Settings.ModelAbsoluteTolerance = 0.000001
    for instance in variant["instances"]:
        brep = by_id[instance["assetId"]].DuplicateBrep()
        shift = instance["translation"]
        if not brep.Transform(rg.Transform.Translation(shift[0], shift[1], shift[2])):
            raise Exception("Component placement failed")
        attributes = Rhino.DocObjects.ObjectAttributes()
        attributes.Name = instance["id"]
        attributes.SetUserString("assetId", instance["assetId"])
        attributes.SetUserString("kind", instance["kind"])
        attributes.SetUserString("material", instance["material"])
        cad.Objects.AddBrep(brep, attributes)
    if not cad.Write(output_path + "." + variant["id"] + ".3dm", 7):
        raise Exception("Could not write reference CAD file")
with open(output_path + ".offline-kit.json", "w") as handle:
    json.dump(kit, handle, separators=(",", ":"), allow_nan=False)
print("Real GH solve, two architectural .3dm files and offline-kit.json saved beside: " + output_path)
print("The GH preview overlays reusable local assets at the origin. Inspect the assembled houses in the .3dm files or offline viewer.")
