# 🍬 Sweet Shop Inventory API

A **clean, secure, and production-ready RESTful API** built with **Flask**, **SQLAlchemy**, and **Flask-JWT-Extended** to manage a sweet shop’s inventory, handle sales transactions, and enforce **role-based access control (Admin/User)**.

This project is designed with **scalability, security, and testability** in mind, making it suitable for real-world backend systems, assignments, and interviews.

---

## ✨ Key Features

### 🔐 Authentication & Authorization

* User registration and login using **JWT tokens** (`/auth/*`).
* Role-based access control with **Admin** and **User** permissions.

### 📦 Inventory Management

* Full CRUD operations for sweet items.
* Admin-only privileges for **restocking** and **deleting** items.

### 🛒 Sales & Transactions

* Secure purchase endpoint that **atomically deducts stock**.
* Prevents over-selling and invalid purchases.

### 🔍 Advanced Search & Filtering

* Search sweets dynamically by:

  * Name
  * Category
  * Minimum & Maximum price

### 🛡️ Security Best Practices

* Password hashing using `werkzeug.security`.
* JWT-protected endpoints.
* Strict enforcement of admin-only routes.

---

## 🛠️ Technology Stack

| Layer          | Technology                                  |
| -------------- | ------------------------------------------- |
| Language       | Python 3.x                                  |
| Framework      | Flask                                       |
| Database       | SQLAlchemy (SQLite for development/testing) |
| Authentication | Flask-JWT-Extended                          |
| Security       | werkzeug.security                           |
| Testing        | Pytest                                      |

---

## 🚀 Setup & Installation

### 1️⃣ Clone the Repository

```bash
mkdir sweet-shop
cd sweet-shop
git clone https://github.com/snahanku/Sweets-Management-System.git
cd backend
```

---

### 2️⃣ Create a Virtual Environment

```bash
python3 -m venv venv
```

#### Activate the Virtual Environment

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

### Configure Flask

```bash
# macOS / Linux
export FLASK_APP=app.py

# Windows
set FLASK_APP=app.py
```

### Initialize the Database

```bash
flask shell
```

### Start the Development Server

```bash
flask run
```

The API will be available at:

```
http://127.0.0.1:5000/
```

---

## 📚 API Endpoints Reference

| Endpoint                    | Method | Role Required | Description                                |
| --------------------------- | ------ | ------------- | ------------------------------------------ |
| `/auth/register`            | POST   | Public        | Register a new user (username & password). |
| `/auth/login`               | POST   | Public        | Login and receive a JWT access token.      |
| `/api/add-sweets`           | POST   | User / Admin  | Add a new sweet to the inventory.          |
| `/api/get_all_sweets`       | GET    | User / Admin  | Fetch all sweets from inventory.           |
| `/api/sweets/<id>`          | PUT    | User / Admin  | Update sweet details (name, price, etc.).  |
| `/api/sweets/search`        | GET    | User / Admin  | Search by name, category, and price range. |
| `/api/sweets/<id>/purchase` | POST   | User / Admin  | Purchase a sweet and deduct stock.         |
| `/api/sweets/<id>/restock`  | POST   | Admin         | Increase stock quantity of a sweet.        |
| `/api/sweets/<id>/delete`   | DELETE | Admin         | Permanently delete a sweet item.           |

---

## ✅ Role-Based Access Control

| Role       | Permissions                            |
| ---------- | -------------------------------------- |
| **Public** | Register, Login                        |
| **User**   | View, Search, Purchase, Update sweets  |
| **Admin**  | Full access including Restock & Delete |

---

## 🧪 Testing Strategy

The project includes **well-structured Pytest test suites** to ensure correctness, security, and role-based behavior across all major components.

---

### 🔐 Authentication Tests

Authentication endpoints are tested in:

```
tests/test_auth.py
```

Run:

```bash
pytest tests/test_auth.py
```

✅ Validates user registration, login, and JWT token generation.

<img width="1654" height="167" alt="image" src="https://github.com/user-attachments/assets/82711c5b-646a-4ff9-98f0-fb48aefa4841" />


---

### 🛡️ Admin Endpoint Tests

Admin-only functionality is tested in:

```
tests/test_admin.py
```

Run:

```bash
pytest tests/test_admin.py
```

✅ Ensures restricted endpoints are accessible **only** to admin users.

<img width="1659" height="180" alt="image" src="https://github.com/user-attachments/assets/832c6e7f-e92b-4785-b926-0983bbad5202" />


---

### 🍭 Sweet Inventory Tests

All inventory-related operations are tested in:

```
tests/test_sweet.py
```

Run:

```bash
pytest tests/test_sweet.py
```

✅ Covers add, update, search, purchase, and stock validation workflows.

<img width="1662" height="187" alt="image" src="https://github.com/user-attachments/assets/8f289566-55b3-4834-9120-8e47cb6f9c2c" />


---



Run **all test suites together** with:

```bash
pytest
```

🤖 My AI Usage

This project was developed p through manual coding and design decisions, with AI tools used selectively as productivity and clarity aids, not as code generators.

🔧 AI Tools Used

Google Gemini

ChatGPT (for documentation refinement and explanation)


THE "HOW" 
How I Used AI
1️⃣ API Design & Brainstorming (Google Gemini)

I used  Gemini during the early stages of development to:

Brainstorm RESTful API endpoint structures

Validate naming conventions for routes such as authentication, inventory management, search, purchase, and admin actions

Think through role-based access control flows (Admin vs User vs public)

Clarify expected request/response behavior for edge cases (for example: insufficient stock, invalid inputs)


Impact of AI on My Workflow

Using AI tools helped me:

Think faster about API structure before coding

Reduce time spent on documentation formatting

Improve clarity and confidence in design decisions

However:

Core backend logic : Its a 60- 40 ratio where I implemented the logic  and chatgpt , gemeini help to asses it on different edge cases  which saved time in general

Flask routes : Although flask routes are already mentioned  and the primary boiler plate is assesd by gemini then i manually implemented the code.

SQLAlchemy models : Gemini suggested model  attributes in order to keep track of all posible column values

JWT authentication : Applied  for registration and  login purpose . Gemini help to predict where should i implement them







