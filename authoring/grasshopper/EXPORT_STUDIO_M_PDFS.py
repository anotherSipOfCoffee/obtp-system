"""Generate the three GH review PDFs for default Studio M only.
Run with Python + reportlab: python EXPORT_STUDIO_M_PDFS.py [destination]
This utility does not build, modify or publish a website.
"""
import sys
from pathlib import Path
from obtp.model import build,parameters
from obtp.documentation import assembly,parts_layout
from obtp.schedule_pdf import write
from obtp.ssp_preview import pdf

def export(destination):
    out=Path(destination);out.mkdir(parents=True,exist_ok=True)
    scene=build(parameters(2,program_type=1,roof_type=0,studio_winter_closed=False))
    scene['display_revision']='GH-R21-MODULARITY-AUDIT'
    scene['document_date']='2026-09-27'
    write(scene,out/'Studio_M_R21_Part_Schedule.pdf','GH R21; retained R20 geometry; audited modularity')
    pdf(parts_layout(scene),out/'Studio_M_R21_Parts_Layout.pdf')
    pdf(assembly(scene),out/'Studio_M_R21_Assembly.pdf')
    print('Three default Studio M PDFs:',out)
if __name__=='__main__':export(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent/'gh-documents')
