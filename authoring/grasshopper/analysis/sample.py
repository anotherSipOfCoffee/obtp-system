import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from obtp.model import build,parameters
from obtp.analysis import write_bundle
from obtp.sheets import pdf
out=Path(sys.argv[1]);s=build(parameters(2));a=write_bundle(s,out)
pdf(s,out/'OBTP-M-technical-product.pdf')
print(json.dumps(a['audit'],indent=2))
