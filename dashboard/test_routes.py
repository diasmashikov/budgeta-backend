import unittest
from flask import Flask
from dashboard.routes import dashboard_bp
from http import HTTPStatus

class TestDashboardRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
        self.client = self.app.test_client()
    
    def test_unauthorized_access(self):
        """Test that dashboard requires authentication"""
        response = self.client.get('/api/dashboard')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

if __name__ == '__main__':
    unittest.main()