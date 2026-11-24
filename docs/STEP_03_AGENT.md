# Step 3 — Local agent integration

Step 2 user-reported tests: 2 passed, 8 findings. User-reported Ollama llama3.2:1b structured duplicate-tool request succeeded. This does not establish reliable autonomous selection.

The agent offers six allowlisted, zero-argument tools. It executes valid model requests, returns counts to the model, and logs actual selection provenance. Eight rounds maximum. Any unselected checks run deterministically for complete coverage and are explicitly labeled fallback. No source edits. Only aggregate counts are sent to the model; the final generated commentary is unverified and requires review. Python findings are authoritative. JSON and CSV outputs may contain sensitive source identifiers; do not publish real customer data. CSV spreadsheet formula injection hardening remains a release task for untrusted inputs.

Run `python agent.py` from repository root. Optional flags: --csv, --reference, --model, --output. Run `python -m unittest -v`. Mock test checks dispatch and fallback coverage, not real model reliability. Live integration must be tested locally before publication. HTML reporting and licensing remain pending.
