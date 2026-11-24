# Step 2 — Deterministic validation engine

Status: sample audit and two automated tests passed in the build environment; Windows verification pending.

Run `python run_audit.py` from the project root. Run `python -m unittest -v` to test. Optional arguments: `--csv`, `--reference`, `--output`.

Input: UTF-8 CSV with transaction_id,date,product,quantity,unit_price,amount. Dates are ISO dates. Reference JSON supplies period_start, period_end and an independently obtained reference_total (synthetic in the example). The sales-only schema assumes positive integer quantities, nonnegative prices and amounts, and no discounts or returns. Decimal arithmetic avoids binary floating-point errors. The reconciliation compares the raw total, including suspect records, to the reference; it does not establish a corrected total or prove the cause of a discrepancy.

Output: CSV exception log with logical record number (header counted as 1), column, check, severity and detail. Multiple exceptions may refer to the same record. All current checks use error severity. No source records are modified. Sample: 8 records, 8 exceptions across 6 check categories; raw total 2550, reference 2400, difference 150.

Design: validators are independent of AI and use only the Python standard library. TOOLS exposes the six functions for future bounded agent integration. AI tool execution, reporting UI and publication are not implemented yet. Existing Step 1 documentation is preserved. Tests cover the seeded sample and a clean record, not all edge cases. For production, add schema configuration, malformed-file handling, safe spreadsheet export, larger test coverage and resource limits.
