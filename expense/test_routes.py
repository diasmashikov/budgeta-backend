import unittest
from flask import Flask
from expense.routes import expense_bp
from http import HTTPStatus

class TestExpenseRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(expense_bp, url_prefix='/api/expenses')
        self.client = self.app.test_client()
    
    def test_unauthorized_access(self):
        """Test that endpoints require authentication"""
        response = self.client.get('/api/expenses')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

if __name__ == '__main__':
    unittest.main()