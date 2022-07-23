python# Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

# Start

```bash
uvicorn app:app --port 8080 --reload
```

# After change SW or install Smth.
```bash
pip3 freeze > requirements.txt    --> freeze # ausgabe in datei umleiten
```