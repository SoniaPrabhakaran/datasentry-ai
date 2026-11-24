# DataSentry AI

An open-source, AI-assisted data quality and reconciliation agent powered by Python and Ollama.

## Features

- Duplicate transaction detection
- Missing value detection
- Numeric data validation
- Date consistency checks
- Business-rule validation
- Financial reconciliation
- AI-directed validation tool execution
- Mandatory validation coverage
- CSV exception logs
- HTML audit reports

## Architecture

Ollama selects validation tools.
Python executes deterministic checks.
Required fallback checks ensure complete validation coverage.
Verified findings are exported into structured audit reports.

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

## Limitations

- Currently supports a documented sales transaction schema.
- Sample data is synthetic.
- AI-generated commentary requires human review.
- Source data is not automatically corrected.
- CSV export includes basic formula injection mitigation.

## Roadmap

- Configurable validation rules
- Support for additional dataset schemas
- Improved AI interpretation
- Interactive audit interface
- Database connectivity

## License

MIT
