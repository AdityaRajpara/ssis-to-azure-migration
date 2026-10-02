"""ADF/ADLS-shaped local execution path."""
import json
from pathlib import Path
from migration_demo.ingest.sources import fetch_sources,write_bronze
from migration_demo.transform.jobs import normalize,aggregate,quality

def run(root=Path('lake'),live=False,engine='python'):
    data=fetch_sources(live);write_bronze(data,Path(root)/'cloud')
    if engine=='spark':
        from migration_demo.transform.spark_job import transform
        silver,gold=transform(data)
    else: silver=normalize(data);gold=aggregate(silver)
    base=Path(root)/'cloud'
    for layer,payload in [('silver',silver),('gold',gold)]:
        for name,rows in payload.items():
            path=base/layer/name;path.mkdir(parents=True,exist_ok=True)
            (path/'data.json').write_text(json.dumps(rows,indent=2,sort_keys=True))
    return {'silver':silver,'gold':gold,'quality':quality(silver)}
