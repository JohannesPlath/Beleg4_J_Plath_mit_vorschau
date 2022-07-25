python# Install

# preparate System:
```bash

sudo apt install curl
sudo apt install python3.8-venv
sudo apt install gcc
sudo apt install libpython3.8-dev
sudo apt-get install openslide-tools

pip install "fastapi[all]"
pip install "uvicorn[standard]"

``` 

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