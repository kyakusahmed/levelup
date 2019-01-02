from .import user_register, admin_register, admin_login, user_login
from app.models.migration import Migration
from app import app
import unittest
import json


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.migration = Migration()
        self.app = app.test_client()
        
    def return_admin_token(self):
        """admin token."""
        self.app.post('/api/v1/users/register', content_type="application/json", json=admin_register)
        response = self.app.post('/api/v1/users/login', json=admin_login)
        data = json.loads(response.data)
        return json.loads(response.data)['access_token']

    def return_user_token(self):
        """user token."""
        self.app.post('/api/v1/users/register', json=user_register)
        response = self.app.post('/api/v1/users/login', json=user_login)
        data = json.loads(response.data)
        return json.loads(response.data)['access_token']
        
