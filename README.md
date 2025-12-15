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
* create a folder 
* git clone [https://github.com/snahanku/Sweets-Management-System.git](https://github.com/snahanku/Sweets-Management-System.git)
* cd backend

Set Up the virtual Environment
--> python3 -m venv venv

Activate the virtual environment
source venv/bin/activate  # macOS/Linux
 venv\Scripts\activate   # Windows

Install Dependencies
pip install -r requirements.txt


Running the Application
# Set Flask application to the app.py file
export FLASK_APP=app.py
# Run data base creation  command
flask shell


**Start the Server**
* flask run

***Running Tests***
pytest


***API Endpoints Reference***
Endpoint,Method,Role Required,Description
/auth/register,POST,Public,"Registers a new user (username, password)."
/auth/login,POST,Public,"Logs in a user, returns JWT access token."
/api/add-sweets,POST,User/Admin,Adds a new sweet to the inventory.
/api/get_all_sweets,GET,User/Admin,Lists all sweets in the inventory.
/api/sweets/<id>,PUT,User/Admin,"Updates sweet details (e.g., price, name)."
/api/sweets/search,GET,User/Admin,"Searches by name, category, min_price, max_price."
/api/sweets/<id>/purchase,POST,User/Admin,Processes a sale and deducts stock.
/api/sweets/<id>/restock,POST,Admin,Increases the stock quantity.
/api/sweets/<id>/delete,DELETE,Admin,Permanently deletes a sweet item.











 
