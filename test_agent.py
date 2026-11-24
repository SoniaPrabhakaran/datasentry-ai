import unittest, tempfile, json
from types import SimpleNamespace as NS
from pathlib import Path
from agent import run_agent
from validators import load_data, audit
class AgentTests(unittest.TestCase):
    def test_dispatch_and_coverage(self):
        rows=load_data('sample_data/sales.csv'); config=json.loads(Path('sample_data/reference.json').read_text())
        def fake_chat(**kwargs):
            if 'tools' in kwargs and any(t['function']['name']=='check_duplicates' for t in kwargs['tools']):
                return NS(message=NS(tool_calls=[NS(function=NS(name='check_duplicates',arguments={}))]))
            return NS(message=NS(tool_calls=[],content='Review exceptions.'))
        with tempfile.TemporaryDirectory() as d:
            r=run_agent(rows,config,fake_chat,'mock',d)
            self.assertEqual(r['findings'],audit(rows,config)); self.assertEqual(r['trace'][0]['source'],'AI-selected'); self.assertEqual(len(r['trace']),6)
            self.assertTrue(Path(d,'agent_audit.json').exists())
