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

<img width="1657" height="167" alt="image" src="https://github.com/user-attachments/assets/af9808e6-12d9-40c1-9e51-260cca262c1f" />


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

<img width="1648" height="126" alt="image" src="https://github.com/user-attachments/assets/06f313e3-bfa5-4d70-a908-ecc592d8440f" />


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

<img width="1662" height="187" alt="image" src="https://github.com/user-attachments/assets/1e2eb3dc-886e-48e7-8b91-32cc68dfb986" />


---

### 🧠 Pro Tip

Run **all test suites together** with:

```bash
pytest
```

This provides a complete health check of the application.

---

## 📌 Final Notes

* SQLite is used for development and testing; the system can be easily migrated to PostgreSQL or MySQL.
* JWT tokens must be sent via the `Authorization` header:

  ```
  Authorization: Bearer <access_token>
  ```

---

🚀 *Built with backend best practices, clean architecture, and test-driven confidence.*

---

## 🤖 My AI Usage

This project was developed primarily through **manual coding and design decisions**, with AI tools used **selectively** as productivity and clarity aids — **not** as automatic code generators.

---

### 🔧 AI Tools Used

* **Google Gemini**
  Used mainly for brainstorming and validating backend design decisions.

* **ChatGPT**
  Used for refining documentation, explanations, and improving overall readability.

---

### 🧩 The "How" — How I Used AI

#### 1️⃣ API Design & Brainstorming (Google Gemini)

During the early stages of development, I used **Gemini** to:

* Brainstorm RESTful API endpoint structures
* Validate naming conventions for:

  * Authentication routes
  * Inventory management routes
  * Search and filtering endpoints
  * Purchase and admin-only actions
* Think through **role-based access control flows** (Public vs User vs Admin)
* Clarify expected request/response behavior for edge cases such as:

  * Insufficient stock
  * Invalid inputs
  * Unauthorized access

---

### 📈 Impact of AI on My Workflow

Using AI tools helped me to:

* Think faster about API structure **before writing code**
* Reduce time spent on documentation formatting
* Improve clarity and confidence in architectural decisions

---

### ⚖️ Ownership & Code Responsibility

* **Core backend logic**:
  Approximately a **60–40 split**, where I implemented the main logic manually, and AI (ChatGPT/Gemini) helped assess edge cases and validate scenarios — saving time without reducing ownership.

* **Flask routes**:
  High-level route ideas and boilerplate were reviewed with Gemini, but **all route implementations were written manually**.

* **SQLAlchemy models**:
  Gemini suggested possible model attributes to ensure all necessary fields were considered, while the final schema design and implementation were done by me.

* **JWT authentication**:
  JWT was manually implemented for registration and login flows. Gemini assisted in reasoning about **where authentication and authorization checks should be enforced**.

---

✅ **Summary**: AI acted as a **design assistant and reviewer**, while the **entire codebase, logic, and testing remain my own work**.
