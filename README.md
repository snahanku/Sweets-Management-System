*Sweet Shop Inventory API*

A robust RESTful API built with Flask, SQLAlchemy, and Flask-JWT-Extended to manage a sweet shop's inventory, handle sales transactions, and implement role-based access control (Admin/User).

Features

* **Authentication:** User registration and JWT-based login (`/auth/*`).
* **Inventory Management:** CRUD operations for sweets (Admin-only for deletion/restock).
* **Sales & Transactions:** Secure purchase endpoint to decrease stock (`/purchase`).
* **Search & Filtering:** Dynamic searching by name, category, and price range.
* **Security:** Password hashing (using `werkzeug.security`) and Admin role enforcement.

Technology Stack

* **Framework:** Python 3.x, Flask
* **Database:** SQLAlchemy (SQLite for development/testing)
* **Authentication:** Flask-JWT-Extended
* **Security:** `werkzeug.security`

***Setup and Installation***
* **Framework:** Python 3.x, Flask
* **Database:** SQLAlchemy (SQLite for development/testing)
* **Authentication:** Flask-JWT-Extended
* **Security:** `werkzeug.security`


*** Steps to clone  and run locally :- ****
create a folder 
git clone [https://github.com/snahanku/Sweets-Management-System.git](https://github.com/snahanku/Sweets-Management-System.git)
cd backend
