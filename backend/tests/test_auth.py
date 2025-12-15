
import sys
import os
# Add the parent directory (backend/) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import json
# You must import your application's components (create_app, db, User_Details)
from app import create_app, db, User_Details 
# NOTE: Make sure the import path 'backend.app' is correct for your structure.

# --- 1. The 'app' Fixture (REQUIRED for 'client') ---
@pytest.fixture()
def app():
    # Use an in-memory database for testing
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False, 
    })

    with app.app_context():
        # Create all tables before the tests run
        db.create_all()
        yield app
        # Drop all tables after the tests finish
        db.drop_all()

# --- 2. The 'client' Fixture (REQUIRED by your test function) ---
# This fixture uses the 'app' fixture automatically.
@pytest.fixture()
def client(app):
    return app.test_client()

# --- 3. The 'user_data' Fixture (REQUIRED by your test function) ---
@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "Password123"
    }


def test_register_user_success(client, user_data):
    """Tests successful user registration."""
    response = client.post(
        '/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'user registered successfully' in data['message']
    assert data['user-details']['user-name'] == 'testuser'


def test_register_duplicate_user_exist(client, user_data):
    """Tests that registering the same user twice fails."""
    # First registration (Success)
    client.post(
        '/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )

    # Second registration (Should fail)
    response = client.post(
        '/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    assert response.status_code == 200 # Note: Your current code returns 200 with an error message
    data = response.get_json()
    assert 'user already exisit' in data['message'] # Use the exact message from your code
    

def test_register_missing_fields_fails(client):
    
    response = client.post(
        '/auth/register',
        data=json.dumps({"username": "missingpass"}),
        content_type='application/json'
    )
    assert response.status_code == 200 # Your code currently returns 200 for this failure
    data = response.get_json()
    assert "Username and password are required" in data['message']




def test_login_success(client, user_data):
    """Tests successful user login after registration."""
    # 1. Register the user first
    client.post('/auth/register', data=json.dumps(user_data), content_type='application/json')
    
    # 2. Attempt login
    response = client.post(
        '/auth/login',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'Login successful' in data['message']
    assert 'access_token' in data


def test_login_invalid_password(client, user_data):
    """Tests login fails with invalid password."""
    # 1. Register the user first
    client.post('/auth/register', data=json.dumps(user_data), content_type='application/json')
    
    # 2. Attempt login with wrong password
    invalid_data = user_data.copy()
    invalid_data['password'] = 'wrongpassword'

    response = client.post(
        '/auth/login',
        data=json.dumps(invalid_data),
        content_type='application/json'
    )
    assert response.status_code == 401
    assert 'Invalid credentials' in response.get_json()['message']


def test_login_user_not_found(client, user_data):
    """Tests login fails if the user does not exist."""
    # Do not register the user
    response = client.post(
        '/auth/login',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    # The login logic attempts to fetch the user. Since the user doesn't exist, 
    # the check_password part is skipped, leading to the 401.
    assert response.status_code == 401
    assert 'Invalid credentials' in response.get_json()['message']