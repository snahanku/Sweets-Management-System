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

<p align="center">
  <img width="1654" height="233" alt="Auth Tests Output" src="https://github.com/user-attachments/assets/ae6cfec2-6e01-4919-b6b3-45992c03bafa" />
</p>

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

<p align="center">
  <img width="1657" height="173" alt="Admin Tests Output" src="https://github.com/user-attachments/assets/783a1c37-7902-411e-9cdb-7f7447ed5933" />
</p>

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

<p align="center">
  <img width="1665" height="197" alt="Sweet Tests Output" src="https://github.com/user-attachments/assets/b93fc944-8665-4e90-9899-2be49f973ba4" />
</p>

---



Run **all test suites together** with:

```bash
pytest
```


