
import sys
import os
# Add the parent directory (backend/) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



import pytest
import json
# Imports from app.py and JWT-Extended:
from app import create_app, db, Sweet, User_Details 
from flask_jwt_extended import create_access_token 
from flask import jsonify # Ensure this is imported if used in fixtures
import random

# --- FIXTURES (COPIED FROM conftest.py) ---


def register_user(client, username, password, is_admin=False):
    """Helper function to register a user and return the response data."""
    data = {"username": username, "password": password, "is_admin": is_admin}
    response = client.post('/auth/register', data=json.dumps(data), content_type='application/json')
    return response.get_json()

def get_auth_token(client, username, password):
    """Helper function to log in and return the JWT token."""
    response = client.post('/auth/login', data=json.dumps({"username": username, "password": password}), content_type='application/json')
    return response.get_json()['access_token']



@pytest.fixture(scope='session')
def user_token(client):
    """Fixture for a standard user's JWT token."""
    # Register and log in a standard user
    register_user(client, "stduser", "password123", is_admin=False)
    return get_auth_token(client, "stduser", "password123")

@pytest.fixture(scope='session')
def admin_token(client):
    """Fixture for an admin user's JWT token."""
    # Register and log in an admin user
    register_user(client, "adminuser", "adminpass", is_admin=True)
    return get_auth_token(client, "adminuser", "adminpass")





@pytest.fixture(scope='session')
def app():
    """Fixture to set up a clean, testable application instance."""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_sweet_shop.db' 
    app.config['TESTING'] = True
    
    with app.app_context():
        # Clean slate: Drop all tables and create new ones
        db.drop_all()
        db.create_all()
        
        # --- Add Initial Test Data ---
        user = User_Details(username='test_user', role='user')
        user.set_password('secure')
        db.session.add(user)

        admin = User_Details(username='admin_user', role='admin')
        admin.set_password('secure_admin')
        db.session.add(admin)

        sweet = Sweet(name='Chocolate Bar', price=2.50,category="chocolate" ,quantity=100)
        db.session.add(sweet)

        db.session.commit()
    
    yield app 

@pytest.fixture(scope='session')
def client(app):
    """Fixture for a test client to make HTTP requests."""
    return app.test_client()

@pytest.fixture(scope='function')
def auth_tokens(app):
    """Fixture to generate valid JWTs for standard user and admin."""
    with app.app_context():
        test_user = User_Details.query.filter_by(username='test_user').first()
        admin_user = User_Details.query.filter_by(username='admin_user').first()
        
        user_token = create_access_token(identity=str(test_user.id))
        admin_token = create_access_token(identity=str(admin_user.id))
        
        return {
            'user': user_token,
            'admin': admin_token
        }
@pytest.fixture
def initial_sweet_id(app):
    """Fixture to add an initial sweet to the database and return its ID, and clean up."""
    
    # We must use a try...finally block to guarantee cleanup runs!
    sweet = None # Initialize sweet outside try block
    
    with app.app_context():
        try:
            # 1. Create a sample sweet object
            sweet = Sweet(
                name="Chocolate Chip", 
                category="Cookie", 
                price=2.50, 
                quantity=100
            )
            
            # 2. Add and commit (necessary to get the ID)
            db.session.add(sweet)
            db.session.commit()
            db.session.refresh(sweet) 
            
            # 3. Yield the ID for use in the tests
            yield sweet.id
            
        finally:
            # VITAL FIX: TEARDOWN LOGIC
            # This ensures the database is clean for the next test.
            if sweet and sweet.id is not None:
                # Retrieve the sweet again to ensure we are deleting a non-stale object
                sweet_to_delete = db.session.get(Sweet, sweet.id)
                if sweet_to_delete:
                    db.session.delete(sweet_to_delete)
                    db.session.commit() # Commit the deletion
            db.session.remove()




# --- THE ACTUAL TEST (RED PHASE) ---

def test_restock_requires_admin_role(client, auth_tokens):
    """
    RED PHASE: Test that a standard user is FORBIDDEN (403) from restocking.
    This test will FAIL until the Admin role check is implemented in app.py.
    """
    # 1. Get the non-admin token
    user_token = auth_tokens['user']
    
    # 2. Make the request using the actual, valid non-admin token
    response = client.post(
        '/api/sweets/1/restock',
        json={'quantity_added': 5},
        headers={'Authorization': f'Bearer {user_token}'} 
    )
    
    # 3. Assertion (EXPECTED FAILURE)
    assert response.status_code == 403 
    assert b"Admin privileges required" in response.data

def test_purchase_sweet(client, user_token, initial_sweet_id):
    """POST /api/sweets/:id/purchase: Tests purchasing a sweet."""
    purchase_data = {"quantity_purchased": 10}
    response = client.post(
        f'/api/sweets/{initial_sweet_id}/purchase',
        headers={'Authorization': f'Bearer {user_token}'},
        data=json.dumps(purchase_data),
        content_type='application/json'


    )

    if response.status_code != 200:
        print("API Error Response:", response.get_json())
        print("API Error Text:", response.data)

    assert response.status_code == 200
    data = response.get_json()
    
    
    # Verify the quantity decreased (Initial was 100, now 90)
    assert 'Successfully purchased' in data['message']
    assert data['details']['quantity'] == 90 


def test_add_sweet_success(client, user_token):
    """POST /api/add-sweets: Tests adding a new sweet."""
    new_sweet = {"name": "Gummy Bear", "category": "Candy", "price": 0.50, "quantity": 500}
    response = client.post(
        '/api/add-sweets',
        headers={'Authorization': f'Bearer {user_token}'},
        data=json.dumps(new_sweet),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['Sweet-details']['name'] == 'Gummy Bear'
    assert data['Sweet-details']['quantity'] == 500



def test_get_all_sweets(client, user_token):
    """GET /api/sweets: Tests retrieving all sweets."""
    response = client.get(
        '/api/get_all_sweets',
        headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 200
    
    # 1. 'data' IS the list now. No need to access 'sweet_list' key.
    data = response.get_json()
    
    # 2. Assert that 'data' itself is a list
    assert isinstance(data, list)
    
    # 3. Assert the length of 'data' itself
    assert len(data) >= 1
    
    # Optional: Verify content of the first item in the list
    if data:
        assert 'name' in data[0]



def test_update_sweet_details(client, user_token, initial_sweet_id):
    """PUT /api/sweets/:id: Tests updating an existing sweet."""
    update_data = {"price": 3.00, "category": "Premium Cookie"}
    response = client.put(
        f'/api/sweets/{initial_sweet_id}',
        headers={'Authorization': f'Bearer {user_token}'},
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['details']['price'] == 3.00
    assert data['details']['category'] == 'Premium Cookie'




def test_unauthenticated_access_fails(client):
    """Tests that protected routes require a token."""
    response = client.get('/api/get_all_sweets')
    assert response.status_code == 401

def test_search_sweets_by_category(client, user_token ,initial_sweet_id):
    """GET /api/sweets/search: Tests searching for sweets."""
    # Search for the "Cookie" category used in the initial_sweet_id fixture
    response = client.get(
        '/api/sweets/search?category=Cookie',
        headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert len(data['sweets']) >= 1 # Should find the cookie
    assert data['sweets'][0]['category'] == 'Cookie'


# In tests/test_sweet.py, add this new test:
# NOTE: Ensure you import Sweet and db from your app

def test_add_sweet_invalid_price_type(client, user_token):
    """
    🔴 RED: Tests that adding a sweet with a non-numeric price fails with 400.
    Expected to fail if the endpoint relies only on Python's automatic JSON parsing 
    without explicit type validation.
    """
    invalid_sweet = {
        "name": "Invalid Gummy", 
        "category": "Candy", 
        "price": "not_a_number", # Intentionally wrong type
        "quantity": 100
    }
    response = client.post(
        '/api/add-sweets',
        headers={'Authorization': f'Bearer {user_token}'},
        data=json.dumps(invalid_sweet),
        content_type='application/json'
    )
    
    # Assert a specific failure status code
    assert response.status_code == 400
    data = response.get_json()
    assert 'Price must be a valid number' in data['message']