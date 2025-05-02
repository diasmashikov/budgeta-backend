from income.repository import IncomeRepository
from datetime import datetime

class IncomeService:
    def __init__(self):
        self.repository = IncomeRepository()
    
    def get_incomes(self, user_id, month=None, year=None):
        incomes = self.repository.get_incomes(user_id, month, year)
        processed_incomes = []
        
        for income in incomes:
            processed_income = dict(income)
            
            # Convert date strings to date objects for serialization
            if processed_income['due_date']:
                processed_income['due_date'] = datetime.strptime(processed_income['due_date'], '%Y-%m-%d').date()
            
            if processed_income['receive_date']:
                processed_income['receive_date'] = datetime.strptime(processed_income['receive_date'], '%Y-%m-%d').date()
            
            processed_incomes.append(processed_income)
        
        # Calculate totals
        total_expected, total_received = self.repository.calculate_income_totals(incomes)
        
        return processed_incomes, total_expected, total_received
    
    def get_income_by_id(self, user_id, income_id):
        income = self.repository.get_income_by_id(user_id, income_id)
        
        if not income:
            return None
        
        # Convert date strings to date objects for serialization
        if income['due_date']:
            income['due_date'] = datetime.strptime(income['due_date'], '%Y-%m-%d').date()
        
        if income['receive_date']:
            income['receive_date'] = datetime.strptime(income['receive_date'], '%Y-%m-%d').date()
        
        return income
    
    def create_income(self, user_id, create_request):
        income_id = self.repository.create_income(
            user_id=user_id,
            source_name=create_request.source_name,
            expected_amount=create_request.expected_amount,
            month=create_request.month,
            year=create_request.year,
            due_date=create_request.due_date,
            description=create_request.description
        )
        
        return self.get_income_by_id(user_id, income_id)
    
    def update_income(self, user_id, income_id, update_request):
        income = self.repository.get_income_by_id(user_id, income_id)
        
        if not income:
            return None
        
        success = self.repository.update_income(
            user_id=user_id,
            income_id=income_id,
            source_name=update_request.source_name,
            expected_amount=update_request.expected_amount,
            actual_amount=update_request.actual_amount,
            is_received=update_request.is_received,
            due_date=update_request.due_date,
            receive_date=update_request.receive_date,
            month=update_request.month,
            year=update_request.year,
            description=update_request.description
        )
        
        if not success:
            return None
        
        # If income was updated and affects savings, update savings
        if update_request.is_received is not None or update_request.actual_amount is not None:
            self.update_savings(user_id, income['month'], income['year'])
        
        # If month or year was changed, update savings for both old and new periods
        if (update_request.month is not None and update_request.month != income['month']) or \
           (update_request.year is not None and update_request.year != income['year']):
            self.update_savings(user_id, income['month'], income['year'])
            self.update_savings(user_id, update_request.month or income['month'], 
                               update_request.year or income['year'])
        
        return self.get_income_by_id(user_id, income_id)
    
    def delete_income(self, user_id, income_id):
        income = self.repository.get_income_by_id(user_id, income_id)
        
        if not income:
            return False
        
        month, year = income['month'], income['year']
        
        success = self.repository.delete_income(user_id, income_id)
        
        if success:
            # Update savings after deleting income
            self.update_savings(user_id, month, year)
        
        return success
    
    def receive_income(self, user_id, income_id, receive_request):
        income = self.repository.get_income_by_id(user_id, income_id)
        
        if not income:
            return None
        
        success = self.repository.receive_income(
            user_id=user_id,
            income_id=income_id,
            actual_amount=receive_request.actual_amount,
            receive_date=receive_request.receive_date
        )
        
        if not success:
            return None
        
        # Update savings after receiving income
        self.update_savings(user_id, income['month'], income['year'])
        
        return self.get_income_by_id(user_id, income_id)
    
    def update_savings(self, user_id, month, year):
        # Import locally to avoid circular imports
        from budget.routes import update_savings
        return update_savings(user_id, month, year)