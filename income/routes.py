from flask import request, jsonify, g
from utils.auth import login_required
from income.service import IncomeService
from income import income_bp
from datetime import date

income_service = IncomeService()

@income_bp.route('', methods=['GET'])
@login_required
def get_incomes():
    user_id = g.user['user_id']
    
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    
    incomes, total_expected, total_received = income_service.get_incomes(user_id, month, year)
    
    return jsonify({
        'status': 'success',
        'incomes': incomes,
        'total_expected': total_expected,
        'total_received': total_received
    })

@income_bp.route('/<int:income_id>', methods=['GET'])
@login_required
def get_income(income_id):
    user_id = g.user['user_id']
    
    income = income_service.get_income_by_id(user_id, income_id)
    
    if not income:
        return jsonify({
            'status': 'error',
            'message': 'Income not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'income': income
    })

@income_bp.route('', methods=['POST'])
@login_required
def create_income():
    user_id = g.user['user_id']
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request data'
        }), 400
    
    required_fields = ['source_name', 'expected_amount', 'month', 'year']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Convert request data to DTO
    class CreateIncomeRequest:
        def __init__(self, source_name, expected_amount, month, year, due_date=None, description=None):
            self.source_name = source_name
            self.expected_amount = expected_amount
            self.month = month
            self.year = year
            self.due_date = due_date
            self.description = description
    
    create_request = CreateIncomeRequest(
        source_name=data['source_name'],
        expected_amount=data['expected_amount'],
        month=data['month'],
        year=data['year'],
        due_date=data.get('due_date'),
        description=data.get('description', '')
    )
    
    try:
        new_income = income_service.create_income(user_id, create_request)
        
        return jsonify({
            'status': 'success',
            'income': new_income
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@income_bp.route('/<int:income_id>', methods=['PUT'])
@login_required
def update_income(income_id):
    user_id = g.user['user_id']
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request data'
        }), 400
    
    # Convert request data to DTO
    class UpdateIncomeRequest:
        def __init__(self, **kwargs):
            self.source_name = kwargs.get('source_name')
            self.expected_amount = kwargs.get('expected_amount')
            self.actual_amount = kwargs.get('actual_amount')
            self.is_received = kwargs.get('is_received')
            self.due_date = kwargs.get('due_date')
            self.receive_date = kwargs.get('receive_date')
            self.month = kwargs.get('month')
            self.year = kwargs.get('year')
            self.description = kwargs.get('description')
    
    update_request = UpdateIncomeRequest(**data)
    
    try:
        updated_income = income_service.update_income(user_id, income_id, update_request)
        
        if not updated_income:
            return jsonify({
                'status': 'error',
                'message': 'Income not found or does not belong to user'
            }), 404
        
        return jsonify({
            'status': 'success',
            'income': updated_income
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@income_bp.route('/<int:income_id>', methods=['DELETE'])
@login_required
def delete_income(income_id):
    user_id = g.user['user_id']
    
    try:
        success = income_service.delete_income(user_id, income_id)
        
        if not success:
            return jsonify({
                'status': 'error',
                'message': 'Income not found or does not belong to user'
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Income deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@income_bp.route('/<int:income_id>/receive', methods=['PATCH'])
@login_required
def receive_income(income_id):
    user_id = g.user['user_id']
    
    data = request.get_json()
    
    if not data or 'actual_amount' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Actual amount is required'
        }), 400
    
    # Convert request data to DTO
    class ReceiveIncomeRequest:
        def __init__(self, actual_amount, receive_date=None):
            self.actual_amount = actual_amount
            self.receive_date = receive_date or date.today().isoformat()
    
    receive_request = ReceiveIncomeRequest(
        actual_amount=data['actual_amount'],
        receive_date=data.get('receive_date')
    )
    
    try:
        updated_income = income_service.receive_income(user_id, income_id, receive_request)
        
        if not updated_income:
            return jsonify({
                'status': 'error',
                'message': 'Income not found or does not belong to user'
            }), 404
        
        return jsonify({
            'status': 'success',
            'income': updated_income
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500