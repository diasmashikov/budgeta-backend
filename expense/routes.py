from flask import request, jsonify, g
from utils.auth import login_required
from expense.service import ExpenseService
from expense import expense_bp

expense_service = ExpenseService()

@expense_bp.route('', methods=['GET'])
@login_required
def get_expenses():
    user_id = g.user['user_id']
    
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    category_id = request.args.get('category', type=int)
    
    expenses, total_amount = expense_service.get_expenses(user_id, month, year, category_id)
    
    return jsonify({
        'status': 'success',
        'expenses': expenses,
        'total_amount': total_amount
    })

@expense_bp.route('/<int:expense_id>', methods=['GET'])
@login_required
def get_expense(expense_id):
    user_id = g.user['user_id']
    
    expense = expense_service.get_expense_by_id(user_id, expense_id)
    
    if not expense:
        return jsonify({
            'status': 'error',
            'message': 'Expense not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'expense': expense
    })

@expense_bp.route('', methods=['POST'])
@login_required
def create_expense():
    user_id = g.user['user_id']
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request data'
        }), 400
    
    required_fields = ['category_id', 'amount', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Convert request data to DTO
    class CreateExpenseRequest:
        def __init__(self, category_id, amount, date, description=None):
            self.category_id = category_id
            self.amount = amount
            self.date = date
            self.description = description
    
    create_request = CreateExpenseRequest(
        category_id=data['category_id'],
        amount=data['amount'],
        date=data['date'],
        description=data.get('description')
    )
    
    try:
        new_expense = expense_service.create_expense(user_id, create_request)
        
        return jsonify({
            'status': 'success',
            'expense': new_expense
        }), 201
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@expense_bp.route('/<int:expense_id>', methods=['PUT'])
@login_required
def update_expense(expense_id):
    user_id = g.user['user_id']
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request data'
        }), 400
    
    # Convert request data to DTO
    class UpdateExpenseRequest:
        def __init__(self, **kwargs):
            self.category_id = kwargs.get('category_id')
            self.amount = kwargs.get('amount')
            self.date = kwargs.get('date')
            self.description = kwargs.get('description')
    
    update_request = UpdateExpenseRequest(**data)
    
    try:
        updated_expense = expense_service.update_expense(user_id, expense_id, update_request)
        
        if not updated_expense:
            return jsonify({
                'status': 'error',
                'message': 'Expense not found or does not belong to user'
            }), 404
        
        return jsonify({
            'status': 'success',
            'expense': updated_expense
        })
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@expense_bp.route('/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    user_id = g.user['user_id']
    
    try:
        print(f"Attempting to delete expense {expense_id} for user {user_id}")
        success = expense_service.delete_expense(user_id, expense_id)
        
        if not success:
            return jsonify({
                'status': 'error',
                'message': 'Expense not found or does not belong to user'
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Expense deleted successfully'
        })
        
    except Exception as e:
        print(f"Error deleting expense {expense_id}: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@expense_bp.route('/categories/summary', methods=['GET'])
@login_required
def get_expense_category_summary():
    user_id = g.user['user_id']
    
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    
    if not month or not year:
        return jsonify({
            'status': 'error',
            'message': 'Month and year parameters are required'
        }), 400
    
    expenses_by_category = expense_service.get_monthly_expenses_by_category(user_id, month, year)
    
    return jsonify({
        'status': 'success',
        'month': month,
        'year': year,
        'categories': expenses_by_category
    })

@expense_bp.route('/recent', methods=['GET'])
@login_required
def get_recent_expenses():
    user_id = g.user['user_id']
    
    limit = request.args.get('limit', default=5, type=int)
    
    recent_expenses = expense_service.get_recent_expenses(user_id, limit)
    
    return jsonify({
        'status': 'success',
        'expenses': recent_expenses
    })