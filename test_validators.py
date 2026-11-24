import unittest,json
from collections import Counter
from pathlib import Path
from validators import load_data,audit
ROOT=Path(__file__).resolve().parent
class AuditTests(unittest.TestCase):
    def test_sample(self):
        rows=load_data(ROOT/'sample_data/sales.csv')
        config=json.loads((ROOT/'sample_data/reference.json').read_text())
        findings=audit(rows,config)
        self.assertEqual(Counter(x['check'] for x in findings), {'duplicate':1,'missing':1,'numeric':1,'date':1,'business_rule':3,'reconciliation':1})
        self.assertIn('difference 150.00',findings[-1]['detail'])
    def test_clean(self):
        rows=[dict(transaction_id='A',date='2026-11-01',product='Pen',quantity='2',unit_price='50',amount='100')]
        self.assertEqual(audit(rows,dict(period_start='2026-11-01',period_end='2026-11-30',reference_total='100')),[])
if __name__=='__main__': unittest.main()
