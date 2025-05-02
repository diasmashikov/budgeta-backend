from utils.db import query_db, insert_db, update_db
from datetime import datetime
import calendar

class BudgetRepository:
    def get_budgets(self, user_id, month=None, year=None):
        query = '''
            SELECT 
                b.budget_id, 
                b.category_id, 
                c.name AS category_name, 
                b.amount, 
                b.month, 
                b.year
            FROM budget_allocations b
            JOIN categories c ON b.category_id = c.category_id
            WHERE b.user_id = ?
        '''
        
        args = [user_id]
        
        if month and year:
            query += ' AND b.month = ? AND b.year = ?'
            args.extend([month, year])
        elif month:
            query += ' AND b.month = ?'
            args.append(month)
        elif year:
            query += ' AND b.year = ?'
            args.append(year)
        
        query += ' ORDER BY c.name ASC'
        
        budgets = query_db(query, tuple(args))
        return [dict(budget) for budget in budgets]
    
    def get_budget_by_id(self, user_id, budget_id):
        budget = query_db('''
            SELECT 
                b.budget_id, 
                b.category_id, 
                c.name AS category_name, 
                b.amount, 
                b.month, 
                b.year
            FROM budget_allocations b
            JOIN categories c ON b.category_id = c.category_id
            WHERE b.budget_id = ? AND b.user_id = ?
        ''', (budget_id, user_id), one=True)
        
        return dict(budget) if budget else None
    
    def get_expenses_for_budget(self, user_id, category_id, month, year):
        _, last_day = calendar.monthrange(year, month)
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day:02d}"
        
        expense_query = '''
            SELECT SUM(amount) as total_spent
            FROM expenses
            WHERE user_id = ? AND category_id = ? AND date BETWEEN ? AND ?
        '''
        
        spent = query_db(expense_query, (user_id, category_id, start_date, end_date), one=True)
        
        return float(spent['total_spent']) if spent['total_spent'] else 0.0
    
    def get_category(self, user_id, category_id):
        return query_db('''
            SELECT * FROM categories 
            WHERE category_id = ? AND user_id = ?
        ''', (category_id, user_id), one=True)
    
    def check_budget_exists(self, user_id, category_id, month, year):
        return query_db('''
            SELECT * FROM budget_allocations
            WHERE user_id = ? AND category_id = ? AND month = ? AND year = ?
        ''', (user_id, category_id, month, year), one=True)
    
    def create_budget(self, user_id, category_id, amount, month, year):
        return insert_db('''
            INSERT INTO budget_allocations (user_id, category_id, amount, month, year)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category_id, amount, month, year))
    
    def update_budget(self, user_id, budget_id, amount):
        rows_affected = update_db('''
            UPDATE budget_allocations
            SET amount = ?, updated_at = CURRENT_TIMESTAMP
            WHERE budget_id = ? AND user_id = ?
        ''', (amount, budget_id, user_id))
        
        return rows_affected > 0
    
    def delete_budget(self, user_id, budget_id):
        rows_affected = update_db('''
            DELETE FROM budget_allocations
            WHERE budget_id = ? AND user_id = ?
        ''', (budget_id, user_id))
        
        return rows_affected > 0
    
    def get_budget_month_year(self, user_id, budget_id):
        budget = query_db('''
            SELECT month, year FROM budget_allocations
            WHERE budget_id = ? AND user_id = ?
        ''', (budget_id, user_id), one=True)
        
        return (budget['month'], budget['year']) if budget else (None, None)
    
    def get_income_summary(self, user_id, month, year):
        income = query_db('''
            SELECT 
                SUM(expected_amount) as expected_income,
                SUM(CASE WHEN is_received = 1 THEN actual_amount ELSE 0 END) as actual_income
            FROM income_sources
            WHERE user_id = ? AND month = ? AND year = ?
        ''', (user_id, month, year), one=True)
        
        expected_income = float(income['expected_income'] or 0)
        actual_income = float(income['actual_income'] or 0)
        
        return expected_income, actual_income
    
    def get_expenses_summary(self, user_id, month, year):
        _, last_day = calendar.monthrange(year, month)
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day:02d}"
        
        expenses = query_db('''
            SELECT SUM(amount) as total_expenses
            FROM expenses
            WHERE user_id = ? AND date BETWEEN ? AND ?
        ''', (user_id, start_date, end_date), one=True)
        
        return float(expenses['total_expenses'] or 0)
    
    def get_existing_savings(self, user_id, month, year):
        savings = query_db('''
            SELECT * FROM savings
            WHERE user_id = ? AND month = ? AND year = ?
        ''', (user_id, month, year), one=True)
        
        return dict(savings) if savings else None
    
    def create_savings(self, user_id, amount, month, year):
        return insert_db('''
            INSERT INTO savings (user_id, amount, month, year)
            VALUES (?, ?, ?, ?)
        ''', (user_id, amount, month, year))
    
    def update_savings(self, savings_id, amount):
        return update_db('''
            UPDATE savings
            SET amount = ?, updated_at = CURRENT_TIMESTAMP
            WHERE savings_id = ?
        ''', (amount, savings_id))