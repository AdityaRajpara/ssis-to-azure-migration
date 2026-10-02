"""Configuration-driven SSIS-like package control-flow simulation."""
import json
from pathlib import Path
from migration_demo.ingest.sources import fetch_sources,write_bronze
from migration_demo.transform.jobs import normalize,aggregate,quality

def run(root=Path('lake'),live=False):
    workflow=json.loads(Path('config/legacy_workflow.json').read_text())
    data=fetch_sources(live);write_bronze(data,Path(root)/'legacy')
    silver=normalize(data); gold=aggregate(silver); checks=quality(silver)
    out=Path(root)/'legacy'/'gold';out.mkdir(parents=True,exist_ok=True)
    (out/'mart.json').write_text(json.dumps(gold,indent=2,sort_keys=True))
    return {'workflow':workflow['package_name'],'silver':silver,'gold':gold,'quality':checks}
