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
    
    from auth import get_blueprint as get_auth_blueprint
    app.register_blueprint(get_auth_blueprint(), url_prefix='/api/auth')
    
    from category import get_blueprint as get_category_blueprint
    app.register_blueprint(get_category_blueprint(), url_prefix='/api/categories')
    
    from budget import get_blueprint as get_budget_blueprint
    app.register_blueprint(get_budget_blueprint(), url_prefix='/api/budgets')
    
    from income import get_blueprint as get_income_blueprint
    app.register_blueprint(get_income_blueprint(), url_prefix='/api/income')
    
    from expense import get_blueprint as get_expense_blueprint
    app.register_blueprint(get_expense_blueprint(), url_prefix='/api/expenses')
    
    from dashboard import get_blueprint as get_dashboard_blueprint
    app.register_blueprint(get_dashboard_blueprint(), url_prefix='/api/dashboard')
    
    print("RUN")
    
    @app.route('/api/health', methods=['GET'])
    def healthcheck():
        app.logger.info("Health check endpoint accessed")
        return jsonify({'status': 'ok'}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)