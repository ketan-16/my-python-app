# my-python-app

A minimal FastAPI service.

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API docs.

## Test

```bash
pytest -q
```
