from .import user_register, admin_login, user_login
from app import app
import unittest
import json
from app.models.migration import Migration


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.migration = Migration()
        self.app = app.test_client()
        
    def return_admin_token(self):
    #     """admin token."""
    #     self.app.post('/api/v1/users/register', content_type="application/json", json=admin_register)
        response = self.app.post('/api/v1/users/login', json=admin_login)
        return json.loads(response.data)['access_token']

    def return_user_token(self):
        """user token."""
        self.app.post('/api/v1/users/register', json=user_register)
        response = self.app.post('/api/v1/users/login', json=user_login)
        return json.loads(response.data)['access_token']
        
