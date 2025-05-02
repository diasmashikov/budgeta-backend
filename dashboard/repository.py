from utils.db import query_db
import calendar
from datetime import datetime, date

class DashboardRepository:
    def get_income_summary(self, user_id, month, year):
        income_query = '''
            SELECT 
                SUM(expected_amount) as expected_income,
                SUM(CASE WHEN is_received = 1 THEN actual_amount ELSE 0 END) as actual_income
            FROM income_sources
            WHERE user_id = ? AND month = ? AND year = ?
        '''
        
        income = query_db(income_query, (user_id, month, year), one=True)
        
        return {
            'expected_income': float(income['expected_income'] or 0),
            'actual_income': float(income['actual_income'] or 0)
        }
    
    def get_expenses_total(self, user_id, month, year):
        # Get the first and last day of the month
        _, last_day = calendar.monthrange(year, month)
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day:02d}"
        
        expense_query = '''
            SELECT SUM(amount) as total_expenses
            FROM expenses
            WHERE user_id = ? AND date BETWEEN ? AND ?
        '''
        
        expenses = query_db(expense_query, (user_id, start_date, end_date), one=True)
        
        return float(expenses['total_expenses'] or 0)
    
    def get_budget_summary(self, user_id, month, year):
        budget_query = '''
            SELECT 
                b.category_id,
                c.name as category_name,
                b.amount as budget_amount
            FROM budget_allocations b
            JOIN categories c ON b.category_id = c.category_id
            WHERE b.user_id = ? AND b.month = ? AND b.year = ?
            ORDER BY c.name
        '''
        
        budgets = query_db(budget_query, (user_id, month, year))
        return [dict(budget) for budget in budgets]
    
    def get_expenses_by_category(self, user_id, month, year):
        # Get the first and last day of the month
        _, last_day = calendar.monthrange(year, month)
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day:02d}"
        
        category_expense_query = '''
            SELECT 
                e.category_id,
                SUM(e.amount) as spent_amount
            FROM expenses e
            WHERE e.user_id = ? AND e.date BETWEEN ? AND ?
            GROUP BY e.category_id
        '''
        
        category_expenses = query_db(category_expense_query, (user_id, start_date, end_date))
        
        return {
            expense['category_id']: float(expense['spent_amount'] or 0)
            for expense in category_expenses
        }
    
    def get_recent_expenses(self, user_id, month, year, limit=5):
        # Get the first and last day of the month
        _, last_day = calendar.monthrange(year, month)
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day:02d}"
        
        recent_expenses_query = '''
            SELECT 
                'expense' as type,
                e.expense_id as id,
                e.amount,
                e.date as transaction_date,
                e.description,
                c.name as category_name,
                c.category_id
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
            WHERE e.user_id = ? AND e.date BETWEEN ? AND ?
            ORDER BY e.date DESC, e.created_at DESC
            LIMIT ?
        '''
        
        recent_expenses = query_db(recent_expenses_query, (user_id, start_date, end_date, limit))
        return [dict(expense) for expense in recent_expenses]
    
    def get_recent_income(self, user_id, month, year, limit=5):
        recent_income_query = '''
            SELECT 
                'income' as type,
                i.income_id as id,
                CASE WHEN i.is_received = 1 THEN i.actual_amount ELSE i.expected_amount END as amount,
                CASE WHEN i.is_received = 1 THEN i.receive_date ELSE i.due_date END as transaction_date,
                i.description,
                i.source_name
            FROM income_sources i
            WHERE i.user_id = ? AND i.month = ? AND i.year = ?
            ORDER BY transaction_date DESC
            LIMIT ?
        '''
        
        recent_income = query_db(recent_income_query, (user_id, month, year, limit))
        return [dict(income) for income in recent_income]
    
    def get_savings(self, user_id, month, year):
        savings_query = '''
            SELECT amount
            FROM savings
            WHERE user_id = ? AND month = ? AND year = ?
        '''
        
        savings = query_db(savings_query, (user_id, month, year), one=True)
        
        return float(savings['amount']) if savings and savings['amount'] else 0