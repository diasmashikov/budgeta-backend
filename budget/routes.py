from flask import request, jsonify, g
from utils.auth import login_required
from budget.service import BudgetService
from budget.dto import CreateBudgetRequest, UpdateBudgetRequest, BudgetSingleResponse, BudgetListResponse
from budget import budget_bp

budget_service = BudgetService()

@budget_bp.route('', methods=['GET'])
@login_required
def get_budgets():
    user_id = g.user['user_id']
    
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    
    budgets, total_budget, total_spent = budget_service.get_budgets(user_id, month, year)
    
    response = BudgetListResponse(
        status="success",
        budgets=budgets,
        total_budget=total_budget,
        total_spent=total_spent,
        total_remaining=total_budget - total_spent
    )
    
    return jsonify(response.__dict__)

@budget_bp.route('/<int:budget_id>', methods=['GET'])
@login_required
def get_budget(budget_id):
    user_id = g.user['user_id']
    
    budget = budget_service.get_budget_by_id(user_id, budget_id)
    
    if not budget:
        return jsonify({
            'status': 'error',
            'message': 'Budget not found'
        }), 404
    
    response = BudgetSingleResponse(
        status="success",
        budget=budget
    )
    
    return jsonify(response.__dict__)

@budget_bp.route('', methods=['POST'])
@login_required
def create_budget():
    user_id = g.user['user_id']
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request data'
        }), 400
    
    required_fields = ['category_id', 'amount', 'month', 'year']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    budget_request = CreateBudgetRequest(
        category_id=data['category_id'],
        amount=data['amount'],
        month=data['month'],
        year=data['year']
    )
    
    try:
        new_budget = budget_service.create_budget(user_id, budget_request)
        
        response = BudgetSingleResponse(
            status="success",
            budget=new_budget
        )
        
        return jsonify(response.__dict__), 201
        
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

@budget_bp.route('/<int:budget_id>', methods=['PUT'])
@login_required
def update_budget(budget_id):
    user_id = g.user['user_id']
    
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request data: amount is required'
        }), 400
    
    update_request = UpdateBudgetRequest(amount=data['amount'])
    
    try:
        updated_budget = budget_service.update_budget(user_id, budget_id, update_request)
        
        if not updated_budget:
            return jsonify({
                'status': 'error',
                'message': 'Budget not found or does not belong to user'
            }), 404
        
        response = BudgetSingleResponse(
            status="success",
            budget=updated_budget
        )
        
        return jsonify(response.__dict__)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@budget_bp.route('/<int:budget_id>', methods=['DELETE'])
@login_required
def delete_budget(budget_id):
    user_id = g.user['user_id']
    
    try:
        success = budget_service.delete_budget(user_id, budget_id)
        
        if not success:
            return jsonify({
                'status': 'error',
                'message': 'Budget not found or does not belong to user'
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Budget allocation deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def update_savings(user_id, month, year):
    return budget_service.update_savings(user_id, month, year)