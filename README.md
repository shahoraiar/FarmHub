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

### Step 1: Clone your repository inside it
```bash
git clone https://github.com/shahoraiar/FarmHub.git
```
### Step 2: Go inside the repo
```bash
cd FarmHub
```
### 4. Create virtual environment
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
## 🚀 Run the Project

## Run Django 
```txt
Example: if your terminal looks like this: 
(venv) I:\FarmHub>
```
👉 First go inside the core folder:
```bash
cd core
```
👉 Then run the Django server:
```bash
python manage.py runserver
```

## Run FastAPI (Reporting Service)
⚡ Important: You must open another terminal window/tab and also activate the virtual environment there.
```txt
Example: in the second terminal, if you are here:
(venv) I:\FarmHub>
```
👉 Run the FastAPI server:
```bash
uvicorn reporting.main:app --port 5000 --reload
```



