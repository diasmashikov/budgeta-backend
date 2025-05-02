from expense.repository import ExpenseRepository
from datetime import datetime

class ExpenseService:
    def __init__(self):
        self.repository = ExpenseRepository()
    
    def get_expenses(self, user_id, month=None, year=None, category_id=None):
        expenses = self.repository.get_expenses(user_id, month, year, category_id)
        processed_expenses = []
        
        for expense in expenses:
            processed_expense = dict(expense)
            
            # Convert date string to date object for serialization
            if processed_expense['date']:
                processed_expense['date'] = datetime.strptime(processed_expense['date'], '%Y-%m-%d').date()
            
            processed_expenses.append(processed_expense)
        
        # Calculate total amount
        total_amount = self.repository.calculate_total_amount(expenses)
        
        return processed_expenses, total_amount
    
    def get_expense_by_id(self, user_id, expense_id):
        expense = self.repository.get_expense_by_id(user_id, expense_id)
        
        if not expense:
            return None
        
        # Convert date string to date object for serialization
        if expense['date']:
            expense['date'] = datetime.strptime(expense['date'], '%Y-%m-%d').date()
        
        return expense
    
    def create_expense(self, user_id, create_request):
        # Check if category exists and belongs to user
        category = self.repository.get_category(user_id, create_request.category_id)
        
        if not category:
            raise ValueError("Category not found or does not belong to user")
        
        # Create new expense
        expense_id = self.repository.create_expense(
            user_id=user_id,
            category_id=create_request.category_id,
            amount=create_request.amount,
            expense_date=create_request.date,
            description=create_request.description
        )
        
        # Get the newly created expense
        expense = self.get_expense_by_id(user_id, expense_id)
        
        # Update savings
        if expense:
            expense_date = datetime.strptime(create_request.date, '%Y-%m-%d').date()
            self.update_savings(user_id, expense_date.month, expense_date.year)
        
        return expense
    
    def update_expense(self, user_id, expense_id, update_request):
        # Get current expense
        expense = self.repository.get_expense_by_id(user_id, expense_id)
        
        if not expense:
            return None
        
        # Store old date for savings update
        old_date = datetime.strptime(expense['date'], '%Y-%m-%d').date()
        
        # Validate category if changed
        if update_request.category_id is not None and update_request.category_id != expense['category_id']:
            category = self.repository.get_category(user_id, update_request.category_id)
            if not category:
                raise ValueError("Category not found or does not belong to user")
        
        # Update expense
        success = self.repository.update_expense(
            user_id=user_id,
            expense_id=expense_id,
            category_id=update_request.category_id,
            amount=update_request.amount,
            expense_date=update_request.date,
            description=update_request.description
        )
        
        if not success:
            return None
        
        # Get updated expense
        updated_expense = self.get_expense_by_id(user_id, expense_id)
        
        # Update savings if needed
        if updated_expense:
            has_changes = (
                update_request.amount is not None and float(update_request.amount) != float(expense['amount']) or
                update_request.date is not None and update_request.date != expense['date'] or
                update_request.category_id is not None and update_request.category_id != expense['category_id']
            )
            
            if has_changes:
                # Update savings for old month/year
                self.update_savings(user_id, old_date.month, old_date.year)
                
                # If date changed, update savings for new month/year as well
                if update_request.date is not None and update_request.date != expense['date']:
                    new_date = datetime.strptime(update_request.date, '%Y-%m-%d').date()
                    if new_date.month != old_date.month or new_date.year != old_date.year:
                        self.update_savings(user_id, new_date.month, new_date.year)
        
        return updated_expense
    
    def delete_expense(self, user_id, expense_id):
        # Get expense before deletion
        expense = self.repository.get_expense_by_id(user_id, expense_id)
        
        if not expense:
            return False
        
        # Store date for savings update
        expense_date = datetime.strptime(expense['date'], '%Y-%m-%d').date()
        
        # Delete expense
        success = self.repository.delete_expense(user_id, expense_id)
        
        # Update savings if deletion was successful
        if success:
            self.update_savings(user_id, expense_date.month, expense_date.year)
        
        return success
    
    def get_monthly_expenses_by_category(self, user_id, month, year):
        return self.repository.get_monthly_expenses_by_category(user_id, month, year)
    
    def get_recent_expenses(self, user_id, limit=5):
        expenses = self.repository.get_recent_expenses(user_id, limit)
        
        for expense in expenses:
            if expense['date']:
                expense['date'] = datetime.strptime(expense['date'], '%Y-%m-%d').date()
        
        return expenses
    
    def update_savings(self, user_id, month, year):
        # Import locally to avoid circular imports
        from budget.routes import update_savings
        return update_savings(user_id, month, year)