from utils.db import query_db, insert_db, update_db

class CategoryRepository:
    def get_categories(self, user_id):
        categories = query_db(
            'SELECT category_id, name FROM categories WHERE user_id = ? ORDER BY name',
            (user_id,)
        )
        return [dict(category) for category in categories]
    
    def get_category_by_id(self, user_id, category_id):
        category = query_db(
            'SELECT category_id, name FROM categories WHERE category_id = ? AND user_id = ?',
            (category_id, user_id),
            one=True
        )
        return dict(category) if category else None
    
    def find_category_by_name(self, user_id, name):
        category = query_db(
            'SELECT category_id FROM categories WHERE user_id = ? AND LOWER(name) = LOWER(?)',
            (user_id, name),
            one=True
        )
        return dict(category) if category else None
    
    def check_duplicate_name_for_update(self, user_id, name, category_id):
        category = query_db(
            'SELECT category_id FROM categories WHERE user_id = ? AND LOWER(name) = LOWER(?) AND category_id != ?',
            (user_id, name, category_id),
            one=True
        )
        return dict(category) if category else None
    
    def create_category(self, user_id, name):
        return insert_db(
            'INSERT INTO categories (user_id, name) VALUES (?, ?)',
            (user_id, name)
        )
    
    def update_category(self, user_id, category_id, name):
        rows_affected = update_db(
            'UPDATE categories SET name = ? WHERE category_id = ? AND user_id = ?',
            (name, category_id, user_id)
        )
        return rows_affected > 0
    
    def delete_category(self, user_id, category_id):
        rows_affected = update_db(
            'DELETE FROM categories WHERE category_id = ? AND user_id = ?',
            (category_id, user_id)
        )
        return rows_affected > 0
    
    def check_category_in_use(self, user_id, category_id):
        # Check if category is in use in budgets
        budget_count = query_db(
            'SELECT COUNT(*) as count FROM budget_allocations WHERE user_id = ? AND category_id = ?',
            (user_id, category_id),
            one=True
        )
        
        # Check if category is in use in expenses
        expense_count = query_db(
            'SELECT COUNT(*) as count FROM expenses WHERE user_id = ? AND category_id = ?',
            (user_id, category_id),
            one=True
        )
        
        return budget_count['count'] > 0 or expense_count['count'] > 0