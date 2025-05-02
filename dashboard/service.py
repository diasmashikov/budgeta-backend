from dashboard.repository import DashboardRepository
from datetime import datetime, date

class DashboardService:
    def __init__(self):
        self.repository = DashboardRepository()
    
    def get_dashboard_overview(self, user_id, month, year):
        # 1. Get income summary
        income_summary = self.repository.get_income_summary(user_id, month, year)
        expected_income = income_summary['expected_income']
        actual_income = income_summary['actual_income']
        
        # 2. Get total expenses
        total_expenses = self.repository.get_expenses_total(user_id, month, year)
        
        # 3. Get budget summary
        budgets = self.repository.get_budget_summary(user_id, month, year)
        
        # 4. Get expenses by category
        expenses_by_category = self.repository.get_expenses_by_category(user_id, month, year)
        
        # 5. Combine budget and expenses data
        budget_summary = []
        for budget in budgets:
            category_id = budget['category_id']
            spent_amount = expenses_by_category.get(category_id, 0)
            budget_amount = float(budget['budget_amount'])
            remaining = budget_amount - spent_amount
            percentage_used = (spent_amount / budget_amount * 100) if budget_amount > 0 else 0
            
            budget_summary.append({
                'category_id': category_id,
                'category_name': budget['category_name'],
                'budget_amount': budget_amount,
                'spent_amount': spent_amount,
                'remaining': remaining,
                'percentage_used': percentage_used
            })
        
        # 6. Get recent transactions
        recent_expenses = self.repository.get_recent_expenses(user_id, month, year, 5)
        recent_income = self.repository.get_recent_income(user_id, month, year, 5)
        
        # Combine and sort transactions
        transactions = []
        
        for expense in recent_expenses:
            expense_dict = dict(expense)
            if expense_dict['transaction_date']:
                expense_dict['transaction_date'] = datetime.strptime(
                    expense_dict['transaction_date'], '%Y-%m-%d').date()
            transactions.append(expense_dict)
        
        for income in recent_income:
            income_dict = dict(income)
            if income_dict['transaction_date']:
                income_dict['transaction_date'] = datetime.strptime(
                    income_dict['transaction_date'], '%Y-%m-%d').date()
            transactions.append(income_dict)
        
        # Sort by date (most recent first)
        transactions.sort(key=lambda x: x['transaction_date'] if x['transaction_date'] else date.max, reverse=True)
        transactions = transactions[:10]  # Limit to 10 most recent
        
        # 7. Get savings
        savings_amount = self.repository.get_savings(user_id, month, year)
        
        # If savings record doesn't exist, calculate it
        if savings_amount == 0:
            # Update savings
            from budget.routes import update_savings
            try:
                savings_amount = update_savings(user_id, month, year)
            except:
                # If update_savings function fails, calculate it here as fallback
                savings_amount = actual_income - total_expenses
        
        # 8. Calculate remaining budget
        remaining_budget = actual_income - total_expenses
        
        # 9. Construct response
        return {
            'month': month,
            'year': year,
            'balance': {
                'expected_income': expected_income,
                'actual_income': actual_income,
                'total_expenses': total_expenses,
                'remaining_budget': remaining_budget
            },
            'budget_summary': budget_summary,
            'recent_transactions': transactions,
            'savings': savings_amount
        }