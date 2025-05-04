import unittest
from flask import Flask
from budget.routes import budget_bp
from http import HTTPStatus

class TestBudgetRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(budget_bp, url_prefix='/api/budgets')
        self.client = self.app.test_client()
    
    def test_unauthorized_access(self):
        """Test that endpoints require authentication"""
        response = self.client.get('/api/budgets')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

if __name__ == '__main__':
    unittest.main()