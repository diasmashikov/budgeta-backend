from flask import request, jsonify, g
from http import HTTPStatus
from utils.auth import login_required
from category.service import CategoryService
from category import category_bp

category_service = CategoryService()

@category_bp.route('', methods=['GET'])
@login_required
def get_categories():
    user_id = g.user['user_id']
    categories = category_service.get_categories(user_id)
    
    return jsonify({
        'status': 'success',
        'categories': categories
    }), HTTPStatus.OK

@category_bp.route('/<int:category_id>', methods=['GET'])
@login_required
def get_category(category_id):
    user_id = g.user['user_id']
    category = category_service.get_category_by_id(user_id, category_id)
    
    if not category:
        return jsonify({
            'status': 'error',
            'message': 'Category not found'
        }), HTTPStatus.NOT_FOUND
    
    return jsonify({
        'status': 'success',
        'category': category
    }), HTTPStatus.OK

@category_bp.route('', methods=['GET', 'POST', 'OPTIONS'])
@login_required
def create_category():
    user_id = g.user['user_id']
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Category name is required'
        }), HTTPStatus.BAD_REQUEST
    
    try:
        new_category = category_service.create_category(user_id, data['name'])
        
        return jsonify({
            'status': 'success',
            'category': new_category
        }), HTTPStatus.CREATED
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An internal error occurred while creating the category: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@category_bp.route('/<int:category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    user_id = g.user['user_id']
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Category name is required'
        }), HTTPStatus.BAD_REQUEST
    
    try:
        updated_category = category_service.update_category(user_id, category_id, data['name'])
        
        if not updated_category:
            return jsonify({
                'status': 'error',
                'message': 'Category not found or access denied'
            }), HTTPStatus.NOT_FOUND
        
        return jsonify({
            'status': 'success',
            'category': updated_category
        }), HTTPStatus.OK
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An internal error occurred while updating the category: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    user_id = g.user['user_id']
    
    try:
        success, message = category_service.delete_category(user_id, category_id)
        
        if not success:
            return jsonify({
                'status': 'error',
                'message': message
            }), HTTPStatus.BAD_REQUEST if "in use" in message else HTTPStatus.NOT_FOUND
        
        return jsonify({
            'status': 'success',
            'message': message
        }), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An internal error occurred while deleting the category: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR