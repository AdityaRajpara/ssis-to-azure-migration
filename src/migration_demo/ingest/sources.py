"""Source adapters for public APIs, SQLite, and delimited files."""
import csv, json, os, sqlite3
from pathlib import Path
from datetime import date
import urllib.parse, urllib.request

ROOT = Path(__file__).resolve().parents[3]

def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as f: return list(csv.DictReader(f))

def http_get(url, params=None, headers=None):
    if params: url += ('&' if '?' in url else '?') + urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers=headers or {})
    with urllib.request.urlopen(req,timeout=30) as response: return json.loads(response.read().decode('utf-8'))

def fetch_sources(live=False):
    cfg=json.loads((ROOT/'config/sources.json').read_text())
    if live:
        nyc=http_get(cfg['live']['nyc_311_url'],params={'$limit':100,'$order':'created_date DESC','$select':'unique_key,created_date,complaint_type,borough,descriptor'})
        key=os.getenv('FRED_API_KEY'); fred=[]
        if key:
            fred=http_get(cfg['live']['fred_series_url'],params={'series_id':cfg['live']['fred_series_id'],'api_key':key,'file_type':'json','observation_start':'2025-01-01'}).get('observations',[])
        else: fred=read_csv(ROOT/cfg['offline']['fred_fixture'])
        ua=os.getenv(cfg['live']['sec_user_agent_env'])
        sec={}
        if ua:
            sec=http_get(cfg['live']['sec_companyfacts_url'],headers={'User-Agent':ua,'Accept-Encoding':'gzip, deflate'})
        else: sec=json.loads((ROOT/cfg['offline']['sec_fixture']).read_text())
    else:
        nyc=read_csv(ROOT/cfg['offline']['311_fixture']);fred=read_csv(ROOT/cfg['offline']['fred_fixture']);sec=json.loads((ROOT/cfg['offline']['sec_fixture']).read_text())
    # Relational source simulates the on-prem finance/operations database.
    db=sqlite3.connect(':memory:'); db.execute('create table accounts(account_id integer, domain text, account_name text, exposure_usd real, risk_band text)')
    db.executemany('insert into accounts values (:account_id,:domain,:account_name,:exposure_usd,:risk_band)',[{**x,'account_id':int(x['account_id']),'exposure_usd':float(x['exposure_usd'])} for x in read_csv(ROOT/cfg['offline']['accounts_fixture'])]);db.row_factory=sqlite3.Row
    accounts=[dict(x) for x in db.execute('select * from accounts')]; db.close()
    return {'311':nyc,'fred':fred,'sec':sec,'accounts':accounts}

def write_bronze(data, root=Path('lake')):
    base=Path(root)/'bronze'
    for name, rows in data.items():
        d=base/name;d.mkdir(parents=True,exist_ok=True)
        p=d/'records.jsonl'
        serial=rows if isinstance(rows,list) else [rows]
        p.write_text(''.join(json.dumps(x,sort_keys=True,default=str)+'\n' for x in serial),encoding='utf-8')
    return base
