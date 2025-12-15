

import sys
import os
# Add the parent directory (backend/) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pytest
import json
from app import db, User_Details, Sweet, app as flask_app_instance # Import your model and db
import uuid
@pytest.fixture(scope="session")
def app():
    """
    Defines the 'app' fixture required by pytest-flask. 
    It sets up and tears down the database tables once per test session.
    """
    with flask_app_instance.app_context():
        # Setup: Create all database tables at the start of the session
        db.create_all()
    
    yield flask_app_instance
    
    with flask_app_instance.app_context():
        # Teardown: Drop all tables at the end of the session
        db.drop_all()

@pytest.fixture(autouse=True)
def setup_teardown_db(app):
    """
    Ensures a clean database state for every single test function 
    by rolling back changes automatically.
    """
    with app.app_context():
        # Start a nested transaction
        db.session.begin_nested()
        
        yield # Run the test
        
        # Rollback all changes made during the test
        db.session.rollback()
        db.session.remove()



@pytest.fixture(scope="function")
def admin_user(app):
    """Creates a dedicated admin user in the database."""
    # REMOVE: with app.app_context():
    unique_username = f"admin_{uuid.uuid4().hex}"
    # The code below is now correctly running inside the context 
    # provided by the setup_teardown_db fixture.
    admin = User_Details(username=unique_username, role="admin")
    admin.set_password("123") 
    
    db.session.add(admin)
    db.session.commit()
    
    yield admin




@pytest.fixture 
def admin_token(client, admin_user):
    """Logs in the admin user and returns a fresh JWT token."""
    login_data = {
        "username": admin_user.username,
        "password": "123"
    }
    
    response = client.post(
        '/auth/login', # Path is now correct
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    # Check for successful login and extract the token
    assert response.status_code == 200
    data = response.get_json()
    return data['access_token']


# Assuming you added 'import uuid' at the top of tests/test_admin.py already

@pytest.fixture
def initial_sweet_id(app):
    """Fixture to add an initial sweet to the database and return its ID, and clean up."""
    
    sweet = None # Initialize sweet outside try block
    
    # REMOVED: with app.app_context(): (as per previous fix)
    
    try:
        # --- CHANGE START ---
        # 1. Create a sample sweet object with a unique name
        unique_sweet_name = f"choco_chip_{uuid.uuid4().hex[:8]}" 

        sweet = Sweet(
            name=unique_sweet_name, # Use the unique name here
            category="Cookie", 
            price=2.50, 
            quantity=100
        )
        # --- CHANGE END ---
        
        # 2. Add and commit (necessary to get the ID)
        db.session.add(sweet)
        db.session.commit()
        db.session.refresh(sweet) 
        
        # 3. Yield the ID for use in the tests
        yield sweet.id ,sweet.name
        
    finally:
        # Cleanup logic remains removed (relies on rollback)
        pass


@pytest.fixture(scope="function")
def user_details(app):
    """Creates a standard non-admin user in the database with a unique username."""
    # Note: Runs inside the transactional setup
    
    # Generate a unique username to avoid IntegrityError
    unique_username = f"user_{uuid.uuid4().hex[:8]}" 
    
    user = User_Details(username=unique_username, role="user")
    user.set_password("userpass") 
    
    db.session.add(user)
    db.session.commit()
    
    yield user


@pytest.fixture
def user_token(client, user_details):
    """Logs in the standard user and returns a fresh JWT token."""
    login_data = {
        "username": user_details.username,
        "password": "userpass"
    }
    
    response = client.post(
        '/auth/login', 
        data=json.dumps(login_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    return response.get_json()['access_token']





def test_restock_sweet_for_client(client, admin_token, initial_sweet_id):
    """Tests restock endpoint with a valid admin token."""
    sweet_id,_ = initial_sweet_id
    restock_data = {"quantity_added": 50}
    response = client.post(
        f'/api/sweets/{sweet_id}/restock',
        # Use the admin_token here
        headers={'Authorization': f'Bearer {admin_token}'}, 
        data=json.dumps(restock_data),
        content_type='application/json'
    )
    # This should now pass the role check and return 200
    assert response.status_code == 200



def test_delete_sweet_success(client, admin_token, initial_sweet_id):
    """Tests if an admin can successfully delete an existing sweet."""
    sweet_id,_ = initial_sweet_id
    
    # 1. DELETE request using Admin token
    response = client.delete(
        f'/api/sweets/{sweet_id}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    assert response.get_json()['message'] == "Data deleted"
    
    # 2. Verification: Check if the sweet is truly gone from the database
    with client.application.app_context():
        deleted_sweet = db.session.get(Sweet, sweet_id)
        assert deleted_sweet is None



def test_search_sweets_by_name(client, user_token, initial_sweet_id):
    """GET /api/sweets/search: Tests searching for sweets by name."""
    
    # --- CRITICAL CHANGE: UNPACK THE TUPLE ---
    _, unique_sweet_name = initial_sweet_id
    
    # 1. Search for the sweet using the dynamically generated name
    # Note: I am removing the quotes in the query string as they are usually not
    # needed unless your endpoint implementation requires exact string matching on the name.
    response = client.get(
        f'/api/sweets/search?name={unique_sweet_name}',
        headers={'Authorization': f'Bearer {user_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['sweets']) > 0
    
    # 2. Assertions
    # Note: If your endpoint uses case-insensitive search, your dynamic name is safer.
    assert len(data['sweets']) == 1 # Should find exactly one sweet
    assert data['sweets'][0]['name'] == unique_sweet_name


def test_restock_sweet_by_non_admin(client, user_token, initial_sweet_id):
    """
    RED: Tests that a standard user is FORBIDDEN (403) from restocking.
    """
    # Unpack the ID. The name is not needed here.
    sweet_id, _ = initial_sweet_id
    restock_data = {"quantity_added": 50}
    
    response = client.post(
        f'/api/sweets/{sweet_id}/restock',
        # Use the standard user_token here
        headers={'Authorization': f'Bearer {user_token}'}, 
        data=json.dumps(restock_data),
        content_type='application/json'
    )
    
    # This assertion should FAIL until the admin check is implemented.
    assert response.status_code == 403