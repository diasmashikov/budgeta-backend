from dotenv import load_dotenv
load_dotenv('.flaskenv')
from flask import Flask, jsonify
from flask_cors import CORS
import os
from utils.db import init_app

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    import config
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DATABASE'] = config.DATABASE
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    init_app(app)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    from api.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from api.category import categories_bp
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    
    from budget import get_blueprint
    app.register_blueprint(get_blueprint(), url_prefix='/api/budgets')
    
    from api.income import income_bp
    app.register_blueprint(income_bp, url_prefix='/api/income')
    
    from api.expense import expenses_bp
    app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
    
    from api.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    print("RUN")
    
    @app.route('/api/health', methods=['GET'])
    def healthcheck():
        app.logger.info("Health check endpoint accessed")
        return jsonify({'status': 'ok'}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)