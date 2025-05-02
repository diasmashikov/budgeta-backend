from flask import Flask, request, jsonify
from dataclasses import dataclass, asdict
from typing import List, Dict
from http import HTTPStatus

@dataclass
class CreateCategoryRequest:
    name: str

@dataclass
class UpdateCategoryRequest:
    name: str

@dataclass
class CategoryResponse:
    category_id: int
    name: str

@dataclass
class CategoryListResponse:
    status: str
    categories: List[CategoryResponse]

@dataclass
class CategorySingleResponse:
    status: str
    category: CategoryResponse

@dataclass
class SuccessMessageResponse:
    status: str
    message: str

@dataclass
class ErrorResponse:
    status: str = "error"
    message: str = "An error occurred"

app = Flask(__name__)

categories_db: Dict[int, Dict[str, str]] = {
    1: {"name": "Housing"},
    2: {"name": "Food"},
    3: {"name": "Transportation"},
    4: {"name": "Entertainment"},
    5: {"name": "Utilities"}
}
next_category_id = 6

def find_category_by_name(name: str) -> int | None:
    for cat_id, cat_data in categories_db.items():
        if cat_data['name'].lower() == name.lower():
            return cat_id
    return None

@app.route('/api/categories', methods=['GET'])
def get_all_categories():
    category_list = [
        CategoryResponse(category_id=cat_id, name=data['name'])
        for cat_id, data in categories_db.items()
    ]
    response_data = CategoryListResponse(status="success", categories=category_list)
    return jsonify(asdict(response_data)), HTTPStatus.OK

@app.route('/api/categories', methods=['POST'])
def create_category():
    global next_category_id
    data = request.get_json()

    if not data or 'name' not in data or not data['name'].strip():
        error_response = ErrorResponse(message="Category name is required")
        return jsonify(asdict(error_response)), HTTPStatus.BAD_REQUEST

    category_name = data['name'].strip()

    existing_id = find_category_by_name(category_name)
    if existing_id is not None:
        error_response = ErrorResponse(message="Category with this name already exists")
        return jsonify(asdict(error_response)), HTTPStatus.BAD_REQUEST

    new_category_id = next_category_id
    categories_db[new_category_id] = {"name": category_name}
    next_category_id += 1

    created_category = CategoryResponse(category_id=new_category_id, name=category_name)
    response_data = CategorySingleResponse(status="success", category=created_category)
    return jsonify(asdict(response_data)), HTTPStatus.CREATED

@app.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id: int):
    if category_id not in categories_db:
        error_response = ErrorResponse(message="Category not found")
        return jsonify(asdict(error_response)), HTTPStatus.NOT_FOUND

    data = request.get_json()

    if not data or 'name' not in data or not data['name'].strip():
        error_response = ErrorResponse(message="Category name is required")
        return jsonify(asdict(error_response)), HTTPStatus.BAD_REQUEST

    new_name = data['name'].strip()

    existing_id_for_new_name = find_category_by_name(new_name)
    if existing_id_for_new_name is not None and existing_id_for_new_name != category_id:
         error_response = ErrorResponse(message="Category with this name already exists")
         return jsonify(asdict(error_response)), HTTPStatus.BAD_REQUEST

    categories_db[category_id]['name'] = new_name

    updated_category = CategoryResponse(category_id=category_id, name=new_name)
    response_data = CategorySingleResponse(status="success", category=updated_category)
    return jsonify(asdict(response_data)), HTTPStatus.OK

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id: int):
    if category_id not in categories_db:
        error_response = ErrorResponse(message="Category not found")
        return jsonify(asdict(error_response)), HTTPStatus.NOT_FOUND


    del categories_db[category_id]

    response_data = SuccessMessageResponse(status="success", message="Category deleted successfully")
    return jsonify(asdict(response_data)), HTTPStatus.OK

if __name__ == '__main__':
    app.run(debug=True)