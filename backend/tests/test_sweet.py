# tests/test_sweets.py
import sys
import os
# Add the parent directory (backend/) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



import pytest
# Imports from app.py and JWT-Extended:
from app import create_app, db, Sweet, User_Details 
from flask_jwt_extended import create_access_token 
from flask import jsonify # Ensure this is imported if used in fixtures

# --- FIXTURES (COPIED FROM conftest.py) ---

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

        sweet = Sweet(name='Chocolate Bar', category='Candy', price=2.50, quantity=100)
        db.session.add(sweet)

        db.session.commit()
    
    yield app 

@pytest.fixture(scope='function')
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

# --- THE ACTUAL TEST (RED PHASE) ---

def test_restock_requires_admin_role_403(client, auth_tokens):
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