"""Run in Rhino 8 Windows ScriptEditor, Python 3. Read-only source check.
Select the original W-S.3dm and the viewer's downloaded model.json.
Does not modify the open Rhino document. Writes a report where you choose.
"""
import json,hashlib
import Rhino
import rhinoscriptsyntax as rs

def main():
    source=rs.OpenFileName('Select original W-S.3dm','Rhino model (*.3dm)|*.3dm||')
    if not source: return
    packet=rs.OpenFileName('Select downloaded web model.json','JSON (*.json)|*.json||')
    if not packet: return
    with open(source,'rb') as f: raw=f.read()
    sha=hashlib.sha1(('blob %d\0'%len(raw)).encode()+raw).hexdigest()
    if sha!='932338ca81fdc2acdd345cd0fc9df09d2a9888b2': raise ValueError('Source hash does not match pinned W-S')
    with open(packet) as f: web=json.load(f)
    if web.get('schema')!='obtp-source-mesh/1' or web.get('units')!='mm': raise ValueError('Unexpected web geometry')
    model=Rhino.FileIO.File3dm.Read(source)
    if model.Settings.ModelUnitSystem!=Rhino.UnitSystem.Millimeters: raise ValueError('Unexpected CAD units')
    refs=[o for o in model.Objects if isinstance(o.Geometry,Rhino.Geometry.InstanceReferenceGeometry)]
    if len(refs)!=1: raise ValueError('Expected one source instance')
    xf=refs[0].Geometry.Xform
    objects={str(o.Attributes.Id):o for o in model.Objects}
    report={'source_blob_sha':sha,'rhino_version':str(Rhino.RhinoApp.Version),'parts':[],'limits':'Bounds and validity only; no structural, fabrication or full surface-deviation certification.'}
    for asset in web['assets']:
        source_object=objects[asset['id']]
        geo=source_object.Geometry.DuplicateBrep();geo.Transform(xf)
        bounds=geo.GetBoundingBox(True)
        cad=[[bounds.Min.X,bounds.Min.Y,bounds.Min.Z],[bounds.Max.X,bounds.Max.Y,bounds.Max.Z]]
        mesh=[[fn(v[k] for v in asset['vertices']) for k in range(3)] for fn in (min,max)]
        delta=max(abs(cad[i][k]-mesh[i][k]) for i in range(2) for k in range(3))
        report['parts'].append({'id':asset['id'],'valid':geo.IsValid,'solid':geo.IsSolid,'rhino_bounds_mm':cad,'mesh_bounds_mm':mesh,'bounds_delta_mm':delta})
    output=rs.SaveFileName('Save W-S Rhino comparison report','JSON (*.json)|*.json||',filename='W-S-rhino8-report.json')
    if output:
        with open(output,'w') as f: json.dump(report,f,indent=2)
        print('Saved comparison for %d parts to %s'%(len(report['parts']),output))
main()
