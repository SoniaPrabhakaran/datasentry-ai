import argparse
import json
from collections import Counter
from validators import load_data, audit, write_exceptions

def main():
    p=argparse.ArgumentParser(description='DataSentry deterministic audit')
    p.add_argument('--csv',default='sample_data/sales.csv'); p.add_argument('--reference',default='sample_data/reference.json'); p.add_argument('--output',default='outputs/exceptions.csv')
    args=p.parse_args()
    with open(args.reference,encoding='utf-8') as f: config=json.load(f)
    rows=load_data(args.csv); findings=audit(rows,config); write_exceptions(args.output,findings)
    print(f'Rows scanned: {len(rows)} | Exceptions: {len(findings)}')
    for check,count in Counter(x['check'] for x in findings).items(): print(f'{check}: {count}')
    for x in findings: print(f"Row {x['row']} | {x['column']} | {x['detail']}")
    print(f'Exception log: {args.output}')
if __name__=='__main__': main()
