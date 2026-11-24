import unittest
from reporting import render
class ReportTests(unittest.TestCase):
    def test_verified_and_escaped(self):
        a={'model':'<script>','evidence':{'rows_scanned':8,'exception_count':1},'trace':[{'tool':'check_duplicates','source':'AI-selected','exceptions':1}],'findings':[{'row':2,'column':'id','check':'duplicate','severity':'error','detail':'<bad>'}],'ai_summary_unverified':'WRONG COUNT'}
        s=render(a); self.assertIn('1/1',s); self.assertIn('&lt;bad&gt;',s); self.assertNotIn('<script>',s); self.assertNotIn('WRONG COUNT',s)
