import pytest
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.models import User

# Set up the Flask app for testing


@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Disable CSRF protection for testing
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

# Create a fixture for a fake user


@pytest.fixture
def fake_user():
    # Create a fake user and add them to the database
    password_hash = generate_password_hash('testpassword', method="sha256")
    user = User(username='testuser', password=password_hash)
    db.session.add(user)
    db.session.commit()
    return user

# Helper function to log in a user


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

# Helper function to log out a user


def logout(client):
    return client.get('/logout', follow_redirects=True)

# Test cases


def test_index_route_unauthenticated(client):
    # When not logged in, it should redirect to the login page
    response = client.get('/')
    assert response.status_code == 302
    assert b'login' in response.data


def test_login_route(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_logout_route(client):
    # Log in the fake user first
    login(client, 'testuser', 'testpassword')

    # Then, log them out
    response = logout(client)
    assert response.status_code == 200
    assert b'login' in response.data


def test_protected_route(client):
    response = client.get('/')
    assert response.status_code == 302


def test_index_route_authenticated(client):
    # Log in the fake user
    login(client, 'testuser', 'testpassword')
    response = client.get('/')
    assert response.status_code == 302
