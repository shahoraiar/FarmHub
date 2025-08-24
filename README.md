# 🌾 FarmHub

FarmHub is a farm management platform built with **Django** and **FastAPI**. 

This project combines **Django (Admin & APIs)** and **FastAPI (Reporting APIs)** with **role-based permissions**.

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
---

## 🔑 Authentication & Tokens
| URL | Method | Description | Permission |
|-----|--------|-------------|-------------|
| `/dashboard/login/` | GET | Redirects to **Django Admin Login** | Public |
| `/dashboard/` | GET | Django Admin Dashboard | Logged-in users (role-based) |
| `/` | GET | Default login page (Django’s default `LoginView`) | Public |
| `/token/` | POST | Get JWT token (username & password) | Public |
| `/token/refresh/` | POST | Refresh JWT token | Authenticated users |

---

## 👥 User Registration & Roles
| URL | Method | Description | Who Can Do It? |
|-----|--------|-------------|----------------|
| `/registration/` | POST | Register a new user with a specific role (SuperAdmin, Agent, Farmer) | Conditions below |

### 📝 Role-based Conditions for Registration
- **SuperAdmin** → can only be created by **SuperUser (root admin)**  
- **Agent** → can only be created by a **SuperAdmin**  
- **Farmer** → can be created via **Farm apps** only (not directly)  
- Anonymous users → ❌ cannot create roles (except SuperUser creates SuperAdmin first)  

---

## 🌱 Farms & Farmers

### Farmer (Role User)
| URL | Method | Description | Permission |
|-----|--------|-------------|-------------|
| `/farms/farmer/create/` | POST | Create a **Farmer user** + Farmer profile | SuperAdmin, Agent (with model perms) |
| `/farms/farmer/list/` | GET | List Farmers under your control | SuperAdmin (all via Agents) / Agent (own farmers) |

**Conditions**:
- When creating Farmer, must select a Farm.  
- Farm must belong to the logged-in Agent/SuperAdmin.  
- Created Farmer automatically gets a **User account** + assigned to `Farmer` group.  

---

### Farm
| URL | Method | Description | Permission |
|-----|--------|-------------|-------------|
| `/farms/create/` | POST | Create a Farm | SuperAdmin, Agent (with model perms) |
| `/farms/list/` | GET | List Farms | SuperAdmin (sees farms of own agents), Agent (own farms), Farmer (only their assigned farm) |

**Conditions**:
- **SuperAdmin** → can assign farms to Agents created by them.  
- **Agent** → can only assign farms to themselves.  
- **Farmer** → only sees the farm assigned to them.  

---

## 🛠️ Django Admin Customizations

- **Users (Admin UI)**:
  - SuperUser → full control over all users  
  - SuperAdmin → can only create/manage **Agents** and their Farmers  
  - Agent → can only manage their Farmers  
  - Farmer → ❌ cannot create others  

- **Farmers (Admin UI)**:
  - SuperAdmin → can create Farmers for their Agents  
  - Agent → can create Farmers for themselves  
  - Farmer → ❌ cannot create  

- **Farms (Admin UI)**:
  - SuperAdmin → can create farms for their Agents  
  - Agent → can create farms for themselves  
  - Farmer → can only see their own farm  

---

## ✅ Permissions System

Permissions are enforced by **Django Groups + DRF Custom Permissions**:

| Role | Can Create | Can View | Can Update/Delete |
|------|------------|----------|-------------------|
| **SuperUser** | SuperAdmin, Agent, Farmer | All | All |
| **SuperAdmin** | Agent, Farmer | Own + Agents | Own + Agents |
| **Agent** | Farmer | Own Farmers, Own Farms | Own only |
| **Farmer** | ❌ | Own farm & profile only | ❌ |

---

## 🔗 API + Admin Flow

1. **SuperUser** creates a `SuperAdmin` via `/registration/`  
2. **SuperAdmin** logs in → creates **Agents**  
3. **Agents** log in → create **Farms**  
4. **Agents/SuperAdmins** → create **Farmers** inside farms  
5. **Farmers** → only access their own farm data  

---

## 📌 Example Workflows

### Create SuperAdmin
```bash
POST /registration/
{
  "username": "admin1",
  "password": "1234",
  "user_role": "SuperAdmin"
}
```

