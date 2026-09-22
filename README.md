# Quality Compass — evaluation suite

Synthetic test suite for evaluating an AI assistant that turns feature requests
into clarifying questions, risk analysis, and draft test strategy.

**Tallowbrook is a fictional product.** All requests and data are synthetic.

## Contents
- `product_overview.md` — context for the fictional product
- `taxonomy.md` — risk categories and codes
- `scoring_rules.md` — how outputs are graded
- `answer_keys/` — one YAML file per feature request
- `validate_keys.py` — checks answer keys for schema errors and reports category coverage

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python validate_keys.py
```
