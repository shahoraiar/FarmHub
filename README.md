# 🌾 FarmHub

FarmHub is a farm management platform built with **Django** and **FastAPI**.  
- **Django** handles authentication, role management (SuperAdmin, Agent, Farmer), and database models.  
- **FastAPI** is used for reporting APIs (`/farms`, `/cow/details`, `/production/milk/summary`, etc.).  

---

## ⚙️ Project Structure

```text
farmhub/
│── core/ # Django project
│     ├── apps/ # Django apps
│     │     ├── accounts/ # User module
│     │     ├── farms/ # Farm, Farmer
│     │     ├── livestock/ # Cow, CowActivity
│     │     ├── production/ # MilkProduction
│     │
│     ├── core/ # Django settings
│     ├── system/ # Permissions & roles
│     ├── templates/ # Django templates
│     ├── db.sqlite3 # Default database
│     └── manage.py
│
│── reporting/ # FastAPI microservice
│     ├── main.py # FastAPI entrypoint
│     ├── user_routes.py # Auth, JWT, user info
│     ├── farm_routes.py # Farm, Farmer, Cow, Activity, Production APIs
│     ├── database.py # DB connection to Django (SQLite)
│     ├── models.py # Shared DB models
│
│── requirements.txt # Dependencies
│── venv/ # Virtual environment
└── README.md # Project documentation
```

---

## 🚀 Setup Instructions

### Step 1: Create the main project folder
```bash
mkdir FarmHub
cd FarmHub
```
### Step 2: Clone your repository inside it
```bash
git clone https://github.com/shahoraiar/FarmHub.git
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




