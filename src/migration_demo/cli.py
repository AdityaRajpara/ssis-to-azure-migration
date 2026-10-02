import argparse,csv,json,time
from pathlib import Path
from migration_demo.legacy.package import run as legacy_run
from migration_demo.cloud.pipeline import run as cloud_run
from migration_demo.ingest.sources import fetch_sources
from migration_demo.transform.jobs import normalize,aggregate,quality

ROOT=Path(__file__).resolve().parents[2]
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def reconcile(root=Path('lake')):
    a=json.loads((Path(root)/'legacy/gold/mart.json').read_text())
    # Load generated gold tables in their distinct layouts.
    g=Path(root)/'cloud/gold'
    b={name:json.loads((g/name/'data.json').read_text()) for name in ['complaints_by_type','exposure_by_domain','daily_rates']}
    checks=[{'check':k,'passed':canonical(a[k])==canonical(b[k])} for k in sorted(a)]
    p=Path('artifacts');p.mkdir(exist_ok=True);(p/'reconciliation.json').write_text(json.dumps({'passed':all(x['passed'] for x in checks),'checks':checks},indent=2))
    if not all(x['passed'] for x in checks): raise SystemExit('Reconciliation failed')
    print(json.dumps({'passed':True,'checks':checks},indent=2))
def benchmark(iterations=3):
    import tempfile
    from migration_demo.legacy.package import run as legacy
    from migration_demo.cloud.pipeline import run as cloud
    rows=[]
    with tempfile.TemporaryDirectory() as temp:
      for mode,fn in [('legacy',lambda:legacy(root=Path(temp)/'legacy')['gold']),('cloud',lambda:cloud(root=Path(temp)/'cloud')['gold'])]:
        samples=[]
        for i in range(iterations):
            t=time.perf_counter();result=fn();samples.append(round(time.perf_counter()-t,6))
        size=len(canonical(result).encode());rows.append({'mode':mode,'iterations':iterations,'seconds':samples,'median_seconds':sorted(samples)[len(samples)//2],'output_bytes':size})
    Path('artifacts').mkdir(exist_ok=True);Path('artifacts/benchmark.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
def main():
    import os
    os.chdir(ROOT)
    ap=argparse.ArgumentParser(prog='migration-demo');sub=ap.add_subparsers(dest='cmd',required=True)
    r=sub.add_parser('run');r.add_argument('--mode',choices=['legacy','cloud','both'],default='both');r.add_argument('--live',action='store_true');r.add_argument('--engine',choices=['python','spark'],default='python')
    sub.add_parser('reconcile');b=sub.add_parser('benchmark');b.add_argument('--iterations',type=int,default=3)
    a=ap.parse_args()
    if a.cmd=='run':
        if a.mode in ('legacy','both'): legacy_run(live=a.live)
        if a.mode in ('cloud','both'): cloud_run(live=a.live,engine=a.engine)
        print(f"Completed {a.mode} run. Output: lake/")
    elif a.cmd=='reconcile':reconcile()
    else:benchmark(max(1,a.iterations))
if __name__=='__main__':main()
