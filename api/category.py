from flask import Blueprint, request, jsonify, g  
from utils.db import query_db, insert_db, update_db
from utils.auth import login_required 
from http import HTTPStatus

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['GET'])
@login_required 
def get_categories(): 
    current_user = g.user 
    categories = query_db(
        'SELECT category_id, name FROM categories WHERE user_id = ? ORDER BY name',
        (current_user['user_id'],)
    )
    return jsonify({
        'status': 'success',
        'categories': [dict(category) for category in categories]
    }), HTTPStatus.OK

@categories_bp.route('', methods=['POST'])
@login_required 
def create_category():
    current_user = g.user 
    data = request.get_json()
    user_id = current_user['user_id']

    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({'status': 'error', 'message': 'Category name is required'}), HTTPStatus.BAD_REQUEST

    category_name = data['name'].strip()

    existing_category = query_db(
        'SELECT category_id FROM categories WHERE user_id = ? AND LOWER(name) = LOWER(?)',
        (user_id, category_name),
        one=True
    )

    if existing_category:
        return jsonify({'status': 'error', 'message': 'Category with this name already exists'}), HTTPStatus.BAD_REQUEST

    try:
        new_category_id = insert_db(
            'INSERT INTO categories (user_id, name) VALUES (?, ?)',
            (user_id, category_name)
        )
        if new_category_id:
             return jsonify({
                 'status': 'success',
                 'category': {
                     'category_id': new_category_id,
                     'name': category_name
                 }
             }), HTTPStatus.CREATED
        else:
             return jsonify({'status': 'error', 'message': 'Failed to create category'}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        print(f"Error creating category for user {user_id}: {e}")
        return jsonify({'status': 'error', 'message': 'An internal error occurred while creating the category'}), HTTPStatus.INTERNAL_SERVER_ERROR


@categories_bp.route('/<int:category_id>', methods=['PUT'])
@login_required 
def update_category(category_id):
   
    current_user = g.user 
    data = request.get_json()
    user_id = current_user['user_id']

    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({'status': 'error', 'message': 'Category name is required'}), HTTPStatus.BAD_REQUEST

    new_name = data['name'].strip()

    category_to_update = query_db(
        'SELECT category_id FROM categories WHERE category_id = ? AND user_id = ?',
        (category_id, user_id),
        one=True
    )

    if not category_to_update:
        return jsonify({'status': 'error', 'message': 'Category not found or access denied'}), HTTPStatus.NOT_FOUND

    existing_category = query_db(
        'SELECT category_id FROM categories WHERE user_id = ? AND LOWER(name) = LOWER(?) AND category_id != ?',
        (user_id, new_name, category_id),
        one=True
    )

    if existing_category:
        return jsonify({'status': 'error', 'message': 'Another category with this name already exists'}), HTTPStatus.BAD_REQUEST

    try:
        rows_affected = update_db(
            'UPDATE categories SET name = ? WHERE category_id = ? AND user_id = ?',
            (new_name, category_id, user_id)
        )
        if rows_affected > 0:
            return jsonify({
                'status': 'success',
                'category': {
                    'category_id': category_id,
                    'name': new_name
                }
            }), HTTPStatus.OK
        else:
            return jsonify({'status': 'error', 'message': 'Category not found or update failed'}), HTTPStatus.NOT_FOUND
    except Exception as e:
        print(f"Error updating category {category_id} for user {user_id}: {e}")
        return jsonify({'status': 'error', 'message': 'An internal error occurred while updating the category'}), HTTPStatus.INTERNAL_SERVER_ERROR

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@login_required 
def delete_category(category_id):
    """Delete a category for the current user."""
    current_user = g.user 
    user_id = current_user['user_id']

    category_to_delete = query_db(
        'SELECT category_id FROM categories WHERE category_id = ? AND user_id = ?',
        (category_id, user_id),
        one=True
    )

    if not category_to_delete:
        return jsonify({'status': 'error', 'message': 'Category not found or access denied'}), HTTPStatus.NOT_FOUND

    try:
        rows_affected = update_db(
            'DELETE FROM categories WHERE category_id = ? AND user_id = ?',
            (category_id, user_id)
        )
        if rows_affected > 0:
            return jsonify({
                'status': 'success',
                'message': 'Category deleted successfully'
            }), HTTPStatus.OK
        else:
             return jsonify({'status': 'error', 'message': 'Category not found or delete failed'}), HTTPStatus.NOT_FOUND

    except Exception as e:
        print(f"Error deleting category {category_id} for user {user_id}: {e}")
        return jsonify({'status': 'error', 'message': 'An internal error occurred while deleting the category'}), HTTPStatus.INTERNAL_SERVER_ERROR