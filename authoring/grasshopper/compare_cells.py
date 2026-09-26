"""Compatibility entry point; all comparisons use the manufacturing audit."""
from compare_manufacturing import run
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('destination');p.add_argument('--full-catalogue',action='store_true');a=p.parse_args()
    run(a.destination,a.full_catalogue)
