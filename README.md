# Installing

Create Virtual Environment
```bash
python3 -m venv venv
```
Activate Virtual Environment


**Windows**
```bash
source venv/Scripts/activate
```
**Unix**
```bash
source venv/bin/activate
```

Install Modules
```bash
pip install -r requirements.txt
```

Create Database and insert data
```bash
python migrate.py
```