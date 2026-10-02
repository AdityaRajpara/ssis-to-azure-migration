"""Deterministic Bronze-to-Silver-to-Gold transformations."""
from datetime import datetime

def normalize(data):
    accounts=[]
    for x in data['accounts']:
        accounts.append({'account_id':int(x['account_id']),'domain':x['domain'].lower(),'account_name':x['account_name'].strip(),'exposure_usd':round(float(x['exposure_usd']),2),'risk_band':x['risk_band'].upper()})
    requests=[]
    for x in data['311']:
        requests.append({'request_id':str(x.get('unique_key',x.get('request_id',''))),'created_date':str(x.get('created_date',''))[:10],'complaint_type':str(x.get('complaint_type','')).strip().upper(),'borough':str(x.get('borough','UNKNOWN')).strip().upper()})
    rates=[]
    for x in data['fred']:
        try: val=float(x['value'])
        except (ValueError,TypeError,KeyError): continue
        rates.append({'date':x.get('date',x.get('observation_date','')),'yield_pct':round(val,4)})
    return {'accounts':accounts,'service_requests':requests,'rates':rates}

def aggregate(silver):
    counts={}
    for r in silver['service_requests']: counts[r['complaint_type']]=counts.get(r['complaint_type'],0)+1
    exposure={}
    for a in silver['accounts']: exposure[a['domain']]=round(exposure.get(a['domain'],0)+a['exposure_usd'],2)
    return {'complaints_by_type':[{'complaint_type':k,'request_count':v} for k,v in sorted(counts.items())], 'exposure_by_domain':[{'domain':k,'exposure_usd':v} for k,v in sorted(exposure.items())], 'daily_rates':sorted(silver['rates'],key=lambda x:x['date'])}

def quality(silver):
    checks=[]
    ids=[a['account_id'] for a in silver['accounts']]
    checks.append({'check':'unique_account_id','passed':len(ids)==len(set(ids)),'observed':len(ids)})
    checks.append({'check':'nonnegative_exposure','passed':all(a['exposure_usd']>=0 for a in silver['accounts']),'observed':sum(a['exposure_usd']<0 for a in silver['accounts'])})
    checks.append({'check':'request_id_present','passed':all(bool(r['request_id']) for r in silver['service_requests']),'observed':sum(not bool(r['request_id']) for r in silver['service_requests'])})
    return checks
