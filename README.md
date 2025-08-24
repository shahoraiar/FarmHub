# 🌾 FarmHub

FarmHub is a farm management platform built with **Django** and **FastAPI**.  
- **Django** handles authentication, role management (SuperAdmin, Agent, Farmer), and database models.  
- **FastAPI** is used for reporting APIs (`/farms`, `/cow/details`, `/production/milk/summary`, etc.).  

---

## ⚙️ Project Structure

```text
farmhub/
│── core/ # Django project
│ ├── core/ # Django settings
│ ├── farms/ # Django app with models
│ ├── manage.py
│
│── reporting/ # FastAPI service
│ ├── main.py # FastAPI entrypoint
│ ├── requirements.txt
│
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone & Install
```bash
git clone https://github.com/shahoraiar/FarmHub.git
cd farmhub
```
### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac[git bash]
venv\Scripts\activate      # Windows[powershell]
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
---
## Run Django 
```bash
cd core
python manage.py runserver
```

## Run FastAPI (Reporting) in another Terminal
```bash
uvicorn reporting.main:app --port 5000 --reload
```




