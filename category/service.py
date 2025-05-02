from category.repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()
    
    def get_categories(self, user_id):
        return self.repository.get_categories(user_id)
    
    def get_category_by_id(self, user_id, category_id):
        return self.repository.get_category_by_id(user_id, category_id)
    
    def create_category(self, user_id, name):
        # Validate name
        name = name.strip()
        if not name:
            raise ValueError("Category name is required")
        
        # Check for duplicate
        existing_category = self.repository.find_category_by_name(user_id, name)
        if existing_category:
            raise ValueError("Category with this name already exists")
        
        # Create category
        category_id = self.repository.create_category(user_id, name)
        
        if category_id:
            return {
                'category_id': category_id,
                'name': name
            }
        else:
            raise Exception("Failed to create category")
    
    def update_category(self, user_id, category_id, name):
        # Validate name
        name = name.strip()
        if not name:
            raise ValueError("Category name is required")
        
        # Check if category exists
        category = self.repository.get_category_by_id(user_id, category_id)
        if not category:
            return None
        
        # Check for duplicate
        existing_category = self.repository.check_duplicate_name_for_update(user_id, name, category_id)
        if existing_category:
            raise ValueError("Another category with this name already exists")
        
        # Update category
        success = self.repository.update_category(user_id, category_id, name)
        
        if success:
            return {
                'category_id': category_id,
                'name': name
            }
        else:
            return None
    
    def delete_category(self, user_id, category_id):
        # Check if category exists
        category = self.repository.get_category_by_id(user_id, category_id)
        if not category:
            return False, "Category not found"
        
        # Check if category is in use
        in_use = self.repository.check_category_in_use(user_id, category_id)
        if in_use:
            return False, "Cannot delete category that is in use in budgets or expenses"
        
        # Delete category
        success = self.repository.delete_category(user_id, category_id)
        
        if success:
            return True, "Category deleted successfully"
        else:
            return False, "Failed to delete category"