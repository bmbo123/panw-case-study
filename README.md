# panw-case-study

Case Study Challenge - PANW

## Setup

First install requirements:

```bash
pip install -r requirements.txt
```

Get the spaCy model:

```bash
python -m spacy download en_core_web_sm
```

## Running It

Add an entry:

```bash
python run_cli.py add "I'm crushing it at work today!"
```

View last entries:

```bash
python run_cli.py last --n 5
```

Show stats:

```bash
python run_cli.py stats --n 10
```

## Testing

Run the tests:

```bash
pytest tests/test_analyzer.py -v
```

20 tests, all pass.
