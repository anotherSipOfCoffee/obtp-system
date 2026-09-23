# OBTP Grasshopper geometry stage 0.1.0
# Input: house_json (item access, text). Outputs: mesh_json (text), geometry (Breps).
# Compatible syntax for legacy GhPython / IronPython 2.7 and Rhino Python 3.
# AUTHORED, NOT EXECUTED IN RHINO IN THIS CHECKPOINT.
import json
import math
import Rhino
import Rhino.Geometry as rg

SCRIPT_VERSION = "obtp-gh-0.1.0"
TOLERANCE_M = 0.000001  # computational tolerance, not a manufacturing tolerance

def finite(v):
    n = float(v)
    if math.isnan(n) or math.isinf(n):
        raise ValueError("Non-finite geometry input")
    return n

def build_house(raw):
    data = json.loads(str(raw))
    if data.get("schema") != "obtp-gh-input/1" or data.get("units") != "m":
        raise ValueError("Unsupported input schema or units")
    if data.get("scriptVersion") != SCRIPT_VERSION:
        raise ValueError("Script version mismatch")
    components = data.get("components", [])
    if not components or len(components) > 2000:
        raise ValueError("Invalid component count")
    objects, breps, seen = [], [], set()
    for item in components:
        cid = item["id"]
        if cid in seen:
            raise ValueError("Duplicate component ID")
        seen.add(cid)
        g = item["geometry"]
        if g["type"] == "box":
            x, y, z = [finite(g[k]) for k in ("x", "y", "z")]
            w, d, h = [finite(g[k]) for k in ("width", "depth", "height")]
            if min(w, d, h) <= 0:
                raise ValueError("Non-positive box size")
            brep = rg.Box(rg.Plane.WorldXY, rg.Interval(x, x+w),
                          rg.Interval(y, y+d), rg.Interval(z, z+h)).ToBrep()
        elif g["type"] == "polygon":
            pts = [rg.Point3d(*[finite(v) for v in p]) for p in g["vertices"]]
            if len(pts) == 3:
                brep = rg.Brep.CreateFromCornerPoints(pts[0], pts[1], pts[2], TOLERANCE_M)
            elif len(pts) == 4:
                brep = rg.Brep.CreateFromCornerPoints(pts[0], pts[1], pts[2], pts[3], TOLERANCE_M)
            else:
                raise ValueError("Only triangular/quadrilateral concept surfaces supported")
        else:
            raise ValueError("Unsupported component geometry")
        if brep is None or not brep.IsValid:
            raise ValueError("Invalid Brep: " + cid)
        pieces = rg.Mesh.CreateFromBrep(brep, rg.MeshingParameters.Default)
        if pieces is None or len(pieces) == 0:
            raise ValueError("Meshing failed: " + cid)
        mesh = rg.Mesh()
        for piece in pieces:
            mesh.Append(piece)
        mesh.Faces.ConvertQuadsToTriangles()
        mesh.Normals.ComputeNormals()
        mesh.Compact()
        if not mesh.IsValid or mesh.Vertices.Count == 0:
            raise ValueError("Invalid mesh: " + cid)
        vertices = [[float(p.X), float(p.Y), float(p.Z)] for p in mesh.Vertices]
        faces = [[int(f.A), int(f.B), int(f.C)] for f in mesh.Faces]
        objects.append({"id": cid, "kind": item["kind"], "material": item["material"],
                        "vertices": vertices, "faces": faces})
        breps.append(brep)
    packet = {"schema": "obtp-gh-mesh/1", "scriptVersion": SCRIPT_VERSION,
              "requestKey": data["requestKey"], "units": "m",
              "producer": "RhinoCommon via Grasshopper",
              "runtime": str(Rhino.RhinoApp.Version), "objects": objects}
    return json.dumps(packet, separators=(",", ":"), allow_nan=False), breps

mesh_json = None
geometry = []
if house_json:
    mesh_json, geometry = build_house(house_json)
