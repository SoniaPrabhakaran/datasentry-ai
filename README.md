# DataSentry AI

An open-source, local AI-assisted data quality and reconciliation agent powered by Python and Ollama.

**AI decides. Python verifies. DataSentry enforces coverage.**

## Features

- Duplicate transaction detection
- Missing value detection
- Numeric data validation
- Date consistency checks
- Business-rule validation
- Financial reconciliation
- Native AI tool calling
- Mandatory validation coverage
- Dual-layer AI guardrails
- Deterministic numerical summaries
- Evidence-constrained AI recommendations
- Transparent AI and fallback execution tracking
- Read-only data auditing
- CSV exception logs
- HTML audit reports

## Architecture

1. Ollama selects validation tools.
2. Python executes deterministic validation checks.
3. Required fallback checks enforce mandatory coverage.
4. Python generates factual audit summaries.
5. AI selects recommendations from approved labels.
6. Unsupported recommendations trigger a deterministic fallback.
7. Verified findings are exported into structured audit reports.

## Dual-Layer AI Guardrails

### Execution Layer

Mandatory validation checks are executed even when the
AI model fails to select them.

### Reporting Layer

Numerical summaries are generated directly from verified
Python results. AI recommendations are restricted to
approved, evidence-compatible labels.

Unsupported responses are rejected and replaced with
a deterministic recommendation.

## Installation

Requires Python and a running Ollama installation.

    pip install -r requirements.txt
    ollama pull llama3.2:1b

## Usage

Run the AI agent:

    python agent.py

Generate the HTML report:

    python reporting.py

Run automated tests:

    python -m unittest -v

## Outputs

- outputs/exceptions.csv
- outputs/agent_audit.json
- outputs/audit_report.html

## Testing

Seven automated tests passed, covering:

- Validation tool dispatch and mandatory coverage
- Rejection of incorrect AI commentary
- Acceptance of valid AI recommendations
- Rejection of inappropriate recommendations
- HTML reporting and content escaping
- Clean dataset validation
- Sample dataset validation

## Limitations

- Currently supports a documented sales transaction schema.
- Validation coverage is limited to six configured checks.
- Sample data is synthetic.
- AI recommendations use predefined options.
- Human review remains necessary.
- Source data is not automatically corrected.
- CSV export includes basic formula injection mitigation.
- This is an experimental release, not a production-ready enterprise solution.

## Roadmap

- Configurable validation rules
- Support for additional dataset schemas
- Expanded evidence-based recommendations
- Interactive audit interface
- Database connectivity

## Development Documentation

See the docs directory for implementation details,
security considerations and AI guardrail design.

## License

MIT
