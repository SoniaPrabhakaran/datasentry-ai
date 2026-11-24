
import unittest
import tempfile
import json

from types import SimpleNamespace as NS
from pathlib import Path
from agent import run_agent
from validators import load_data, audit


class AgentTests(unittest.TestCase):

    def setUp(self):
        self.rows = load_data("sample_data/sales.csv")
        self.config = json.loads(
            Path("sample_data/reference.json").read_text()
        )

    def test_dispatch_and_coverage(self):

        def fake_chat(**kwargs):
            if "tools" in kwargs and any(
                t["function"]["name"] == "check_duplicates"
                for t in kwargs["tools"]
            ):
                return NS(message=NS(tool_calls=[
                    NS(function=NS(
                        name="check_duplicates",
                        arguments={}
                    ))
                ]))

            return NS(message=NS(
                tool_calls=[],
                content="Review exceptions."
            ))

        with tempfile.TemporaryDirectory() as d:

            r = run_agent(
                self.rows, self.config,
                fake_chat, "mock", d
            )

            self.assertEqual(
                r["findings"],
                audit(self.rows, self.config)
            )

            self.assertEqual(
                r["trace"][0]["source"],
                "AI-selected"
            )

            self.assertEqual(len(r["trace"]), 6)

            self.assertEqual(
                sum(
                    t["source"] == "Required coverage fallback"
                    for t in r["trace"]
                ),
                5
            )

            self.assertTrue(
                Path(d, "agent_audit.json").exists()
            )

    def test_reject_incorrect_ai_commentary(self):

        def fake_chat(**kwargs):
            return NS(message=NS(
                tool_calls=[],
                content="Completed 8 validation checks."
            ))

        with tempfile.TemporaryDirectory() as d:

            r = run_agent(
                self.rows, self.config,
                fake_chat, "mock", d
            )

            self.assertEqual(
                r["commentary_source"],
                "Deterministic fallback"
            )

            self.assertIn(
                "Completed 6 validation checks",
                r["guarded_summary"]
            )

            self.assertIn(
                "Detected 8 exceptions",
                r["guarded_summary"]
            )

            self.assertNotIn(
                "Completed 8 validation checks",
                r["guarded_summary"]
            )

    def test_accept_valid_ai_recommendation(self):

        def fake_chat(**kwargs):
            return NS(message=NS(
                tool_calls=[],
                content="RECONCILE"
            ))

        with tempfile.TemporaryDirectory() as d:

            r = run_agent(
                self.rows, self.config,
                fake_chat, "mock", d
            )

            self.assertEqual(
                r["commentary_source"],
                "AI-selected recommendation"
            )

            self.assertEqual(
                r["recommendation_label"],
                "RECONCILE"
            )

            self.assertIn(
                "Investigate reconciliation differences",
                r["guarded_summary"]
            )

    def test_reject_unsafe_recommendation(self):

        def fake_chat(**kwargs):
            return NS(message=NS(
                tool_calls=[],
                content="PROCEED"
            ))

        with tempfile.TemporaryDirectory() as d:

            r = run_agent(
                self.rows, self.config,
                fake_chat, "mock", d
            )

            self.assertEqual(
                r["commentary_source"],
                "Deterministic fallback"
            )

            self.assertEqual(
                r["recommendation_label"],
                "REVIEW"
            )

            self.assertGreater(
                r["evidence"]["exception_count"], 0
            )


if __name__ == "__main__":
    unittest.main()
