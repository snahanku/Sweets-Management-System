# 🍬 Sweet Shop Inventory API

A robust, secure, and scalable **RESTful API** built using **Flask**, **SQLAlchemy**, and **Flask-JWT-Extended** to manage a sweet shop’s inventory, handle sales transactions, and enforce **role-based access control (Admin/User)**.

---

## ✨ Features

* 🔐 **Authentication**
  User registration and JWT-based login (`/auth/*`).

* 📦 **Inventory Management**
  Full CRUD operations for sweets. Admin-only actions include deletion and restocking.

* 🛒 **Sales & Transactions**
  Secure purchase endpoint that deducts stock atomically.

* 🔍 **Search & Filtering**
  Dynamic search by **name**, **category**, and **price range**.

* 🛡️ **Security**
  Password hashing using `werkzeug.security` and strict admin-role enforcement.

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

### 2️⃣ Set Up Virtual Environment

```bash
python3 -m venv venv
```

#### Activate the Environment

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

### Set Flask App

```bash
export FLASK_APP=app.py   # macOS / Linux
set FLASK_APP=app.py      # Windows
```

### Initialize Database

```bash
flask shell
```

### Start the Server

```bash
flask run
```

The server will start at:

```
http://127.0.0.1:5000/
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📚 API Endpoints Reference

| Endpoint                    | Method | Role Required | Description                                      |
| --------------------------- | ------ | ------------- | ------------------------------------------------ |
| `/auth/register`            | POST   | Public        | Registers a new user (username, password).       |
| `/auth/login`               | POST   | Public        | Authenticates user and returns JWT access token. |
| `/api/add-sweets`           | POST   | User / Admin  | Adds a new sweet to the inventory.               |
| `/api/get_all_sweets`       | GET    | User / Admin  | Retrieves all sweets from inventory.             |
| `/api/sweets/<id>`          | PUT    | User / Admin  | Updates sweet details (name, price, etc.).       |
| `/api/sweets/search`        | GET    | User / Admin  | Search sweets by name, category, min/max price.  |
| `/api/sweets/<id>/purchase` | POST   | User / Admin  | Purchases a sweet and deducts stock.             |
| `/api/sweets/<id>/restock`  | POST   | Admin         | Restocks a sweet item.                           |
| `/api/sweets/<id>/delete`   | DELETE | Admin         | Permanently deletes a sweet from inventory.      |

---

## ✅ Role-Based Access Summary

* **Public** → Register & Login
* **User** → View, Search, Purchase, Update sweets
* **Admin** → Full control (Restock & Delete)

---

## 📌 Notes

* SQLite is used for development/testing.
* JWT tokens must be passed via the `Authorization` header as:

  ```
  Authorization: Bearer <token>
  ```

---

💡 *This API is designed to be easily extendable for production-grade databases, caching, and deployment pipelines.*












 
