from budget.repository import BudgetRepository
from budget.dto import CreateBudgetRequest, UpdateBudgetRequest, BudgetResponse

class BudgetService:
    def __init__(self):
        self.repository = BudgetRepository()
    
    def get_budgets(self, user_id, month=None, year=None):
        budget_allocations = self.repository.get_budgets(user_id, month, year)
        
        budget_responses = []
        total_budget = 0.0
        total_spent = 0.0
        
        for budget in budget_allocations:
            spent_amount = self.repository.get_expenses_for_budget(
                user_id, budget["category_id"], budget["month"], budget["year"]
            )
            
            remaining = budget["amount"] - spent_amount
            percentage_used = (spent_amount / budget["amount"] * 100) if budget["amount"] > 0 else 0
            
            budget_response = BudgetResponse(
                budget_id=budget["budget_id"],
                category_id=budget["category_id"],
                category_name=budget["category_name"],
                amount=budget["amount"],
                month=budget["month"],
                year=budget["year"],
                spent_amount=spent_amount,
                remaining=remaining,
                percentage_used=percentage_used
            )
            
            budget_responses.append(budget_response)
            total_budget += budget["amount"]
            total_spent += spent_amount
        
        return budget_responses, total_budget, total_spent
    
    def get_budget_by_id(self, user_id, budget_id):
        budget = self.repository.get_budget_by_id(user_id, budget_id)
        
        if not budget:
            return None
        
        spent_amount = self.repository.get_expenses_for_budget(
            user_id, budget["category_id"], budget["month"], budget["year"]
        )
        
        remaining = budget["amount"] - spent_amount
        percentage_used = (spent_amount / budget["amount"] * 100) if budget["amount"] > 0 else 0
        
        return BudgetResponse(
            budget_id=budget["budget_id"],
            category_id=budget["category_id"],
            category_name=budget["category_name"],
            amount=budget["amount"],
            month=budget["month"],
            year=budget["year"],
            spent_amount=spent_amount,
            remaining=remaining,
            percentage_used=percentage_used
        )
    
    def create_budget(self, user_id, budget_request: CreateBudgetRequest):
        # Check if category exists and belongs to user
        category = self.repository.get_category(user_id, budget_request.category_id)
        
        if not category:
            raise ValueError("Category not found or does not belong to user")
        
        # Check if budget allocation already exists
        existing_budget = self.repository.check_budget_exists(
            user_id, budget_request.category_id, budget_request.month, budget_request.year
        )
        
        if existing_budget:
            raise ValueError("Budget allocation already exists for this category, month, and year")
        
        # Create new budget allocation
        budget_id = self.repository.create_budget(
            user_id, 
            budget_request.category_id, 
            budget_request.amount, 
            budget_request.month, 
            budget_request.year
        )
        
        # Get the newly created budget
        return self.get_budget_by_id(user_id, budget_id)
    
    def update_budget(self, user_id, budget_id, update_request: UpdateBudgetRequest):
        # Check if budget exists
        budget = self.repository.get_budget_by_id(user_id, budget_id)
        
        if not budget:
            return None
        
        # Update budget amount
        success = self.repository.update_budget(user_id, budget_id, update_request.amount)
        
        if not success:
            return None
        
        # Get the updated budget
        return self.get_budget_by_id(user_id, budget_id)
    
    def delete_budget(self, user_id, budget_id):
        # Check if budget exists
        budget = self.repository.get_budget_by_id(user_id, budget_id)
        
        if not budget:
            return False
        
        # Delete budget
        return self.repository.delete_budget(user_id, budget_id)
    
    def update_savings(self, user_id, month, year):
        # Get income summary
        expected_income, actual_income = self.repository.get_income_summary(user_id, month, year)
        
        # Get total expenses
        total_expenses = self.repository.get_expenses_summary(user_id, month, year)
        
        # Calculate savings
        total_income = actual_income if actual_income > 0 else expected_income
        savings_amount = total_income - total_expenses
        
        # Check if savings record already exists
        existing_savings = self.repository.get_existing_savings(user_id, month, year)
        
        if existing_savings:
            # Update existing savings record
            self.repository.update_savings(existing_savings['savings_id'], savings_amount)
        else:
            # Insert new savings record
            self.repository.create_savings(user_id, savings_amount, month, year)
        
        return savings_amount