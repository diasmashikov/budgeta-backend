from flask import request, jsonify, g
from http import HTTPStatus
from utils.auth import login_required
from dashboard.service import DashboardService
from dashboard import dashboard_bp
from datetime import date

dashboard_service = DashboardService()

@dashboard_bp.route('', methods=['GET'])
@login_required
def get_dashboard():
    user_id = g.user['user_id']
    
    # Get query parameters with defaults for current month/year
    current_date = date.today()
    month = request.args.get('month', type=int, default=current_date.month)
    year = request.args.get('year', type=int, default=current_date.year)
    
    try:
        dashboard_data = dashboard_service.get_dashboard_overview(user_id, month, year)
        
        return jsonify({
            'status': 'success',
            **dashboard_data
        }), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An error occurred while generating the dashboard: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR