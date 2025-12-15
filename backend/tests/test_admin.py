

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pytest
import json
from app import db, User_Details, Sweet, app as flask_app_instance # Import model and db
import uuid
@pytest.fixture(scope="session")
def app():
    #
    ##Defines the 'app' fixture required by pytest-flask. 
    ##It sets up and tears down the database tables once per test session.
    
    with flask_app_instance.app_context():
        # Setup: Create all database tables at the start of the session
        db.create_all()
    
    yield flask_app_instance
    
    with flask_app_instance.app_context():
        # Teardown: Drop all tables at the end of the session
        db.drop_all()


@pytest.fixture(autouse=True)
def setup_teardown_db(app):
    #Ensures a clean database state for every single test function 
    # by rolling back changes automatically.
    
    with app.app_context():
    
        db.session.begin_nested()
        
        yield # Run the test
        
        # Rollback all changes made during the test
        db.session.rollback()
        db.session.remove()



@pytest.fixture(scope="function")
def admin_user(app):
    """Creates a dedicated admin user in the database."""
    #Create  unique admin user name using uuid
    unique_username = f"admin_{uuid.uuid4().hex}"
    admin = User_Details(username=unique_username, role="admin") #assigning unique admin user name
    admin.set_password("123") 
    
    db.session.add(admin)
    db.session.commit()
    
    yield admin




@pytest.fixture 
def admin_token(client, admin_user):
    # Logs in the admin user and returns a fresh JWT token.
    login_data = {
        "username": admin_user.username,
        "password": "123"
    }
    
    response = client.post(
        '/auth/login', 
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    #Check for successful login and extract the  admin token
    assert response.status_code == 200
    data = response.get_json()
    return data['access_token']



@pytest.fixture
def initial_sweet_id(app):
    # Fixture to add an initial sweet to the database and return its ID, and clean up.
    
    sweet = None # Initialize sweet outside try block
    
    try:
       
        #  Create a sample sweet object with a unique name using uuid
        unique_sweet_name = f"choco_chip_{uuid.uuid4().hex[:8]}" 

        sweet = Sweet(
            name=unique_sweet_name, # Use the unique name here
            category="Cookie", 
            price=2.50, 
            quantity=100
        )
        
        
        #  Add and commit 
        db.session.add(sweet)
        db.session.commit()
        db.session.refresh(sweet) 
        
        # 3. Yield the dD  , name for use in the tests
        yield sweet.id ,sweet.name
        
    finally:
        pass


@pytest.fixture(scope="function")
def user_details(app):
    # Creates a standard non-admin user in the database with a unique username.
    
    # Generate a unique username  everytime to avoid Integrity error
    unique_username = f"user_{uuid.uuid4().hex[:8]}" 
    
    user = User_Details(username=unique_username, role="user")
    user.set_password("userpass") 
    
    db.session.add(user)
    db.session.commit()
    
    yield user


@pytest.fixture
def user_token(client, user_details):
    # Loggged in the standard user and returns a fresh JWT token."""
    login_data = {
        "username": user_details.username,
        "password": "userpass"
    }
    
    response = client.post(
        '/auth/login', 
        data=json.dumps(login_data),
        content_type='application/json'
    )
    assert response.status_code == 200 # check for valid  ok http response.
    return response.get_json()['access_token'] ## returning  generated access token 





def test_restock_sweet_for_client(client, admin_token, initial_sweet_id): #Tests restock endpoint with a valid admin token.#
    sweet_id,_ = initial_sweet_id
    restock_data = {"quantity_added": 50}
    response = client.post(
        f'/api/sweets/{sweet_id}/restock',
        # Use the admin_token here
        headers={'Authorization': f'Bearer {admin_token}'}, 
        data=json.dumps(restock_data),
        content_type='application/json'
    )
    #This should pass the role check and return 200
    assert response.status_code == 200



def test_delete_sweet_success(client, admin_token, initial_sweet_id): #Tests if an admin can successfully delete an existing sweet.
    #unpacking the tuple  for sweet id  and sweet name
    sweet_id,_ = initial_sweet_id
    
    #  DELETE request using Admin token
    response = client.delete(
        f'/api/sweets/{sweet_id}/delete',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    assert response.get_json()['message'] == "Data deleted"
    
    #  Verification to  Check if the sweet is truly deleted from the database
    with client.application.app_context():
        deleted_sweet = db.session.get(Sweet, sweet_id)
        assert deleted_sweet is None



def test_search_sweets_by_name(client, user_token, initial_sweet_id): # Tests  related to searching for sweets by name
    """ Method : GET /api/sweets/search:  method in app.py to search sweet by different filters"""
    
    # unpacking the tuple to assign sweet id value  and unique sweet name value
    _, unique_sweet_name = initial_sweet_id
    
    # --Search for the sweet using the dynamically generated name.
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

    #Tests that a standard user is FORBIDDEN from restocking.
    
    # Unpacking the ID from tuple .
    sweet_id, _ = initial_sweet_id
    restock_data = {"quantity_added": 50}
    
    response = client.post(
        f'/api/sweets/{sweet_id}/restock',
        # Use the standard user_token here
        headers={'Authorization': f'Bearer {user_token}'}, 
        data=json.dumps(restock_data),
        content_type='application/json'
    )
    
    # assertion should FAIL until the admin check is implemented.
    assert response.status_code == 403