"""Rhino 8 Python: import the System browser's OBTP cassette JSON as closed Breps.
Run in a millimetre document. Does not alter existing objects or document units.
Nominal research geometry only; no fabrication or engineering release.
"""
import json
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs

def main():
    if sc.doc.ModelUnitSystem != Rhino.UnitSystem.Millimeters:
        raise ValueError('Open a millimetre document before import; no automatic rescale.')
    path = rs.OpenFileName('Choose OBTP cassette geometry JSON', 'JSON (*.json)|*.json||')
    if not path:
        return
    with open(path, encoding='utf-8') as stream:
        data = json.load(stream)
    if data.get('schema') != 'obtp-cassette-boxes/1' or data.get('units') != 'mm':
        raise ValueError('Unsupported export')
    breps = []
    for part in data['parts']:
        points = [Rhino.Geometry.Point3d(*p) for p in part['corners']]
        brep = Rhino.Geometry.Brep.CreateFromBox(points)
        if not brep or not brep.IsValid or not brep.IsSolid:
            raise ValueError('Invalid closed part: ' + part['id'])
        breps.append((part, brep))
    layer = 'OBTP::Cassette01::Research'
    if not rs.IsLayer(layer):
        rs.AddLayer(layer)
    for part, brep in breps:
        attr = Rhino.DocObjects.ObjectAttributes()
        attr.Name = part['id']
        attr.LayerIndex = sc.doc.Layers.FindByFullPath(layer, -1)
        attr.SetUserString('system', data['system'])
        attr.SetUserString('material', part['material'])
        attr.SetUserString('status', data['status'])
        attr.SetUserString('manufacturingRelease', 'false')
        sc.doc.Objects.AddBrep(brep, attr)
    sc.doc.Views.Redraw()
    print('Imported {} closed Breps. Concept only; review interface JSON separately.'.format(len(breps)))

if __name__ == '__main__':
    main()
