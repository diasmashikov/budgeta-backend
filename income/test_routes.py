import unittest
from flask import Flask
from income.routes import income_bp
from http import HTTPStatus

class TestIncomeRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(income_bp, url_prefix='/api/income')
        self.client = self.app.test_client()
    
    def test_unauthorized_access(self):
        """Test that endpoints require authentication"""
        response = self.client.get('/api/income')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

if __name__ == '__main__':
    unittest.main()