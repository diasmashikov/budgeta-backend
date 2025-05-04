import unittest
import json
from flask import Flask
from auth.routes import auth_bp
from http import HTTPStatus

class TestAuthRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(auth_bp, url_prefix='/api/auth')
        self.client = self.app.test_client()
    
    def test_logout_success(self):
        """Test logout endpoint"""
        response = self.client.post('/api/auth/logout')
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Logged out successfully')

if __name__ == '__main__':
    unittest.main()