import json
from .base_test import BaseTest


class UserTest(BaseTest):


    def test_user_register(self):
        """Test successful register"""
        regiseter_user = {
            "first_name":"ahmed",
            "last_name":"kyakus",
            "email": "kyakusahmed@out.com",
            "password": "1988ch",
            "isAdmin": False
        }
        response = self.app.post('/api/v1/users/register', json=regiseter_user)
        self.assertEqual(response.status_code, 201)
        assert json.loads(response.data)['data'] == "user registered successfully"

    def test_missing_fields(self):
        """Test register without data"""
        regiseter_user = {
            "first_name":"",
            "last_name":"kyakus",
            "email": "kyakusahmed@outlook.com",
            "password": "1988ch",
            "isAdmin": False
        }
        response = self.app.post('/api/v1/users/register', json=regiseter_user)
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['error']['message'] == 'first_name is required'

    def test_user_register_email_exist(self):
        """Test user email exists."""
        register_user = {
            "first_name":"avdb",
            "last_name":"kyakus",
            "email": "kyakusahmed@outlook.com",
            "password": "1988ch",
            "isAdmin": False
        }
        self.app.post('/api/v1/users/register', json=register_user)
        response = self.app.post('/api/v1/users/register', json=register_user)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "user registered already"

    def test_successful_user_login(self):
        """Test successful login."""
        register_user = {
            "first_name":"avdb",
            "last_name":"kyakus",
            "email": "kyakusahmed@outlook.com",
            "password": "1988ch",
            "isAdmin": False
        }
        self.app.post('/api/v1/users/register', json=register_user)
        response = self.app.post('/api/v1/users/login', json=register_user)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "Login successful"

    def test_user_not_registered(self):
        """Test missing login email and password."""
        register_user = {
            "email": "kyaku@outlook.com",
            "password": "1988fh"
        }
        response = self.app.post('/api/v1/users/login', json=register_user)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "register first"

    def test_invalid_email(self):
        register_user = {
            "email": "kyaku@outlook.",
            "password": "1988fh"
        }
        response = self.app.post('/api/v1/users/login', json=register_user)
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['error']['message'] == "invalid email"

    
    def test_password_too_short(self):
        register_user = {
            "first_name":"avdb",
            "last_name":"kyakus",
            "email": "kyaku@outlook.com",
            "password": "18fh",
            "isAdmin": False
        }
        response = self.app.post('/api/v1/users/register', json=register_user)
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['error'] == "password should be atleast five characters"


