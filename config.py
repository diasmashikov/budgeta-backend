import os


SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
DATABASE = os.path.join('instance', 'budget_tracker.db')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_secret')
JWT_ACCESS_TOKEN_EXPIRES = 3600  