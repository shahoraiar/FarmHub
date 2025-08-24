# 🌾 FarmHub

FarmHub is a Django-based farm management system with role-based access and integrated livestock & production management.

The system uses Django Admin for backend control and DRF APIs for frontend/mobile integration.

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
```
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
| Role           | Can Create                | Can View            | Can Update/Delete | Notes                   |
| -------------- | ------------------------- | ------------------- | ----------------- | ----------------------- |
| **SuperUser**  | SuperAdmin, Agent, Farmer | All                 | All               | Root admin              |
| **SuperAdmin** | Agent, Farmer             | Own + Agents + Farmer | Own + Agents      | Cannot create SuperUser |
| **Agent**      | Farmer                         | Own Farmers & Farms | ❌                 | Only read access        |
| **Farmer**     | ❌                         | Own data            | ❌                 | Only read access        |

---
## User Registration API
| URL              | Method | Description         | Who Can Create                                                                    |
| ---------------- | ------ | ------------------- | --------------------------------------------------------------------------------- |
| `/registration/` | POST   | Register a new user | SuperUser → SuperAdmin <br> SuperAdmin → Agent <br> Farmers created via Farms app |


## 🌱 Farms & Farmers

### Farmer (Role User)
> **Note:** To create a Farmer user, you must first create a Farm.  
> A Farmer must be assigned to a Farm, and a Farm can have many Farmers.
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
### 📌 Step-by-step Flow

1. SuperUser (Django system user) is created with:
```
python manage.py createsuperuser
```
→ Enter credentials (username, email, password).  
→ Login to /dashboard (Django Admin).

2. From the Admin UI, the SuperUser can create a SuperAdmin user.
3. SuperAdmin logs in and can create Agents.
4. Agents log in and create Farms.
5. Agents/SuperAdmins create Farmers inside Farms (each Farmer must belong to a Farm).
6. Farmers only access their own farm data.

### 📌 Creating a SuperAdmin via API
If you use the API, you don’t need to log in first.
You can directly call:
POST
http://127.0.0.1:8000/api/v1/registration/
```
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "yourpassword",
  "user_role": "SuperUser"
}
```
This will create a SuperAdmin account directly via API.

✅ Clear difference:

- Django Admin UI → create via createsuperuser + Dashboard login.
- API → send JSON to /registration/, no login needed first.
  
---

Create Agent
POST /registration/ (with JWT of SuperAdmin)
```text
{
  "username": "agent1",
  "password": "1234",
  "user_role": "Agent"
}
```
Create Farm
POST /farms/create/ (with JWT of Agent/SuperAdmin)
```text
{
  "name": "Green Farm",
  "location": "Village X"
}
````
Create Farmer
POST /farms/farmer/create/ (with JWT of Agent/SuperAdmin)
```text
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "farmer_john",
  "email": "john@example.com",
  "password": "1234",
  "phone": "1234567890",
  "address": "Village Road",
  "farm": 1
}
```
Note:  
After successful creation, this user is automatically added to the Farmer Role group.  

🐄 Livestock Management
Cow
| URL            | Method | Description  | Permission                                             |
| -------------- | ------ | ------------ | ------------------------------------------------------ |
| `/cow/create/` | POST   | Create a cow | Farmer                                                 |
| `/cow/list/`   | GET    | List cows    | SuperAdmin, Agent (under hierarchy), Farmer (own cows) |

Cow Activity
| URL                     | Method | Description           | Permission                |
| ----------------------- | ------ | --------------------- | ------------------------- |
| `/cow/activity/create/` | POST   | Create a cow activity | Farmer                    |
| `/cow/activity/list/`   | GET    | List cow activities   | SuperAdmin, Agent, Farmer |

## Validation rules:  
- Farmer can only add cows/activities for own farm  
-- Cow must belong to the selected farm  

## Admin UI:
- SuperAdmin → see all agents’ farmers’ cows
- Agent → see their farmers’ cows
- Farmer → see own cows
- 
🥛 Milk Production
| URL                          | Method | Description        | Permission                |
| ---------------------------- | ------ | ------------------ | ------------------------- |
| `/production/cow/milk/`      | POST   | Create milk record | Farmer                    |
| `/production/cow/milk/list/` | GET    | List milk records  | SuperAdmin, Agent, Farmer |

Rules:  
- Farmer can add milk for own cows only
- SuperAdmin can create/update/delete
- Agent → view only, no create/update/delete
- Total yield automatically calculated as morning + evening

Admin UI:  
- SuperAdmin → manage all cows/milk
- Agent → view under hierarchy
- Farmer → create & edit their own milk records
  
🛠️ Permissions Summary

| Role           | Cow                | CowActivity        | MilkProduction     | Farms                | Farmers                             |
| -------------- | ------------------ | ------------------ | ------------------ | -------------------- | ----------------------------------- |
| **SuperAdmin** | View all           | View all           | View all           | Create/Read/Update   | Create/Read/Update Agents & Farmers |
| **Agent**      | View hierarchy     | View hierarchy     | View hierarchy     | Create/Read/Update   | Create/Read/Update                  |
| **Farmer**     | Create/Read/Update | Create/Read/Update | Create/Read/Update | Read-only (assigned) | Read-only (self)                    |

🔗 Example API Workflows
Create Cow (Farmer)  
POST /cow/create/  
```text
{
  "cow_tag": "C-101",
  "name": "Daisy",
  "breed": "Holstein",
  "gender": "Female",
  "farm": 1,
  "farmer": 1,
  "weight_kg": 120,
  "source": "born"
}
```
Create Cow Activity (Farmer)  
POST /cow/activity/create/  
```text
{
  "cow": 1,
  "activity_type": "Vaccination",
  "title": "FMD Vaccine",
  "date": "2025-08-25",
  "priority": "High",
  "is_completed": false
}
```
Create Milk Record (Farmer)  
POST /production/cow/milk/  
```text
{
  "cow": 1,
  "morning_yield_liters": 10,
  "evening_yield_liters": 8,
  "date": "2025-08-25"
}
```  
- List Farms – GET /farms/list/
- List Farmers – GET /farms/farmer/list/
- List Cows – GET /cow/list/
- List Cow Activities – GET /cow/activity/list/
- List Milk Production – GET /production/cow/milk/list/

--- 

🌾 FarmHub Reporting API **(FastAPI)**

FarmHub Reporting API is a FastAPI-based reporting service for livestock and farm management.  
It works alongside the Django FarmHub system and provides reporting endpoints for farms, cows, cow activities, and milk production.  

🔑 Authentication   
FarmHub Reporting API uses JWT tokens for authentication.

1. Login to get Token
Endpoint: /auth/token  
Method: POST  
Payload:  
```
{
  "username": "super1",
  "password": "12345678"
}
```

Response:
```
{
  "access": "<JWT_ACCESS_TOKEN>",
  "refresh": "<JWT_REFRESH_TOKEN>"
}
```

access: Use this token in the Authorization header for API requests.

👤 User Endpoints

| Endpoint    | Method | Description           | Notes                                     |
| ----------- | ------ | --------------------- | ----------------------------------------- |
| `/users/me` | GET    | Get current user info | Must pass `Authorization: Bearer <token>` |

🌱 Farm Endpoints
| Endpoint | Method | Description | Permissions                                                  |
| -------- | ------ | ----------- | ------------------------------------------------------------ |
| `/farms` | GET    | List farms  | SuperAdmin: all, Agent: own hierarchy, Farmer: assigned farm |

🐄 Cow Endpoints
| Endpoint                | Method | Description                              | Permissions                                         |
| ----------------------- | ------ | ---------------------------------------- | --------------------------------------------------- |
| `/cow/details`          | GET    | List cows                                | SuperAdmin: all, Agent: hierarchy, Farmer: own cows |
| `/cow/activity/summary` | GET    | Cow activity report (treatments & costs) | Same as above                                       |

🥛 Milk Production Endpoints
| Endpoint                   | Method | Description                              | Permissions                                         |
| -------------------------- | ------ | ---------------------------------------- | --------------------------------------------------- |
| `/production/milk/summary` | GET    | Milk production report (per cow & month) | SuperAdmin: all, Agent: hierarchy, Farmer: own cows |

⚙️ Roles & Permissions
| Role           | Farms              | Cows               | Cow Activities     | Milk Production    |
| -------------- | ------------------ | ------------------ | ------------------ | ------------------ |
| **SuperAdmin** | View all           | View all           | View all           | View all           |
| **Agent**      | View own hierarchy | View own hierarchy | View own hierarchy | View own hierarchy |
| **Farmer**     | Assigned farm only | Own cows           | Own cows           | Own cows           |

- **Farmer** can only see data related to their own farm and cows.  
- **Agent** can see all farmers under them.   
- **SuperAdmin** sees all data.
  
## 🧩 Notes
- JWT expires after 3 hours by default. Refresh token expires in 1 day.
- All reporting endpoints use FastAPI Dependency Injection to get the current user from token.
- Monthly milk summary uses SQL extract(year, month) for aggregation.
- Cow activity and milk reports return totals per cow and grand totals.

---

```
Developer
❤️ Shahoraiar Hossain
```

