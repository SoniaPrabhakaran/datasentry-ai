# Step 4 — HTML reporting

Run `python reporting.py` after `python agent.py`. The standalone report reads the existing JSON evidence, tool trace and exception register. It distinguishes AI-selected tools from coverage fallback and escapes all dynamic HTML text. No external assets or network calls are needed. Unverified model commentary is excluded because the live model misstated the check count. This is a deliberate release decision; raw commentary remains in the JSON for review. Report tests verify escaping and exclusion of commentary. CSV export hardening remains a release task.
