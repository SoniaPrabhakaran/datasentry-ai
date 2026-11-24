"""Deterministic checks for the documented sales CSV schema."""
import csv
import json
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

COLUMNS = ('transaction_id','date','product','quantity','unit_price','amount')

def load_data(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if not set(COLUMNS).issubset(reader.fieldnames or []):
            raise ValueError('Missing required columns: ' + ', '.join(sorted(set(COLUMNS)-set(reader.fieldnames or []))))
        return [{k:(r.get(k) or '').strip() for k in COLUMNS} for r in reader]

def number(value):
    try:
        n = Decimal(value)
        return n if n.is_finite() else None
    except InvalidOperation:
        return None

def issue(row, column, check, detail, severity='error'):
    return dict(row=row, column=column, check=check, severity=severity, detail=detail)

def check_duplicates(rows, config):
    seen=set(); out=[]
    for i,r in enumerate(rows,2):
        key=r['transaction_id']
        if key and key in seen: out.append(issue(i,'transaction_id','duplicate',f'Repeated ID: {key}'))
        if key: seen.add(key)
    return out

def check_missing(rows, config):
    return [issue(i,k,'missing','Required value missing') for i,r in enumerate(rows,2) for k in COLUMNS if not r[k]]

def check_numeric(rows, config):
    return [issue(i,k,'numeric','Not a finite number') for i,r in enumerate(rows,2) for k in ('quantity','unit_price','amount') if r[k] and number(r[k]) is None]

def check_dates(rows, config):
    start=date.fromisoformat(config['period_start']); end=date.fromisoformat(config['period_end']); out=[]
    for i,r in enumerate(rows,2):
        if not r['date']: continue
        try: d=date.fromisoformat(r['date'])
        except ValueError:
            out.append(issue(i,'date','date','Invalid ISO date')); continue
        if not start<=d<=end: out.append(issue(i,'date','date','Outside reporting period'))
    return out

def check_business_rules(rows, config):
    out=[]
    for i,r in enumerate(rows,2):
        q,p,a=(number(r[k]) for k in ('quantity','unit_price','amount'))
        if q is not None and (q<=0 or q!=q.to_integral_value()): out.append(issue(i,'quantity','business_rule','Quantity must be a positive integer'))
        if p is not None and p<0: out.append(issue(i,'unit_price','business_rule','Negative unit price'))
        if a is not None and a<0: out.append(issue(i,'amount','business_rule','Negative sales amount'))
        if None not in (q,p,a) and q*p!=a: out.append(issue(i,'amount','business_rule','Amount differs from quantity × unit price'))
    return out

def check_reconciliation(rows, config):
    values=[number(r['amount']) for r in rows]
    if None in values: return [issue('dataset','amount','reconciliation','Cannot reconcile: missing or invalid amount')]
    actual=sum(values,Decimal(0)); expected=number(str(config['reference_total']))
    if expected is None: raise ValueError('Invalid reference_total')
    if actual!=expected: return [issue('dataset','amount','reconciliation',f'Raw total {actual:.2f}; reference {expected:.2f}; difference {actual-expected:.2f}')]
    return []

TOOLS={f.__name__:f for f in (check_duplicates,check_missing,check_numeric,check_dates,check_business_rules,check_reconciliation)}

def audit(rows, config):
    return [item for fn in TOOLS.values() for item in fn(rows,config)]

def safe_csv_cell(value):
    if isinstance(value, str):
        if value.lstrip().startswith(('=', '+', '-', '@')) or value.startswith(('\t', '\r', '\n')):
            return "'" + value
    return value

def write_exceptions(path, findings):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['row', 'column', 'check', 'severity', 'detail']
        )
        writer.writeheader()
        writer.writerows(
            {k: safe_csv_cell(v) for k, v in item.items()}
            for item in findings
        )

