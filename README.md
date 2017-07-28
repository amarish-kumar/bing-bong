# bing-bong

### Install Virtualenv

 - Make sure you have python 2.7.x and pip installed.
```bash 
pip install virtualenv
virtualenv flask
source flask/bin/activate
```

### Clone the repo

```bash
git clone https://github.com/royalharsh/bing-bong.git
cd bing-bong
```

### Install dependencies and create database 

```bash
pip install -r requirements.txt
python -m nltk.downloader all
python db_create.py
```

### Run the app

```bash
gunicorn app:app
```

### Browse to http://localhost:8000

#### Feel free to open an issue if you face any problems.
