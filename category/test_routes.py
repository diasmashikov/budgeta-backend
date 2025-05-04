import unittest
from flask import Flask
from category.routes import category_bp
from http import HTTPStatus

class TestCategoryRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(category_bp, url_prefix='/api/categories')
        self.client = self.app.test_client()
    
    def test_unauthorized_access(self):
        """Test that endpoints require authentication"""
        response = self.client.get('/api/categories')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

if __name__ == '__main__':
    unittest.main()